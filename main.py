from sqlalchemy import create_engine
import uvicorn
import os
import json
from fastapi import FastAPI, Body, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists
from sqlalchemy import select
from sqlalchemy.sql.expression import literal
# Schemas
from app.schema.userSchema import UserSchema, EmployeeIdSchema, UserLoginSchema
from app.schema.bookingSchema import approveSchema, vehicleBookingByUser
# Modals
from app.modals.userModal import Accounts, EmployeeId, BookingModel

from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
import psycopg2
from config import config
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.environ['DATABASE_URL']

app = FastAPI()

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine )
Base = declarative_base()

app.add_middleware(DBSessionMiddleware, db_url=DB_URL)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db:Session = Depends(get_db)

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/userLogin")
async def checkUser(loginDetail: UserLoginSchema= Body(default =None)):
    try: 
        response = userInDatabase(loginDetail)         
        if response[0]:
            user = response[1]
            return user
        else:
            return 404
    except Exception as e:
        return e 
    
    
@app.post('/userSignup/')
def user(user:UserSchema= Body(default =None)):
    try:
        db_accounts = Accounts(
            empId = user.empId,
            username = user.username,
            email = user.email,
            password = user.password,
            department = user.department,
            phoneNumber = user.phoneNumber,
            uid = user.uid
            )
        db_EmployeeIdList = EmployeeId(
            empId= user.empId
            )
        db.session.add(db_EmployeeIdList)
        db.session.add(db_accounts)
        db.session.commit()
        return True
    except :
        return 404
        
        
def userInDatabase(data: UserLoginSchema):
    try:
        user = db.session.scalars(
            select(Accounts).where(Accounts.empId== data.empId)).first()
        if user.password == data.password:
            return [True, user]
        else: 
            return [False]
    except Exception as e :
        return [False,e]


 
    
@app.get("/allId")
async def checkUser(db:Session = Depends(get_db)):
    try:
        allId = db.query(EmployeeId).all()
        if allId != "null":
            print("user exist")
        else:
            print("not found")
        
        return allId
    except Exception as e:
        return e 

@app.post('/vehicleBooking/')
async def user(data:vehicleBookingByUser= Body(default =None)):
    try:
        db_vehicleBooking = BookingModel(
            empId= data.empId,
            empUsername= data.empUsername,
            userDepartment= data.userDepartment,
            tripDate = data.tripDate,
            startLocation= data.startLocation,
            destination= data.destination,
            startTime= data.startTime,
            endTime= data.endTime,
            bookingNumber= data.bookingNumber,
            vehicleAlloted= data.vehicleAlloted,
            vehicleNumber= data.vehicleNumber,
            tripStatus= data.tripStatus,
            tripCompleted= data.tripCompleted,
            tripCanceled= data.tripCanceled,
            reason =data.reason,
            remark = data.remark,
            )
        db.session.add(db_vehicleBooking)
        db.session.commit()
    except Exception as e:
        return e
    
@app.get('/userBookings/{userId}/')
async def user(userId : str):
    try:
        res = []
        allBooking = db.session.query(BookingModel).all()   
        for booking in allBooking:
            if booking.empId == userId:
                res.append(booking)
        if allBooking != "null":
            print("booking exist")
        else:
            print("booking not found")
        
        return res
    except Exception as e:
        return e

@app.get("/allBookingRequests/")
async def checkUser(db:Session = Depends(get_db)):
    try:
        allRequest = db.query(BookingModel).all()
        if allRequest != "null":
            print("user exist")
        else:
            print("not found")
        
        return allRequest
    except Exception as e:
        return e 
     
@app.put('/approveRequest/{bookingId}')
async def approveUserRequest(bookingId,data: approveSchema):
    try:
        booking = db.session.query(BookingModel).filter(BookingModel.bookingNumber == bookingId)
        if not booking.first():
            return "error" 
        booking.update({
            "vehicleAlloted": data.vehicleAlloted,
            "vehicleNumber": data.vehicleNumber,
            "tripStatus": data.tripStatus,
            "tripCanceled": data.tripCanceled,
            "remark": data.remark
        })
        db.session.commit()
        return{
        "code":"success",
        "message":"approval made"}
    except Exception as e:
        return e
     
@app.put('/rejectRequest/{bookingId}')
async def rejectUserRequest(bookingId,data: approveSchema):
    try:
        booking = db.session.query(BookingModel).filter(BookingModel.bookingNumber == bookingId)
        if not booking.first():
            return "error" 
        booking.update({
            "vehicleAlloted": data.vehicleAlloted,
            "vehicleNumber": data.vehicleNumber,
            "tripStatus": data.tripStatus,
            "tripCanceled": data.tripCanceled,
            "remark": data.remark
        })
        db.session.commit()
        return{
        "code":"success",
        "message":"donation made"}
    except Exception as e:
        return e




            
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    




# def connect():
#     connection = None
#     try:
#         params = config()
#         print('Connecting to the postgresql database......')
#         connection = psycopg2.connect(**params)
        
#         # create a cursor
        
#         crsr = connection.cursor()
#         print("postgresql database version: ")
#         crsr.execute('SELECT version()')
#         db_version = crsr.fetchone()
#         print(db_version)   
#         crsr.close()
        
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if connection is not None:
#             print(config())
#             connection.close()
#             print("Database connection terminated")

    

# users = []
# vehicleBookings = []

# app = FastAPI()

# #for user login
# @app.post("/", tags=["user"])
# def user_login(user: UserLoginSchema= Body(default =None)):
    
#     try:
#         response = check_user(user)
#         if response[0]:
#             # return signJWT(user.empId)
#             return response[1]
#         else:
#             return 404
#     except Exception as e :
#         print(e)


# #User Signup [Create a new user]
# @app.post("/user/signup", tags=["user"])
# def user_signup(user:UserSchema = Body(default=None)):
#     users.append(user)
#     return signJWT(user.empId)

# def check_user(data: UserLoginSchema ):
#     try:
#         currentUserData : UserSchema
#         for user in users:
#             if user.empId == data.empId and user.password == data.password:
#                 currentUserData =  user
#                 return [True,currentUserData]
#                 # return True
#             return False
#     except Exception as e :
#         print(e)
    
    
# #vehical Booking [create a new travel request]
# @app.post("/user/bookVehicle", dependencies=[Depends(jwtBearer())], tags=["bookVehicle"])
# def vehicle_booking(bookVehicle: vehicleBookingByUser = Body(default=None) ):
#     vehicleBookings.append(bookVehicle)
    



