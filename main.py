from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os
import uuid
import shutil
from datetime import datetime
import google.generativeai as genai
import asyncio
from config import settings

# Create FastAPI app
app = FastAPI(title="Farm2Market", description="Connect farmers with buyers")

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Create directories if they don't exist
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# In-memory data storage (in production, use a proper database)
users = {}
crops = {}
cart_items = {}
orders = {}
messages = {}
farmer_ratings = {}
user_preferences = {}
carbon_data = {}

# Pydantic models
class User(BaseModel):
    id: str
    full_name: str
    age: int
    email: str
    phone: str
    password: str
    location: Optional[str] = None
    role: str  # "farmer" or "buyer"

class Crop(BaseModel):
    id: str
    farmer_id: str
    name: str
    quantity: float
    unit: str
    location: str
    price: float
    image_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CartItem(BaseModel):
    crop_id: str
    quantity: float
    buyer_id: str

class Order(BaseModel):
    id: str
    buyer_id: str
    farmer_id: str
    crop_id: str
    quantity: float
    total_price: float
    status: str
    created_at: datetime

class Message(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    content: str
    timestamp: datetime

class FarmerRating(BaseModel):
    id: str
    farmer_id: str
    buyer_id: str
    rating: float  # 1-5 stars
    review: Optional[str] = None
    order_id: str
    created_at: datetime

class UserPreference(BaseModel):
    user_id: str
    preferred_crops: List[str]
    budget_range: Optional[str] = None
    dietary_preferences: List[str]
    location_preference: Optional[str] = None
    last_updated: datetime

class CarbonFootprint(BaseModel):
    id: str
    user_id: str
    crop_id: str
    quantity: float
    distance_km: float
    transport_mode: str
    carbon_saved: float  # kg CO2
    calculated_at: datetime

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

# AI Assistant endpoint
@app.post("/api/ai-chat")
async def ai_chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        user_context = data.get("context", {})
        
        if not user_message.strip():
            return JSONResponse({
                "success": False,
                "error": "Message cannot be empty",
                "response": "Please enter a message to get help."
            }, status_code=400)
        
        # Create context-aware prompt based on language
        language = user_context.get("language", "en")
        
        if language == "hi":
            system_prompt = """आप Farm2Market AI सहायक हैं, एक सहायक AI हैं जो हमारे कृषि बाज़ार प्लेटफॉर्म पर किसानों और खरीदारों की सहायता करने के लिए डिज़ाइन किया गया है।

            प्लेटफॉर्म संदर्भ:
            - Farm2Market छोटे और सीमांत किसानों को सीधे खरीदारों से जोड़ता है
            - हम उचित मूल्य सुनिश्चित करने के लिए बिचौलियों को हटाते हैं
            - प्लेटफॉर्म की सुविधाएं: फसल सूची, AI मूल्य सुझाव, रीयल-टाइम चैट, सुरक्षित भुगतान
            
            आपकी क्षमताएं:
            - किसानों को फसल सूची बनाने में सहायता करना
            - खेती की सलाह और सर्वोत्तम प्रथाएं प्रदान करना
            - खरीदारों को सही फसल खोजने में सहायता करना
            - प्लेटफॉर्म की सुविधाओं और प्रक्रियाओं की व्याख्या करना
            - मूल्य मार्गदर्शन और बाज़ार अंतर्दृष्टि देना
            """
        elif language == "ta":
            system_prompt = """நீங்கள் Farm2Market AI உதவியாளர், எங்கள் விவசாய சந்தை தளத்தில் விவசாயிகள் மற்றும் வாங்குபவர்களுக்கு உதவ வடிவமைக்கப்பட்ட உதவிகரமான AI ஆவீர்கள்.

            தளத்தின் சூழல்:
            - Farm2Market சிறிய மற்றும் விளிம்பு விவசாயிகளை நேரடியாக வாங்குபவர்களுடன் இணைக்கிறது
            - நியாயமான விலைகளை உறுதிசெய்ய நாங்கள் இடைத்தரகர்களை நீக்குகிறோம்
            - தளத்தின் அம்சங்கள்: பயிர் பட்டியல், AI விலை பரிந்துரைகள், நிகழ்நேர அரட்டை, பாதுகாப்பான கொடுப்பனவுகள்
            
            உங்கள் திறன்கள்:
            - விவசாயிகளுக்கு பயிர்களை பட்டியலிட உதவுதல்
            - விவசாய ஆலோசனை மற்றும் சிறந்த நடைமுறைகளை வழங்குதல்
            - வாங்குபவர்களுக்கு சரியான பயிர்களைக் கண்டறிய உதவுதல்
            - தளத்தின் அம்சங்கள் மற்றும் செயல்முறைகளை விளக்குதல்
            """
        else:
            system_prompt = """You are Farm2Market AI Assistant, a helpful AI designed to assist farmers and buyers on our agricultural marketplace platform.

            Platform Context:
            - Farm2Market connects small and marginal farmers directly with buyers
            - We eliminate middlemen to ensure fair prices
            - Platform features: crop listing, AI price suggestions, real-time chat, secure payments
            - We support English, Hindi, and Tamil languages
            
            Your capabilities:
            - Help farmers list crops effectively
            - Provide farming advice and best practices
            - Assist buyers in finding the right crops
            - Explain platform features and processes
            - Give price guidance and market insights
            - Help with technical issues
            - Provide agricultural knowledge
            
            Guidelines:
            - Be helpful, friendly, and knowledgeable
            - Keep responses concise but informative
            - Use farming and marketplace terminology appropriately
            - Suggest platform features when relevant
            - If asked about technical issues, provide practical solutions
            - For farming advice, be practical and region-appropriate
            """
        
        # Add user context
        context_info = f"\nUser Context: {json.dumps(user_context)}"
        full_prompt = f"{system_prompt}{context_info}\n\nUser Question: {user_message}\n\nAssistant:"
        
        # Generate response using Gemini with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Configure generation parameters for better responses
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1000,
                }
                
                response = model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
                
                if response.text:
                    ai_response = response.text.strip()
                    break
                else:
                    raise Exception("Empty response from Gemini")
                    
            except Exception as gemini_error:
                print(f"Gemini API error (attempt {attempt + 1}): {gemini_error}")
                if attempt == max_retries - 1:
                    # Final fallback with helpful responses based on common queries
                    ai_response = get_fallback_response(user_message, language)
                else:
                    continue

        return JSONResponse({
            "success": True,
            "response": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"AI Chat general error: {e}")
        return JSONResponse({
            "success": False,
            "error": "AI service temporarily unavailable",
            "response": "I'm sorry, I'm having trouble responding right now. Please try again in a moment."
        }, status_code=500)

def get_fallback_response(message, language="en"):
    """Provide helpful fallback responses when AI is unavailable"""
    message_lower = message.lower()
    
    responses = {
        "en": {
            "price": "For pricing help, try using our AI price suggestion feature when listing crops. Consider factors like crop quality, season, and local market demand.",
            "sell": "To sell crops: 1) Login as farmer 2) Add crop details with photos 3) Set competitive prices 4) Wait for buyer inquiries. Make sure to provide accurate crop information!",
            "buy": "To buy crops: 1) Browse available crops 2) Use search and filters 3) Add to cart 4) Contact farmers directly 5) Complete secure payment.",
            "help": "I can help with: crop listing, pricing guidance, platform navigation, farming tips, and connecting with other users. What specific topic interests you?",
            "default": "I'm currently running in basic mode. I can still help with general platform questions. Try asking about selling crops, buying process, or pricing guidance!"
        },
        "hi": {
            "price": "मूल्य सहायता के लिए, फसल सूची बनाते समय हमारी AI मूल्य सुझाव सुविधा का उपयोग करें। फसल की गुणवत्ता, मौसम और स्थानीय बाजार की मांग को ध्यान में रखें।",
            "sell": "फसल बेचने के लिए: 1) किसान के रूप में लॉगिन करें 2) फोटो के साथ फसल विवरण जोड़ें 3) प्रतिस्पर्धी मूल्य निर्धारित करें 4) खरीदार पूछताछ की प्रतीक्षा करें।",
            "buy": "फसल खरीदने के लिए: 1) उपलब्ध फसलों को ब्राउज़ करें 2) खोज और फिल्टर का उपयोग करें 3) कार्ट में जोड़ें 4) किसानों से सीधे संपर्क करें।",
            "help": "मैं इनमें मदद कर सकता हूं: फसल सूची, मूल्य मार्गदर्शन, प्लेटफॉर्म नेवीगेशन, खेती की सुझाव। आप किस विषय में रुचि रखते हैं?",
            "default": "मैं वर्तमान में बेसिक मोड में चल रहा हूं। मैं अभी भी सामान्य प्लेटफॉर्म प्रश्नों में मदद कर सकता हूं!"
        },
        "ta": {
            "price": "விலை உதவிக்கு, பயிர்களைப் பட்டியலிடும்போது எங்கள் AI விலை பரிந்துரை அம்சத்தைப் பயன்படுத்துங்கள். பயிரின் தரம், பருவம் மற்றும் உள்ளூர் சந்தைத் தேவையைக் கவனியுங்கள்.",
            "sell": "பயிர்களை விற்க: 1) விவசாயியாக உள்நுழைக 2) புகைப்படங்களுடன் பயிர் விவரங்களைச் சேர்க்கவும் 3) போட்டித்தன்மையான விலைகளை நிர்ணயிக்கவும் 4) வாங்குவோர் விசாரணைக்காக காத்திருக்கவும்.",
            "buy": "பயிர்களை வாங்க: 1) கிடைக்கும் பயிர்களை உலாவவும் 2) தேடல் மற்றும் வடிகட்டிகளைப் பயன்படுத்துங்கள் 3) வண்டியில் சேர்க்கவும் 4) விவசாயிகளை நேரடியாகத் தொடர்பு கொள்ளுங்கள்.",
            "help": "நான் இவற்றில் உதவ முடியும்: பயிர் பட்டியல், விலை வழிகாட்டுதல், தளம் வழிசெலுத்தல், விவசாய உதவிக்குறிப்புகள். எந்த குறிப்பிட்ட தலைப்பில் ஆர்வமாக உள்ளீர்கள்?",
            "default": "நான் தற்போது அடிப்படை பயன்முறையில் இயங்குகிறேன். பொதுவான தளம் கேள்விகளில் நான் இன்னும் உதவ முடியும்!"
        }
    }
    
    lang_responses = responses.get(language, responses["en"])
    
    # Check for keywords and return appropriate response
    for keyword, response in lang_responses.items():
        if keyword in message_lower and keyword != "default":
            return response
    
    return lang_responses["default"]

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/farmer-auth", response_class=HTMLResponse)
async def farmer_auth(request: Request):
    return templates.TemplateResponse("farmer_auth.html", {"request": request})

@app.get("/buyer-auth", response_class=HTMLResponse)
async def buyer_auth(request: Request):
    return templates.TemplateResponse("buyer_auth.html", {"request": request})

@app.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    # Find existing user with this email, role, and password
    existing_user = None
    existing_user_id = None
    for user_id, user_data in users.items():
        if user_data["email"] == email and user_data["role"] == role and user_data["password"] == password:
            existing_user = user_data
            existing_user_id = user_id
            break
    
    if existing_user:
        # Login successful, redirect to dashboard
        user_id = existing_user_id
        if role == "farmer":
            return RedirectResponse(url=f"/farmer-dashboard?user_id={user_id}", status_code=303)
        else:
            return RedirectResponse(url=f"/buyer-dashboard?user_id={user_id}", status_code=303)
    else:
        # Login failed, redirect back with error
        if role == "farmer":
            return RedirectResponse(url="/farmer-auth?error=invalid_credentials", status_code=303)
        else:
            return RedirectResponse(url="/buyer-auth?error=invalid_credentials", status_code=303)

@app.post("/signup")
async def signup(
    full_name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    location: str = Form(""),
    role: str = Form(...)
):
    # Check if user already exists with this email and role
    existing_user = None
    existing_user_id = None
    for user_id, user_data in users.items():
        if user_data["email"] == email and user_data["role"] == role:
            existing_user = user_data
            existing_user_id = user_id
            break
    
    if existing_user:
        # Check if password matches
        if existing_user["password"] == password:
            # Password matches, redirect to their dashboard
            user_id = existing_user_id
        else:
            # Password doesn't match, return error
            if role == "farmer":
                return RedirectResponse(url="/farmer-auth?error=invalid_password", status_code=303)
            else:
                return RedirectResponse(url="/buyer-auth?error=invalid_password", status_code=303)
    else:
        # Create new user
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            full_name=full_name,
            age=age,
            email=email,
            phone=phone,
            password=password,
            location=location,
            role=role
        )
        users[user_id] = user.model_dump()
    
    if role == "farmer":
        return RedirectResponse(url=f"/farmer-dashboard?user_id={user_id}", status_code=303)
    else:
        return RedirectResponse(url=f"/buyer-dashboard?user_id={user_id}", status_code=303)

