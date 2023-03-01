from pydantic import BaseModel, Field

        
    
class vehicleBookingByUser(BaseModel):
    empId: str = Field(default= None)
    empUsername: str = Field(default= None)
    userDepartment: str = Field(default= None)
    startLocation: str = Field(default= None)
    destination: str = Field(default= None)
    startTime: str = Field(default = None)
    endTime: str = Field(default = None)
    tripTime: str = Field(default = None)
    bookingNumber: str = Field(default = None)
    tripCompleted: bool = Field(default=False)
    tripCanceled: bool = Field(default=False)
    
    
    
        
