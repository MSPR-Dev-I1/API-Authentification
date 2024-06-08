from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connexion import test_connection,get_db

router = APIRouter()


@router.get("")
async def hello_mate(db: Session = Depends(get_db)):
    """
        This API tests the connection with the database and returns a simple message.
    """
    try:
        test_connection()
        return {"Hello": "Mate"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
