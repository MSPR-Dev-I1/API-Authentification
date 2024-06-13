import os
from unittest.mock import patch
import datetime
import importlib
import jwt

# pylint: disable=import-outside-toplevel
@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
def test_encode_jwt():
    """
        Testing if we can encode a payload without losing it
    """
    import app.tokken.tokken
    importlib.reload(app.tokken.tokken)

    access_key_list = ['key1', 'key2']
    token = app.tokken.tokken.encode_jwt(access_key_list)

    decoded_payload = jwt.decode(token,
                                 'test_secret_key',
                                 algorithms=['HS512'],
                                 options={'verify_signature':False})

    assert decoded_payload['accesses'] == access_key_list

# pylint: disable=import-outside-toplevel
patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_success(mock_decode):
    """
        Testing if we can verify that an access is available in a token
    """
    from app.tokken.tokken import verify_access

    mock_decode.return_value = {
        'accesses': ['key1', 'key2', 'key3']
    }

    token = 'dummy_token' # nosec
    access_key = 'key2'

    result = verify_access(access_key, token)

    assert result is True

# pylint: disable=import-outside-toplevel
@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_failure(mock_decode):
    """
        Testing if we can verify that an access is unavailable in a token
    """
    from app.tokken.tokken import verify_access

    mock_decode.return_value = {
        'accesses': ['key1', 'key2', 'key3']
    }

    token = 'dummy_token' # nosec
    access_key = 'key4'

    result = verify_access(access_key, token)

    assert result is False

# pylint: disable=import-outside-toplevel
@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_empty_list(mock_decode):
    """
        Testing if we can verify that there is no access in a token
    """
    from app.tokken.tokken import verify_access

    mock_decode.return_value = {
        'accesses': []
    }

    token = 'dummy_token' # nosec
    access_key = 'key1'

    result = verify_access(access_key, token)

    assert result is False

# pylint: disable=import-outside-toplevel
@patch.dict(os.environ, {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_access_no_accesses_key(mock_decode):
    """
        Testing if we can verify that the accesses key is unavailable in a token
    """
    from app.tokken.tokken import verify_access

    mock_decode.return_value = {
        'other_key': ['key1', 'key2', 'key3']
    }

    token = 'dummy_token' # nosec
    access_key = 'key1'

    result = verify_access(access_key, token)

    assert result is False

# pylint: disable=wrong-import-position
from app.tokken.tokken import verify_validity

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
def test_verify_validity_token_in_deactivated_list():
    """
        Testing if a token in the deactivated list in unvalide
    """
    token_value = 'dummy_token' # nosec
    deactivated_token_list = ['dummy_token']

    result = verify_validity(token_value, deactivated_token_list)

    assert result is False

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_missing_creation_date(mock_jwt_decode):
    """
        Testing if a token without a creation date in unvalide
    """
    token_value = 'dummy_token' # nosec
    deactivated_token_list = []
    mock_jwt_decode.return_value = {}

    result = verify_validity(token_value, deactivated_token_list)

    assert result is False

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_valid(mock_jwt_decode):
    """
        Testing if a standard token created half a day early is valid
    """
    token_value = 'dummy_token' # nosec
    deactivated_token_list = []
    creation_timestamp = (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12)
        ).timestamp()
    mock_jwt_decode.return_value = {'creation_date': creation_timestamp}

    result = verify_validity(token_value, deactivated_token_list)

    assert result is True

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_expired(mock_jwt_decode):
    """
        Testing if a standard token two day earlier is unvalid
    """
    token_value = 'dummy_token' # nosec
    deactivated_token_list = []
    creation_timestamp = (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)
        ).timestamp()
    mock_jwt_decode.return_value = {'creation_date': creation_timestamp}

    result = verify_validity(token_value, deactivated_token_list)

    assert result is False

@patch.dict('os.environ', {'JWT_KEY': 'test_secret_key'})
@patch('jwt.decode')
def test_verify_validity_token_no_creation_date(mock_jwt_decode):
    """
        Testing if a token with unexpected keys and without the expected keys is unvalid
    """
    token_value = 'dummy_token' # nosec
    deactivated_token_list = []
    mock_jwt_decode.return_value = {'other_key': 'value'}

    result = verify_validity(token_value, deactivated_token_list)

    assert result is False
