from datetime import datetime
from sqlalchemy import create_engine
from sqlmodel import SQLModel
import uvicorn
import os
import json
import random
from fastapi import FastAPI, Body, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists
from sqlalchemy import select
from sqlalchemy.sql.expression import literal
# Admin
# Mail
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
# Schemas
from app.schema.userSchema import EmailVerificationSchema, UserSchema, UserLoginSchema, updatePasswordSchema, verifyEmailOtp
from app.schema.bookingSchema import approveSchema, bookingDumpSchema, vehicleBookingByUser, vehicleSchema
# Modals
from app.modals.userModal import Accounts, BookingsBackup, EmailVerification, EmployeeId, BookingModel, VehicleModel
# Urls
from urls import urls
from app.auth.hash_passwor import hashPassword, decodeHashedPassword
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.environ['DATABASE_URL']

app = FastAPI()

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.add_middleware(DBSessionMiddleware, db_url=DB_URL)

# Create initialized database table

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# configuration to send mail
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ['MAIL_FROM'],
    MAIL_PASSWORD=os.environ['MAIL_PASSWORD'],
    MAIL_FROM=os.environ['MAIL_FROM'],
    MAIL_PORT=465,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


url = urls()
# db:Session = Depends(get_db)

# @app.get("/")
# async def root():
#     return {"message": "hello world"}


# Login function
@app.post(url["login"])
async def checkUser(loginDetail: UserLoginSchema = Body(default=None)):
    try:
        response = userInDatabase(loginDetail)
        if response[0]:
            user = response[1]
            return [200,user]
        elif response[0] == response[1]:
            return [204,"None"]
        else:
            return [404,"None"]
    except:
        return [404,"None"]

# Signup function
@app.post(url["signup"])
def signup(user: UserSchema = Body(default=None)):
    try:
        userPassword = hashPassword(user.password)
        db_accounts = Accounts(
            empId=user.empId,
            username=user.username,
            email=user.email,
            password=userPassword,
            department=user.department,
            phoneNumber=user.phoneNumber,
            isAuthorized=user.isAuthorized,
            verifyPhoneNumber=user.verifyPhoneNumber,
            verifyEmail=user.verifyEmail,
            isOwner=user.isOwner,
            isAdmin=user.isAdmin,
            uid=user.uid
        )
        db_EmployeeIdList = EmployeeId(
            empId=user.empId,
            email = user.email
        )
        db.session.add(db_EmployeeIdList)
        db.session.add(db_accounts)
        db.session.commit()
        return True
    except:
        return 404

# Get and verify user in database
def userInDatabase(data: UserLoginSchema):
    try:
        user = db.session.scalars(
            select(Accounts).where(Accounts.empId == data.empId)).first()
        if decodeHashedPassword(user.password) == data.password:
            return [True, user]
        else:
            return [False,False]
    except Exception as e:
        return [False, e]

