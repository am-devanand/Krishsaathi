# KRISHSAATHI - Main application
# Enterprise-grade agricultural intelligence platform

import os
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session

from config import (
    SUPPORTED_LANGUAGES,
    LANGUAGE_CODES,
    DEFAULT_LANGUAGE,
    LOCALES_DIR,
    INDIAN_STATES,
    CROP_TYPES,
    CROP_STAGES,
    SEASONS,
)
from translations import get_translation, get_chatbot_template, translate_crop
from language_middleware import get_request_language
from services.weather import fetch_weather
from services.mandi import fetch_mandi
from services.schemes import get_schemes
from services.soil import get_soil_advisory
from services.satellite import get_satellite_info
from services.advisory import get_advisory
from services.pest_health_ai import get_pest_health_reply
from models import db, Farmer, FarmerCrop, ChatSession, ChatMessage

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates',
)
app.config.from_object('config')

# Serverless (Vercel etc.): default instance path is read-only. Use /tmp so db.init_app can create dirs/files.
def _writable(path):
    try:
        os.makedirs(path, exist_ok=True)
        f = os.path.join(path, '.write_check')
        open(f, 'w').close()
        os.remove(f)
        return True
    except (OSError, PermissionError):
        return False

if not _writable(app.instance_path):
    app.instance_path = '/tmp/krishsaathi_instance'
    os.makedirs(app.instance_path, exist_ok=True)

# If using SQLite, put DB in writable instance path so serverless can open it
if app.config.get('SQLALCHEMY_DATABASE_URI', '').startswith('sqlite'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'krishsaathi.db')

db.init_app(app)

SESSION_FARMER_ID = 'farmer_id'


def get_current_farmer():
    """Return Farmer for session or None."""
    fid = session.get(SESSION_FARMER_ID)
    if not fid:
        return None
    return Farmer.query.get(fid)


def get_farmer_display_name(farmer):
    """Name to show in greetings; never placeholder."""
    if farmer and farmer.name and farmer.name.strip():
        return farmer.name.strip()
    return None


@app.context_processor
def inject_i18n():
    farmer = get_current_farmer()
    lang = get_request_language(farmer)
    farmer_name = get_farmer_display_name(farmer) if farmer else None
    # Use farmer name in templates; fallback to translated "Farmer" only when not logged in
    welcome_name = farmer_name if farmer_name else get_translation(lang, 'common', 'farmer')
    return {
        'supported_languages': SUPPORTED_LANGUAGES,
        'current_language': lang,
        'current_farmer': farmer,
        'farmer_name': farmer_name,
        'welcome_name': welcome_name,
        't': lambda key, module='common', **kwargs: get_translation(lang, module, key, **kwargs),
    }


# ---------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        mobile = (request.form.get('mobile') or '').strip()
        mobile = ''.join(c for c in mobile if c.isdigit())[-10:]
        if not name or len(mobile) != 10:
            return render_template('login.html', error='Please enter name and a valid 10-digit mobile number.')
        farmer = Farmer.query.filter_by(mobile=mobile).first()
        if not farmer:
            farmer = Farmer(name=name, mobile=mobile, language_code=DEFAULT_LANGUAGE)
            db.session.add(farmer)
            db.session.commit()
        else:
            farmer.name = name
            farmer.updated_at = farmer.updated_at
            db.session.commit()
        session[SESSION_FARMER_ID] = farmer.id
        session.permanent = True
        # If profile incomplete, go to profile; else dashboard
        if not farmer.district and not farmer.state:
            return redirect(url_for('profile'))
        return redirect(url_for('dashboard'))
    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    session.pop(SESSION_FARMER_ID, None)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    farmer = get_current_farmer()
    if not farmer:
        return redirect(url_for('login'))
    if request.method == 'POST':
        farmer.language_code = (request.form.get('language_code') or farmer.language_code or DEFAULT_LANGUAGE).strip()[:5]
        if farmer.language_code not in LANGUAGE_CODES:
            farmer.language_code = DEFAULT_LANGUAGE
        farmer.state = (request.form.get('state') or '').strip()[:10]
        farmer.district = (request.form.get('district') or '').strip()[:80]
        farmer.village = (request.form.get('village') or '').strip()[:80]
        # Crops: replace with submitted list
        FarmerCrop.query.filter_by(farmer_id=farmer.id).delete()
        crop_type = request.form.getlist('crop_type')
        stage = request.form.getlist('stage')
        season = request.form.getlist('season')
        for i, ct in enumerate(crop_type):
            if ct and ct.strip():
                st = (stage[i] if i < len(stage) else '').strip()
                se = (season[i] if i < len(season) else '').strip()
                db.session.add(FarmerCrop(farmer_id=farmer.id, crop_type=ct.strip(), stage=st, season=se))
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template(
        'profile.html',
        farmer=farmer,
        states=INDIAN_STATES,
        crop_types=CROP_TYPES,
        crop_stages=CROP_STAGES,
        seasons=SEASONS,
    )


