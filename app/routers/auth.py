from fastapi import APIRouter, HTTPException
from app.database import test_connection

router = APIRouter()


@router.get("")
async def test_database():
    """
        This API tests the connection with the database and returns a simple message.
    """
    try:
        test_connection()
        return {"Hello": "Mate"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