@app.get("/farmer-dashboard", response_class=HTMLResponse)
async def farmer_dashboard(request: Request, user_id: str):
    if user_id not in users:
        return RedirectResponse(url="/", status_code=303)
    
    user = users[user_id]
    user_crops = [crop for crop in crops.values() if crop["farmer_id"] == user_id]
    
    # Get orders for this farmer
    farmer_orders = [order for order in orders.values() if order["farmer_id"] == user_id]
    
    # Get messages for this farmer
    farmer_messages = [msg for msg in messages.values() if msg["receiver_id"] == user_id or msg["sender_id"] == user_id]
    
    return templates.TemplateResponse("farmer_dashboard.html", {
        "request": request,
        "user": user,
        "crops": user_crops,
        "orders": farmer_orders,
        "messages": farmer_messages,
        "users": users,
        "all_crops": crops  # Pass the crops dictionary for order lookup
    })

@app.get("/buyer-dashboard", response_class=HTMLResponse)
async def buyer_dashboard(request: Request, user_id: str):
    if user_id not in users:
        return RedirectResponse(url="/", status_code=303)
    
    user = users[user_id]
    all_crops = list(crops.values())
    
    # Add farmer names to crops
    for crop in all_crops:
        farmer = users.get(crop["farmer_id"], {})
        crop["farmer_name"] = farmer.get("full_name", "Unknown")
    
    return templates.TemplateResponse("buyer_dashboard.html", {
        "request": request,
        "user": user,
        "crops": all_crops,
        "users": users
    })

