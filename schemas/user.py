from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ronald Abu Saleh",
                    "email": "ronald.test@gmail.com",
                    "password": "123456789",
                }
            ]
        }
    }
