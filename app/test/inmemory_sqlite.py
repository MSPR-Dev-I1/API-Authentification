from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.database.premier_schema import Base

def memory_db():
    """
        Return a sqlalchemy session connected to an in memory sqlite
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    return session
