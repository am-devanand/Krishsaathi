# OpenAI-Powered Agricultural AI Service for KRISHSAATHI
# Full OpenAI GPT-4o integration for Voice Assistant and Chatbot

import re
import os
from openai import OpenAI
from services.chatbot_engine import get_chatbot_reply, analyze_image_symptoms, RESPONSE_TEMPLATES
from translations import get_translation
from models import db, Farmer

# Initialize OpenAI client
try:
    from config import OPENAI_API_KEY
    if OPENAI_API_KEY:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        openai_client = None
except Exception as e:
    print(f"OpenAI init error: {e}")
    openai_client = None

# Language name mapping for prompts
LANGUAGE_NAMES = {
    'hi': 'Hindi (हिंदी)', 'bn': 'Bengali (বাংলা)', 'te': 'Telugu (తెలుగు)', 
    'mr': 'Marathi (मराठी)', 'ta': 'Tamil (தமிழ்)', 'gu': 'Gujarati (ગુજરાતી)', 
    'kn': 'Kannada (ಕನ್ನಡ)', 'or': 'Odia (ଓଡ଼ିଆ)', 'ml': 'Malayalam (മലയാളം)', 
    'pa': 'Punjabi (ਪੰਜਾਬੀ)', 'as': 'Assamese (অসমীয়া)', 'en': 'English',
}

# System prompt for agricultural AI
SYSTEM_PROMPT = """You are KRISHSAATHI, an expert AI agricultural assistant for Indian farmers.

YOUR CAPABILITIES:
1. **Crop Advisory**: Expert knowledge on paddy, wheat, cotton, sugarcane, maize, soybean, groundnut, chickpea, and all major Indian crops
2. **Pest & Disease Management**: Identify pests/diseases, suggest organic and chemical treatments
3. **Government Schemes**: PM-KISAN, Fasal Bima Yojana, KCC, Soil Health Card, eNAM
4. **Market Information**: Mandi prices, selling strategies, MSP information
5. **Weather Advisory**: Farming tips based on weather conditions
6. **Soil & Fertilizer**: Soil health, fertilizer recommendations, organic farming

IMPORTANT RULES:
1. ALWAYS respond in {language} language using the appropriate script
2. Be practical and actionable - farmers need immediate solutions
3. Use bullet points, emojis, and formatting for clarity
4. Mention specific dosages, timings, and methods
5. If unsure, recommend contacting local Krishi Vigyan Kendra
6. Be encouraging and supportive of the farmer
7. For government schemes, mention eligibility and how to apply
8. Include both organic and chemical solutions when relevant

CONTEXT:
- Farmer's name: {farmer_name}
- Location: {location}
- Current season: Consider Indian agricultural seasons (Kharif: June-Oct, Rabi: Oct-Mar, Zaid: Mar-June)

Remember: You are the farmer's trusted companion. Respond with empathy and expertise."""

