from pydantic import BaseModel, Field, EmailStr

        
    
class UserSchema(BaseModel):
    username: str = Field(default= None)
    email: EmailStr = Field(default= None)
    password: str = Field(default= None)
    empID: int = Field(default= None)
    department: str = Field(default = None)
    phoneNumber: int = Field(default = None)
    
    
    # class Config:
    #     user_schema = {
    #         "user_detail": {
    #             "name": "prashant",
    #             "email": "pk@gmail.com",
    #             "password": "5683"
    #         }
    #     }
        
        
        
class UserLoginSchema(BaseModel):
    empID: int = Field(default= None)
    password: str = Field(default= None)
    # class Config:
    #     user_schema = {
    #         "user_detail": {
    #             "email": "pk@gmail.com",
    #             "password": "5683"
    #         }
    #     }