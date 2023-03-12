from pydantic import BaseModel, Field
import secrets
        
    
class UserSchema(BaseModel):
    username: str 
    email: str
    password: str
    empID: str
    department: str
    phoneNumber: str
    uid: str = Field(default= secrets.token_urlsafe(16))
    
    class Config:
        orm_mode = True
        
class EmployeeIdSchema(BaseModel):
    empID: str
    
    class Config:
        orm_mode = True  
           
        
class UserLoginSchema(BaseModel):
    empID: str = Field(default= None)
    password: str = Field(default= None)
    
    class Config:
        orm_mode = True  
        
