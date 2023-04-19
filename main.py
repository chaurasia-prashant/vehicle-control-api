from sqlalchemy import create_engine
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
# Mail
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
# Schemas
from app.schema.userSchema import EmailVerificationSchema, UserSchema, UserLoginSchema, updatePasswordSchema, verifyEmailOtp
from app.schema.bookingSchema import approveSchema, vehicleBookingByUser, vehicleSchema
# Modals
from app.modals.userModal import Accounts, EmailVerification, EmployeeId, BookingModel, VehicleModel
# Urls
from urls import urls
from app.auth.hash_passwor import hashPassword, decodeHashedPassword
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.environ.get('DATABASE_URL')

app = FastAPI()

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.add_middleware(DBSessionMiddleware, db_url=DB_URL)


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


@app.post(url["signup"])
def user(user: UserSchema = Body(default=None)):
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
        return "error"


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
        
        
@app.get(url["allId"])
async def checkUser(db: Session = Depends(get_db)):
    try:
        allId = db.query(EmployeeId).all()
        return allId
    except Exception as e:
        return e


@app.post(url["vehicleBooking"])
async def user(data: vehicleBookingByUser = Body(default=None)):
    try:
        db_vehicleBooking = BookingModel(
            empId=data.empId,
            empUsername=data.empUsername,
            userDepartment=data.userDepartment,
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
        return e


@app.get(url["userBookings"] + '{userId}/')
async def user(userId: str):
    try:
        res = []
        allBooking = db.session.query(BookingModel).all()
        for booking in allBooking:
            if booking.empId == userId:
                res.append(booking)
        return res
    except Exception as e:
        return e


@app.get(url["allBookingRequests"])
async def checkUser(db: Session = Depends(get_db)):
    try:
        allRequest = db.query(BookingModel).all()
        return allRequest
    except Exception as e:
        return e


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


@app.post(url["vehicleRegister"])
async def user(data: vehicleSchema = Body(default=None)):
    try:
        db_vehicleRegister = VehicleModel(
            vehicleNumber=data.vehicleNumber,
            vehiclePhoneNumber=data.vehiclePhoneNumber,
            bookedTime=data.bookedTime,
        )
        db.session.add(db_vehicleRegister)
        db.session.commit()
        return "Successfully Registered"
    except Exception as e:
        return 404


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