@app.route('/dashboard')
def dashboard():
    farmer = get_current_farmer()
    if not farmer:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/chatbot')
def chatbot_page():
    farmer = get_current_farmer()
    if not farmer:
        return redirect(url_for('login'))
    return render_template('chatbot.html')


# API: Current farmer (for frontend: name, language, etc.)
@app.route('/api/me')
def api_me():
    farmer = get_current_farmer()
    if not farmer:
        return jsonify({'logged_in': False})
    crops = [{'crop_type': c.crop_type, 'stage': c.stage, 'season': c.season} for c in farmer.crops]
    return jsonify({
        'logged_in': True,
        'name': farmer.name,
        'language': farmer.language_code,
        'district': farmer.district,
        'village': farmer.village,
        'state': farmer.state,
        'crops': crops,
    })


# API: Update language (persist to farmer in DB)
@app.route('/api/user/update-language', methods=['POST'])
def update_language():
    data = request.get_json() or {}
    lang = (data.get('language') or '').strip()[:5]
    if lang not in LANGUAGE_CODES:
        return jsonify({'error': 'Invalid language code'}), 400
    farmer = get_current_farmer()
    if farmer:
        farmer.language_code = lang
        db.session.commit()
    return jsonify({'success': True, 'language': lang})


# API: Pest Health chatbot (uses farmer language and name when logged in)
@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    data = request.get_json() or {}
    farmer = get_current_farmer()
    user_lang = (farmer.language_code if farmer else None) or request.headers.get('Accept-Language', 'hi')[:2]
    if user_lang not in LANGUAGE_CODES:
        user_lang = DEFAULT_LANGUAGE
    message = (data.get('message') or '').strip()
    image_base64 = data.get('image_base64') or None
    conversation_id = data.get('conversation_id')
    farmer_id = farmer.id if farmer else None
    
    # History: Get or Create Session
    session_id = None
    if conversation_id:
        chat_session = ChatSession.query.get(conversation_id)
        if chat_session and (chat_session.farmer_id == farmer_id or (not farmer_id and chat_session.guest_id)):
            session_id = chat_session.id
    
    if not session_id:
        chat_session = ChatSession(farmer_id=farmer_id)
        db.session.add(chat_session)
        db.session.commit()
        session_id = chat_session.id

    # Save User Message
    if message:
        user_msg = ChatMessage(session_id=session_id, is_user=True, text=message, language_code=user_lang)
        db.session.add(user_msg)
        db.session.commit()

    farmer_name = get_farmer_display_name(farmer)
    reply = get_pest_health_reply(
        message, 
        user_lang, 
        image_base64, 
        conversation_id=session_id, 
        farmer_name=farmer_name,
        farmer_id=farmer_id
    )
    
    # Save Bot Message
    if reply:
        bot_msg = ChatMessage(session_id=session_id, is_user=False, text=reply, language_code=user_lang)
        db.session.add(bot_msg)
        db.session.commit()
        
    return jsonify({'reply': reply, 'language': user_lang, 'conversation_id': session_id})


@app.route('/api/chatbot/analyze-image', methods=['POST'])
def chatbot_analyze_image():
    data = request.get_json() or {}
    farmer = get_current_farmer()
    user_lang = (farmer.language_code if farmer else None) or request.headers.get('Accept-Language', 'hi')[:2]
    if user_lang not in LANGUAGE_CODES:
        user_lang = DEFAULT_LANGUAGE
    image_base64 = data.get('image_base64') or data.get('image')
    reply = get_pest_health_reply('', user_lang, image_base64, data.get('conversation_id'), farmer_name=get_farmer_display_name(farmer))
    return jsonify({'reply': reply, 'language': user_lang})
