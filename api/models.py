from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class Order(BaseModel):
    id: int
    username: str
    email: str
    description: str
