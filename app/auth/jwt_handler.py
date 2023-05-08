# This file is responsible for signing, encoding, decoding and returning JWTs.


import time

import jwt

from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Function returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "access token" : token
    }
    
    
#Function used for signing the JWT string
def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }    
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)
    
    
    
def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms= JWT_ALGORITHM)
        return True if decode_token['expiry'] >= time.time() else False
    except Exception as e:
        print(e)
        return False  
    