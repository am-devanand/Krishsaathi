# Language detection - session (logged-in farmer) > URL > header > default

from flask import request

from config import LANGUAGE_CODES, DEFAULT_LANGUAGE


def get_request_language(session_farmer=None):
    """Priority: logged-in farmer language > URL ?lang= > Accept-Language > default."""
    # 1. Session farmer language (persisted; all content in selected language)
    if session_farmer and getattr(session_farmer, 'language_code', None):
        lang = (session_farmer.language_code or '').strip()[:5]
        if lang in LANGUAGE_CODES:
            return lang

    # 2. URL parameter (deep linking)
    url_lang = request.args.get('lang', '').strip()[:5]
    if url_lang in LANGUAGE_CODES:
        return url_lang

    # 3. Accept-Language header
    accept = request.headers.get('Accept-Language', '')
    for part in accept.split(','):
        part = part.strip().split(';')[0].strip()
        code = part.split('-')[0].lower() if part else ''
        if code in LANGUAGE_CODES:
            return code

    return DEFAULT_LANGUAGE
