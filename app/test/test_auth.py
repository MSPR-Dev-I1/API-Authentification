from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.database.connexion import get_db

client = TestClient(app)

def override_get_db():
    """
        Mock the database connexion
    """
    db = MagicMock()
    yield db

app.dependency_overrides[get_db] = override_get_db

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
