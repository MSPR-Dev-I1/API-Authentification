import pytest
from unittest.mock import patch, MagicMock
from app.database.premier_schema import Role, Utilisateur, UtilisateurClient, Access
from app.compute.compute import (
    create_utilisateur,
    create_utilisateur_client,
    create_role,
    create_access,
    get_utilisateur,
    get_utilisateur_client,
    get_role,
    get_access,
    update_utilisateur,
    update_utilisateur_client,
    update_role,
    update_access,
    delete_utilisateur,
    delete_utilisateur_client,
    delete_role,
    delete_access,
)

@patch('app.compute.compute.get_db')
def test_create_utilisateur(mock_get_db):
    mock_get_db.return_value = MagicMock()
    role = Role()
    utilisateur = create_utilisateur(role)
    assert isinstance(utilisateur, Utilisateur)

@patch('app.compute.compute.get_db')
def test_create_utilisateur_client(mock_get_db):
    mock_get_db.return_value = MagicMock()
    utilisateur = Utilisateur()
    utilisateur_client = create_utilisateur_client(utilisateur)
    assert isinstance(utilisateur_client, UtilisateurClient)

@patch('app.compute.compute.get_db')
def test_create_role(mock_get_db):
    mock_get_db.return_value = MagicMock()
    access = Access()
    role = create_role(name="name", accesses=[access])
    assert isinstance(role, Role)

@patch('app.compute.compute.get_db')
def test_create_role_too_long_name(mock_get_db):
    mock_get_db.return_value = MagicMock()
    access = Access()
    name = """
..............................................................................
..............................................................................
..............................................................................
..............................................................................
"""
    with pytest.raises(ValueError, match="A role name should not be longer than 100 characters"):
        create_role(name=name, accesses=[access])

@patch('app.compute.compute.get_db')
def test_create_role_none_access_in_accesslist(mock_get_db):
    mock_get_db.return_value = MagicMock()
    access = "I am an access, I swear !"
    with pytest.raises(TypeError, match="A role needs a list of Access to be created"):
        create_role(name="name", accesses=[access])

@patch('app.compute.compute.get_db')
def test_create_access(mock_get_db):
    mock_get_db.return_value = MagicMock()
    access = create_access(service_key="a kay")
    assert isinstance(access, Access)

@patch('app.compute.compute.get_db')
def test_create_access_too_long_key(mock_get_db):
    mock_get_db.return_value = MagicMock()
    service_key = """
..............................................................................
..............................................................................
..............................................................................
..............................................................................
"""
    with pytest.raises(ValueError, match="A service key should not be longer than 250 characters"):
        create_access(service_key=service_key)
