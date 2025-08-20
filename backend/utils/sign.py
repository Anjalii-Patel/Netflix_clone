# backend/utils/sign.py
import datetime, jwt
from django.conf import settings
from django.utils import timezone

ALGO = "HS256"

def gen_stream_token(user_id: int, video_id: int, ttl_seconds: int = 300):
    exp = timezone.now() + datetime.timedelta(seconds=ttl_seconds)
    payload = {"uid": user_id, "vid": video_id, "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)

def verify_stream_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
    except jwt.PyJWTError:
        return None
