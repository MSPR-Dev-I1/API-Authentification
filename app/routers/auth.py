from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connexion import test_connection,get_db
from app.validation.schemas import ValidationRequest,ValidationResponse,TokenRequest,TokenResponse
from app.compute.compute import get_deactivated_tokens, get_role, get_utilisateur
from app.tokken.tokken import verify_validity, verify_access, encode_jwt
from app.database.premier_schema import Role, Utilisateur

router = APIRouter()

@router.get("")
async def hello_mate():
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

@router.post("/token", response_model=TokenResponse)
async def deploy_token(request:TokenRequest,db: Session = Depends(get_db)):
    """
        This API recieve a user id.
        It returns a new token corresponding to that user.
        Later, it will verify an identity token.
    """
    try:
        user: Utilisateur = get_utilisateur(db, request.user)
        if user is None:
            raise HTTPException(status_code=404,
                                detail="Cannot deliver any token for an user that does not exist.")
        role: Role = get_role(db, user.id_role)
        if role is None:
            raise HTTPException(status_code=404,
                                detail="Cannot deliver any token for a user without a role.")
        if len(role.accesses) == 0:
            raise HTTPException(status_code=404,
                                detail=f"Cannot deliver any token for the role {role.nom}")
        access_key_list = []
        for access in role.accesses:
            if access.cle_de_service is None:
                raise ValueError(f"There is a corrupted access in the role {role.nom}")
            access_key_list.append(access.cle_de_service)
        response = TokenResponse(token= encode_jwt(access_key_list))
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e
