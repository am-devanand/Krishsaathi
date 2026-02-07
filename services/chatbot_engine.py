# Intelligent Chatbot Engine for KRISHSAATHI
# Uses agricultural knowledge base for smart responses in regional languages

import re
import random
from translations import get_translation

# Import knowledge base
try:
    from services.agri_knowledge import (
        CROP_DATABASE, PEST_DATABASE, DISEASE_DATABASE,
        GOVERNMENT_SCHEMES, WEATHER_ADVISORY, IMAGE_ANALYSIS_PATTERNS
    )
except ImportError:
    CROP_DATABASE = {}
    PEST_DATABASE = {}
    DISEASE_DATABASE = {}
    GOVERNMENT_SCHEMES = {}
    WEATHER_ADVISORY = {}
    IMAGE_ANALYSIS_PATTERNS = {}

# =============================================================================
# Language-aware response templates
# =============================================================================

RESPONSE_TEMPLATES = {
    "en": {
        "greeting": "Hello! I'm your intelligent farming assistant. Ask me about crops, pests, diseases, weather, mandi prices, or government schemes. How can I help you today?",
        "crop_info": "Here's information about {crop}:\n\n🌱 **Season**: {season}\n💧 **Water Need**: {water}\n🌍 **Soil Type**: {soil}\n📊 **Yield Potential**: {yield_}\n\n**Common Pests**: {pests}\n**Common Diseases**: {diseases}",
        "pest_info": "**{pest}** ({hindi})\n\n**Affects**: {affects}\n**Identification**: {id_}\n\n**🌿 Organic Treatment**:\n{organic}\n\n**💊 Chemical Treatment**:\n{chemical}\n\n**🛡️ Prevention**:\n{prevention}",
        "disease_info": "**{disease}** ({hindi})\n\n**Affects**: {affects}\n**Symptoms**: {symptoms}\n\n**Treatment**:\n{treatment}\n\n**Prevention**:\n{prevention}",
        "scheme_info": "**{name}** ({hindi})\n\n💰 **Benefit**: {benefit}\n👤 **Eligibility**: {eligibility}\n📝 **How to Apply**: {how_to}\n📄 **Documents Needed**: {docs}",
        "weather_advice": "Based on the weather conditions, here's my advice:\n\n{advice}",
        "not_found": "I don't have specific information about that, but here are some general tips:\n\n{tips}",
        "image_analysis": "{analysis}\n\n📞 **Need more help?** Contact your local Krishi Vigyan Kendra or agriculture officer.",
        "mandi_prices": "🌾 **Current Mandi Prices** (indicative):\n\nWheat: ₹2,200-2,400/quintal\nPaddy: ₹2,100-2,300/quintal\nCotton: ₹6,000-6,500/quintal\nSoybean: ₹4,200-4,600/quintal\nSugarcane: ₹340-380/quintal\n\n💡 Check eNAM (enam.gov.in) for real-time prices in your area."
    },
    "hi": {
        "greeting": "नमस्ते! मैं आपका कृषि सहायक हूं। फसलों, कीटों, रोगों, मौसम, मंडी भाव या सरकारी योजनाओं के बारे में पूछें। आज मैं आपकी क्या मदद कर सकता हूं?",
        "crop_info": "**{crop}** की जानकारी:\n\n🌱 **सीज़न**: {season}\n💧 **पानी की आवश्यकता**: {water}\n🌍 **मिट्टी का प्रकार**: {soil}\n📊 **उपज क्षमता**: {yield_}\n\n**प्रमुख कीट**: {pests}\n**प्रमुख रोग**: {diseases}",
        "pest_info": "**{pest}** ({hindi})\n\n**प्रभावित फसलें**: {affects}\n**पहचान**: {id_}\n\n**🌿 जैविक उपचार**:\n{organic}\n\n**💊 रासायनिक उपचार**:\n{chemical}\n\n**🛡️ रोकथाम**:\n{prevention}",
        "disease_info": "**{disease}** ({hindi})\n\n**प्रभावित फसलें**: {affects}\n**लक्षण**: {symptoms}\n\n**उपचार**:\n{treatment}\n\n**रोकथाम**:\n{prevention}",
        "scheme_info": "**{name}** ({hindi})\n\n💰 **लाभ**: {benefit}\n👤 **पात्रता**: {eligibility}\n📝 **आवेदन कैसे करें**: {how_to}\n📄 **आवश्यक दस्तावेज़**: {docs}",
        "weather_advice": "मौसम की स्थिति के आधार पर, मेरी सलाह:\n\n{advice}",
        "not_found": "इसके बारे में विशेष जानकारी नहीं है, लेकिन कुछ सामान्य सुझाव:\n\n{tips}",
        "image_analysis": "{analysis}\n\n📞 **अधिक मदद चाहिए?** अपने स्थानीय कृषि विज्ञान केंद्र या कृषि अधिकारी से संपर्क करें।",
        "mandi_prices": "🌾 **वर्तमान मंडी भाव** (अनुमानित):\n\nगेहूं: ₹2,200-2,400/क्विंटल\nधान: ₹2,100-2,300/क्विंटल\nकपास: ₹6,000-6,500/क्विंटल\nसोयाबीन: ₹4,200-4,600/क्विंटल\nगन्ना: ₹340-380/क्विंटल\n\n💡 अपने क्षेत्र की ताज़ा कीमतों के लिए eNAM (enam.gov.in) देखें।"
    }
}

