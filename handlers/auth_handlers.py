from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.dependencies import get_auth_service
from models.dto import LoginReqBody
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login")
def login(
    body: LoginReqBody,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = auth_service.login(body.email, body.password)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {"access_token": token, "token_type": "bearer"}
    

