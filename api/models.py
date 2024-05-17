from pydantic import BaseModel, PrivateAttr

class User(BaseModel):
    _id: int = PrivateAttr()
    name: str
    email: str
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id', None)

class Order(BaseModel):
    id: int
    username: str
    email: str
    description: str
