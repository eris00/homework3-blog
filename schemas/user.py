from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class User(UserBase):
    first_name: str
    last_name: str

class UserCreate(User):
    password: str

class UserResponse(User):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    username: str | None = None