@app.post("/add-crop")
async def add_crop(
    user_id: str = Form(...),
    name: str = Form(...),
    quantity: float = Form(...),
    unit: str = Form(...),
    location: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(None),
    custom_name: str = Form("")
):
    crop_id = str(uuid.uuid4())
    image_url = None
    
    # Handle custom crop name
    crop_name = custom_name.strip() if name == "other" and custom_name.strip() else name
    
    if image:
        image_filename = f"{crop_id}_{image.filename}"
        image_path = os.path.join(settings.UPLOADS_DIR, image_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/{image_filename}"
    
    crop = Crop(
        id=crop_id,
        farmer_id=user_id,
        name=crop_name,
        quantity=quantity,
        unit=unit,
        location=location,
        price=price,
        image_url=image_url,
        created_at=datetime.now()
    )
    
    crops[crop_id] = crop.model_dump()
    return RedirectResponse(url=f"/farmer-dashboard?user_id={user_id}", status_code=303)

@app.post("/add-to-cart")
async def add_to_cart(
    buyer_id: str = Form(...),
    crop_id: str = Form(...),
    quantity: float = Form(...)
):
    # Validate inputs
    if not buyer_id or not crop_id or quantity <= 0:
        return JSONResponse({
            "success": False, 
            "message": "Invalid input data"
        }, status_code=400)
    
    # Check if crop exists
    if crop_id not in crops:
        return JSONResponse({
            "success": False, 
            "message": "Crop not found"
        }, status_code=404)
    
    # Check if buyer exists
    if buyer_id not in users:
        return JSONResponse({
            "success": False, 
            "message": "User not found"
        }, status_code=404)
    
    crop = crops[crop_id]
    
    # Check if enough quantity is available
    if quantity > crop["quantity"]:
        return JSONResponse({
            "success": False, 
            "message": f"Only {crop['quantity']} {crop['unit']} available"
        }, status_code=400)
    
    cart_item = CartItem(crop_id=crop_id, quantity=quantity, buyer_id=buyer_id)
    cart_key = f"{buyer_id}_{crop_id}"
    
    # If item already in cart, update quantity
    if cart_key in cart_items:
        existing_item = cart_items[cart_key]
        new_quantity = existing_item["quantity"] + quantity
        
        if new_quantity > crop["quantity"]:
            return JSONResponse({
                "success": False, 
                "message": f"Cannot add more. Total would exceed available quantity of {crop['quantity']} {crop['unit']}"
            }, status_code=400)
        
        cart_items[cart_key]["quantity"] = new_quantity
        message = "Updated cart quantity"
    else:
        cart_items[cart_key] = cart_item.model_dump()
        message = "Added to cart"
    
    # Get updated cart count
    cart_count = len([item for item in cart_items.values() if item["buyer_id"] == buyer_id])
    
    return JSONResponse({
        "success": True, 
        "message": message,
        "cart_count": cart_count,
        "item_total": quantity * crop["price"]
    })

@app.get("/api/cart-count")
async def get_cart_count(user_id: str):
    """Get the number of items in user's cart"""
    if not user_id:
        return JSONResponse({"success": False, "error": "User ID required"}, status_code=400)
    
    cart_count = len([item for item in cart_items.values() if item["buyer_id"] == user_id])
    return JSONResponse({"success": True, "cart_count": cart_count})

@app.delete("/api/cart/remove/{crop_id}")
async def remove_from_cart(crop_id: str, user_id: str = None):
    """Remove an item from the cart"""
    if not user_id:
        return JSONResponse({"success": False, "error": "User ID required"}, status_code=400)
    
    # Find and remove the cart item
    cart_key = f"{user_id}_{crop_id}"
    if cart_key in cart_items:
        del cart_items[cart_key]
        return JSONResponse({"success": True, "message": "Item removed from cart"})
    else:
        return JSONResponse({"success": False, "message": "Item not found in cart"}, status_code=404)

@app.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request, user_id: str):
    if user_id not in users:
        return RedirectResponse(url="/", status_code=303)
    
    user = users[user_id]
    user_cart_items = [item for key, item in cart_items.items() if item["buyer_id"] == user_id]
    
    cart_with_details = []
    total_price = 0
    
    for cart_item in user_cart_items:
        crop = crops.get(cart_item["crop_id"])
        if crop:
            item_total = cart_item["quantity"] * crop["price"]
            total_price += item_total
            cart_with_details.append({
                "cart_item": cart_item,
                "crop": crop,
                "item_total": item_total
            })
    
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "user": user,
        "cart_items": cart_with_details,
        "total_price": total_price,
        "users": users
    })

