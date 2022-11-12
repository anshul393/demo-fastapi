from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):    #Schema for recived data while cretaing post
    title : str
    content : str
    published : bool = True     # Default value of published is True
    # rating : Optional[int] = None   # rating is optional and its type is int and its default value is None

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner : UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : PostResponse
    votes : int 
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email : EmailStr
    password : str



class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str


class tokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id : str
    dir : int

