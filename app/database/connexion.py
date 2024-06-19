import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

database_host = os.getenv("DATABASE_HOST")
database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')

database_url = f"mysql+pymysql://{database_username}:" \
    f"{database_password}@{database_host}/paye-ton-kawa-Auth"

engine = sqlalchemy.create_engine(database_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
        Créer et retourne une instance la connexion à la base de donnée
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """
        Test la connexion.
        Provoque une exception si l'api n'arrive pas à se connecter à la base de données
    """
    conn = engine.connect()
    conn.close()
