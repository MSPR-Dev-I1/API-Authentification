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

patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_success(mock_decode):
    from app.token.token import verify_access

    # Mock payload returned by jwt.decode
    mock_decode.return_value = {
        'accesses': ['key1', 'key2', 'key3']
    }

    token = 'dummy_token'
    access_key = 'key2'

    # Call the function to be tested
    result = verify_access(access_key, token)

    # Assert the result is True
    assert result is True

@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_failure(mock_decode):
    from app.token.token import verify_access

    # Mock payload returned by jwt.decode
    mock_decode.return_value = {
        'accesses': ['key1', 'key2', 'key3']
    }

    token = 'dummy_token'
    access_key = 'key4'

    # Call the function to be tested
    result = verify_access(access_key, token)

    # Assert the result is False
    assert result is False

@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_empty_list(mock_decode):
    from app.token.token import verify_access

    # Mock payload returned by jwt.decode
    mock_decode.return_value = {
        'accesses': []
    }

    token = 'dummy_token'
    access_key = 'key1'

    # Call the function to be tested
    result = verify_access(access_key, token)

    # Assert the result is False
    assert result is False

@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_no_accesses_key(mock_decode):
    from app.token.token import verify_access

    # Mock payload returned by jwt.decode without 'accesses' key
    mock_decode.return_value = {
        'other_key': ['key1', 'key2', 'key3']
    }

    token = 'dummy_token'
    access_key = 'key1'

    # Call the function to be tested
    result = verify_access(access_key, token)

    # Assert the result is False
    assert result is False