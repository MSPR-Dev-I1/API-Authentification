from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database.premier_schema import Utilisateur, UtilisateurClient, Role, Access
from app.database.connexion import get_db

# Tooling functions
def create(entity):
    db = get_db()
    db.add(entity)
    db.commit()
    db.refresh(entity)
    db.close()
    return entity

def get_entity_by_key(entity_class, pk_value):
    db = get_db()
    inspector = inspect(db.bind)
    table_name = entity_class.__tablename__
    key_columns = inspector.get_pk_constraint(table_name)['constrained_columns'][0]
    if len(key_columns)> 1:
        raise ValueError("""The function get_entity_by_key cannot 
find an entity intance when the model has multiple primary keys""")
    entity = db.query(entity_class).filter_by(**{key_columns[0]: pk_value}).one_or_none()
    db.close()
    return entity

# Create functions
def create_utilisateur(role:Role):
    utilisateur = Utilisateur(role=role)
    return create(utilisateur)

def create_utilisateur_client(utilisateur: Utilisateur):
    utilisateur_client = UtilisateurClient(utilisateur=utilisateur)
    return create(utilisateur_client)

def create_role(name:str,accesses:list):
    if not all(isinstance(obj, (Access)) for obj in accesses):
        raise TypeError("A role needs a list of Access to be created")
    if len(name)>100:
        raise ValueError("A role name should not be longer than 100 characters")
    role = Role(nom=name,accesses=accesses)
    return create(role)

def create_access(service_key: str):
    if len(service_key)>250:
        raise ValueError("A service key should not be longer than 250 characters")
    access = Access(cle_de_service=service_key)
    return create(access)

# Read functions
def get_utilisateur(utilisateur_id: int):
    return get_entity_by_key(Utilisateur,utilisateur_id)

def get_utilisateur_client(utilisateur_client_id: int):
    return get_entity_by_key(UtilisateurClient,utilisateur_client_id)

def get_role(role_id: int):
    return get_entity_by_key(Role,role_id)

def get_access(access_id: int):
    return get_entity_by_key(Access,access_id)

# Update functions
def update_utilisateur(utilisateur_id: int, role: Role):
    utilisateur: Utilisateur = get_utilisateur(utilisateur_id)
    db = get_db()
    utilisateur.role=role
    db.commit()
    db.refresh(utilisateur)
    db.close()
    return utilisateur

def update_utilisateur_client(utilisateur_client_id: int, utilisateur: Utilisateur):
    utilisateur_client: UtilisateurClient = get_utilisateur_client(utilisateur_client_id)
    db = get_db()
    utilisateur_client.utilisateur=utilisateur
    db.commit()
    db.refresh(utilisateur)
    db.close()
    return utilisateur_client

def update_role(role_id: int, name:str=None, accesses:list = None):
    role:Role = get_role(role_id)
    db = get_db()
    if name is not None:
        if len(name)>100:
            raise ValueError("A role name should not be longer than 100 characters")
        role.nom = name
    if accesses is not None:
        if not all(isinstance(obj, (Access)) for obj in accesses):
            raise TypeError("A role needs a list of Access to be created")
        role.accesses = accesses
    db.commit()
    db.refresh(role)
    db.close()
    return role

def update_access(access_id: int, service_key: str):
    if len(service_key)>250:
        raise ValueError("A service key should not be longer than 250 characters")
    access:Access = get_access(access_id)
    db = get_db()
    access.cle_de_service=service_key
    db.commit()
    db.refresh(access)
    return access

# Delete functions
def delete_utilisateur(utilisateur_id: int):
    utilisateur: Utilisateur = get_utilisateur(utilisateur_id)
    db = get_db()
    db.delete(utilisateur)
    db.commit()
    return utilisateur

def delete_utilisateur_client(utilisateur_client_id: int):
    utilisateur_client: UtilisateurClient = get_utilisateur_client(utilisateur_client_id)
    db = get_db()
    db.delete(utilisateur_client)
    db.commit()
    return utilisateur_client

def delete_role(role_id: int):
    role:Role = get_role(role_id)
    db = get_db()
    db.delete(role)
    db.commit()
    return role

def delete_access(access_id: int):
    access:Access = get_access(access_id)
    db = get_db()
    db.delete(access)
    db.commit()
    return access
