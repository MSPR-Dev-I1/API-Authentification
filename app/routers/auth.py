from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connexion import test_connection,get_db
from app.validation.schemas import ValidationRequest,ValidationResponse
from app.compute.compute import get_deactivated_tokens
from app.tokken.tokken import verify_validity, verify_access

router = APIRouter()

# pylint: disable=unused-argument
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

@router.post("/validation_token", response_model=ValidationResponse)
async def validation_token(request: ValidationRequest,db: Session = Depends(get_db)):
    """
        This API recieve a token and a service key.
        It validate if the token authorize that service key.
        It returns the boolean result of the validation.
    """
    try:
        deactivated_tokens = get_deactivated_tokens(db)
        is_valid = verify_validity(request.token,deactivated_tokens)
        is_correct_access = verify_access(request.service_key,request.token)
        response = ValidationResponse(validation= is_valid and is_correct_access)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e
