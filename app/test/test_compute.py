import pytest
from sqlalchemy.orm import Session
from app.database.premier_schema import (
    Role,
    Utilisateur,
    UtilisateurClient,
    Access,
    DeactivatedToken
)
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
    create_deactivated_token,
    get_deactivated_token,
    get_deactivated_tokens
)
from app.test.inmemory_sqlite import memory_db

def set_default_entities(db:Session):
    """
        Return a set of default registered entities
    """
    access = create_access(db,"default")
    role = create_role(db,"default",[access])
    utilisateur = create_utilisateur(db,role)
    utilisateur_client = create_utilisateur_client(db,utilisateur)
    deactivated_token = create_deactivated_token(db,"default")
    return {'access':access,
            'role':role,
            'utilisateur':utilisateur,
            'client':utilisateur_client,
            'token':deactivated_token}

def test_create_utilisateur():
    """
        Testing if we can create a user
    """
    db=memory_db()
    role = Role()
    utilisateur = create_utilisateur(db,role)
    assert isinstance(utilisateur, Utilisateur)

def test_create_utilisateur_client():
    """
        Testing if we can create a client
    """
    db=memory_db()
    utilisateur = Utilisateur()
    utilisateur_client = create_utilisateur_client(db,utilisateur)
    assert isinstance(utilisateur_client, UtilisateurClient)

def test_create_role():
    """
        Testing if we can create a role
    """
    db=memory_db()
    access = Access()
    role = create_role(db,name="name", accesses=[access])
    assert isinstance(role, Role)

def test_create_role_too_long_name():
    """
        Testing if we fail when creating a role with a name too long
    """
    db=memory_db()
    access = Access()
    name = """
..............................................................................
..............................................................................
..............................................................................
..............................................................................
"""
    with pytest.raises(ValueError, match="A role name should not be longer than 100 characters"):
        create_role(db,name=name, accesses=[access])

def test_create_role_none_access_in_accesslist():
    """
        Testing if we fail when creating a role with a fake access
    """
    db=memory_db()
    access = "I am an access, I swear !"
    with pytest.raises(TypeError, match="A role needs a list of Access to be created"):
        create_role(db,name="name", accesses=[access])

def test_create_access():
    """
        Testing if we can create an access
    """
    db=memory_db()
    access = create_access(db,service_key="a kay")
    assert isinstance(access, Access)

def test_create_access_too_long_key():
    """
        Testing if we fail when creating an access with a key too long
    """
    db=memory_db()
    service_key = """
..............................................................................
..............................................................................
..............................................................................
..............................................................................
"""
    with pytest.raises(ValueError, match="A service key should not be longer than 250 characters"):
        create_access(db,service_key=service_key)

def test_update_utilisateur():
    """
        Testing if we can update an user
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    utilisateur: Utilisateur = defaut_entities['utilisateur']
    second_role = create_role(db,"new",[defaut_entities["access"]])
    utilisateur = update_utilisateur(db,utilisateur.id_utilisateur, second_role)
    assert utilisateur.role is second_role

def test_update_utilisateur_client():
    """
        Testing if we can update a client
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    utilisateur_client: UtilisateurClient = defaut_entities['client']
    second_utilisateur = create_utilisateur(db,defaut_entities['role'])
    utilisateur_client = update_utilisateur_client(db,
                                                   utilisateur_client.id_client,
                                                   second_utilisateur)
    assert utilisateur_client.utilisateur is second_utilisateur

def test_update_role_name():
    """
        Testing if we can update the name of a role
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    role: Role = defaut_entities['role']
    name = "mordues"
    role=update_role(db,role.id_role, name)
    assert role.nom == name

def test_update_role_name_too_long():
    """
        Testing if we faile to update a role with a new too long name
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    role: Role = defaut_entities['role']
    name = """
..............................................................................
..............................................................................
..............................................................................
..............................................................................
"""
    with pytest.raises(ValueError, match="A role name should not be longer than 100 characters"):
        update_role(db,role.id_role, name)

def test_update_role_access():
    """
        Testing if we can update the accesses of role
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    role: Role = defaut_entities['role']
    second_access = create_access(db,"keykey")
    role= update_role(db, role_id=role.id_role, accesses=[second_access])
    assert role.accesses[0] is second_access

def test_update_role_incorect_type_access():
    """
        Testing if we fail when updating the accesses of role with a fake access
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    role: Role = defaut_entities['role']
    second_access= "I am an access, I swear !"
    with pytest.raises(TypeError, match="A role needs a list of Access to be created"):
        update_role(db, role_id=role.id_role, accesses=[second_access])

def test_update_role_without_change():
    """
        Testing if the role does not change when updating it with no new information
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    role: Role = defaut_entities['role']
    role_two= update_role(db, role_id=role.id_role)
    assert role is role_two

def test_update_access_key():
    """
        Testing if we can update an access
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    access: Access = defaut_entities['access']
    key = "mordues"
    access=update_access(db,access.id_access, key)
    assert access.cle_de_service == key

def test_update_access_key_too_long():
    """
        Testing if we fail when updating an access with a new key too long
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    access: Access = defaut_entities['access']
    key = """
..............................................................................
..............................................................................
..............................................................................
..............................................................................
"""
    with pytest.raises(ValueError, match="A service key should not be longer than 250 characters"):
        update_access(db,access.id_access, key)

def test_delete_utilisateur():
    """
        Testing if we can delete a user
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    utilisateur:Utilisateur = defaut_entities['utilisateur']
    delete_utilisateur(db,utilisateur.id_utilisateur)
    utilisateur = get_utilisateur(db, utilisateur.id_utilisateur)
    assert utilisateur is None

def test_delete_utilisateur_client():
    """
        Testing if we can delete client
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    utilisateur_client:UtilisateurClient = defaut_entities['client']
    delete_utilisateur_client(db,utilisateur_client.id_client)
    utilisateur_client = get_utilisateur_client(db, utilisateur_client.id_client)
    assert utilisateur_client is None

def test_delete_role():
    """
        Testing if we can delete role
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    role:Role = defaut_entities['role']
    delete_role(db,role.id_role)
    role = get_role(db, role.id_role)
    assert role is None

def test_delete_access():
    """
        Testing if we can delete an access
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    access:Access = defaut_entities['access']
    delete_access(db,access.id_access)
    access = get_access(db, access.id_access)
    assert access is None

def test_create_deactivated_token():
    """
        Testing if we can create a deactivated token
    """
    db=memory_db()
    deactivated_token=create_deactivated_token(db,"token")
    assert isinstance(deactivated_token, DeactivatedToken)

def test_get_deactivated_token():
    """
        Testing if we can find a deactivated token
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    token = get_deactivated_token(db, "default")
    assert token is defaut_entities['token']

def test_get_deactivated_tokens():
    """
        Testing if we can find all the deactivated token
    """
    db=memory_db()
    defaut_entities = set_default_entities(db)
    tokens = get_deactivated_tokens(db)
    assert (len(tokens) == 1) and (tokens[0] is defaut_entities['token'])