@app.route('/api/voice/history')
def api_voice_history():
    farmer = get_current_farmer()
    # For now, only return history for logged-in users? 
    # Or based on conversation_id passed in query param?
    # Let's support both.
    limit = 50
    history = []
    
    cid = request.args.get('conversation_id')
    if cid:
        chat_session = ChatSession.query.get(cid)
        if chat_session:
            # Check ownership
            if farmer and chat_session.farmer_id == farmer.id:
                 history = chat_session.messages[-limit:]
            elif not farmer and not chat_session.farmer_id:
                 # Guest session access by ID
                 history = chat_session.messages[-limit:]
    elif farmer:
        # Get most recent session
        chat_session = ChatSession.query.filter_by(farmer_id=farmer.id).order_by(ChatSession.started_at.desc()).first()
        if chat_session:
             history = chat_session.messages[-limit:]
             
    out = []
    for msg in history:
        out.append({
            'text': msg.text,
            'is_user': msg.is_user,
            'timestamp': msg.timestamp.isoformat()
        })
    
    return jsonify({'history': out})

# ---------- Real-time data APIs (use farmer district/state when logged in) ----------

@app.route('/api/weather')
def api_weather():
    lang = get_request_language(get_current_farmer())
    if lang not in LANGUAGE_CODES:
        lang = DEFAULT_LANGUAGE
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    data = fetch_weather(lat=lat, lon=lon)
    if data.get('current'):
        cond = data['current'].get('condition', '')
        data['current']['condition_label'] = get_translation(lang, 'common', f'weather.conditions.{cond}')
    return jsonify(data)


@app.route('/api/mandi')
def api_mandi():
    lang = get_request_language(get_current_farmer())
    if lang not in LANGUAGE_CODES:
        lang = DEFAULT_LANGUAGE
    limit = request.args.get('limit', default=15, type=int)
    limit = min(max(limit, 1), 50)
    out = fetch_mandi(limit=limit)
    prices = out.get('prices', [])
    for p in prices:
        p['commodity_local'] = translate_crop(p.get('commodity', ''), lang)
    out['prices'] = prices
    return jsonify(out)


@app.route('/api/schemes')
def api_schemes():
    lang = get_request_language(get_current_farmer())
    if lang not in LANGUAGE_CODES:
        lang = DEFAULT_LANGUAGE
    schemes = get_schemes(lang=lang if lang != 'en' else 'en')
    return jsonify({'schemes': schemes})


@app.route('/api/soil')
def api_soil():
    lang = get_request_language(get_current_farmer())
    if lang not in LANGUAGE_CODES:
        lang = DEFAULT_LANGUAGE
    farmer = get_current_farmer()
    state = request.args.get('state') or (farmer.state if farmer else '')
    district = request.args.get('district') or (farmer.district if farmer else '')
    return jsonify(get_soil_advisory(state=state, district=district, lang=lang))


@app.route('/api/satellite')
def api_satellite():
    lang = get_request_language(get_current_farmer())
    if lang not in LANGUAGE_CODES:
        lang = DEFAULT_LANGUAGE
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    farmer = get_current_farmer()
    state = request.args.get('state') or (farmer.state if farmer else '')
    info = get_satellite_info(lat=lat, lon=lon, state=state)
    key = 'description_hi' if lang == 'hi' else 'description_en'
    info['description'] = info.get(key, info['description_en'])
    return jsonify(info)


@app.route('/api/advisory')
def api_advisory():
    lang = get_request_language(get_current_farmer())
    if lang not in LANGUAGE_CODES:
        lang = DEFAULT_LANGUAGE
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    farmer = get_current_farmer()
    state = request.args.get('state') or (farmer.state if farmer else '')
    return jsonify(get_advisory(lang=lang, lat=lat, lon=lon, state=state, farmer=farmer))


# Serve locale JSON files for frontend i18n
@app.route('/locales/<lang>/<module>.json')
def serve_locale(lang, module):
    if lang not in LANGUAGE_CODES or module not in ['common', 'dashboard', 'chatbot', 'advisory', 'schemes', 'errors', 'validation']:
        return jsonify({}), 404
    path = LOCALES_DIR / lang / f'{module}.json'
    if not path.is_file():
        return jsonify({}), 404
    return send_from_directory(path.parent, f'{module}.json', mimetype='application/json')


# ---------- Init DB and background jobs ----------

with app.app_context():
    db.create_all()

# Optional: start background scheduler for weather alerts (see services/alert_scheduler.py)
try:
    from services.alert_scheduler import start_alert_scheduler
    start_alert_scheduler(app)
except Exception:
    pass


if __name__ == '__main__':
    os.makedirs(app.static_folder, exist_ok=True)
    os.makedirs(app.template_folder, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', True))
