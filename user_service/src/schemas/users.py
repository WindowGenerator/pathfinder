from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"email": "minecraft@jojo.sus", "password": "security"}
        }


class UserWithTokenSchema(BaseModel):
    user: User = Field(...)
    access_token: str = Field(...)


class UserFromDBSchema(User):
    hashed_password: str = Field(...)
