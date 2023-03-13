from pydantic import BaseModel, Field, EmailStr

        
    
class vehicleSchema(BaseModel):
    vehocleNumber: str = Field(default= None)
    vehiclePhoneNumber: str = Field(default= None)
    bookStatus: str = Field(default= None)
    vehicleTimeLine: str = Field(default= None)
    bookedTime: list = Field(default = None)
    
    
        
