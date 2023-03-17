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
from app.schema.bookingSchema import approveSchema, vehicleBookingByUser, vehicleSchema
# Modals
from app.modals.userModal import Accounts, EmployeeId, BookingModel, VehicleModel

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
            isAuthorized= user.isAuthorized,
            verifyPhoneNumber= user.verifyPhoneNumber,
            verifyEmail= user.verifyEmail,
            isOwner= user.isOwner,
            isAdmin= user.isAdmin,
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
     
@app.put('/approveRequest/{bookingId}/{vehiclNo}')
async def approveUserRequest(bookingId,vehiclNo,data: approveSchema):
    try:
        errCode = 0
        booking = db.session.query(BookingModel).filter(BookingModel.bookingNumber == bookingId)
        vehicle = db.session.query(VehicleModel).filter(VehicleModel.vehicleNumber == vehiclNo)
        vehicleBookData = vehicle.first().bookedTime
        bk = booking.first()
        updateBooking = False
        # inst = [f"{bk.tripDate}", {f"{bk.bookingNumber}":[f"{bk.startTime}",f"{bk.endTime}"]},]
        inst = [bk.tripDate, {bk.bookingNumber:[bk.startTime,bk.endTime]},]
        if vehicleBookData != None:
            vehicleBookData = json.loads(vehicleBookData)
            
            # inst = ["16-03-2023", {"gyi":["25200","80000"]}]
            keys = list(vehicleBookData.keys())
            # print(keys)
            dt = list(inst[1].keys())[0]
            dt = inst[1][dt]
            canInsert = 0
            if  inst[0] in keys:
                dataKeys = vehicleBookData[inst[0]]
                inkeys = dataKeys.keys()
                for j in inkeys:
                    check = dataKeys[j]
                    if int(check[0]) <= int(dt[0]) and (int(dt[0])+1) > int(check[1] ):
                        canInsert = 1
                    elif int(check[0]) >= int(dt[1]) and (int(dt[1])-1) <= int(check[1]):
                        canInsert = 1
                    else:
                        canInsert = 0
                        errCode = 904
                        #print("Already booking for this time interval")
                        break
                if canInsert == 1:
                    dataKeys[list(inst[1].keys())[0]] = dt
                    updateBooking = True
                    # print("Successfully approved")
                else:
                    updateBooking = False
                    # print("Already booking for this time")
            else:
                vehicleBookData[inst[0]] = inst[1]
                updateBooking = True
                # print("Successfully approved")
        else:
            vehicleBookData = {}
            vehicleBookData[inst[0]] = inst[1]
            updateBooking = True    
        # print(vehicleBookData)
        if updateBooking:
            # if not booking.first():
            #     return "error" 
            booking.update({
                "vehicleAlloted": vehiclNo,
                "vehicleNumber": vehicle.first().vehiclePhoneNumber,
                "tripStatus": True,
                "tripCanceled": False,
                "remark": data.remark
            })
            try:
                vehicle.update({
                    "bookedTime": json.dumps(vehicleBookData)
                    })
            except Exception as e:
                print(e)
            db.session.commit()
            # print("Booking Approved Successfully")
            if errCode != 904:
                return 901
        else:
            # print("Already booking for this time interval")
            return 904
    except Exception as e:
        return 500
     
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



@app.post('/vehicleRegister/')
async def user(data:vehicleSchema= Body(default =None)):
    try:
        db_vehicleRegister = VehicleModel(
            vehicleNumber = data.vehicleNumber,
            vehiclePhoneNumber = data.vehiclePhoneNumber,
            bookedTime = data.bookedTime,
            )
        db.session.add(db_vehicleRegister)
        db.session.commit()
        return "Successfully Registered"
    except Exception as e:
        return 404


@app.get("/getAllVehicles/")
async def checkUser(db:Session = Depends(get_db)):
    try:
        allVehicles = db.query(VehicleModel).all()
        if allVehicles != "null":
            return allVehicles
        else:
            return 404
        
        
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

 