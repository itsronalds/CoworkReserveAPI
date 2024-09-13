from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ryan Williams",
                    "email": "example@domain.com",
                    "password": "123456789",
                }
            ]
        }
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@domain.com",
                    "password": "123456789",
                }
            ]
        }
    }
