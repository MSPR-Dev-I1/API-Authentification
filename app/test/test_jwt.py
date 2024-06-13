import pytest
import jwt
from unittest.mock import patch
import os
import datetime
import importlib

@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
def test_encode_jwt():
    import app.tokken.tokken
    importlib.reload(app.tokken.tokken)

    access_key_list = ['key1', 'key2']
    jwt_key = os.getenv("JWT_KEY")
    print("jwt_key")
    print(jwt_key)
    print("--------------------------------------------------------------------------------")
    token = app.tokken.tokken.encode_jwt(access_key_list)

    decoded_payload = jwt.decode(token, 'test_secret_key', algorithms=['HS512'],options={'verify_signature':False})

    assert decoded_payload['accesses'] == access_key_list

patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_success(mock_decode):
    from app.tokken.tokken import verify_access

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
    from app.tokken.tokken import verify_access

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
    from app.tokken.tokken import verify_access

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
    from app.tokken.tokken import verify_access

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


from app.tokken.tokken import verify_validity

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_in_deactivated_list(mock_jwt_decode):
    # Setup
    token_value = 'dummy_token'
    deactivated_token_list = ['dummy_token']
    
    # Call the function
    result = verify_validity(token_value, deactivated_token_list)
    
    # Assert
    assert result is False

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_missing_creation_date(mock_jwt_decode):
    # Setup
    token_value = 'dummy_token'
    deactivated_token_list = []
    mock_jwt_decode.return_value = {}
    
    # Call the function
    result = verify_validity(token_value, deactivated_token_list)
    
    # Assert
    assert result is False

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_valid(mock_jwt_decode):
    # Setup
    token_value = 'dummy_token'
    deactivated_token_list = []
    creation_timestamp = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12)).timestamp()
    mock_jwt_decode.return_value = {'creation_date': creation_timestamp}
    
    # Call the function
    result = verify_validity(token_value, deactivated_token_list)
    
    # Assert
    assert result is True

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_expired(mock_jwt_decode):
    # Setup
    token_value = 'dummy_token'
    deactivated_token_list = []
    creation_timestamp = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)).timestamp()
    mock_jwt_decode.return_value = {'creation_date': creation_timestamp}
    
    # Call the function
    result = verify_validity(token_value, deactivated_token_list)
    
    # Assert
    assert result is False

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_no_creation_date(mock_jwt_decode):
    # Setup
    token_value = 'dummy_token'
    deactivated_token_list = []
    mock_jwt_decode.return_value = {'other_key': 'value'}
    
    # Call the function
    result = verify_validity(token_value, deactivated_token_list)
    
    # Assert
    assert result is False
