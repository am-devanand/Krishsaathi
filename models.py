from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(15), unique=True, index=True)
    language_code = db.Column(db.String(10), default='en')
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    village = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Using onupdate to automatically update the timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    crops = db.relationship('FarmerCrop', backref='farmer', lazy=True, cascade="all, delete-orphan")
    chat_sessions = db.relationship('ChatSession', backref='farmer', lazy=True)

class FarmerCrop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
    crop_type = db.Column(db.String(100))
    stage = db.Column(db.String(100))
    season = db.Column(db.String(100))

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=True)
    guest_id = db.Column(db.String(100), nullable=True) # For non-logged in users
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade="all, delete-orphan")

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    is_user = db.Column(db.Boolean, default=True) # True = User, False = Bot
    text = db.Column(db.Text)
    language_code = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
