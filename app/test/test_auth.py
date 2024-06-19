from fastapi.testclient import TestClient
from app.main import app
from app.database.connexion import get_db
from app.test.inmemory_sqlite import memory_db

client = TestClient(app)


app.dependency_overrides[get_db] = memory_db

def test_hello_mate(mocker):
    """
    Cas passant
    """
    mocker.patch("app.routers.auth.test_connection", return_value=None)
    hello_mate = {"Hello": "Mate"}
    response = client.get("/authentification")
    assert response.status_code == 200
    assert response.json() == hello_mate

def test_hello_mate_error_500(mocker):
    """
    Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.routers.auth.test_connection", side_effect=Exception("Connection error"))
    response = client.get("/authentification")
    assert response.status_code == 500

def test_validation_token_valid(mocker):
    """
        Testing if the validation route return true whent the token is valid and permit access
    """
    mocker.patch("app.routers.auth.get_deactivated_tokens", return_value=[])
    mocker.patch("app.routers.auth.verify_validity", return_value=True)
    mocker.patch("app.routers.auth.verify_access", return_value=True)

    request_data = {
        "token": "valid_token",
        "service_key": "valid_service_key"
    }
    response = client.post("/authentification/validation_token", json=request_data)

    assert response.status_code == 200
    assert response.json() == {'validation': True}

def test_validation_token_invalid_token(mocker):
    """
        Testing if the validation route return false whent the token is invalid
    """
    mocker.patch("app.routers.auth.get_deactivated_tokens", return_value=[])
    mocker.patch("app.routers.auth.verify_validity", return_value=False)
    mocker.patch("app.routers.auth.verify_access", return_value=True)

    request_data = {
        "token": "invalid_token",
        "service_key": "valid_service_key"
    }
    response = client.post("/authentification/validation_token", json=request_data)

    assert response.status_code == 200
    assert response.json() == {'validation': False}

def test_validation_token_invalid_access(mocker):
    """
        Testing if the validation route return alse whent the token does not permit access
    """
    mocker.patch("app.routers.auth.get_deactivated_tokens", return_value=[])
    mocker.patch("app.routers.auth.verify_validity", return_value=True)
    mocker.patch("app.routers.auth.verify_access", return_value=False)

    request_data = {
        "token": "valid_token",
        "service_key": "invalid_service_key"
    }
    response = client.post("/authentification/validation_token", json=request_data)

    assert response.status_code == 200
    assert response.json() == {'validation': False}

def test_validation_token_exception(mocker):
    """
        Testing if the validation route return 500 when there is an exception
    """
    mocker.patch("app.routers.auth.get_deactivated_tokens",
                side_effect = Exception("Database error"))
    mocker.patch("app.routers.auth.verify_validity", return_value=True)
    mocker.patch("app.routers.auth.verify_access", return_value=True)

    request_data = {
        "token": "valid_token",
        "service_key": "valid_service_key"
    }
    response = client.post("/authentification/validation_token", json=request_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}
