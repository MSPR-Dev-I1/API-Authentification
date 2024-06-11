import pytest
import jwt
from unittest.mock import patch
import os

@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
def test_encode_jwt():
    from app.token.token import encode_jwt

    access_key_list = ['key1', 'key2']

    token = encode_jwt(access_key_list)

    decoded_payload = jwt.decode(token, 'test_secret_key', algorithms=['HS512'])

    assert decoded_payload == {'accesses': access_key_list}
