from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title : str
    tag : str

class UserCreate(BaseModel):
    username : str
    email : str
    password : str