@app.post("/checkout")
async def checkout(user_id: str = Form(...)):
    # Process payment and create orders
    user_cart_items = [item for key, item in cart_items.items() if item["buyer_id"] == user_id]
    
    for cart_item in user_cart_items:
        crop = crops.get(cart_item["crop_id"])
        if crop:
            order_id = str(uuid.uuid4())
            order = Order(
                id=order_id,
                buyer_id=user_id,
                farmer_id=crop["farmer_id"],
                crop_id=cart_item["crop_id"],
                quantity=cart_item["quantity"],
                total_price=cart_item["quantity"] * crop["price"],
                status="confirmed",
                created_at=datetime.now()
            )
            orders[order_id] = order.model_dump()
    
    # Clear only this user's cart items
    keys_to_remove = [key for key, item in cart_items.items() if item["buyer_id"] == user_id]
    for key in keys_to_remove:
        del cart_items[key]
    
    # Redirect with success message
    return RedirectResponse(url=f"/buyer-dashboard?user_id={user_id}&order_success=1", status_code=303)

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, user_id: str, other_user_id: str):
    if user_id not in users or other_user_id not in users:
        return RedirectResponse(url="/", status_code=303)
    
    user = users[user_id]
    other_user = users[other_user_id]
    
    # Get chat messages between these users
    chat_messages = [
        msg for msg in messages.values() 
        if (msg["sender_id"] == user_id and msg["receiver_id"] == other_user_id) or
           (msg["sender_id"] == other_user_id and msg["receiver_id"] == user_id)
    ]
    chat_messages.sort(key=lambda x: x["timestamp"])
    
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "user": user,
        "other_user": other_user,
        "messages": chat_messages
    })

@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def user_profile(request: Request, user_id: str, current_user_id: str = None):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile_user = users[user_id]
    current_user = users.get(current_user_id) if current_user_id else None
    
    # Get user's crops if they are a farmer
    user_crops = []
    if profile_user["role"] == "farmer":
        user_crops = [crop for crop in crops.values() if crop["farmer_id"] == user_id]
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "profile_user": profile_user,
        "current_user": current_user,
        "crops": user_crops
    })

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_id = str(uuid.uuid4())
            message = Message(
                id=message_id,
                sender_id=user_id,
                receiver_id=message_data["receiver_id"],
                content=message_data["content"],
                timestamp=datetime.now()
            )
            
            messages[message_id] = message.model_dump()
            
            # Send message to receiver
            await manager.send_personal_message(
                json.dumps({
                    "sender_id": user_id,
                    "content": message_data["content"],
                    "timestamp": message.timestamp.isoformat()
                }),
                message_data["receiver_id"]
            )
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)

@app.get("/api/debug/messages")
async def debug_messages():
    """Debug endpoint to check all messages"""
    return {
        "total_messages": len(messages),
        "messages": messages
    }

@app.get("/api/debug/orders")
async def debug_orders():
    """Debug endpoint to check all orders"""
    return {
        "total_orders": len(orders),
        "orders": orders
    }

