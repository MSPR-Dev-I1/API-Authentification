from fastapi.testclient import TestClient
from app.main import app
from app.database.connexion import get_db
from app.test.inmemory_sqlite import memory_db
from app.database.premier_schema import Role,Access, Utilisateur

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

def test_deploy_token_role_not_found(mocker):
    """
        Testing if the token route return a 404 error when the role does not exist
    """
    mocker.patch("app.routers.auth.get_utilisateur", return_value=Utilisateur())
    mocker.patch("app.routers.auth.get_role", return_value=None)

    response = client.post("/authentification/token", json={"user": 1})

    assert response.status_code == 404
    assert response.json() == {"detail": "Cannot deliver any token for a user without a role."}

def test_deploy_token_no_access(mocker):
    """
        Testing if the token route return a 404 error when the role has no accesses
    """
    role_mock = Role(nom="Test Role", accesses=[])
    mocker.patch("app.routers.auth.get_utilisateur", return_value=Utilisateur())
    mocker.patch("app.routers.auth.get_role", return_value=role_mock)

    response = client.post("/authentification/token", json={"user": 1})

    assert response.status_code == 404
    assert response.json() == {"detail": "Cannot deliver any token for the role Test Role"}

def test_deploy_token_success(mocker):
    """
        Testing if the token route can return a token
    """
    access_mock = Access(cle_de_service="service_key_1")
    role_mock = Role(nom="Test Role", accesses=[access_mock])
    mocker.patch("app.routers.auth.get_utilisateur", return_value=Utilisateur())
    mocker.patch("app.routers.auth.get_role", return_value=role_mock)
    mocker.patch("app.routers.auth.encode_jwt", return_value="mock_token")

    response = client.post("/authentification/token", json={"user": 1})

    assert response.status_code == 200
    assert response.json() == {"token": "mock_token"}

def test_deploy_token_internal_server_error(mocker):
    """
        Testing if the token route can return a 500 during internal errors
    """
    mocker.patch("app.routers.auth.get_utilisateur", return_value=Utilisateur())
    mocker.patch("app.routers.auth.get_role", side_effect=Exception("DB Error"))

    response = client.post("/authentification/token", json={"user": 1})

    assert response.status_code == 500
    assert response.json() == {"detail": "DB Error"}
