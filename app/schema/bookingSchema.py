from pydantic import BaseModel, Field
import secrets
        
    
class vehicleBookingByUser(BaseModel):
    empId: str 
    empUsername: str
    userDepartment: str
    startLocation: str
    destination: str
    startTime: str
    endTime: str
    bookingNumber: Field(default= secrets.token_hex(8))
    vehicleAlloted: str
    vehicleNumber: str
    tripStatus: bool
    tripCompleted: bool
    tripCanceled: bool
    
    class Config:
        orm_mode = True
    
    
    
        
