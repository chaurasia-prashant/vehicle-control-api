from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class Accounts(Base):
    
    __tablename__ = 'accounts'
    empId = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    department = Column(String)
    phoneNumber = Column(String)
    uid = Column(String)
    
    # __table__ = Table(__tablename__, Base.metadata,
    #     autoload=True,
    #     autoload_with=create_engine(db_url))

    


class EmployeeId(Base):
    __tablename__ = 'employeeId'
    empId = Column(String, primary_key=True, index=True)