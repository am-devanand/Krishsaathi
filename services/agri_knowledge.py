# Agricultural Knowledge Base for KRISHSAATHI AI
# Comprehensive Indian farming knowledge for intelligent responses

# =============================================================================
# CROP DATABASE - Major Indian Crops with Complete Information
# =============================================================================

CROP_DATABASE = {
    "paddy": {
        "hindi": "धान",
        "season": ["kharif"],
        "water_need": "high",
        "soil_type": ["clay", "loamy"],
        "common_pests": ["stem_borer", "brown_planthopper", "leaf_folder", "gall_midge"],
        "common_diseases": ["blast", "bacterial_leaf_blight", "sheath_blight", "tungro"],
        "growth_stages": {
            "nursery": "20-30 days",
            "transplanting": "21-25 days after germination",
            "tillering": "30-45 days after transplanting",
            "flowering": "60-70 days after transplanting",
            "maturity": "110-150 days total"
        },
        "fertilizer": {
            "basal": "DAP 100kg/ha + MOP 60kg/ha",
            "top_dressing": "Urea 60kg/ha at tillering, 40kg/ha at panicle initiation"
        },
        "yield_potential": "4-6 tonnes/hectare"
    },
    "wheat": {
        "hindi": "गेहूं",
        "season": ["rabi"],
        "water_need": "medium",
        "soil_type": ["loamy", "clay loam"],
        "common_pests": ["aphid", "termite", "pink_borer", "army_worm"],
        "common_diseases": ["rust", "loose_smut", "karnal_bunt", "powdery_mildew"],
        "growth_stages": {
            "sowing": "November",
            "germination": "7-10 days",
            "tillering": "25-30 days",
            "heading": "75-85 days",
            "maturity": "120-150 days"
        },
        "fertilizer": {
            "basal": "N:P:K = 120:60:40 kg/ha",
            "top_dressing": "Half nitrogen at sowing, half at first irrigation"
        },
        "yield_potential": "4-5 tonnes/hectare"
    },
    "cotton": {
        "hindi": "कपास",
        "season": ["kharif"],
        "water_need": "medium",
        "soil_type": ["black cotton soil", "loamy"],
        "common_pests": ["bollworm", "whitefly", "aphid", "jassid", "pink_bollworm"],
        "common_diseases": ["bacterial_blight", "grey_mildew", "leaf_spot", "root_rot"],
        "growth_stages": {
            "sowing": "April-May",
            "squaring": "45-50 days",
            "flowering": "60-70 days",
            "boll_formation": "80-100 days",
            "maturity": "150-180 days"
        },
        "fertilizer": {
            "basal": "N:P:K = 60:30:30 kg/ha",
            "foliar": "2% DAP spray at flowering"
        },
        "yield_potential": "15-20 quintals/hectare"
    },
    "sugarcane": {
        "hindi": "गन्ना",
        "season": ["year_round"],
        "water_need": "very high",
        "soil_type": ["loamy", "clay loam"],
        "common_pests": ["top_borer", "stem_borer", "pyrilla", "white_grub"],
        "common_diseases": ["red_rot", "smut", "wilt", "ratoon_stunting"],
        "growth_stages": {
            "germination": "30-45 days",
            "tillering": "45-120 days",
            "grand_growth": "120-270 days",
            "maturity": "270-365 days"
        },
        "fertilizer": {
            "N": "250-300 kg/ha in splits",
            "P": "60-80 kg/ha at planting",
            "K": "60 kg/ha"
        },
        "yield_potential": "80-100 tonnes/hectare"
    },
    "maize": {
        "hindi": "मक्का",
        "season": ["kharif", "rabi", "zaid"],
        "water_need": "medium",
        "soil_type": ["loamy", "sandy loam"],
        "common_pests": ["stem_borer", "fall_armyworm", "aphid", "shoot_fly"],
        "common_diseases": ["turcicum_leaf_blight", "downy_mildew", "stalk_rot", "rust"],
        "growth_stages": {
            "germination": "5-7 days",
            "vegetative": "35-40 days",
            "tasseling": "55-60 days",
            "silking": "60-65 days",
            "maturity": "90-120 days"
        },
        "fertilizer": {
            "basal": "N:P:K = 120:60:40 kg/ha"
        },
        "yield_potential": "5-8 tonnes/hectare"
    },
    "soybean": {
        "hindi": "सोयाबीन",
        "season": ["kharif"],
        "water_need": "medium",
        "soil_type": ["loamy", "clay loam"],
        "common_pests": ["stem_fly", "girdle_beetle", "leaf_miner", "pod_borer"],
        "common_diseases": ["yellow_mosaic", "bacterial_pustule", "anthracnose", "charcoal_rot"],
        "growth_stages": {
            "germination": "5-7 days",
            "flowering": "35-45 days",
            "pod_formation": "50-60 days",
            "maturity": "90-120 days"
        },
        "fertilizer": {
            "basal": "N:P:K = 20:60:40 kg/ha",
            "rhizobium": "Seed treatment recommended"
        },
        "yield_potential": "2-3 tonnes/hectare"
    },
    "groundnut": {
        "hindi": "मूंगफली",
        "season": ["kharif", "rabi"],
        "water_need": "medium",
        "soil_type": ["sandy loam", "loamy"],
        "common_pests": ["white_grub", "aphid", "thrips", "leaf_miner"],
        "common_diseases": ["tikka_disease", "collar_rot", "stem_rot", "rust"],
        "growth_stages": {
            "germination": "7-10 days",
            "pegging": "40-50 days",
            "pod_formation": "60-75 days",
            "maturity": "100-130 days"
        },
        "fertilizer": {
            "basal": "N:P:K = 25:50:40 kg/ha",
            "gypsum": "500 kg/ha at pegging"
        },
        "yield_potential": "2-3 tonnes/hectare"
    },
    "chickpea": {
        "hindi": "चना",
        "season": ["rabi"],
        "water_need": "low",
        "soil_type": ["loamy", "clay loam"],
        "common_pests": ["pod_borer", "cutworm", "aphid"],
        "common_diseases": ["wilt", "ascochyta_blight", "collar_rot", "stunt"],
        "growth_stages": {
            "germination": "7-10 days",
            "flowering": "45-55 days",
            "pod_formation": "65-75 days",
            "maturity": "95-110 days"
        },
        "fertilizer": {
            "basal": "N:P:K = 20:40:20 kg/ha",
            "rhizobium": "Seed treatment recommended"
        },
        "yield_potential": "1.5-2.5 tonnes/hectare"
    }
}

