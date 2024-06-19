from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app.database.connexion import get_db
from app.database.premier_schema import Base

client = TestClient(app)

def override_get_db_with_sqlite():
    """
        Return a sqlalchemy session connected to an in memory sqlite
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    return session

app.dependency_overrides[get_db] = override_get_db_with_sqlite

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
    mocker.patch("app.routers.auth.get_deactivated_tokens", side_effect = Exception("Database error"))
    mocker.patch("app.routers.auth.verify_validity", return_value=True)
    mocker.patch("app.routers.auth.verify_access", return_value=True)

    request_data = {
        "token": "valid_token",
        "service_key": "valid_service_key"
    }
    response = client.post("/authentification/validation_token", json=request_data)
    
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}
