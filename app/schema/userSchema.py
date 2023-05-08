from typing import List
from pydantic import BaseModel, EmailStr, Field
import secrets
        
    
class UserSchema(BaseModel):
    username: str 
    email: str
    password: str
    empId: str
    department: str
    phoneNumber: str
    isAuthorized: bool= Field(default= False)
    verifyPhoneNumber:bool= Field(default= False)
    verifyEmail:bool= Field(default= False)
    isOwner: str
    isAdmin:bool= Field(default= False)
    uid: str
    
    class Config:
        orm_mode = True
        
class EmployeeIdSchema(BaseModel):
    empId: str
    
    class Config:
        orm_mode = True  
           
        
class UserLoginSchema(BaseModel):
    empId: str = Field(default= None)
    password: str = Field(default= None)
    
    class Config:
        orm_mode = True  
        
class EmailVerificationSchema(BaseModel):
    email: List[EmailStr]
    # otp: str = Field(default= None)
    
    class Config:
        orm_mode = True  

class verifyEmailOtp(BaseModel):
    email: str = Field(default= None)
    otp: str = Field(default= None)
    
    class Config:
        orm_mode = True  
        
class updatePasswordSchema(BaseModel):
    email: str = Field(default= None)
    password: str = Field(default= None)
    
    class Config:
        orm_mode = True 