# =============================================================================
# PEST DATABASE - Identification and Treatment
# =============================================================================

PEST_DATABASE = {
    "stem_borer": {
        "hindi": "तना छेदक",
        "affects": ["paddy", "maize", "sugarcane"],
        "symptoms": ["dead_heart", "white_ear", "bore_holes_in_stem"],
        "identification": "Larvae bore into stems, cause dead hearts in vegetative stage and white ears at flowering",
        "organic_treatment": [
            "Release Trichogramma wasps (50,000/ha) at weekly intervals",
            "Install pheromone traps (5/ha)",
            "Apply neem oil 5ml/liter spray",
            "Collect and destroy egg masses"
        ],
        "chemical_treatment": [
            "Carbofuran 3G granules 25 kg/ha in leaf whorls",
            "Chlorantraniliprole 18.5 SC @ 0.3ml/liter spray",
            "Fipronil 5 SC @ 2ml/liter spray"
        ],
        "prevention": [
            "Use resistant varieties",
            "Maintain proper water management",
            "Remove and destroy stubbles after harvest",
            "Avoid late planting"
        ]
    },
    "bollworm": {
        "hindi": "बॉलवर्म / सुंडी",
        "affects": ["cotton", "chickpea", "tomato"],
        "symptoms": ["bore_holes_in_bolls", "damaged_squares", "excreta_on_bolls"],
        "identification": "Green/brown caterpillar with lateral stripes, bores into cotton bolls and chickpea pods",
        "organic_treatment": [
            "HaNPV (Helicoverpa Nuclear Polyhedrosis Virus) 250 LE/ha",
            "Bacillus thuringiensis (Bt) 1kg/ha spray",
            "Neem seed kernel extract 5% spray",
            "Bird perches 20/ha"
        ],
        "chemical_treatment": [
            "Emamectin benzoate 5 SG @ 0.4g/liter",
            "Spinosad 45 SC @ 0.3ml/liter",
            "Profenophos 50 EC @ 2ml/liter"
        ],
        "prevention": [
            "Early sowing",
            "Trap crops like marigold",
            "Pheromone traps 5/ha",
            "Regular monitoring"
        ]
    },
    "whitefly": {
        "hindi": "सफेद मक्खी",
        "affects": ["cotton", "vegetables", "pulses"],
        "symptoms": ["yellowing_leaves", "sticky_honeydew", "sooty_mold", "leaf_curl"],
        "identification": "Tiny white flying insects on leaf undersides, cause yellowing and transmit viral diseases",
        "organic_treatment": [
            "Yellow sticky traps 25/ha",
            "Neem oil 2ml/liter + soap solution spray",
            "Verticillium lecanii 2ml/liter spray",
            "Spray in evening hours"
        ],
        "chemical_treatment": [
            "Diafenthiuron 50 WP @ 1g/liter",
            "Spiromesifen 240 SC @ 0.8ml/liter",
            "Pyriproxyfen 10 EC @ 1ml/liter"
        ],
        "prevention": [
            "Remove weed hosts",
            "Avoid excess nitrogen",
            "Maintain field hygiene",
            "Use resistant varieties"
        ]
    },
    "aphid": {
        "hindi": "माहू / चेपा",
        "affects": ["wheat", "mustard", "vegetables", "cotton"],
        "symptoms": ["curled_leaves", "stunted_growth", "honeydew", "black_sooty_mold"],
        "identification": "Small soft-bodied insects in clusters on young shoots and leaf undersides",
        "organic_treatment": [
            "Lady beetle release (natural enemy)",
            "Neem oil 5ml/liter spray",
            "Soap water spray (5g/liter)",
            "Remove heavily infested parts"
        ],
        "chemical_treatment": [
            "Imidacloprid 17.8 SL @ 0.3ml/liter",
            "Thiamethoxam 25 WG @ 0.3g/liter",
            "Dimethoate 30 EC @ 2ml/liter"
        ],
        "prevention": [
            "Timely sowing",
            "Avoid excess nitrogen",
            "Reflective mulches",
            "Crop rotation"
        ]
    },
    "fall_armyworm": {
        "hindi": "फॉल आर्मीवर्म / सैनिक कीट",
        "affects": ["maize", "sorghum", "millets"],
        "symptoms": ["windowing_of_leaves", "tattered_leaves", "bore_holes", "larval_frass"],
        "identification": "Brown/green caterpillar with inverted Y on head, feeds in whorls, leaves ragged appearance",
        "organic_treatment": [
            "Sand + lime (9:1) application in whorls",
            "Metarhizium anisopliae spray",
            "Bacillus thuringiensis spray",
            "Release Telenomus parasitoid"
        ],
        "chemical_treatment": [
            "Spinetoram 11.7 SC @ 0.5ml/liter",
            "Chlorantraniliprole 18.5 SC @ 0.4ml/liter",
            "Emamectin benzoate 5 SG @ 0.4g/liter"
        ],
        "prevention": [
            "Early detection crucial",
            "Pheromone traps for monitoring",
            "Intercropping with pulses",
            "Avoid monocropping"
        ]
    },
    "brown_planthopper": {
        "hindi": "भूरा फुदका",
        "affects": ["paddy"],
        "symptoms": ["hopperburn", "circular_dead_patches", "honeydew", "sooty_mold"],
        "identification": "Small brown insects at base of rice tillers, cause hopper burn in circular patches",
        "organic_treatment": [
            "Drain water from field for 3-4 days",
            "Beauveria bassiana spray",
            "Avoid broad-spectrum insecticides",
            "Encourage natural enemies (spiders, dragonflies)"
        ],
        "chemical_treatment": [
            "Pymetrozine 50 WG @ 0.6g/liter",
            "Buprofezin 25 SC @ 1.6ml/liter",
            "Dinotefuran 20 SG @ 0.4g/liter"
        ],
        "prevention": [
            "Resistant varieties (very effective)",
            "Avoid excess nitrogen",
            "Do not spray in early stages",
            "Maintain 20-25 hills gap for ventilation"
        ]
    }
}

