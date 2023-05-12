from sqlalchemy import Column,String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Accounts(Base):

    __tablename__ = 'accounts'
    empId = Column(String, primary_key=True, index=True, unique=True)
    username = Column(String)
    email = Column(String)
    password = Column(String(600))
    department = Column(String)
    phoneNumber = Column(String)
    isAuthorized= Column(Boolean)
    verifyPhoneNumber= Column(Boolean)
    verifyEmail= Column(Boolean)
    isOwner= Column(String)
    isAdmin= Column(Boolean)
    uid = Column(String)


class EmployeeId(Base):
    __tablename__ = 'employeeId'
    empId = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String)


class BookingModel(Base):
    __tablename__ = 'vehicle_Bookings'
    bookingNumber = Column(String, primary_key=True, index=True,unique=False)
    empId = Column(String)
    empUsername = Column(String)
    userDepartment = Column(String)
    isGuestBooking= Column(Boolean) #Booking detail added for guest
    guestName = Column(String) #Booking detail added for guest
    guestMobileNumber  = Column(String) #Booking detail added for guest
    vehicleType  = Column(String) #Booking detail for departmental booking
    tripDate = Column(String)
    startLocation = Column(String)
    destination = Column(String)
    startTime = Column(String)
    endTime = Column(String)
    vehicleAlloted = Column(String)
    vehicleNumber = Column(String)
    tripStatus = Column(Boolean)
    tripCompleted = Column(Boolean)
    tripCanceled = Column(Boolean)
    reason = Column(String)
    remark = Column(String)
    


class VehicleModel(Base):
    __tablename__ = 'vehicle_Details'
    vehicleNumber = Column(String, primary_key=True, index=True)
    vehiclePhoneNumber = Column(String)
    vehicleType = Column(String)
    bookedTime = Column(JSON)


class EmailVerification(Base):
    __tablename__ = 'Email_Verification'
    email = Column(String, primary_key=True, index=True)
    otp = Column(String)
    
    
class BookingsBackup(Base):
    __tablename__ = 'booking_backup'
    bookingMonth = Column(String, primary_key=True, index=True)
    bookedTime = Column(JSON)