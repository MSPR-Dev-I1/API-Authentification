import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
'''
def test_get_client(mocker):
    """
        Cas passant
    """
    mocker.patch("app.routers.client.test_connection", return_value=None)
    get_client = {"Hello": "Client"}
    response = client.get("/client")
    assert response.status_code == 200
    assert response.json() == get_client

def test_get_client_error_500():
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    with unittest.mock.patch("app.routers.client.test_connection") as mocked_test_connection:
        mocked_test_connection.side_effect = Exception("Connection error")
        response = client.get("/client")
        assert response.status_code == 500
        assert response.json() == {"detail": "Connection failed: Connection error"}
'''