# =============================================================================
# DISEASE DATABASE - Identification and Treatment
# =============================================================================

DISEASE_DATABASE = {
    "blast": {
        "hindi": "झुलसा रोग / ब्लास्ट",
        "affects": ["paddy"],
        "symptoms": ["diamond_shaped_lesions", "node_blast", "neck_blast", "panicle_blast"],
        "identification": "Diamond/spindle-shaped spots with grey center and brown margin on leaves",
        "treatment": [
            "Tricyclazole 75 WP @ 0.6g/liter spray",
            "Isoprothiolane 40 EC @ 1.5ml/liter",
            "Carbendazim 50 WP @ 1g/liter"
        ],
        "organic": [
            "Pseudomonas fluorescens seed treatment",
            "Trichoderma viride application",
            "Avoid excess nitrogen"
        ],
        "prevention": [
            "Resistant varieties (most effective)",
            "Balanced fertilization",
            "Proper water management",
            "Avoid late planting"
        ]
    },
    "rust": {
        "hindi": "रतुआ / गेरुआ",
        "affects": ["wheat", "pulses"],
        "types": ["brown_rust", "yellow_rust", "black_rust"],
        "symptoms": ["orange_pustules_on_leaves", "yellow_stripes", "black_pustules_on_stems"],
        "identification": "Small orange-brown pustules on leaves that release rusty spores when touched",
        "treatment": [
            "Propiconazole 25 EC @ 1ml/liter",
            "Tebuconazole 25.9 EC @ 1ml/liter",
            "Mancozeb 75 WP @ 2.5g/liter (preventive)"
        ],
        "prevention": [
            "Grow resistant varieties",
            "Early sowing",
            "Remove volunteer wheat plants",
            "Balanced fertilization"
        ]
    },
    "bacterial_leaf_blight": {
        "hindi": "जीवाणु पत्ती झुलसा",
        "affects": ["paddy"],
        "symptoms": ["water_soaked_lesions", "yellow_to_white_lesions", "milky_ooze"],
        "identification": "Yellow to white lesions starting from leaf tips, bacterial ooze in morning",
        "treatment": [
            "Streptocycline 0.025% + Copper oxychloride 0.3% spray",
            "Drain water and stop nitrogen application",
            "Remove infected leaves"
        ],
        "prevention": [
            "Resistant varieties",
            "Avoid excess nitrogen",
            "Balanced potassium application",
            "Avoid walking in wet fields"
        ]
    },
    "wilt": {
        "hindi": "उकठा / विल्ट",
        "affects": ["chickpea", "pigeonpea", "cotton"],
        "symptoms": ["yellowing", "wilting", "brown_vascular_tissue", "sudden_death"],
        "identification": "Plants wilt and dry despite moisture, brown discoloration in vascular tissue when stem cut",
        "treatment": [
            "Carbendazim 50 WP seed treatment @ 2g/kg",
            "Trichoderma viride seed treatment",
            "Soil drenching with fungicide"
        ],
        "prevention": [
            "Resistant varieties (most important)",
            "Crop rotation (3-4 years)",
            "Deep summer ploughing",
            "Avoid waterlogging"
        ]
    },
    "yellow_mosaic": {
        "hindi": "पीला मोज़ेक",
        "affects": ["soybean", "mungbean", "urdbean"],
        "symptoms": ["yellow_patches_on_leaves", "mosaic_pattern", "stunted_growth", "reduced_pods"],
        "identification": "Irregular yellow and green patches on leaves giving mosaic appearance, transmitted by whitefly",
        "treatment": [
            "Control whitefly vector",
            "Imidacloprid seed treatment",
            "Remove and destroy infected plants"
        ],
        "prevention": [
            "Resistant/tolerant varieties (best control)",
            "Early sowing to escape whitefly peak",
            "Border crop of maize/sorghum",
            "Yellow sticky traps"
        ]
    },
    "powdery_mildew": {
        "hindi": "चूर्णी फफूंद / पाउडरी मिल्ड्यू",
        "affects": ["wheat", "vegetables", "grapes"],
        "symptoms": ["white_powdery_growth", "yellowing", "leaf_distortion"],
        "identification": "White powdery coating on leaves, stems, and pods",
        "treatment": [
            "Sulphur 80 WP @ 2.5g/liter",
            "Karathane 48 EC @ 1ml/liter",
            "Hexaconazole 5 EC @ 1ml/liter"
        ],
        "organic": [
            "Milk spray (1:9 ratio with water)",
            "Baking soda 1 tsp/liter spray",
            "Neem oil spray"
        ],
        "prevention": [
            "Resistant varieties",
            "Proper spacing for air circulation",
            "Avoid overhead irrigation"
        ]
    }
}

