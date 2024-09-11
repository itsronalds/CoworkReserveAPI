import jsonwebtoken as jwt
from config import CONFIG


def encode_jwt(payload: dict) -> str:
    return jwt.encode(payload, str(CONFIG['TOKEN_SECRET']), algorithm='HS256')


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, str(CONFIG['TOKEN_SECRET']), algorithms=['HS256'])
