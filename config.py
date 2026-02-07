# KrishiNirnay AI - Configuration
# Enterprise-grade agricultural intelligence platform

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Supported languages (15 major Indian languages + English)
# ISO 639-1 codes, native name, script
SUPPORTED_LANGUAGES = [
    ('hi', 'हिंदी', 'Hindi', 'Devanagari'),
    ('bn', 'বাংলা', 'Bengali', 'Bengali'),
    ('te', 'తెలుగు', 'Telugu', 'Telugu'),
    ('mr', 'मराठी', 'Marathi', 'Devanagari'),
    ('ta', 'தமிழ்', 'Tamil', 'Tamil'),
    ('gu', 'ગુજરાતી', 'Gujarati', 'Gujarati'),
    ('kn', 'ಕನ್ನಡ', 'Kannada', 'Kannada'),
    ('or', 'ଓଡ଼ିଆ', 'Odia', 'Odia'),
    ('ml', 'മലയാളം', 'Malayalam', 'Malayalam'),
    ('pa', 'ਪੰਜਾਬੀ', 'Punjabi', 'Gurmukhi'),
    ('as', 'অসমীয়া', 'Assamese', 'Bengali'),
    ('mai', 'मैथिली', 'Maithili', 'Devanagari'),
    ('sat', 'ᱥᱟᱱᱛᱟᱲᱤ', 'Santali', 'Ol Chiki'),
    ('ks', 'कॉशुर', 'Kashmiri', 'Devanagari'),
    ('en', 'English', 'English', 'Latin'),
]

# Language code list for validation
LANGUAGE_CODES = [code for code, *_ in SUPPORTED_LANGUAGES]

# Default/fallback language
DEFAULT_LANGUAGE = 'hi'

# Locale mapping for Intl (JavaScript-style for reference; Python uses babel or similar)
LANGUAGE_LOCALE_MAP = {
    'hi': 'hi-IN',
    'bn': 'bn-IN',
    'te': 'te-IN',
    'mr': 'mr-IN',
    'ta': 'ta-IN',
    'gu': 'gu-IN',
    'kn': 'kn-IN',
    'or': 'or-IN',
    'ml': 'ml-IN',
    'pa': 'pa-IN',
    'as': 'as-IN',
    'mai': 'hi-IN',  # Maithili fallback
    'sat': 'hi-IN',  # Santali fallback
    'ks': 'ks-IN',
    'en': 'en-IN',
}

# Translation module names (must match locale JSON filenames)
TRANSLATION_MODULES = ['common', 'dashboard', 'chatbot', 'advisory', 'schemes', 'errors', 'validation']

# Path to locale JSON files
LOCALES_DIR = BASE_DIR / 'locales'

# Flask
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
PERMANENT_SESSION_LIFETIME = 86400 * 30  # 30 days (sessions persist after app closed)

# SQL database (SQLite by default; use DATABASE_URL for PostgreSQL in production)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///krishsaathi.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Indian states (code, name) for profile - major agricultural states
INDIAN_STATES = [
    ('AP', 'Andhra Pradesh'), ('TG', 'Telangana'), ('KA', 'Karnataka'), ('TN', 'Tamil Nadu'),
    ('KL', 'Kerala'), ('MH', 'Maharashtra'), ('GJ', 'Gujarat'), ('RJ', 'Rajasthan'),
    ('MP', 'Madhya Pradesh'), ('UP', 'Uttar Pradesh'), ('WB', 'West Bengal'), ('BH', 'Bihar'),
    ('PB', 'Punjab'), ('HR', 'Haryana'), ('OR', 'Odisha'), ('AS', 'Assam'), ('MN', 'Manipur'),
]

# Major Indian crops for profile
CROP_TYPES = [
    'paddy', 'wheat', 'cotton', 'sugarcane', 'maize', 'millets', 'pulses', 'oilseeds',
    'soybean', 'groundnut', 'chickpea', 'sorghum', 'bajra', 'jowar',
]
CROP_STAGES = ['sowing', 'vegetative', 'flowering', 'harvesting', 'post_harvest']
SEASONS = ['kharif', 'rabi', 'zaid', 'year_round']