# =============================================================================
# GOVERNMENT SCHEMES DATABASE
# =============================================================================

GOVERNMENT_SCHEMES = {
    "pm_kisan": {
        "name": "PM-KISAN Samman Nidhi",
        "hindi": "पीएम किसान सम्मान निधि",
        "benefit": "₹6000 per year in 3 installments of ₹2000 each",
        "eligibility": "All landholding farmer families",
        "how_to_apply": "Register at pmkisan.gov.in or through CSC center",
        "documents": ["Aadhaar", "Bank Account", "Land Records (Khatauni)"]
    },
    "pm_fasal_bima": {
        "name": "PM Fasal Bima Yojana",
        "hindi": "पीएम फसल बीमा योजना",
        "benefit": "Crop insurance with minimal premium (1.5-2% for Rabi/Kharif)",
        "eligibility": "All farmers including sharecroppers and tenant farmers",
        "how_to_apply": "Apply through bank, CSC, or insurance company before sowing deadline",
        "documents": ["Aadhaar", "Bank Account", "Land Records", "Sowing Certificate"]
    },
    "kcc": {
        "name": "Kisan Credit Card",
        "hindi": "किसान क्रेडिट कार्ड",
        "benefit": "Short-term credit up to ₹3 lakh at 4% interest (with subsidy)",
        "eligibility": "All farmers, including tenant farmers",
        "how_to_apply": "Apply at any bank branch with land documents",
        "documents": ["Aadhaar", "Land Records", "Identity Proof", "Passport Photo"]
    },
    "soil_health_card": {
        "name": "Soil Health Card Scheme",
        "hindi": "मृदा स्वास्थ्य कार्ड",
        "benefit": "Free soil testing and fertilizer recommendations",
        "eligibility": "All farmers",
        "how_to_apply": "Apply through agriculture department or Krishi Vigyan Kendra",
        "documents": ["Land Details", "Contact Information"]
    },
    "e_nam": {
        "name": "e-NAM (National Agriculture Market)",
        "hindi": "ई-नाम",
        "benefit": "Better prices through transparent online trading",
        "eligibility": "All farmers with produce to sell",
        "how_to_apply": "Register at enam.gov.in or through registered mandi",
        "documents": ["Aadhaar", "Bank Account", "Mobile Number"]
    }
}

