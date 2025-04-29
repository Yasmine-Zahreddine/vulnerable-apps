from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    id: int
    user_id: int
    content: str
