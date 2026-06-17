from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

otp_store = {}

def create_otp(phone: str):
    import random
    otp = str(random.randint(100000, 999999))

    otp_store[phone] = {
        "otp": otp,
        "expires": datetime.now() + timedelta(minutes=5)
    }

    from sms import send_sms

def create_otp(phone: str):
    import random
    otp = str(random.randint(100000, 999999))

    otp_store[phone] = {
        "otp": otp,
        "expires": datetime.now() + timedelta(minutes=5)
    }

    message = f"کد ورود شما به سیستم جیره‌نویسی: {otp}"

    send_sms(phone, message)

    return otp


def verify_otp(phone: str, otp: str):
    data = otp_store.get(phone)

    if not data:
        return False

    if data["otp"] != otp:
        return False

    if datetime.now() > data["expires"]:
        return False

    return True


def create_token(phone: str):
    payload = {
        "sub": phone,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
python-jose
passlib[bcrypt]
python-multipart 