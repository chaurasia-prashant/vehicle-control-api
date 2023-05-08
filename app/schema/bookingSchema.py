from pydantic import BaseModel, Field
import secrets
import datetime
        
    
class vehicleBookingByUser(BaseModel):
    bookingNumber:str = Field(default= secrets.token_urlsafe(5))
    empId: str 
    empUsername: str
    userDepartment: str
    isGuestBooking: bool= Field(default= False)  #Booking detail added for guest
    guestName: str  #Booking detail added for guest
    guestMobileNumber : str  #Booking detail added for guest
    vehicleType : str = Field(default=None) #Select for departmental or admin approval
    tripDate: str= Field(default= None)
    startLocation: str= Field(default= None)
    destination: str= Field(default= None)
    startTime: str= Field(default= None)
    endTime: str= Field(default= None)
    vehicleAlloted: str= Field(default= None)
    vehicleNumber: str= Field(default= None)
    tripStatus: bool= Field(default= False)
    tripCompleted: bool= Field(default= False)
    tripCanceled: bool= Field(default= False)
    reason: str = Field(default= None)
    remark: str= Field(default= None)
    
    class Config:
        orm_mode = True
        
class approveSchema(BaseModel):
    vehicleAlloted: str= Field(default= None)
    # vehicleNumber: str= Field(default= None)
    # bookingNumber:str = Field(default= None)
    # tripDate: str= Field(default= None)
    # startTime : str= Field(default= None)
    # endTime : str= Field(default= None)
    # tripStatus: bool= Field(default= False)
    # tripCanceled: bool= Field(default= False)
    remark: str= Field(default= None)
    
    class Config:
        orm_mode = True

class vehicleSchema(BaseModel):
    vehicleNumber: str = Field(default= None)
    vehiclePhoneNumber: str = Field(default= None)
    vehicleType : str = Field(default=None)
    bookedTime: dict = Field(default = None)

    class Config:
        orm_mode = True
        
    
class bookingBackupSchema(BaseModel):
    bookingMonth: str = Field(default=None)
    vehicleNumber: str = Field(default= None)
    vehicleType : str = Field(default=None)
    bookedTime: dict = Field(default = None)

    class Config:
        orm_mode = True    
        
