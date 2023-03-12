from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Accounts(Base):

    __tablename__ = 'accounts'
    empId = Column(String, primary_key=True, index=True, unique=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    department = Column(String)
    phoneNumber = Column(String)
    uid = Column(String)


class EmployeeId(Base):
    __tablename__ = 'employeeId'
    empId = Column(String, primary_key=True, index=True, unique=True)


class BookingModel(Base):
    __tablename__ = 'vehicle_Bookings'
    bookingNumber = Column(String, primary_key=True, index=True)
    empId = Column(String)
    empUsername = Column(String)
    userDepartment = Column(String)
    tripDate = Column(DateTime)
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
    
    # __allow_unmapped__ = True

