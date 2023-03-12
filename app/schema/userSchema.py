from pydantic import BaseModel, Field
import secrets
        
    
class UserSchema(BaseModel):
    username: str 
    email: str
    password: str
    empId: str
    department: str
    phoneNumber: str
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
        
