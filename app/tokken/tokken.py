import os
import datetime
import jwt

jwt_key = os.getenv("JWT_KEY")

def encode_jwt(access_key_list, ):
    """
        Encode a jwt token with a key found the .env file
        The payload id the list of permited accesses and the current timestamp
    """
    payload = {
        'accesses': access_key_list,
        'creation_date':datetime.datetime.now(datetime.UTC).timestamp()
    }
    token = jwt.encode(payload, jwt_key, algorithm='HS512')
    return token

def verify_access(access_key, token):
    """
        Verify if the access can be found in the token
    """
    payload = jwt.decode(token, jwt_key, algorithms=['HS512'])
    try:
        access_key_list = payload["accesses"]
    except KeyError:
        return False
    for key in access_key_list:
        if access_key== key:
            return True
    return False

def verify_validity(token, deactivated_token_list):
    """
        Verify if the token is valid
    """
    for deactivated_token in deactivated_token_list:
        if deactivated_token == token :
            return False

    payload = jwt.decode(token, jwt_key, algorithms=['HS512'])
    try:
        creation_date = datetime.datetime.fromtimestamp(
            payload["creation_date"], tz=datetime.timezone.utc)
    except KeyError:
        return False

    now = datetime.datetime.now(datetime.UTC)
    time_difference = now - creation_date
    return time_difference.days <= 1