# Send email for email verification
@app.post(url["sendEmailOTP"])
async def sendOTPonEmail(userMail: EmailVerificationSchema):
    try:
        otp = random.randrange(000000, 999999)
        html = f"""
        <h>Dear user,</h>
        <p>Your OTP for mail Id verification is given below</p>
        </br>
        <center><h1 style="color: skyblue">{otp}</h1> </center>
        """
        message = MessageSchema(
            subject="OTP verification for MPL vehical Management",
            recipients=userMail.dict().get("email"),
            body=html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        verify = db.session.query(EmailVerification).filter(
            EmailVerification.email == userMail.email[0])
        if not verify.first():
            data = EmailVerification(
                email=userMail.email[0],
                otp=str(otp)
            )
            db.session.add(data)
            db.session.commit()
            return 200
        else:
            verify.update(
                {"otp": str(otp)}
            )
            db.session.commit()
            return 200

    except Exception as e:
        print(e)
        return "error"

# Verify otp for email verification
@app.post(url["verifyEmailOTP"])
async def verifyOTPonEmail(userMail: verifyEmailOtp, db: Session = Depends(get_db)):
    try:
        verify = db.query(EmailVerification).filter(
            EmailVerification.email == userMail.email)
        if not verify.first():
            return "not found"
        else:
            verify = verify.first()
            if userMail.otp == verify.otp:
                db.delete(verify)
                db.commit()
                return 200
            else:
                return 203
    except:
        return 405


# Update password of a user
@app.post(url["updatePassword"])
async def updatePassword(passwordRequest: updatePasswordSchema,db: Session = Depends(get_db)):
    try:
        user = db.query(Accounts).filter(Accounts.email == passwordRequest.email)
        if not user.first():
            return 404
        else:
            newpassword = hashPassword(passwordRequest.password)
            user.update({
                "password" : newpassword
            })
            db.commit()
            return 200
    except Exception as e:
        return "error"
        
# Get all registered IDs
@app.get(url["allId"])
async def getAllId(db: Session = Depends(get_db)):
    try:
        allId = db.query(EmployeeId).all()
        return allId
    except Exception as e:
        return e



# Book a vehicle
@app.post(url["vehicleBooking"])
async def vehicleBooking(data: vehicleBookingByUser = Body(default=None)):
    try:
        db_vehicleBooking = BookingModel(
            empId=data.empId,
            empUsername=data.empUsername,
            userDepartment=data.userDepartment,
            isGuestBooking=data.isGuestBooking,
            guestName=data.guestName,
            guestMobileNumber=data.guestMobileNumber,
            vehicleType = data.vehicleType,
            tripDate=data.tripDate,
            startLocation=data.startLocation,
            destination=data.destination,
            startTime=data.startTime,
            endTime=data.endTime,
            bookingNumber=data.bookingNumber,
            vehicleAlloted=data.vehicleAlloted,
            vehicleNumber=data.vehicleNumber,
            tripStatus=data.tripStatus,
            tripCompleted=data.tripCompleted,
            tripCanceled=data.tripCanceled,
            reason=data.reason,
            remark=data.remark,
        )
        db.session.add(db_vehicleBooking)
        db.session.commit()
    except Exception as e:
        print(e)
        return e

# Get all user bookings
@app.get(url["userBookings"] + '{userId}/')
async def getUserBookings(userId: str):
    try:
        res = []
        allBooking = db.session.query(BookingModel).all()
        for booking in allBooking:
            if booking.empId == userId:
                res.append(booking) 
        return res
    except Exception as e:
        return e

# Get  all bookings
@app.get(url["allBookingRequests"])
async def getAllBooking(db: Session = Depends(get_db)):
    try:
        allRequest = db.query(BookingModel).all()
        # allRequest.sort(key="tripDate", reverse= True)
        
        return allRequest
    except Exception as e:
        return e


# Approve a booking request
@app.put(url["approveRequest"]+'{bookingId}/{vehiclNo}')
async def approveUserRequest(bookingId, vehiclNo, data: approveSchema):
    try:
        errCode = 0
        booking = db.session.query(BookingModel).filter(
            BookingModel.bookingNumber == bookingId)
        vehicle = db.session.query(VehicleModel).filter(
            VehicleModel.vehicleNumber == vehiclNo)
        vehicleBookData = vehicle.first().bookedTime
        bk = booking.first()
        updateBooking = False
        # inst = [f"{bk.tripDate}", {f"{bk.bookingNumber}":[f"{bk.startTime}",f"{bk.endTime}"]},]
        inst = [bk.tripDate, {bk.bookingNumber: [bk.startTime, bk.endTime]},]
        if vehicleBookData != None:
            vehicleBookData = json.loads(vehicleBookData)

            # inst = ["16-03-2023", {"gyi":["25200","80000"]}]
            keys = list(vehicleBookData.keys())
            # print(keys)
            dt = list(inst[1].keys())[0]
            dt = inst[1][dt]
            canInsert = 0
            if inst[0] in keys:
                dataKeys = vehicleBookData[inst[0]]
                inkeys = dataKeys.keys()
                for j in inkeys:
                    check = dataKeys[j]
                    if int(check[0]) <= int(dt[0]) and (int(dt[0])+1) > int(check[1]):
                        canInsert = 1
                    elif int(check[0]) >= int(dt[1]) and (int(dt[1])-1) <= int(check[1]):
                        canInsert = 1
                    else:
                        canInsert = 0
                        errCode = 904
                        # print("Already booking for this time interval")
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
                pass
            db.session.commit()
            # print("Booking Approved Successfully")
            if errCode != 904:
                return 901
        else:
            # print("Already booking for this time interval")
            return 904
    except Exception as e:
        return 500

# Reject a user request
@app.put(url["rejectRequest"]+'{bookingId}')
async def rejectUserRequest(bookingId, data: approveSchema):
    try:
        booking = db.session.query(BookingModel).filter(
            BookingModel.bookingNumber == bookingId)
        if not booking.first():
            return "error"
        booking.update({
            "vehicleAlloted": None,
            "vehicleNumber": None,
            # "tripStatus": data.tripStatus,
            "tripCanceled": True,
            "remark": data.remark
        })
        db.session.commit()
        return {
            "code": "success",
            "message": "donation made"}
    except Exception as e:
        return e

# Register a vehical
@app.post(url["vehicleRegister"])
async def vehicleRegister(data: vehicleSchema = Body(default=None)):
    try:
        db_vehicleRegister = VehicleModel(
            vehicleNumber=data.vehicleNumber,
            vehiclePhoneNumber=data.vehiclePhoneNumber,
            vehicleType = data.vehicleType,
            bookedTime=data.bookedTime,
        )
        db.session.add(db_vehicleRegister)
        db.session.commit()
        return "Successfully Registered"
    except Exception as e:
        return 404

# Get all registered vehicle
@app.get(url["getAllVehicles"])
async def checkUser(db: Session = Depends(get_db)):
    try:
        allVehicles = db.query(VehicleModel).all()
        if allVehicles != "null":
            return allVehicles
        else:
            return 404

    except Exception as e:
        return e

        
# Backup booking data    

@app.post(url["backupBooking"])
async def backupBookings():
    try:
        allRequest = db.session.query(VehicleModel).all()
        cmy = datetime.today()
        cmy = cmy.strftime('%m-%Y')
        res = {}
        for i in allRequest:
            if i.bookedTime != None:
                bkt = json.loads(i.bookedTime)
                for j in list(bkt.keys()):
                    dt = datetime.strptime(j,"%Y-%m-%d")
                    dt = dt.strftime('%m-%Y')
                    if cmy != dt:
                        if dt not in res.keys():
                            res[dt] = {}
                        if i.vehicleNumber not in res[dt].keys():
                            res[dt][i.vehicleNumber] = {}
                        
                        res[dt][i.vehicleNumber].update({j: bkt[j]})
                        del bkt[j]
                        i.bookedTime = json.dumps(bkt)
        if res != {}:
            for i in res:
                backup = db.session.query(BookingsBackup).filter(BookingsBackup.bookingMonth == i)
                if not backup.first():
                    data = BookingsBackup(
                        bookingMonth = i,
                        bookedTime = json.dumps(res[i])
                    )
                    db.session.add(data)
                    db.session.commit()
                else:
                    backup.update({
                        "bookedTime" : json.dumps(res[i])
                    })   
                    db.session.commit()    
        for i in allRequest:
            updateRequest = db.session.query(VehicleModel).filter(VehicleModel.vehicleNumber == i.vehicleNumber)
            updateRequest.update({
                "bookedTime": i.bookedTime
            })
            db.session.commit() 
            
        return "Successfully backup done"
            
    except Exception as e:
        return e


@app.post(url["getBookingDump"])
async def getBookingDump(data : bookingDumpSchema):
    try:
        dt = datetime.today().replace(day=1)
        dt = dt.strftime('%m-%Y')
        if data.backupDate != dt:
            dump = db.session.scalars(
            select(BookingsBackup).where(BookingsBackup.bookingMonth == data.backupDate)).first()
            return [200,dump]
        else:
            allRequest = db.session.query(VehicleModel).all()
            cmy = data.backupDate
            res = {}
            for i in allRequest:
                if i.bookedTime != None:
                    bkt = json.loads(i.bookedTime)
                    for j in list(bkt.keys()):
                        dt = datetime.strptime(j,"%Y-%m-%d")
                        dt = dt.strftime('%m-%Y')
                        if cmy == dt:
                            if dt not in res.keys():
                                res[dt] = {}
                            if i.vehicleNumber not in res[dt].keys():
                                res[dt][i.vehicleNumber] = {}
                            res[dt][i.vehicleNumber].update({j: bkt[j]})
                            del bkt[j]
                            i.bookedTime = json.dumps(bkt)
            return [200,res]
            
    except Exception as e:
        print(e)
        return 404


@app.post(url["assignRole"]+'{id}')
def assignRole(id):
    try:
        user = db.session.query(Accounts).filter(
            Accounts.empId == id)
    
        if user.first():
            user.update({
                "isOwner" : True
            })
            db.session.commit()
            return 200
        else:
            return 204
    except Exception as e:
        return e
    
@app.post(url["roleReject"]+'{id}')
def rejectRole(id):
    try:
        user = db.session.query(Accounts).filter(
            Accounts.empId == id)
    
        if user.first():
            user.update({
                "isOwner" : False
            })
            db.session.commit()
            return 200
        else:
            return 204
    except Exception as e:
        return e

@app.post(url["addAdmin"]+'{id}')
def addAdmin(id):
    try:
        user = db.session.query(Accounts).filter(
            Accounts.empId == id)
    
        if user.first():
            user.update({
                "isAdmin" : True
            })
            db.session.commit()
            return 200
        else:
            return 204
    except Exception as e:
        return e 
    
@app.post(url["removeAdmin"]+'{id}')
def removeAdmin(id):
    try:
        user = db.session.query(Accounts).filter(
            Accounts.empId == id)
    
        if user.first():
            user.update({
                "isAdmin" : False
            })
            db.session.commit()
            return 200
        else:
            return 204
    except Exception as e:
        return e

# Main function
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





# {
#   "username": "Prashant Kumar Chaurasia",
#   "email": "pkc5683@gmail.com",
#   "password": "568300",
#   "empId": "208448",
#   "department": "IMD",
#   "phoneNumber": "8005089340",
#   "isAuthorized": true,
#   "verifyPhoneNumber": false,
#   "verifyEmail": true,
#   "isOwner": false,
#   "isAdmin": true,
#   "uid": "string"
# }