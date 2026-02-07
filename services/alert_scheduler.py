# Background weather alerts: monitor forecast and send SMS/notification to farmers
# Uses farmer's stored mobile and district. SMS gateway (e.g. MSG91, Twilio) can be wired in send_sms().

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def send_sms(mobile: str, message: str) -> bool:
    """
    Send SMS to farmer. Replace with real gateway (MSG91, Twilio, etc.) in production.
    Set SMS_GATEWAY_URL or MSG91_AUTH_KEY etc. and implement HTTP call here.
    """
    mobile = (mobile or "").strip()
    if not mobile or len(mobile) < 10:
        return False
    # Stub: log only. In production: POST to SMS API with mobile and message.
    logger.info("SMS stub: to=%s msg=%s", mobile[-10:], message[:80])
    if os.environ.get("ALERT_LOG_ONLY") != "1":
        pass  # Could write to queue (Redis, DB) for a worker to send
    return True


def check_weather_and_alert(app):
    """Run inside app context: fetch weather for farmers with district; send alert if severe."""
    from models import Farmer
    from services.weather import fetch_weather

    with app.app_context():
        farmers = Farmer.query.filter(Farmer.mobile != "", Farmer.district != "").all()
        for f in farmers:
            try:
                # Use district/state for lat/lon if you have a geocoding API; else skip or use default
                data = fetch_weather()
                if not data or not data.get("current"):
                    continue
                cur = data["current"]
                temp = cur.get("temperature")
                cond = (cur.get("condition") or "").lower()
                msg = None
                # Stricter thresholds to reduce false positives (aligned with dashboard)
                if cond == "stormy":
                    msg = "KRISHSAATHI: Storm likely. Keep crops and yourself safe."
                elif cond == "rainy":
                    msg = "KRISHSAATHI: Rain expected. Reduce irrigation, check drainage."
                elif temp is not None and temp >= 43:
                    msg = "KRISHSAATHI: Extreme heat. Ensure water and shade for crops."
                elif temp is not None and temp <= 1:
                    msg = "KRISHSAATHI: Cold conditions. Protect sensitive crops."
                if msg:
                    send_sms(f.mobile, msg)
            except Exception as e:
                logger.warning("Alert check failed for farmer %s: %s", f.id, e)


def start_alert_scheduler(flask_app):
    """Start APScheduler to run check_weather_and_alert periodically (e.g. every 6 hours)."""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            lambda: check_weather_and_alert(flask_app),
            "interval",
            hours=6,
            id="weather_alert",
        )
        scheduler.start()
        logger.info("Weather alert scheduler started (every 6h)")
    except Exception as e:
        logger.warning("Could not start alert scheduler: %s", e)
