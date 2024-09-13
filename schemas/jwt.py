from pydantic import BaseModel
from config import CONFIG


class JWTSettings(BaseModel):
    authjwt_secret_key: str = 'SECRET KEY'