# =============================================================================
# WEATHER-BASED ADVISORY
# =============================================================================

WEATHER_ADVISORY = {
    "rain_expected": {
        "general": [
            "Postpone irrigation if rain expected within 24 hours",
            "Complete any pending pesticide sprays today",
            "Ensure field drainage is clear",
            "Harvest mature crops if possible"
        ],
        "paddy": ["Stop fertilizer application", "Ensure bund repair"],
        "cotton": ["Check for waterlogging prevention", "Scout for bollworm after rain"]
    },
    "hot_weather": {
        "general": [
            "Irrigate during evening or early morning",
            "Apply mulch to conserve moisture",
            "Postpone transplanting to evening hours",
            "Provide shade to nurseries"
        ],
        "vegetables": ["Increase irrigation frequency", "Use shade nets"],
        "wheat": ["Urgent irrigation if heading stage"]
    },
    "cold_wave": {
        "general": [
            "Light irrigation in evening for frost protection",
            "Cover sensitive crops with straw/plastic",
            "Avoid irrigation during cold night",
            "Smoke/burning around field for frost protection"
        ],
        "vegetables": ["Cover plants with plastic/jute"],
        "wheat": ["Monitor for frost damage in reproductive stage"]
    }
}

# =============================================================================
# IMAGE ANALYSIS PATTERNS (for simulated image analysis)
# =============================================================================

