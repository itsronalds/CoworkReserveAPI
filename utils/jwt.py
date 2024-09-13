from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# jwt
import jsonwebtoken as jwt

# config
from config import CONFIG

# logger
from utils.logger import logger


TOKEN_SECRET = CONFIG['TOKEN_SECRET'] or 'Default secret'


def encode_jwt(payload: dict) -> str:
    return jwt.encode(payload, str(CONFIG['TOKEN_SECRET']), algorithm='HS256')


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, str(CONFIG['TOKEN_SECRET']), algorithms=['HS256'])


def check_jwt(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
        return payload
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Unauthorized'}
        )
