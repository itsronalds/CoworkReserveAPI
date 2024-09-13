from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    email: EmailStr
    password: str
