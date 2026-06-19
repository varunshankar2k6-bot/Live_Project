from pydantic import BaseModel, EmailStr
#Signup
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    gender: str
    date_of_birth: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
#Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#User Response
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str
    phone_number: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    points: int
    class Config:
        from_attributes = True