# Keywords for intent detection (multilingual)
INTENT_KEYWORDS = {
    "crop": ["crop", "फसल", "paddy", "धान", "wheat", "गेहूं", "cotton", "कपास", "maize", "मक्का", "soybean", "सोयाबीन", "sugarcane", "गन्ना", "groundnut", "मूंगफली", "chickpea", "चना"],
    "pest": ["pest", "कीट", "insect", "कीड़ा", "borer", "छेदक", "caterpillar", "सुंडी", "bollworm", "whitefly", "aphid", "माहू", "armyworm"],
    "disease": ["disease", "रोग", "blight", "झुलसा", "rust", "गेरुआ", "wilt", "उकठा", "mildew", "फफूंद", "blast", "yellow", "पीला", "rot", "सड़न"],
    "scheme": ["scheme", "योजना", "pm kisan", "पीएम किसान", "fasal bima", "बीमा", "kcc", "credit card", "subsidy", "सब्सिडी", "loan", "ऋण"],
    "weather": ["weather", "मौसम", "rain", "बारिश", "temperature", "तापमान", "forecast", "hot", "cold", "ठंड", "humidity"],
    "mandi": ["mandi", "मंडी", "price", "भाव", "rate", "दर", "sell", "बेचना", "market", "बाजार"],
    "soil": ["soil", "मिट्टी", "fertilizer", "उर्वरक", "खाद", "nutrient", "पोषक", "nitrogen", "urea", "यूरिया", "dap"],
    "greeting": ["hello", "hi", "namaste", "नमस्ते", "help", "मदद", "hii", "hey"]
}

def detect_intent(message):
    """Detect user intent from message."""
    msg_lower = message.lower()
    
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in msg_lower:
                return intent
    
    return "general"

def find_crop_in_message(message):
    """Find crop name in message."""
    msg_lower = message.lower()
    
    # Check all crops
    for crop_key, crop_data in CROP_DATABASE.items():
        if crop_key in msg_lower or crop_data.get("hindi", "").lower() in msg_lower:
            return crop_key
    
    return None

def find_pest_in_message(message):
    """Find pest name in message."""
    msg_lower = message.lower()
    
    for pest_key, pest_data in PEST_DATABASE.items():
        if pest_key.replace("_", " ") in msg_lower or pest_data.get("hindi", "").lower() in msg_lower:
            return pest_key
    
    return None

