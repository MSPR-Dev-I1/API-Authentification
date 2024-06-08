from sqlalchemy.ext.declarative import declarative_base
from .connexion import engine
from sqlalchemy import inspect, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

def setup_database():
    # Vérifiez si la base de données est vide et créez les tables si nécessaire
    inspector = inspect(engine)
    if not inspector.get_table_names():
        Base.metadata.create_all(bind=engine)
        print("Database setup completed")


class Utilisateur(Base):
    __tablename__ = "Utilisateur"
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    utilisateur_clients = relationship("Utilisateur_Client", back_populates="utilisateur", uselist=False)
    roles = relationship("Role", back_populates="utilisateur")

class Utilisateur_Client(Base):
    __tablename__ = "Utilisateur_Client"
    id_client = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey('Utilisateur.id_utilisateur'))
    utilisateur = relationship("Utilisateur", back_populates="utilisateur_clients")

association_table = Table('user_post_association', Base.metadata,
    Column('id_role', Integer, ForeignKey('Role.id_role')),
    Column('id_access', Integer, ForeignKey('Access.id_access'))
)

class Role(Base):
    __tablename__ = "Role"
    id_role = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    id_utilisateur = Column(Integer, ForeignKey('Utilisateur.id_utilisateur'))
    utilisateur = relationship("Utilisateur", back_populates="utilisateur_clients")
    accesses = relationship("Access", secondary=association_table, back_populates="roles")

class Access(Base):
    __tablename__ = "Access"
    id_access = Column(Integer, primary_key=True, index=True)
    cle_de_service = Column(String(250))
    roles = relationship("Role", secondary=association_table, back_populates="accesses")
