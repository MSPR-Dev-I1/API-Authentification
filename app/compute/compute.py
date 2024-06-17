from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database.premier_schema import (
    Utilisateur, UtilisateurClient, Role,
    Access, DeactivatedToken
)

# Tooling functions
def create(db:Session,entity):
    """
        Create an entity in the session and database
    """
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity

def get_entity_by_key(db:Session,entity_class, pk_value):
    """
        Find an entity with a single primary key
        Return None if no entity is found
    """
    inspector = inspect(db.bind)
    table_name = entity_class.__tablename__
    key_columns = inspector.get_pk_constraint(table_name)['constrained_columns']
    if len(key_columns)> 1:
        raise ValueError("""The function get_entity_by_key cannot
find an entity intance when the model has multiple primary keys""")
    entity = db.query(entity_class).filter_by(**{key_columns[0]: pk_value}).one_or_none()
    return entity

# Create functions
def create_utilisateur(db:Session,role:Role):
    """
        Create an user
    """
    utilisateur = Utilisateur(role=role)
    return create(db,utilisateur)

def create_utilisateur_client(db:Session,utilisateur: Utilisateur):
    """
        Create a client
    """
    utilisateur_client = UtilisateurClient(utilisateur=utilisateur)
    return create(db,utilisateur_client)

def create_role(db:Session,name:str,accesses:list):
    """
        Create a role
    """
    if not all(isinstance(obj, (Access)) for obj in accesses):
        raise TypeError("A role needs a list of Access to be created")
    if len(name)>100:
        raise ValueError("A role name should not be longer than 100 characters")
    role = Role(nom=name,accesses=accesses)
    return create(db,role)

def create_access(db:Session,service_key: str):
    """
        Create an access
    """
    if len(service_key)>250:
        raise ValueError("A service key should not be longer than 250 characters")
    access = Access(cle_de_service=service_key)
    return create(db,access)

def create_deactivated_token(db:Session,token: str):
    """
        Create an access
    """
    if len(token)>250:
        raise ValueError("A service key should not be longer than 250 characters")
    previous_deactivated_token = get_deactivated_token(db,token)
    if previous_deactivated_token is not None:
        return previous_deactivated_token
    deactivated_token = DeactivatedToken(token=token)
    return create(db,deactivated_token)

# Read functions
def get_utilisateur(db:Session,utilisateur_id: int):
    """
        Find an user with its id
    """
    return get_entity_by_key(db,Utilisateur,utilisateur_id)

def get_utilisateur_client(db:Session,utilisateur_client_id: int):
    """
       Find a client with its id 
    """
    return get_entity_by_key(db,UtilisateurClient,utilisateur_client_id)

def get_role(db:Session,role_id: int):
    """
        Find a role with its id
    """
    return get_entity_by_key(db,Role,role_id)

def get_access(db:Session,access_id: int):
    """
        Find an access with its id
    """
    return get_entity_by_key(db,Access,access_id)

def get_deactivated_token(db:Session,token: str):
    """
        Find a deactivated token instance with its token
    """
    return get_entity_by_key(db,DeactivatedToken,token)

def get_deactivated_tokens(db:Session):
    """
        Find the deactivated tokens
    """
    return db.query(DeactivatedToken).all()

# Update functions
def update_utilisateur(db:Session,utilisateur_id: int, role: Role):
    """
        Update an user
    """
    utilisateur: Utilisateur = get_utilisateur(db,utilisateur_id)
    utilisateur.role=role
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

def update_utilisateur_client(db:Session,utilisateur_client_id: int, utilisateur: Utilisateur):
    """
        Update a client
    """
    utilisateur_client: UtilisateurClient = get_utilisateur_client(db,utilisateur_client_id)
    utilisateur_client.utilisateur=utilisateur
    db.commit()
    db.refresh(utilisateur)
    return utilisateur_client

def update_role(db:Session,role_id: int, name:str=None, accesses:list = None):
    """
       Update a role 
    """
    role:Role = get_role(db,role_id)
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
    return role

def update_access(db:Session,access_id: int, service_key: str):
    """
        Update an access
    """
    if len(service_key)>250:
        raise ValueError("A service key should not be longer than 250 characters")
    access:Access = get_access(db,access_id)
    access.cle_de_service=service_key
    db.commit()
    db.refresh(access)
    return access

# Delete functions
def delete_utilisateur(db:Session,utilisateur_id: int):
    """
        Delete an user
    """
    utilisateur: Utilisateur = get_utilisateur(db,utilisateur_id)
    db.delete(utilisateur)
    db.commit()
    return utilisateur

def delete_utilisateur_client(db:Session,utilisateur_client_id: int):
    """
        Delete a client
    """
    utilisateur_client: UtilisateurClient = get_utilisateur_client(db,utilisateur_client_id)
    db.delete(utilisateur_client)
    db.commit()
    return utilisateur_client

def delete_role(db:Session,role_id: int):
    """
        Delete a role
    """
    role:Role = get_role(db,role_id)
    db.delete(role)
    db.commit()
    return role

def delete_access(db:Session,access_id: int):
    """
       Delete an access 
    """
    access:Access = get_access(db,access_id)
    db.delete(access)
    db.commit()
    return access
