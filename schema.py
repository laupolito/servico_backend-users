from pydantic import BaseModel

class UsersSchema(BaseModel):
    id: int
    username: str
    password: str
    cpf: str
