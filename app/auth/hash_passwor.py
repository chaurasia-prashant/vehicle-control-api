# This file is responsible for hashing password using JWTs.


import jwt
from cryptography.fernet import Fernet
from decouple import config


JWT_SECRET = b'PhiEL8cZ8XDLqbyXdY9KqC-nycu66Mcz6wsri_-YBLk='
JWT_ALGORITHM = config("algorithm")

fernet = Fernet(JWT_SECRET)  
    
#Function used for signing the JWT string
def hashPassword(userID: str):
    hashed_password = fernet.encrypt(userID.encode())
    hashed_password =str(hashed_password)
    return hashed_password
    
    
    
def decodeHashedPassword(userPassword: str):
    try:
        userPassword = userPassword[2:-1]
        userPassword.encode('utf-8')
        original_password = fernet.decrypt(userPassword).decode()
        
        return original_password
    except Exception as e:
        print("error ", e)
        return "invalid" 
    