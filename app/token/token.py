import jwt
import os

jwt_key = os.getenv("JWT_KEY")

def encode_jwt(access_key_list, ):

    payload = {
        'accesses': access_key_list
    }
    token = jwt.encode(payload, jwt_key, algorithm='HS512')

    return token

def verify_access(access_key, token):
    payload = jwt.decode(token, 'test_secret_key', algorithms=['HS512'])
    try:
        access_key_list = payload["accesses"]
    except KeyError:
        return False
    for key in access_key_list:
        if access_key== key: return True
    return False