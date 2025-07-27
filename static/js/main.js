// Farm2Market JavaScript - Complete functionality
class Farm2Market {
    constructor() {
        this.currentLanguage = 'en';
        this.cartCount = 0;
        this.aiMessages = [];
        this.currentUserId = this.getUserIdFromURL();
        this.translations = {
            en: {
                search: "Search for crops...",
                addToCart: "Add to Cart",
                quickAdd: "Quick Add",
                price: "Price",
                quantity: "Quantity",
                location: "Location",
                farmer: "Farmer",
                total: "Total",
                cart: "Cart",
                welcome: "Welcome",
                aiPlaceholder: "Ask me anything about farming or our platform...",
                loading: "Loading...",
                error: "Error occurred",
                success: "Success!",
                addedToCart: "Added to cart successfully!",
                chatWithFarmer: "Chat with Farmer",
                buyNow: "Buy Now",
                searchResults: "Search Results",
                noResults: "No crops found matching your search.",
                priceRange: "Price Range",
                sortBy: "Sort By",
                name: "Name",
                priceLowToHigh: "Price: Low to High",
                priceHighToLow: "Price: High to Low",
                newest: "Newest First",
                vegetables: "Vegetables",
                fruits: "Fruits",
                grains: "Grains",
                rice: "Rice",
                wheat: "Wheat",
                pulses: "Pulses",
                spices: "Spices",
                // Homepage translations
                about: "About",
                features: "Features", 
                contact: "Contact",
                welcome: "Welcome to Farm2Market",
                hero_description: "Connecting small and marginal farmers directly with buyers through a transparent, AI-powered marketplace",
                farmer_role: "I'm a Farmer",
                buyer_role: "I'm a Buyer",
                farmer_description: "List your crops, get fair prices, and connect with buyers directly",
                buyer_description: "Find fresh crops directly from farmers at transparent prices",
                direct_connection: "🤝 Direct Connection",
                direct_connection_desc: "Eliminate middlemen and connect farmers directly with buyers for better prices and fresher produce.",
                ai_pricing: "🤖 AI-Powered Pricing",
                ai_pricing_desc: "Get intelligent price suggestions based on market data, location, and crop quality.",
                realtime_communication: "💬 Real-time Communication",
                realtime_communication_desc: "Chat directly with farmers and buyers to negotiate and coordinate deliveries.",
                mobile_friendly: "📱 Mobile Friendly",
                mobile_friendly_desc: "Access the platform from any device - desktop, tablet, or mobile phone.",
                chatWithFarmer: "Chat with Farmer"
            },
            hi: {
                search: "फसल खोजें...",
                addToCart: "कार्ट में जोड़ें",
                quickAdd: "तुरंत जोड़ें",
                price: "मूल्य",
                quantity: "मात्रा",
                location: "स्थान",
                farmer: "किसान",
                total: "कुल",
                cart: "कार्ट",
                welcome: "स्वागत है",
                aiPlaceholder: "खेती या हमारे प्लेटफॉर्म के बारे में कुछ भी पूछें...",
                loading: "लोड हो रहा है...",
                error: "त्रुटि हुई",
                success: "सफल!",
                addedToCart: "कार्ट में सफलतापूर्वक जोड़ा गया!",
                chatWithFarmer: "किसान से बात करें",
                buyNow: "अभी खरीदें",
                searchResults: "खोज परिणाम",
                noResults: "आपकी खोज से मेल खाने वाली कोई फसल नहीं मिली।",
                priceRange: "मूल्य सीमा",
                sortBy: "क्रमबद्ध करें",
                name: "नाम",
                priceLowToHigh: "मूल्य: कम से अधिक",
                priceHighToLow: "मूल्य: अधिक से कम",
                newest: "सबसे नया पहले",
                vegetables: "सब्जियां",
                fruits: "फल",
                grains: "अनाज",
                rice: "चावल",
                wheat: "गेहूं",
                pulses: "दाल",
                spices: "मसाले",
                // Homepage translations
                about: "के बारे में",
                features: "विशेषताएं",
                contact: "संपर्क",
                welcome: "Farm2Market में आपका स्वागत है",
                hero_description: "पारदर्शी, AI-संचालित बाज़ार के माध्यम से छोटे और सीमांत किसानों को सीधे खरीदारों से जोड़ना",
                farmer_role: "मैं एक किसान हूं",
                buyer_role: "मैं एक खरीदार हूं",
                farmer_description: "अपनी फसल सूचीबद्ध करें, उचित मूल्य प्राप्त करें, और खरीदारों से सीधे जुड़ें",
                buyer_description: "पारदर्शी मूल्यों पर किसानों से सीधे ताजी फसल खोजें",
                direct_connection: "🤝 प्रत्यक्ष संपर्क",
                direct_connection_desc: "बिचौलियों को हटाएं और बेहतर मूल्य और ताजा उत्पादन के लिए किसानों को सीधे खरीदारों से जोड़ें।",
                ai_pricing: "🤖 AI-संचालित मूल्य निर्धारण",
                ai_pricing_desc: "बाजार डेटा, स्थान और फसल गुणवत्ता के आधार पर बुद्धिमान मूल्य सुझाव प्राप्त करें।",
                realtime_communication: "💬 रीयल-टाइम संचार",
                realtime_communication_desc: "बातचीत और डिलीवरी समन्वयन के लिए किसानों और खरीदारों से सीधे चैट करें।",
                mobile_friendly: "📱 मोबाइल फ्रेंडली",
                mobile_friendly_desc: "किसी भी डिवाइस से प्लेटफॉर्म तक पहुंचें - डेस्कटॉप, टैबलेट, या मोबाइल फोन।",
                chatWithFarmer: "किसान से बात करें"
            },
            ta: {
                search: "பயிர்களைத் தேடுங்கள்...",
                addToCart: "கார்ட்டில் சேர்க்கவும்",
                quickAdd: "விரைவாக சேர்க்கவும்",
                price: "விலை",
                quantity: "அளவு",
                location: "இடம்",
                farmer: "விவசாயி",
                total: "மொத்தம்",
                cart: "கார்ட்",
                welcome: "வரவேற்கிறோம்",
                aiPlaceholder: "விவசாயம் அல்லது எங்கள் தளத்தைப் பற்றி எதையும் கேளுங்கள்...",
                loading: "ஏற்றுகிறது...",
                error: "பிழை ஏற்பட்டது",
                success: "வெற்றி!",
                addedToCart: "கார்ட்டில் வெற்றிகரமாக சேர்க்கப்பட்டது!",
                chatWithFarmer: "விவசாயியுடன் அரட்டை",
                buyNow: "இப்போது வாங்கவும்",
                searchResults: "தேடல் முடிவுகள்",
                noResults: "உங்கள் தேடலுக்கு பொருந்தும் பயிர்கள் எதுவும் கிடைக்கவில்லை।",
                priceRange: "விலை வரம்பு",
                sortBy: "வரிசைப்படுத்து",
                name: "பெயர்",
                priceLowToHigh: "விலை: குறைவு முதல் அதிகம்",
                priceHighToLow: "விலை: அதிகம் முதல் குறைவு",
                newest: "புதியது முதலில்",
                vegetables: "காய்கறிகள்",
                fruits: "பழங்கள்",
                grains: "தானியங்கள்",
                rice: "அரிசி",
                wheat: "கோதுமை",
                pulses: "பருப்பு வகைகள்",
                spices: "மசாலாப் பொருட்கள்",
                // Homepage translations
                about: "பற்றி",
                features: "அம்சங்கள்",
                contact: "தொடர்பு",
                welcome: "Farm2Market-க்கு வரவேற்கிறோம்",
                hero_description: "வெளிப்படையான, AI-இயங்கும் சந்தையின் மூலம் சிறிய மற்றும் விளிம்பு விவசாயிகளை நேரடியாக வாங்குபவர்களுடன் இணைத்தல்",
                farmer_role: "நான் ஒரு விவசாயி",
                buyer_role: "நான் ஒரு வாங்குபவர்",
                farmer_description: "உங்கள் பயிர்களைப் பட்டியலிடுங்கள், நியாயமான விலைகளைப் பெறுங்கள், வாங்குபவர்களுடன் நேரடியாக இணைக்கவும்",
                buyer_description: "வெளிப்படையான விலையில் விவசாயிகளிடம் இருந்து நேரடியாக புதிய பயிர்களைக் கண்டறியுங்கள்",
                direct_connection: "🤝 நேரடி இணைப்பு",
                direct_connection_desc: "இடைத்தரகர்களை நீக்கி, சிறந்த விலைகள் மற்றும் புதிய விளைபொருட்களுக்காக விவசாயிகளை நேரடியாக வாங்குபவர்களுடன் இணைக்கவும்।",
                ai_pricing: "🤖 AI-இயங்கும் விலை நிர்ணயம்",
                ai_pricing_desc: "சந்தை தரவு, இருப்பிடம் மற்றும் பயிர் தரத்தின் அடிப்படையில் அறிவார்ந்த விலை பரிந்துரைகளைப் பெறுங்கள்।",
                realtime_communication: "💬 நேரடி தொடர்பு",
                realtime_communication_desc: "பேச்சுவார்த்தை மற்றும் டெலிவரி ஒருங்கிணைப்புக்காக விவசாயிகள் மற்றும் வாங்குபவர்களுடன் நேரடியாக அரட்டையடிக்கவும்।",
                mobile_friendly: "📱 மொபைல் நட்பு",
                mobile_friendly_desc: "எந்த சாதனத்திலிருந்தும் தளத்தை அணுகவும் - டெஸ்க்டாப், டேப்லெட் அல்லது மொபைல் போன்.",
                chatWithFarmer: "விவசாயியுடன் அரட்டை"
            }
        };
        this.init();
    }