@app.get("/api/debug/all")
async def debug_all():
    """Debug endpoint to check all data"""
    return {
        "users": len(users),
        "crops": len(crops),
        "cart_items": len(cart_items),
        "orders": len(orders),
        "messages": len(messages)
    }

@app.get("/api/crops")
async def get_crops(search: str = "", location: str = "", min_price: float = 0, max_price: float = float('inf')):
    filtered_crops = []
    
    for crop in crops.values():
        if (search.lower() in crop["name"].lower() if search else True) and \
           (location.lower() in crop["location"].lower() if location else True) and \
           (min_price <= crop["price"] <= max_price):
            # Add farmer info
            farmer = users.get(crop["farmer_id"], {})
            crop_with_farmer = crop.copy()
            crop_with_farmer["farmer_name"] = farmer.get("full_name", "Unknown")
            filtered_crops.append(crop_with_farmer)
    
    return filtered_crops

@app.get("/api/crops/{crop_id}")
async def get_crop(crop_id: str):
    """Get a specific crop by ID"""
    if crop_id not in crops:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    crop = crops[crop_id]
    farmer = users.get(crop["farmer_id"], {})
    crop_with_farmer = crop.copy()
    crop_with_farmer["farmer_name"] = farmer.get("full_name", "Unknown")
    
    return crop_with_farmer

@app.delete("/api/crops/{crop_id}")
async def delete_crop(crop_id: str):
    """Delete a specific crop"""
    if crop_id not in crops:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Remove the crop
    deleted_crop = crops.pop(crop_id)
    
    # Remove associated cart items
    cart_keys_to_remove = [key for key, item in cart_items.items() if item["crop_id"] == crop_id]
    for key in cart_keys_to_remove:
        cart_items.pop(key)
    
    return {"success": True, "message": "Crop deleted successfully", "deleted_crop": deleted_crop}