IMAGE_ANALYSIS_PATTERNS = {
    "yellow_leaves": {
        "possible_causes": ["nitrogen_deficiency", "iron_deficiency", "virus_attack", "overwatering"],
        "response_template": "I notice yellowing in the leaves. This could be due to:\n1. **Nitrogen deficiency** - Apply urea at 20kg/acre\n2. **Iron deficiency** - Spray ferrous sulphate 0.5%\n3. **Viral infection** - Check for vector insects\n4. **Overwatering** - Ensure proper drainage"
    },
    "brown_spots": {
        "possible_causes": ["fungal_infection", "bacterial_blight", "nutrient_deficiency"],
        "response_template": "The brown spots suggest a possible fungal or bacterial infection:\n1. **Fungal disease** - Spray Mancozeb 2.5g/liter\n2. **Bacterial blight** - Apply Streptocycline 1g/10 liters\n3. Remove and destroy heavily infected leaves"
    },
    "wilting": {
        "possible_causes": ["wilt_disease", "root_rot", "water_stress", "stem_borer"],
        "response_template": "Wilting can have several causes:\n1. **Check soil moisture** - If dry, irrigate immediately\n2. **Cut stem to check** - If brown inside, it's vascular wilt\n3. **Check roots** - If black/rotted, it's root disease\n4. **Apply Carbendazim** drench as treatment"
    },
    "holes_in_leaves": {
        "possible_causes": ["caterpillar", "beetle", "grasshopper"],
        "response_template": "The holes indicate insect feeding damage:\n1. **Caterpillars** - Spray Spinosad or Bt\n2. **Beetles** - Apply Chlorantraniliprole\n3. **Natural control** - Release Trichogramma cards\n4. Install light traps to monitor pests"
    },
    "white_powder": {
        "possible_causes": ["powdery_mildew"],
        "response_template": "This appears to be **Powdery Mildew** fungal infection:\n1. **Spray Sulphur** 80 WP at 2.5g/liter\n2. **Alternative** - Hexaconazole 1ml/liter\n3. **Organic option** - Milk spray (1:9 with water)\n4. Improve air circulation between plants"
    },
    "healthy_crop": {
        "possible_causes": ["normal"],
        "response_template": "Your crop looks healthy! 🌱 Here are tips to maintain it:\n1. Continue balanced fertilization\n2. Scout regularly for early pest detection\n3. Maintain proper irrigation scheduling\n4. Check weather forecasts for any alerts"
    }
}