def find_disease_in_message(message):
    """Find disease name in message."""
    msg_lower = message.lower()
    
    for disease_key, disease_data in DISEASE_DATABASE.items():
        if disease_key.replace("_", " ") in msg_lower or disease_data.get("hindi", "").lower() in msg_lower:
            return disease_key
    
    return None

def find_scheme_in_message(message):
    """Find scheme name in message."""
    msg_lower = message.lower()
    
    for scheme_key, scheme_data in GOVERNMENT_SCHEMES.items():
        keywords = [scheme_key, scheme_data["name"].lower(), scheme_data["hindi"].lower()]
        for kw in keywords:
            if kw.replace("_", " ") in msg_lower:
                return scheme_key
    
    return None

def get_crop_response(crop_key, lang):
    """Generate response for crop query."""
    crop = CROP_DATABASE.get(crop_key)
    if not crop:
        return None
    
    templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
    
    return templates["crop_info"].format(
        crop=crop_key.title(),
        season=", ".join(crop.get("season", [])),
        water=crop.get("water_need", "medium"),
        soil=", ".join(crop.get("soil_type", [])),
        yield_=crop.get("yield_potential", "varies"),
        pests=", ".join(crop.get("common_pests", [])[:4]),
        diseases=", ".join(crop.get("common_diseases", [])[:4])
    )

def get_pest_response(pest_key, lang):
    """Generate response for pest query."""
    pest = PEST_DATABASE.get(pest_key)
    if not pest:
        return None
    
    templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
    
    return templates["pest_info"].format(
        pest=pest_key.replace("_", " ").title(),
        hindi=pest.get("hindi", ""),
        affects=", ".join(pest.get("affects", [])),
        id_=pest.get("identification", ""),
        organic="\n".join(f"• {t}" for t in pest.get("organic_treatment", [])[:3]),
        chemical="\n".join(f"• {t}" for t in pest.get("chemical_treatment", [])[:3]),
        prevention="\n".join(f"• {t}" for t in pest.get("prevention", [])[:3])
    )

def get_disease_response(disease_key, lang):
    """Generate response for disease query."""
    disease = DISEASE_DATABASE.get(disease_key)
    if not disease:
        return None
    
    templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
    
    return templates["disease_info"].format(
        disease=disease_key.replace("_", " ").title(),
        hindi=disease.get("hindi", ""),
        affects=", ".join(disease.get("affects", [])),
        symptoms=", ".join(disease.get("symptoms", [])[:4]),
        treatment="\n".join(f"• {t}" for t in disease.get("treatment", [])[:4]),
        prevention="\n".join(f"• {t}" for t in disease.get("prevention", [])[:3])
    )

def get_scheme_response(scheme_key, lang):
    """Generate response for scheme query."""
    scheme = GOVERNMENT_SCHEMES.get(scheme_key)
    if not scheme:
        return None
    
    templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
    
    return templates["scheme_info"].format(
        name=scheme.get("name", ""),
        hindi=scheme.get("hindi", ""),
        benefit=scheme.get("benefit", ""),
        eligibility=scheme.get("eligibility", ""),
        how_to=scheme.get("how_to_apply", ""),
        docs=", ".join(scheme.get("documents", []))
    )

def analyze_image_symptoms(message):
    """Analyze image based on text description or simulate analysis."""
    msg_lower = message.lower()
    
    # Check for symptom keywords
    if any(word in msg_lower for word in ["yellow", "पीला", "yellowing"]):
        return IMAGE_ANALYSIS_PATTERNS.get("yellow_leaves", {}).get("response_template", "")
    elif any(word in msg_lower for word in ["brown", "भूरा", "spot", "धब्बा"]):
        return IMAGE_ANALYSIS_PATTERNS.get("brown_spots", {}).get("response_template", "")
    elif any(word in msg_lower for word in ["wilt", "मुर्झा", "wilting", "सूख"]):
        return IMAGE_ANALYSIS_PATTERNS.get("wilting", {}).get("response_template", "")
    elif any(word in msg_lower for word in ["hole", "छेद", "eaten", "कटा"]):
        return IMAGE_ANALYSIS_PATTERNS.get("holes_in_leaves", {}).get("response_template", "")
    elif any(word in msg_lower for word in ["white", "सफेद", "powder", "चूर्ण"]):
        return IMAGE_ANALYSIS_PATTERNS.get("white_powder", {}).get("response_template", "")
    else:
        return IMAGE_ANALYSIS_PATTERNS.get("healthy_crop", {}).get("response_template", "")

