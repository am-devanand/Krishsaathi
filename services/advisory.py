# Combined advisory from weather + soil (for "Today's Advisory" card)
# Improvement: at least 3 actionable items, crop-stage and weather aware; 5-year trend stub

from services.weather import fetch_weather
from services.soil import get_soil_advisory
from translations import get_translation


def get_advisory(lang, lat=None, lon=None, state=None, farmer=None):
    weather = fetch_weather(lat=lat, lon=lon)
    soil = get_soil_advisory(state=state, district=(farmer.district if farmer else None), lang=lang)
    items = []
    cur = weather.get("current") if weather else None
    cond = (cur.get("condition") or "sunny") if cur else "sunny"
    cond_label = get_translation(lang, "common", f"weather.conditions.{cond}")
    temp = cur.get("temperature") if cur else None

    # 1. Weather-aware advice (actionable)
    if cur:
        if cond == "rainy":
            items.append(get_translation(lang, "common", "weather_alert.rainy") if lang != "en" else "Rain expected. Reduce irrigation, check drainage.")
        elif cond == "stormy":
            items.append(get_translation(lang, "common", "weather_alert.stormy") if lang != "en" else "Storm likely. Keep crops and yourself safe.")
        elif temp is not None and temp >= 42:
            items.append(get_translation(lang, "common", "weather_alert.extreme_heat") if lang != "en" else "Extreme heat. Ensure water and shade.")
        elif temp is not None and temp <= 2:
            items.append(get_translation(lang, "common", "weather_alert.extreme_cold") if lang != "en" else "Cold conditions. Protect sensitive crops.")
        else:
            items.append((cond_label + (" " + f"{temp:.0f}°C." if temp is not None else ".")) + " Suitable for field work.")
    else:
        items.append(cond_label + ". Check local forecast before spraying or irrigation.")

    # 2. Soil / NPK (actionable)
    soil_summary = soil.get("summary", "")
    if soil_summary:
        items.append(soil_summary)
    npk_tip = soil.get("npk_tip", "")
    if npk_tip:
        items.append(npk_tip)

    # 3. Crop-stage-aware advice when farmer has crops (at least one more actionable)
    if farmer and getattr(farmer, "crops", None):
        for c in list(farmer.crops)[:2]:
            stage = (c.stage or "").strip() or "general"
            crop_name = c.crop_type or "crop"
            if stage == "sowing":
                items.append(f"{crop_name}: Ensure seed treatment and timely sowing; check soil moisture.")
            elif stage == "vegetative":
                items.append(f"{crop_name}: Monitor for pests; avoid excess nitrogen; weeding and irrigation as needed.")
            elif stage == "flowering":
                items.append(f"{crop_name}: Avoid water stress; watch for pests during flowering.")
            elif stage == "harvesting":
                items.append(f"{crop_name}: Plan harvest; avoid rain if possible; store grain dry.")
            else:
                items.append(f"{crop_name}: Regular monitoring for disease and pest; follow recommended spray schedule.")
            break
    if len(items) < 3:
        items.append("Get Soil Health Card and follow recommended doses. Save our number for weather alerts.")

    # Backward compatibility: single text and soil_tip for existing UI
    text = " ".join(items[:2]) if items else (cond_label + ". " + (soil_summary or ""))
    return {
        "text": text,
        "soil_tip": npk_tip,
        "weather": cur,
        "items": items[:6],
        "weather_trend_note": "Past 5 years: Check IMD/state agri portal for regional rainfall trends and drought history.",
    }