    init() {
        this.initializeAI();
        this.initializeLanguageSwitcher();
        this.initializeCart();
        this.initializeSearch();
        this.loadInitialData();
    }

    getUserIdFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('user_id');
    }

    // Language switching functionality
    changeLanguage(lang) {
        this.currentLanguage = lang;
        this.updatePageLanguage();
        localStorage.setItem('farm2market_language', lang);
    }

    updatePageLanguage() {
        const translations = this.translations[this.currentLanguage];
        
        // Update all elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translations[key]) {
                if (element.tagName === 'INPUT') {
                    element.placeholder = translations[key];
                } else {
                    element.textContent = translations[key];
                }
            }
        });

        // Update AI assistant placeholder
        const aiInput = document.getElementById('aiInput');
        if (aiInput) {
            aiInput.placeholder = translations.aiPlaceholder;
        }
    }

    initializeLanguageSwitcher() {
        // Load saved language
        const savedLang = localStorage.getItem('farm2market_language') || 'en';
        this.currentLanguage = savedLang;
        
        const switcher = document.getElementById('languageSwitcher');
        if (switcher) {
            switcher.value = savedLang;
            this.updatePageLanguage();
        }
    }

    // AI Assistant functionality
    initializeAI() {
        const aiToggle = document.getElementById('aiToggle');
        const aiPanel = document.getElementById('aiPanel');
        const aiMinimize = document.getElementById('aiMinimize');
        const aiSend = document.getElementById('aiSend');
        const aiInput = document.getElementById('aiInput');

        if (aiToggle && aiPanel) {
            aiToggle.addEventListener('click', () => {
                aiPanel.classList.toggle('visible');
                if (aiPanel.classList.contains('visible') && this.aiMessages.length === 0) {
                    this.addAIMessage('assistant', this.translations[this.currentLanguage].aiPlaceholder || 'Hello! How can I help you today?');
                }
            });
        }

        if (aiMinimize) {
            aiMinimize.addEventListener('click', () => {
                aiPanel.classList.remove('visible');
            });
        }

        if (aiSend && aiInput) {
            const sendMessage = () => {
                const message = aiInput.value.trim();
                if (message) {
                    this.sendAIMessage(message);
                    aiInput.value = '';
                }
            };

            aiSend.addEventListener('click', sendMessage);
            aiInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        }
    }

    async sendAIMessage(message) {
        const messagesContainer = document.getElementById('aiMessages');
        
        // Add user message
        this.addAIMessage('user', message);
        
        // Add loading message
        const loadingId = 'loading-' + Date.now();
        this.addAIMessage('assistant', this.translations[this.currentLanguage].loading || 'Loading...', loadingId);

        try {
            const response = await fetch('/api/ai-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    context: {
                        user_id: this.currentUserId,
                        language: this.currentLanguage,
                        page: 'buyer_dashboard'
                    }
                })
            });

            const data = await response.json();
            
            // Remove loading message
            const loadingElement = document.getElementById(loadingId);
            if (loadingElement) {
                loadingElement.remove();
            }

            if (data.success) {
                this.addAIMessage('assistant', data.response);
            } else {
                this.addAIMessage('assistant', data.error || 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('AI Chat Error:', error);
            
            // Remove loading message
            const loadingElement = document.getElementById(loadingId);
            if (loadingElement) {
                loadingElement.remove();
            }
            
            this.addAIMessage('assistant', 'I\'m having trouble connecting right now. Please try again in a moment.');
        }
    }

    addAIMessage(type, content, id = null) {
        const messagesContainer = document.getElementById('aiMessages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${type}`;
        if (id) messageDiv.id = id;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        this.aiMessages.push({ type, content, timestamp: new Date() });
    }

    // Cart functionality
    initializeCart() {
        this.updateCartBadge();
    }

    async addToCart(cropId, quantity = 1) {
        if (!this.currentUserId) {
            this.showNotification('error', 'Please login to add items to cart');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('buyer_id', this.currentUserId);
            formData.append('crop_id', cropId);
            formData.append('quantity', quantity);

            const response = await fetch('/add-to-cart', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                // Update cart count from server response
                if (data.cart_count !== undefined) {
                    this.cartCount = data.cart_count;
                } else {
                    this.cartCount++;
                }
                this.updateCartBadge();
                this.showNotification('success', this.translations[this.currentLanguage].addedToCart || 'Added to cart successfully!');
            } else {
                this.showNotification('error', data.message || 'Failed to add to cart');
            }
        } catch (error) {
            console.error('Add to cart error:', error);
            this.showNotification('error', 'Failed to add to cart');
        }
    }

    updateCartBadge() {
        const badge = document.getElementById('cartBadge');
        if (badge) {
            if (this.cartCount > 0) {
                badge.textContent = this.cartCount;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }
    }

    // Search functionality
    initializeSearch() {
        const searchInput = document.getElementById('searchInput');
        const locationFilter = document.getElementById('locationFilter');
        const minPriceFilter = document.getElementById('minPrice');
        const maxPriceFilter = document.getElementById('maxPrice');

        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.searchCrops(e.target.value);
                }, 300);
            });
        }

        if (locationFilter) {
            locationFilter.addEventListener('change', () => this.filterCrops());
        }

        if (minPriceFilter || maxPriceFilter) {
            [minPriceFilter, maxPriceFilter].forEach(filter => {
                if (filter) {
                    filter.addEventListener('input', () => {
                        clearTimeout(this.filterTimeout);
                        this.filterTimeout = setTimeout(() => this.filterCrops(), 500);
                    });
                }
            });
        }
    }

    async searchCrops(searchTerm = '', location = '', minPrice = 0, maxPrice = Infinity) {
        try {
            const params = new URLSearchParams();
            if (searchTerm) params.append('search', searchTerm);
            if (location) params.append('location', location);
            if (minPrice > 0) params.append('min_price', minPrice);
            if (maxPrice !== Infinity) params.append('max_price', maxPrice);

            const response = await fetch(`/api/crops?${params}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const crops = await response.json();
            console.log('Fetched crops:', crops); // Debug log
            
            this.displayCrops(crops);
        } catch (error) {
            console.error('Search error:', error);
            this.showNotification('error', 'Failed to search crops');
            // Show empty state
            this.displayCrops([]);
        }
    }

    filterCrops() {
        const searchTerm = document.getElementById('searchInput')?.value || '';
        const location = document.getElementById('locationFilter')?.value || '';
        const minPrice = parseFloat(document.getElementById('minPrice')?.value) || 0;
        const maxPrice = parseFloat(document.getElementById('maxPrice')?.value) || Infinity;
        
        this.searchCrops(searchTerm, location, minPrice, maxPrice);
    }

    displayCrops(crops) {
        const container = document.getElementById('cropsContainer');
        if (!container) return;

        if (crops.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <h3>${this.translations[this.currentLanguage].noResults || 'No crops found matching your search.'}</h3>
                    <p>Try adjusting your search criteria.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = crops.map(crop => this.createCropCard(crop)).join('');
    }

    createCropCard(crop) {
        const translations = this.translations[this.currentLanguage];
        
        return `
            <div class="crop-card" 
                 data-crop-id="${crop.id}" 
                 data-crop-name="${crop.name}" 
                 data-crop-price="${crop.price}"
                 data-crop-unit="${crop.unit}">
                <div class="crop-image">
                    ${crop.image_url ? 
                        `<img src="${crop.image_url}" alt="${crop.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'crop-placeholder\\'>🌾</div>'">` : 
                        `<div class="crop-placeholder">🌾</div>`
                    }
                </div>
                <div class="crop-info">
                    <h3 class="crop-name">${this.escapeHtml(crop.name)}</h3>
                    <p class="crop-farmer">${translations.farmer}: <a href="/profile/${crop.farmer_id}?current_user_id=${this.currentUserId}" class="farmer-link">${this.escapeHtml(crop.farmer_name || 'Unknown')}</a></p>
                    <p class="crop-location">📍 ${this.escapeHtml(crop.location)}</p>
                    <p class="crop-quantity">${crop.quantity} ${crop.unit} available</p>
                    <div class="crop-price">₹${crop.price}/${crop.unit}</div>
                </div>
                <div class="crop-actions">
                    <button class="btn btn-primary add-to-cart-btn" 
                            onclick="farm2market.addToCart('${crop.id}', 1)">
                        ${translations.addToCart || 'Add to Cart'}
                    </button>
                    <button class="btn btn-secondary" 
                            onclick="window.location.href='/chat?user_id=${this.currentUserId}&other_user_id=${crop.farmer_id}'">
                        ${translations.chatWithFarmer || 'Chat with Farmer'}
                    </button>
                </div>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async loadInitialData() {
        // Load crops on page load
        await this.searchCrops('');
        
        // Load cart count from server
        await this.loadCartCount();
    }

    async loadCartCount() {
        if (!this.currentUserId) return;
        
        try {
            const response = await fetch(`/api/cart-count?user_id=${this.currentUserId}`);
            const data = await response.json();
            
            if (data.success) {
                this.cartCount = data.cart_count;
                this.updateCartBadge();
            }
        } catch (error) {
            console.error('Failed to load cart count:', error);
        }
    }

    // Utility functions
    showNotification(type, message) {
        // Create notification element if it doesn't exist
        let notification = document.getElementById('notification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'notification';
            notification.className = 'notification';
            document.body.appendChild(notification);
        }

        notification.className = `notification ${type} show`;
        notification.textContent = message;

        // Auto hide after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Global notification function for standalone use
    static showGlobalNotification(type, message) {
        let notification = document.getElementById('notification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'notification';
            notification.className = 'notification';
            document.body.appendChild(notification);
        }

        notification.className = `notification ${type} show`;
        notification.textContent = message;

        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Price suggestion functionality
    async getPriceSuggestion(cropName, location) {
        try {
            const response = await fetch(`/api/price-suggestion?crop_name=${encodeURIComponent(cropName)}&location=${encodeURIComponent(location)}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Price suggestion error:', error);
            return null;
        }
    }

    // ==== NEW HACKATHON FEATURES ====

    // 1. Smart Crop Recommendations
    async getSmartRecommendations(userId) {
        try {
            const response = await fetch(`/api/recommendations/${userId}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Smart recommendations error:', error);
            return null;
        }
    }

    displayRecommendations(recommendations) {
        const container = document.getElementById('recommendations-container');
        if (!container) return;

        if (!recommendations || recommendations.ai_recommendations.length === 0) {
            container.innerHTML = '<p>No recommendations available at the moment.</p>';
            return;
        }

        let html = '<div class="recommendations-section">';
        html += '<h3>🤖 AI Recommendations for You</h3>';
        
        recommendations.ai_recommendations.forEach(rec => {
            html += `
                <div class="recommendation-card">
                    <div class="rec-header">
                        <h4>${rec.crop_name}</h4>
                        <span class="season-score">Season Score: ${(rec.season_score * 100).toFixed(0)}%</span>
                    </div>
                    <p class="rec-reason">${rec.reason}</p>
                    <p class="nutrition-benefits"><strong>Benefits:</strong> ${rec.nutrition_benefits}</p>
                    <p class="price-range"><strong>Est. Price:</strong> ${rec.estimated_price_range}</p>
                </div>
            `;
        });

        if (recommendations.available_crops.length > 0) {
            html += '<h4>🌱 Available Now:</h4>';
            recommendations.available_crops.forEach(crop => {
                html += `
                    <div class="available-crop">
                        <span class="crop-name">${crop.farmer_name}</span> - 
                        <span class="crop-price">₹${crop.price}/${crop.unit}</span> 
                        <button onclick="farm2market.addToCart('${crop.crop_id}', 1)" class="btn-sm btn-primary">Add to Cart</button>
                    </div>
                `;
            });
        }

        html += '</div>';
        container.innerHTML = html;
    }

    // 2. Carbon Footprint Calculator
    async calculateCarbonFootprint(userId, cropId, quantity, transportMode) {
        try {
            const formData = new FormData();
            formData.append('user_id', userId);
            formData.append('crop_id', cropId);
            formData.append('quantity', quantity);
            formData.append('transport_mode', transportMode);

            const response = await fetch('/api/carbon-footprint', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Carbon footprint calculation error:', error);
            return null;
        }
    }

    showCarbonFootprint(data) {
        if (!data || !data.success) return;

        const footprint = data.carbon_footprint;
        const modal = document.createElement('div');
        modal.className = 'carbon-modal';
        modal.innerHTML = `
            <div class="carbon-modal-content">
                <div class="carbon-header">
                    <h3>🌍 Your Environmental Impact</h3>
                    <button onclick="this.closest('.carbon-modal').remove()" class="close-btn">&times;</button>
                </div>
                <div class="carbon-details">
                    <div class="carbon-stat">
                        <span class="carbon-label">Carbon Emissions:</span>
                        <span class="carbon-value">${footprint.total_emissions_kg} kg CO₂</span>
                    </div>
                    <div class="carbon-stat highlight">
                        <span class="carbon-label">Carbon Saved:</span>
                        <span class="carbon-value">${footprint.carbon_saved_kg} kg CO₂</span>
                    </div>
                    <div class="carbon-stat">
                        <span class="carbon-label">Distance:</span>
                        <span class="carbon-value">${footprint.distance_km} km</span>
                    </div>
                    <div class="carbon-stat">
                        <span class="carbon-label">Transport:</span>
                        <span class="carbon-value">${footprint.transport_mode}</span>
                    </div>
                    <div class="environmental-message">
                        ${footprint.environmental_impact}
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    async getCarbonHistory(userId) {
        try {
            const response = await fetch(`/api/carbon-history/${userId}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Carbon history error:', error);
            return null;
        }
    }

    // 3. Voice Search Integration
    initializeVoiceSearch() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.log('Voice search not supported in this browser');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onresult = (event) => {
            const query = event.results[0][0].transcript;
            this.processVoiceSearch(query);
        };

        this.recognition.onerror = (event) => {
            console.error('Voice recognition error:', event.error);
            this.showNotification('Voice search error. Please try again.', 'error');
        };

        // Add voice search button to search bars
        this.addVoiceSearchButtons();
    }

    addVoiceSearchButtons() {
        const searchInputs = document.querySelectorAll('input[type="text"]');
        searchInputs.forEach(input => {
            if (input.placeholder && input.placeholder.toLowerCase().includes('search')) {
                const voiceBtn = document.createElement('button');
                voiceBtn.innerHTML = '🎤';
                voiceBtn.className = 'voice-search-btn';
                voiceBtn.type = 'button';
                voiceBtn.onclick = () => this.startVoiceSearch();
                
                input.parentNode.insertBefore(voiceBtn, input.nextSibling);
            }
        });
    }

    startVoiceSearch() {
        if (!this.recognition) {
            this.showNotification('Voice search not available', 'error');
            return;
        }

        this.showNotification('🎤 Listening... Speak now!', 'info');
        this.recognition.start();
    }

    async processVoiceSearch(query) {
        try {
            this.showNotification(`Searching for: "${query}"`, 'info');

            const formData = new FormData();
            formData.append('query', query);

            const response = await fetch('/api/voice-search', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                this.displayVoiceSearchResults(data);
            } else {
                this.showNotification('No results found for your voice search', 'error');
            }
        } catch (error) {
            console.error('Voice search processing error:', error);
            this.showNotification('Voice search failed. Please try again.', 'error');
        }
    }

    displayVoiceSearchResults(data) {
        // Create or update search results container
        let resultsContainer = document.getElementById('voice-search-results');
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'voice-search-results';
            resultsContainer.className = 'voice-search-results';
            
            // Insert after search bar or at top of crop list
            const searchContainer = document.querySelector('.search-bar') || document.querySelector('.crops-container');
            if (searchContainer) {
                searchContainer.parentNode.insertBefore(resultsContainer, searchContainer.nextSibling);
            }
        }

        let html = `
            <div class="voice-results-header">
                <h3>🗣️ Voice Search Results</h3>
                <p><strong>You said:</strong> "${data.original_query}"</p>
                ${data.parsed_query ? `<p><strong>Understood:</strong> Looking for ${data.parsed_query.crops?.join(', ') || 'crops'}${data.parsed_query.location ? ` in ${data.parsed_query.location}` : ''}</p>` : ''}
                <button onclick="this.closest('.voice-search-results').remove()" class="close-btn">×</button>
            </div>
        `;

        if (data.matching_crops && data.matching_crops.length > 0) {
            html += '<div class="voice-crops-grid">';
            data.matching_crops.forEach(crop => {
                html += this.createCropCard(crop);
            });
            html += '</div>';
        } else {
            html += '<p>No crops found matching your voice search. Try speaking more clearly or using different terms.</p>';
        }

        resultsContainer.innerHTML = html;
    }

    // 4. Farmer Rating System
    async submitFarmerRating(farmerId, buyerId, rating, review, orderId) {
        try {
            const formData = new FormData();
            formData.append('farmer_id', farmerId);
            formData.append('buyer_id', buyerId);
            formData.append('rating', rating);
            formData.append('review', review);
            formData.append('order_id', orderId);

            const response = await fetch('/api/rate-farmer', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Rating submission error:', error);
            return null;
        }
    }

    async getFarmerRatings(farmerId) {
        try {
            const response = await fetch(`/api/farmer-ratings/${farmerId}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Get farmer ratings error:', error);
            return null;
        }
    }

    showRatingModal(farmerId, orderId) {
        const modal = document.createElement('div');
        modal.className = 'rating-modal';
        modal.innerHTML = `
            <div class="rating-modal-content">
                <div class="rating-header">
                    <h3>⭐ Rate Your Experience</h3>
                    <button onclick="this.closest('.rating-modal').remove()" class="close-btn">&times;</button>
                </div>
                <div class="rating-form">
                    <div class="star-rating">
                        <span class="star" data-rating="1">⭐</span>
                        <span class="star" data-rating="2">⭐</span>
                        <span class="star" data-rating="3">⭐</span>
                        <span class="star" data-rating="4">⭐</span>
                        <span class="star" data-rating="5">⭐</span>
                    </div>
                    <textarea placeholder="Share your experience with this farmer..." id="review-text" rows="4"></textarea>
                    <button onclick="farm2market.submitRating('${farmerId}', '${orderId}')" class="btn btn-primary">Submit Rating</button>
                </div>
            </div>
        `;

        // Add star rating interaction
        modal.querySelectorAll('.star').forEach(star => {
            star.onclick = () => {
                const rating = star.dataset.rating;
                modal.querySelectorAll('.star').forEach((s, index) => {
                    s.style.opacity = index < rating ? '1' : '0.3';
                });
                modal.dataset.selectedRating = rating;
            };
        });

        document.body.appendChild(modal);
    }

    async submitRating(farmerId, orderId) {
        const modal = document.querySelector('.rating-modal');
        const rating = modal.dataset.selectedRating;
        const review = modal.querySelector('#review-text').value;

        if (!rating) {
            this.showNotification('Please select a star rating', 'error');
            return;
        }

        const result = await this.submitFarmerRating(farmerId, this.currentUserId, rating, review, orderId);
        
        if (result && result.success) {
            this.showNotification('Thank you for your feedback!', 'success');
            modal.remove();
        } else {
            this.showNotification('Failed to submit rating. Please try again.', 'error');
        }
    }

    displayFarmerRatings(ratingsData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const stats = ratingsData.stats;
        
        let html = `
            <div class="farmer-ratings-section">
                <div class="rating-summary">
                    <div class="average-rating">
                        <span class="rating-number">${stats.average_rating}</span>
                        <div class="rating-stars">
                            ${'⭐'.repeat(Math.round(stats.average_rating))}
                        </div>
                        <span class="rating-count">(${stats.total_ratings} reviews)</span>
                    </div>
                </div>
        `;

        if (ratingsData.recent_reviews && ratingsData.recent_reviews.length > 0) {
            html += '<div class="recent-reviews">';
            html += '<h4>Recent Reviews:</h4>';
            ratingsData.recent_reviews.forEach(review => {
                html += `
                    <div class="review-item">
                        <div class="review-header">
                            <span class="reviewer-name">${review.buyer_name}</span>
                            <span class="review-rating">${'⭐'.repeat(review.rating)}</span>
                        </div>
                        <p class="review-text">${review.review}</p>
                    </div>
                `;
            });
            html += '</div>';
        }

        html += '</div>';
        container.innerHTML = html;
    }

    // Initialize all new features
    initializeHackathonFeatures() {
        this.initializeVoiceSearch();
        
        // Load recommendations if on buyer dashboard
        if (window.location.pathname.includes('buyer-dashboard') && this.currentUserId) {
            this.loadSmartRecommendations();
        }

        // Add carbon footprint tracking to add-to-cart actions
        this.enhanceAddToCartWithCarbon();
    }

    async loadSmartRecommendations() {
        const recommendations = await this.getSmartRecommendations(this.currentUserId);
        if (recommendations) {
            this.displayRecommendations(recommendations);
        }
    }

    enhanceAddToCartWithCarbon() {
        // Override existing addToCart to include carbon calculation
        const originalAddToCart = this.addToCart.bind(this);
        
        this.addToCart = async (cropId, quantity) => {
            // Call original function
            const result = await originalAddToCart(cropId, quantity);
            
            // If successful, calculate carbon footprint
            if (result && this.currentUserId) {
                // Show transport mode selection
                this.showTransportModeSelection(cropId, quantity);
            }
            
            return result;
        };
    }

    showTransportModeSelection(cropId, quantity) {
        const modal = document.createElement('div');
        modal.className = 'transport-modal';
        modal.innerHTML = `
            <div class="transport-modal-content">
                <h3>🚛 How will you collect this order?</h3>
                <div class="transport-options">
                    <button onclick="farm2market.selectTransportMode('${cropId}', ${quantity}, 'bike')" class="transport-btn">🏍️ Bike</button>
                    <button onclick="farm2market.selectTransportMode('${cropId}', ${quantity}, 'own_vehicle')" class="transport-btn">🚗 Own Vehicle</button>
                    <button onclick="farm2market.selectTransportMode('${cropId}', ${quantity}, 'public_transport')" class="transport-btn">🚌 Public Transport</button>
                    <button onclick="farm2market.selectTransportMode('${cropId}', ${quantity}, 'truck')" class="transport-btn">🚛 Truck</button>
                    <button onclick="farm2market.selectTransportMode('${cropId}', ${quantity}, 'walking')" class="transport-btn">🚶 Walking</button>
                </div>
                <button onclick="this.closest('.transport-modal').remove()" class="skip-btn">Skip</button>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    async selectTransportMode(cropId, quantity, mode) {
        const footprint = await this.calculateCarbonFootprint(this.currentUserId, cropId, quantity, mode);
        
        if (footprint) {
            this.showCarbonFootprint(footprint);
        }
        
        // Remove transport modal
        document.querySelector('.transport-modal')?.remove();
    }
}

// Initialize Farm2Market when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.farm2market = new Farm2Market();
    
    // Initialize hackathon features
    setTimeout(() => {
        window.farm2market.initializeHackathonFeatures();
    }, 1000);
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Farm2Market;
} 