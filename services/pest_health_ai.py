# Pest Health AI - Conversational assistant for crop/pest/health (OpenAI when configured)

import os
import base64
from typing import Optional

# In-memory conversation history: conversation_id -> list of {role, content} (OpenAI format)
_conversations: dict[str, list[dict]] = {}
MAX_HISTORY = 20

# Language code -> name for system prompt
LANG_NAMES = {
    "hi": "Hindi", "bn": "Bengali", "te": "Telugu", "mr": "Marathi", "ta": "Tamil",
    "gu": "Gujarati", "kn": "Kannada", "or": "Odia", "ml": "Malayalam", "pa": "Punjabi",
    "as": "Assamese", "mai": "Maithili", "sat": "Santali", "ks": "Kashmiri", "en": "English",
}


def _system_prompt(lang: str, farmer_name: Optional[str] = None) -> str:
    lang_name = LANG_NAMES.get(lang, "English")
    name_line = f"- The farmer's name is {farmer_name}. Address them by name when greeting or closing." if (farmer_name and farmer_name.strip()) else ""
    return f"""You are Pest Health, a friendly and expert agricultural assistant for farmers in India.

Your role:
- Analyze crop images and text for growth stage, plant health, pest damage, diseases, and nutrient issues.
- Use step-by-step reasoning: observe first, then identify possible causes, then recommend actions.
- Remember context from earlier in the conversation and refer back when relevant (e.g. crop name, stage).
- Give clear, actionable recommendations. Always prefer in this order: (1) mechanical/physical methods, (2) biological/organic (e.g. neem, biopesticides), (3) chemical only when necessary; mention cost and local availability when you can.
- For pest/disease identification: state your confidence (High / Medium / Low) and what you see (e.g. "Likely X; confidence: Medium because...").
- Use simple language and be supportive. Respond only in {lang_name} unless the user explicitly asks for another language.
- For images: describe what you see (crop type if identifiable, leaf/plant condition, possible pests or diseases) and suggest next steps.
- For text-only: answer questions about crops, pests, weather impact, soil, and farming practices. Keep answers focused and practical for smallholder farmers.
{name_line}""".strip()


def _build_user_content(text: str, image_base64: Optional[str] = None) -> list[dict]:
    content = []
    if text and text.strip():
        content.append({"type": "text", "text": text.strip()})
    if image_base64:
        # Support data URL or raw base64
        if image_base64.startswith("data:"):
            url = image_base64
        else:
            url = f"data:image/jpeg;base64,{image_base64}"
        content.append({
            "type": "image_url",
            "image_url": {"url": url},
        })
    if not content:
        content = [{"type": "text", "text": "What do you see in this image? (Analyze the crop/plant.)"}]
    return content


def _openai_reply(
    message: str,
    lang: str,
    image_base64: Optional[str] = None,
    conversation_id: Optional[str] = None,
    farmer_name: Optional[str] = None,
) -> tuple[str, Optional[str]]:
    """Call OpenAI Chat Completions (vision-capable). Returns (reply_text, error_message)."""
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        return "", "OPENAI_API_KEY is not set. Set it in the environment to use the AI assistant."

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        return "", f"OpenAI client error: {e!s}"

    messages = []
    if conversation_id and conversation_id in _conversations:
        for m in _conversations[conversation_id][-MAX_HISTORY:]:
            messages.append({"role": m["role"], "content": m["content"]})

    if not messages:
        messages.append({"role": "system", "content": _system_prompt(lang, farmer_name)})

    user_content = _build_user_content(message, image_base64)
    messages.append({"role": "user", "content": user_content})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1024,
        )
        choice = response.choices[0] if response.choices else None
        if not choice or not choice.message:
            return "", "No response from the model."
        reply = (choice.message.content or "").strip()
        if not reply:
            return "", "Empty response from the model."

        # Persist history
        if conversation_id:
            if conversation_id not in _conversations:
                _conversations[conversation_id] = []
            _conversations[conversation_id].append({"role": "user", "content": user_content})
            _conversations[conversation_id].append({"role": "assistant", "content": reply})
            _conversations[conversation_id] = _conversations[conversation_id][-MAX_HISTORY:]

        return reply, None
    except Exception as e:
        return "", str(e)


def get_pest_health_reply(
    message: str,
    lang: str,
    image_base64: Optional[str] = None,
    conversation_id: Optional[str] = None,
    farmer_name: Optional[str] = None,
) -> str:
    """
    Get a reply from Pest Health AI (text + optional image).
    Uses OpenAI when OPENAI_API_KEY is set; otherwise falls back to rule-based for text-only.
    """
    # If user sent an image, we need vision → require OpenAI
    if image_base64:
        reply, err = _openai_reply(message, lang, image_base64, conversation_id, farmer_name)
        if err:
            return err
        return reply

    # Text-only: try OpenAI first for conversational behavior
    reply, err = _openai_reply(message, lang, None, conversation_id, farmer_name)
    if not err:
        return reply
    # Fallback to rule-based when no API key
    from services.chatbot_engine import get_chatbot_reply
    return get_chatbot_reply(message, lang)