def get_general_tips(lang):
    """Get general farming tips."""
    tips_en = [
        "🌱 Scout your fields regularly for early pest detection",
        "💧 Irrigate based on crop needs, not on fixed schedule",
        "🧪 Get soil tested every season for balanced fertilization",
        "📱 Use eNAM app for better market prices",
        "📞 Contact local Krishi Vigyan Kendra for expert advice"
    ]
    
    tips_hi = [
        "🌱 कीट-रोगों की जल्दी पहचान के लिए नियमित खेत निरीक्षण करें",
        "💧 सिंचाई फसल की जरूरत के अनुसार करें",
        "🧪 हर सीज़न मिट्टी जांच करवाएं",
        "📱 बेहतर बाजार भाव के लिए eNAM ऐप का उपयोग करें",
        "📞 विशेषज्ञ सलाह के लिए कृषि विज्ञान केंद्र से संपर्क करें"
    ]
    
    tips = tips_hi if lang == "hi" else tips_en
    return "\n".join(tips)

def get_chatbot_reply(message, lang="hi"):
    """
    Main function to generate intelligent chatbot reply.
    Uses knowledge base for comprehensive agricultural responses.
    """
    if not message:
        templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
        return templates["greeting"]
    
    msg = message.strip()
    intent = detect_intent(msg)
    
    # Handle greeting
    if intent == "greeting":
        templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
        return templates["greeting"]
    
    # Handle crop queries
    if intent == "crop":
        crop = find_crop_in_message(msg)
        if crop:
            response = get_crop_response(crop, lang)
            if response:
                return response
    
    # Handle pest queries
    if intent == "pest" or "pest" in msg.lower() or "कीट" in msg:
        pest = find_pest_in_message(msg)
        if pest:
            response = get_pest_response(pest, lang)
            if response:
                return response
        # If no specific pest found, give general pest tips
        if lang == "hi":
            return "कीट प्रबंधन के लिए:\n\n🌿 **जैविक विधियां**:\n• नीम तेल 5ml/लीटर छिड़काव\n• ट्राइकोग्रामा कार्ड लगाएं\n• फेरोमोन ट्रैप 5/हेक्टेयर\n\n💡 **रासायनिक नियंत्रण**: केवल आर्थिक क्षति स्तर (ETL) पार होने पर करें।\n\n📞 अपनी फसल का नाम बताएं तो विस्तृत जानकारी दे सकता हूं।"
        else:
            return "For pest management:\n\n🌿 **Organic methods**:\n• Neem oil 5ml/liter spray\n• Release Trichogramma cards\n• Pheromone traps 5/hectare\n\n💡 **Chemical control**: Only when pest crosses Economic Threshold Level.\n\n📞 Tell me your crop name for specific pest management advice."
    
    # Handle disease queries
    if intent == "disease" or any(word in msg.lower() for word in ["disease", "रोग", "infection", "problem"]):
        disease = find_disease_in_message(msg)
        if disease:
            response = get_disease_response(disease, lang)
            if response:
                return response
        # Analyze symptoms from message
        analysis = analyze_image_symptoms(msg)
        if analysis:
            templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
            return templates["image_analysis"].format(analysis=analysis)
    
    # Handle scheme queries
    if intent == "scheme":
        scheme = find_scheme_in_message(msg)
        if scheme:
            response = get_scheme_response(scheme, lang)
            if response:
                return response
        # List all schemes
        if lang == "hi":
            return "**प्रमुख सरकारी योजनाएं**:\n\n1. 🌾 **PM-KISAN**: ₹6000/वर्ष\n2. 🛡️ **फसल बीमा योजना**: कम प्रीमियम पर बीमा\n3. 💳 **किसान क्रेडिट कार्ड**: 4% ब्याज पर ऋण\n4. 🧪 **मृदा स्वास्थ्य कार्ड**: मुफ्त मिट्टी जांच\n5. 📱 **eNAM**: ऑनलाइन मंडी\n\nकिसी योजना के बारे में विस्तार से जानने के लिए उसका नाम बताएं।"
        else:
            return "**Major Government Schemes**:\n\n1. 🌾 **PM-KISAN**: ₹6000/year\n2. 🛡️ **Fasal Bima Yojana**: Crop insurance at low premium\n3. 💳 **Kisan Credit Card**: Loan at 4% interest\n4. 🧪 **Soil Health Card**: Free soil testing\n5. 📱 **eNAM**: Online trading\n\nAsk about any specific scheme for details."
    
    # Handle mandi/price queries
    if intent == "mandi":
        templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
        return templates["mandi_prices"]
    
    # Handle weather queries
    if intent == "weather":
        if lang == "hi":
            return "**मौसम आधारित सलाह**:\n\n☀️ **गर्मी में**:\n• सुबह/शाम सिंचाई करें\n• पलवार (मल्चिंग) करें\n\n🌧️ **बारिश की संभावना हो तो**:\n• कीटनाशक छिड़काव न करें\n• जल निकासी सुनिश्चित करें\n\n❄️ **ठंड में**:\n• शाम को हल्की सिंचाई (पाला से बचाव)\n• पौधों को ढकें\n\n📱 **सटीक मौसम** के लिए Meghdoot या Kisan Suvidha ऐप देखें।"
        else:
            return "**Weather-based Advisory**:\n\n☀️ **Hot weather**:\n• Irrigate in morning/evening\n• Apply mulch to conserve moisture\n\n🌧️ **Rain expected**:\n• Avoid pesticide spray\n• Ensure drainage\n\n❄️ **Cold wave**:\n• Light irrigation in evening (frost protection)\n• Cover sensitive crops\n\n📱 Check Meghdoot or Kisan Suvidha app for accurate forecast."
    
    # Handle soil/fertilizer queries
    if intent == "soil":
        if lang == "hi":
            return "**मृदा एवं उर्वरक सलाह**:\n\n🧪 **मिट्टी जांच** करवाएं - मुफ्त है!\n\n**सामान्य सिफारिश**:\n• नाइट्रोजन (N): यूरिया से\n• फास्फोरस (P): DAP से\n• पोटाश (K): MOP से\n\n💡 **जैविक विकल्प**:\n• वर्मीकम्पोस्ट 2-5 टन/हेक्टेयर\n• जीवामृत/घनजीवामृत\n• हरी खाद\n\n⚠️ **सावधानी**: बिना मिट्टी जांच के उर्वरक न डालें।"
        else:
            return "**Soil & Fertilizer Advice**:\n\n🧪 **Get soil tested** - It's FREE!\n\n**General recommendations**:\n• Nitrogen (N): from Urea\n• Phosphorus (P): from DAP\n• Potash (K): from MOP\n\n💡 **Organic options**:\n• Vermicompost 2-5 tonnes/hectare\n• Jeevamrit/Ghanjeevamrit\n• Green manuring\n\n⚠️ **Caution**: Don't apply fertilizers without soil test."
    
    # Default helpful response
    templates = RESPONSE_TEMPLATES.get(lang, RESPONSE_TEMPLATES["en"])
    tips = get_general_tips(lang)
    return templates["not_found"].format(tips=tips)
