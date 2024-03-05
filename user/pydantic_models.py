from pydantic import BaseModel
from . models import *
from typing  import List


class usercreate(BaseModel):
    name:str
    email:str
    mobile:int
    country:str
    state:str
    city:str
    gender:Gender
    hobby:Hobby

class personecreate(BaseModel):
    email:str
    password:str


class loginuser(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    acces_token:str
    token_type:str ="bearer"    

class deleteuser(BaseModel):
    id:int


class updateuser(BaseModel):
    id:int
    name:str
    email:str
    mobile:int
    country:str
    state:str
    city:str
    gender:Gender
    hobby:Hobby