@app.put("/api/crops/{crop_id}")
async def update_crop(
    crop_id: str,
    name: str = Form(...),
    quantity: float = Form(...),
    unit: str = Form(...),
    location: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(None),
    custom_name: str = Form("")
):
    """Update a specific crop"""
    if crop_id not in crops:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    crop_data = crops[crop_id]
    
    # Handle custom crop name
    crop_name = custom_name.strip() if name == "other" and custom_name.strip() else name
    
    # Handle image upload
    image_url = crop_data.get("image_url")  # Keep existing image by default
    if image:
        image_filename = f"{crop_id}_{image.filename}"
        image_path = os.path.join(settings.UPLOADS_DIR, image_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/{image_filename}"
    
    # Update crop data
    crop_data.update({
        "name": crop_name,
        "quantity": quantity,
        "unit": unit,
        "location": location,
        "price": price,
        "image_url": image_url
    })
    
    return {"success": True, "message": "Crop updated successfully", "crop": crop_data}

@app.get("/api/price-suggestion")
async def get_price_suggestion(crop_name: str, location: str, unit: str = "kg"):
    try:
        prompt = f"""
        Analyze the current market price for '{crop_name}' in '{location}', India. 
        Consider factors like seasonality, demand, local market trends, and quality.
        Provide a suggested price per {unit} in INR.
        
        Return ONLY a JSON object with this exact structure:
        {{
            "suggested_price": <number>,
            "confidence": <number between 0.1 and 1.0>,
            "explanation": "<brief explanation in 1-2 sentences mentioning price per {unit}>"
        }}
        """
        
        generation_config = {
            "temperature": 0.3,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 200,
        }
        
        response = model.generate_content(prompt, generation_config=generation_config)
        
        if not response.text:
            raise Exception("Empty response from Gemini")
        
        # Clean the response text
        json_str = response.text.strip()
        
        # Remove markdown formatting if present
        if json_str.startswith("```json"):
            json_str = json_str[7:-3].strip()
        elif json_str.startswith("```"):
            json_str = json_str[3:-3].strip()
        
        # Try to parse JSON
        suggestion = json.loads(json_str)
        
        # Validate the response structure
        if not all(key in suggestion for key in ["suggested_price", "confidence", "explanation"]):
            raise Exception("Invalid response structure")
        
        # Ensure confidence is between 0.1 and 1.0
        suggestion["confidence"] = max(0.1, min(1.0, float(suggestion["confidence"])))
        
        return JSONResponse(suggestion)
        
    except Exception as e:
        print(f"Price suggestion error: {e}")
        
        # Enhanced fallback logic with more crops and location adjustments
        base_prices = {
            "rice": 28, "wheat": 32, "tomato": 45, "potato": 22, "onion": 38,
            "corn": 25, "millet": 35, "sugarcane": 30, "cotton": 85, "soybean": 60,
            "mustard": 70, "groundnut": 80, "carrot": 40, "cabbage": 25, "cauliflower": 35,
            "spinach": 30, "beans": 50, "peas": 60, "cucumber": 25, "bitter gourd": 40,
            "okra": 45, "brinjal": 35, "chili": 120, "ginger": 180, "turmeric": 150
        }
        
        # Location-based price adjustment
        location_multipliers = {
            "mumbai": 1.3, "delhi": 1.25, "bangalore": 1.2, "chennai": 1.15,
            "kolkata": 1.1, "pune": 1.2, "hyderabad": 1.1, "ahmedabad": 1.15
        }
        
        # Get base price
        crop_lower = crop_name.lower()
        base_price = 30  # Default price
        
        for crop in base_prices:
            if crop in crop_lower or crop_lower in crop:
                base_price = base_prices[crop]
                break
        
        # Apply location multiplier
        location_lower = location.lower()
        multiplier = 1.0
        for city in location_multipliers:
            if city in location_lower:
                multiplier = location_multipliers[city]
                break
        
        suggested_price = round(base_price * multiplier, 2)
        
        return JSONResponse({
            "suggested_price": suggested_price,
            "confidence": 0.6,
            "explanation": f"Estimated price based on market averages for {crop_name} in {location}. Consider local market conditions for final pricing."
        })

# ==== NEW HACKATHON FEATURES ====

# 1. Smart Crop Recommendations API
@app.get("/api/recommendations/{user_id}")
async def get_smart_recommendations(user_id: str):
    """Get AI-powered crop recommendations for buyers"""
    try:
        if user_id not in users:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        user = users[user_id]
        user_location = user.get("location", "")
        
        # Get user's purchase history for personalization
        user_orders = [order for order in orders.values() if order["buyer_id"] == user_id]
        purchased_crops = list(set([orders[order_id]["crop_id"] for order_id in user_orders if order_id in orders]))
        
        # Get current season recommendations
        current_month = datetime.now().month
        seasonal_crops = get_seasonal_crops(current_month)
        
        # AI-powered recommendations
        prompt = f"""
        Based on user profile and preferences, recommend 5 crops for a buyer in {user_location}.
        User's previous purchases: {purchased_crops if purchased_crops else "None"}
        Current seasonal crops: {seasonal_crops}
        
        Consider:
        1. Seasonal availability
        2. Nutritional variety
        3. Local growing conditions
        4. Price value
        5. Complementary cooking ingredients
        
        Return JSON format:
        {{
            "recommendations": [
                {{
                    "crop_name": "name",
                    "reason": "why recommended",
                    "season_score": 0.8,
                    "nutrition_benefits": "benefits",
                    "estimated_price_range": "₹X-Y per kg"
                }}
            ]
        }}
        """
        
        response = model.generate_content(prompt)
        recommendation_data = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        # Add available crops from our database
        available_crops = []
        for crop_id, crop_data in crops.items():
            crop_name = crop_data["name"].lower()
            for rec in recommendation_data["recommendations"]:
                if rec["crop_name"].lower() in crop_name or crop_name in rec["crop_name"].lower():
                    available_crops.append({
                        "crop_id": crop_id,
                        "farmer_name": users[crop_data["farmer_id"]]["full_name"],
                        "price": crop_data["price"],
                        "location": crop_data["location"],
                        "quantity": crop_data["quantity"],
                        "unit": crop_data["unit"]
                    })
        
        return JSONResponse({
            "ai_recommendations": recommendation_data["recommendations"],
            "available_crops": available_crops,
            "user_location": user_location
        })
        
    except Exception as e:
        print(f"Recommendation error: {e}")
        # Fallback recommendations
        return JSONResponse({
            "ai_recommendations": [
                {"crop_name": "Tomato", "reason": "High in vitamins, versatile cooking", "season_score": 0.9, "nutrition_benefits": "Rich in Vitamin C and antioxidants", "estimated_price_range": "₹30-50 per kg"},
                {"crop_name": "Onion", "reason": "Essential cooking ingredient", "season_score": 0.8, "nutrition_benefits": "Good for heart health", "estimated_price_range": "₹25-40 per kg"},
                {"crop_name": "Potato", "reason": "Staple food, good storage", "season_score": 0.7, "nutrition_benefits": "Source of carbohydrates and potassium", "estimated_price_range": "₹15-30 per kg"}
            ],
            "available_crops": [],
            "user_location": user_location
        })

def get_seasonal_crops(month):
    """Get seasonal crops based on month"""
    seasonal_map = {
        1: ["wheat", "mustard", "peas", "carrot", "cauliflower"],  # Jan
        2: ["wheat", "barley", "gram", "potato", "cabbage"],       # Feb
        3: ["barley", "mustard", "onion", "garlic", "spinach"],    # Mar
        4: ["rice", "cotton", "sugarcane", "maize", "tomato"],     # Apr
        5: ["rice", "cotton", "groundnut", "okra", "cucumber"],    # May
        6: ["rice", "cotton", "sugarcane", "beans", "gourds"],     # Jun
        7: ["rice", "maize", "cotton", "pulses", "leafy greens"], # Jul
        8: ["rice", "sugarcane", "turmeric", "ginger", "chili"],  # Aug
        9: ["rice", "cotton", "soybean", "corn", "vegetables"],   # Sep
        10: ["wheat", "mustard", "potato", "onion", "garlic"],    # Oct
        11: ["wheat", "barley", "peas", "carrot", "radish"],      # Nov
        12: ["wheat", "gram", "mustard", "cabbage", "cauliflower"] # Dec
    }
    return seasonal_map.get(month, ["rice", "wheat", "vegetables"])

# 2. Carbon Footprint Calculator API
@app.post("/api/carbon-footprint")
async def calculate_carbon_footprint(
    user_id: str = Form(...),
    crop_id: str = Form(...),
    quantity: float = Form(...),
    transport_mode: str = Form(...)
):
    """Calculate carbon footprint for a purchase"""
    try:
        if user_id not in users or crop_id not in crops:
            return JSONResponse({"error": "User or crop not found"}, status_code=404)
        
        user = users[user_id]
        crop = crops[crop_id]
        farmer = users[crop["farmer_id"]]
        
        # Calculate distance (simplified - in real app, use geo-coordinates)
        distance_km = calculate_distance(user.get("location", ""), crop["location"])
        
        # Carbon emission factors (kg CO2 per km per kg of produce)
        transport_emissions = {
            "truck": 0.2,      # kg CO2 per km per kg
            "bike": 0.01,      # much lower for bikes
            "walking": 0.0,    # zero emissions
            "public_transport": 0.05,
            "own_vehicle": 0.15
        }
        
        emission_factor = transport_emissions.get(transport_mode, 0.2)
        
        # Calculate emissions
        total_emissions = distance_km * quantity * emission_factor
        
        # Calculate carbon saved vs conventional supply chain (longer distance)
        conventional_distance = 500  # assume 500km average for conventional supply
        conventional_emissions = conventional_distance * quantity * 0.25  # higher emission factor
        carbon_saved = max(0, conventional_emissions - total_emissions)
        
        # Save carbon footprint data
        footprint_id = str(uuid.uuid4())
        carbon_footprint = CarbonFootprint(
            id=footprint_id,
            user_id=user_id,
            crop_id=crop_id,
            quantity=quantity,
            distance_km=distance_km,
            transport_mode=transport_mode,
            carbon_saved=carbon_saved,
            calculated_at=datetime.now()
        )
        
        carbon_data[footprint_id] = carbon_footprint.model_dump()
        
        return JSONResponse({
            "success": True,
            "carbon_footprint": {
                "total_emissions_kg": round(total_emissions, 3),
                "carbon_saved_kg": round(carbon_saved, 3),
                "distance_km": distance_km,
                "transport_mode": transport_mode,
                "farmer_location": crop["location"],
                "buyer_location": user.get("location", ""),
                "environmental_impact": get_environmental_message(carbon_saved),
                "footprint_id": footprint_id
            }
        })
        
    except Exception as e:
        print(f"Carbon footprint calculation error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

def calculate_distance(location1, location2):
    """Simplified distance calculation - in real app, use geolocation APIs"""
    # This is a simplified calculation - in production, use actual geolocation
    if not location1 or not location2:
        return 50  # default 50km
    
    # Simple city-based distance estimation
    city_distances = {
        ("mumbai", "pune"): 150,
        ("delhi", "gurgaon"): 30,
        ("bangalore", "mysore"): 150,
        ("chennai", "coimbatore"): 500,
    }
    
    loc1_lower = location1.lower()
    loc2_lower = location2.lower()
    
    # Check both directions
    distance = city_distances.get((loc1_lower, loc2_lower)) or city_distances.get((loc2_lower, loc1_lower))
    
    if distance:
        return distance
    
    # If same city/area, short distance
    if loc1_lower == loc2_lower:
        return 5
    
    # Default inter-city distance
    return 100

def get_environmental_message(carbon_saved):
    """Get environmental impact message"""
    if carbon_saved > 10:
        return "🌱 Excellent choice! You've significantly reduced your carbon footprint."
    elif carbon_saved > 5:
        return "🌿 Good impact! You're contributing to sustainable agriculture."
    elif carbon_saved > 1:
        return "♻️ Positive impact! Every small step helps the environment."
    else:
        return "🌍 Consider choosing local farmers to reduce environmental impact."

# 3. Voice Search API
@app.post("/api/voice-search")
async def voice_search_crops(query: str = Form(...)):
    """Process voice search queries for crops"""
    try:
        # Clean and process the voice query
        query_lower = query.lower().strip()
        
        # AI-powered query understanding
        prompt = f"""
        Parse this voice search query for an agricultural marketplace: "{query}"
        
        Extract:
        1. Crop names mentioned
        2. Quantity/amount if specified
        3. Location preferences
        4. Price range if mentioned
        5. Quality requirements (organic, fresh, etc.)
        
        Return JSON:
        {{
            "crops": ["crop1", "crop2"],
            "location": "location or null",
            "quantity": "amount or null",
            "price_range": "range or null",
            "quality_filters": ["organic", "fresh"],
            "search_intent": "brief description"
        }}
        """
        
        response = model.generate_content(prompt)
        parsed_query = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        # Search crops based on parsed query
        matching_crops = []
        for crop_id, crop_data in crops.items():
            crop_name_lower = crop_data["name"].lower()
            
            # Check if any mentioned crops match
            crop_match = any(crop.lower() in crop_name_lower or crop_name_lower in crop.lower() 
                           for crop in parsed_query.get("crops", []))
            
            # Check location if specified
            location_match = True
            if parsed_query.get("location"):
                location_match = parsed_query["location"].lower() in crop_data["location"].lower()
            
            if crop_match and location_match:
                farmer_info = users.get(crop_data["farmer_id"], {})
                matching_crops.append({
                    "crop_id": crop_id,
                    "name": crop_data["name"],
                    "farmer_name": farmer_info.get("full_name", "Unknown"),
                    "location": crop_data["location"],
                    "price": crop_data["price"],
                    "quantity": crop_data["quantity"],
                    "unit": crop_data["unit"],
                    "relevance_score": calculate_relevance(crop_data, parsed_query)
                })
        
        # Sort by relevance
        matching_crops.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return JSONResponse({
            "success": True,
            "original_query": query,
            "parsed_query": parsed_query,
            "matching_crops": matching_crops[:10],  # Top 10 results
            "total_results": len(matching_crops)
        })
        
    except Exception as e:
        print(f"Voice search error: {e}")
        # Fallback: simple text search
        matching_crops = []
        query_words = query.lower().split()
        
        for crop_id, crop_data in crops.items():
            if any(word in crop_data["name"].lower() for word in query_words):
                farmer_info = users.get(crop_data["farmer_id"], {})
                matching_crops.append({
                    "crop_id": crop_id,
                    "name": crop_data["name"],
                    "farmer_name": farmer_info.get("full_name", "Unknown"),
                    "location": crop_data["location"],
                    "price": crop_data["price"],
                    "quantity": crop_data["quantity"],
                    "unit": crop_data["unit"]
                })
        
        return JSONResponse({
            "success": True,
            "original_query": query,
            "matching_crops": matching_crops[:10],
            "total_results": len(matching_crops),
            "fallback": True
        })

def calculate_relevance(crop_data, parsed_query):
    """Calculate relevance score for search results"""
    score = 0
    
    # Crop name match
    crop_name_lower = crop_data["name"].lower()
    for crop in parsed_query.get("crops", []):
        if crop.lower() in crop_name_lower:
            score += 10
    
    # Location preference
    if parsed_query.get("location"):
        if parsed_query["location"].lower() in crop_data["location"].lower():
            score += 5
    
    # Price considerations (if available in good range)
    if crop_data["price"] < 100:  # reasonable price
        score += 2
    
    # Quantity availability
    if crop_data["quantity"] > 10:  # good stock
        score += 1
    
    return score

# 4. Farmer Rating System API
@app.post("/api/rate-farmer")
async def rate_farmer(
    farmer_id: str = Form(...),
    buyer_id: str = Form(...),
    rating: float = Form(...),
    review: str = Form(""),
    order_id: str = Form(...)
):
    """Submit a rating for a farmer"""
    try:
        # Validate inputs
        if rating < 1 or rating > 5:
            return JSONResponse({"error": "Rating must be between 1 and 5"}, status_code=400)
        
        if farmer_id not in users or buyer_id not in users:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        if order_id not in orders:
            return JSONResponse({"error": "Order not found"}, status_code=404)
        
        # Check if buyer has already rated this farmer for this order
        existing_rating = None
        for rating_id, rating_data in farmer_ratings.items():
            if (rating_data["farmer_id"] == farmer_id and 
                rating_data["buyer_id"] == buyer_id and 
                rating_data["order_id"] == order_id):
                existing_rating = rating_id
                break
        
        rating_id = existing_rating or str(uuid.uuid4())
        
        # Create or update rating
        farmer_rating = FarmerRating(
            id=rating_id,
            farmer_id=farmer_id,
            buyer_id=buyer_id,
            rating=rating,
            review=review,
            order_id=order_id,
            created_at=datetime.now()
        )
        
        farmer_ratings[rating_id] = farmer_rating.model_dump()
        
        # Calculate new average rating for farmer
        farmer_rating_stats = calculate_farmer_rating_stats(farmer_id)
        
        return JSONResponse({
            "success": True,
            "message": "Rating submitted successfully",
            "farmer_stats": farmer_rating_stats
        })
        
    except Exception as e:
        print(f"Rating submission error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/farmer-ratings/{farmer_id}")
async def get_farmer_ratings(farmer_id: str):
    """Get all ratings and statistics for a farmer"""
    try:
        if farmer_id not in users:
            return JSONResponse({"error": "Farmer not found"}, status_code=404)
        
        farmer_stats = calculate_farmer_rating_stats(farmer_id)
        
        # Get recent reviews
        recent_reviews = []
        for rating_id, rating_data in farmer_ratings.items():
            if rating_data["farmer_id"] == farmer_id and rating_data["review"]:
                buyer_info = users.get(rating_data["buyer_id"], {})
                recent_reviews.append({
                    "rating": rating_data["rating"],
                    "review": rating_data["review"],
                    "buyer_name": buyer_info.get("full_name", "Anonymous"),
                    "created_at": rating_data["created_at"]
                })
        
        # Sort by date (newest first)
        recent_reviews.sort(key=lambda x: x["created_at"], reverse=True)
        
        return JSONResponse({
            "farmer_id": farmer_id,
            "stats": farmer_stats,
            "recent_reviews": recent_reviews[:5],  # Top 5 recent reviews
            "total_reviews": len([r for r in farmer_ratings.values() if r["farmer_id"] == farmer_id and r["review"]])
        })
        
    except Exception as e:
        print(f"Get farmer ratings error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

def calculate_farmer_rating_stats(farmer_id):
    """Calculate rating statistics for a farmer"""
    farmer_rating_list = [rating for rating in farmer_ratings.values() if rating["farmer_id"] == farmer_id]
    
    if not farmer_rating_list:
        return {
            "average_rating": 0,
            "total_ratings": 0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    
    ratings = [rating["rating"] for rating in farmer_rating_list]
    average_rating = sum(ratings) / len(ratings)
    
    # Calculate rating distribution
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for rating in ratings:
        distribution[int(rating)] += 1
    
    return {
        "average_rating": round(average_rating, 2),
        "total_ratings": len(ratings),
        "rating_distribution": distribution
    }

# Get user's carbon footprint history
@app.get("/api/carbon-history/{user_id}")
async def get_carbon_history(user_id: str):
    """Get user's carbon footprint history"""
    try:
        user_footprints = [fp for fp in carbon_data.values() if fp["user_id"] == user_id]
        total_saved = sum(fp["carbon_saved"] for fp in user_footprints)
        
        return JSONResponse({
            "total_carbon_saved": round(total_saved, 2),
            "total_purchases": len(user_footprints),
            "average_distance": round(sum(fp["distance_km"] for fp in user_footprints) / len(user_footprints), 1) if user_footprints else 0,
            "recent_footprints": sorted(user_footprints, key=lambda x: x["calculated_at"], reverse=True)[:10]
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 