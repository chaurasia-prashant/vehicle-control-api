import uvicorn
from fastapi import FastAPI, Body, Depends
from app.models.userModel import UserSchema, UserLoginSchema
from app.models.bookingModel import vehicleBookingByUser
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer



users = []
vehicleBookings = []

app = FastAPI()

#for user login
@app.post("/", tags=["user"])
def user_login(user: UserLoginSchema= Body(default =None)):
    
    if check_user(user):
        return signJWT(user.empID)
    else:
        return {
            "error":"Invalid Login Details!"
        }


#User Signup [Create a new user]
@app.post("/user/signup", tags=["user"])
def user_signup(user:UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.empID)

def check_user(data: UserLoginSchema ):
    for user in users:
        if user.empID == data.empID and user.password == data.password:
            return True
        return False
    
    
#vehical Booking [create a new travel request]
@app.post("/user/bookVehicle", dependencies=[Depends(jwtBearer())], tags=["bookVehicle"])
def vehicle_booking(bookVehicle: vehicleBookingByUser = Body(default=None) ):
    vehicleBookings.append(bookVehicle)
    