def get_openai_response(message, lang, farmer_name=None, location=None, image_base64=None):
    """Get response from OpenAI GPT-4o."""
    if not openai_client:
        return None
    
    try:
        lang_name = LANGUAGE_NAMES.get(lang, 'Hindi (हिंदी)')
        loc = location or "India"
        name = farmer_name or "Kisan"
        
        system_prompt = SYSTEM_PROMPT.format(
            language=lang_name,
            farmer_name=name,
            location=loc
        )
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Handle image analysis
        if image_base64:
            # GPT-4o Vision for image analysis
            content = [
                {"type": "text", "text": f"The farmer has shared this image of their crop and asks: '{message or 'What is wrong with my crop?'}'. Analyze the image and provide detailed diagnosis and treatment recommendations in {lang_name}."}
            ]
            
            # Add image to message
            if ',' in image_base64:
                image_data = image_base64  # Already has data URI prefix
            else:
                image_data = f"data:image/jpeg;base64,{image_base64}"
            
            content.append({
                "type": "image_url",
                "image_url": {"url": image_data}
            })
            
            messages.append({"role": "user", "content": content})
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
        else:
            # Text-only conversation
            messages.append({"role": "user", "content": message})
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
        
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()
        
        return None
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def get_pest_health_reply(message, lang, image_base64=None, conversation_id=None, farmer_name=None, farmer_id=None):
    """
    Main AI function - OpenAI GPT-4o powered agricultural responses.
    
    Features:
    1. Form filling from voice/text (state, district detection)
    2. Image analysis using GPT-4o Vision
    3. Intelligent responses in 15+ Indian languages
    4. Fallback to knowledge base if API unavailable
    """
    msg = (message or "").strip()
    msg_lower = msg.lower()
    
    # Get farmer info for context
    farmer = None
    location = None
    if farmer_id:
        farmer = Farmer.query.get(farmer_id)
        if farmer:
            location = f"{farmer.village or ''}, {farmer.district or ''}, {farmer.state or ''}".strip(', ')
    
    # ==========================================================================
    # 1. FORM FILLING - Detect and update profile from voice commands
    # ==========================================================================
    if farmer and msg:
        update_info = {}
        
        # State patterns (English and Hindi)
        state_patterns = [
            r'(?:state is|from|my state|i am from|मेरा राज्य|राज्य है)\s*[:\s]*([a-zA-Z\u0900-\u097F]+)',
            r'([a-zA-Z]+)\s+state',
        ]
        for pattern in state_patterns:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                state = match.group(1).strip().title()
                if len(state) > 2 and state.lower() not in ['is', 'my', 'the', 'in']:
                    farmer.state = state
                    update_info['state'] = state
                    break
        
        # District patterns
        district_patterns = [
            r'(?:district is|district|my district|जिला|ज़िला)\s*[:\s]*([a-zA-Z\u0900-\u097F]+)',
        ]
        for pattern in district_patterns:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                district = match.group(1).strip().title()
                if len(district) > 2 and district.lower() not in ['is', 'my', 'the']:
                    farmer.district = district
                    update_info['district'] = district
                    break
        
        # Village patterns
        village_patterns = [
            r'(?:village is|my village|गांव|गाँव)\s*[:\s]*([a-zA-Z\u0900-\u097F]+)',
        ]
        for pattern in village_patterns:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                village = match.group(1).strip().title()
                if len(village) > 2:
                    farmer.village = village
                    update_info['village'] = village
                    break
        
        if update_info:
            db.session.commit()
            if lang == 'hi':
                parts = []
                if 'state' in update_info:
                    parts.append(f"राज्य={update_info['state']}")
                if 'district' in update_info:
                    parts.append(f"ज़िला={update_info['district']}")
                if 'village' in update_info:
                    parts.append(f"गांव={update_info['village']}")
                return f"✅ अपडेट किया गया: {', '.join(parts)}। पेज रिफ्रेश करें।"
            else:
                parts = []
                if 'state' in update_info:
                    parts.append(f"State={update_info['state']}")
                if 'district' in update_info:
                    parts.append(f"District={update_info['district']}")
                if 'village' in update_info:
                    parts.append(f"Village={update_info['village']}")
                return f"✅ Updated: {', '.join(parts)}. Please refresh to see changes."
    
    # ==========================================================================
    # 2. OPENAI GPT-4o - Primary AI Engine
    # ==========================================================================
    if openai_client and (msg or image_base64):
        response = get_openai_response(
            message=msg,
            lang=lang,
            farmer_name=farmer_name or (farmer.name if farmer else None),
            location=location,
            image_base64=image_base64
        )
        
        if response:
            return response
    
    # ==========================================================================
    # 3. FALLBACK - Knowledge-based response if OpenAI unavailable
    # ==========================================================================
    
    # Image fallback
    if image_base64:
        analysis = analyze_image_symptoms(msg)
        if analysis:
            templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
            return templates["image_analysis"].format(analysis=analysis)
        
        if lang == 'hi':
            return "🔍 छवि विश्लेषण के लिए OpenAI API आवश्यक है। कृपया OPENAI_API_KEY सेट करें या समस्या का विवरण टाइप करें।"
        else:
            return "🔍 Image analysis requires OpenAI API. Please set OPENAI_API_KEY or describe the problem in text."
    
    # Text fallback to knowledge base
    return get_chatbot_reply(msg, lang)
