import jwt
import os

jwt_key = os.getenv("JWT_KEY")

def encode_jwt(access_key_list, ):

    payload = {
        'accesses': access_key_list
    }
    token = jwt.encode(payload, jwt_key, algorithm='HS512')

    return token