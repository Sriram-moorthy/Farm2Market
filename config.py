import os
from dotenv import load_dotenv

# Try to load .env file, but don't fail if it doesn't exist
try:
    load_dotenv()
except Exception:
    pass

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "farm2market-secret-key-2024")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDLtimwV5QORag6Cu6_x6OR9tBEVBcBEJA")
    
    # Static file paths
    STATIC_DIR = "static"
    TEMPLATES_DIR = "templates"
    UPLOADS_DIR = "static/uploads"

settings = Settings() 