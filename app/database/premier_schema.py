from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .connexion import engine

Base = declarative_base()

def setup_database():
    """
        Setup the database if it is empty
    """
    inspector = inspect(engine)
    if not inspector.get_table_names():
        Base.metadata.create_all(bind=engine)
        print("Database setup completed")


# pylint: disable=too-few-public-methods
class Utilisateur(Base):
    """
        Entity for the users
    """
    __tablename__ = "Utilisateur"
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    utilisateur_clients = relationship("Utilisateur_Client",
                                       back_populates="utilisateur",
                                       uselist=False)
    roles = relationship("Role", back_populates="utilisateur")


# pylint: disable=too-few-public-methods
class UtilisateurClient(Base):
    """
        Entity for the users that are clients
    """
    __tablename__ = "Utilisateur_Client"
    id_client = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey('Utilisateur.id_utilisateur'))
    utilisateur = relationship("Utilisateur", back_populates="utilisateur_clients")

association_table = Table('user_post_association', Base.metadata,
    Column('id_role', Integer, ForeignKey('Role.id_role')),
    Column('id_access', Integer, ForeignKey('Access.id_access'))
)


# pylint: disable=too-few-public-methods
class Role(Base):
    """
        Entity for the user's roles
    """
    __tablename__ = "Role"
    id_role = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    id_utilisateur = Column(Integer, ForeignKey('Utilisateur.id_utilisateur'))
    utilisateur = relationship("Utilisateur", back_populates="utilisateur_clients")
    accesses = relationship("Access", secondary=association_table, back_populates="roles")


# pylint: disable=too-few-public-methods
class Access(Base):
    """
        Entity for the accessable apis
    """
    __tablename__ = "Access"
    id_access = Column(Integer, primary_key=True, index=True)
    cle_de_service = Column(String(250))
    roles = relationship("Role", secondary=association_table, back_populates="accesses")
