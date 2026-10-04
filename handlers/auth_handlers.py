from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.dependencies import get_auth_service
from services.auth_service import AuthService
from models.dto import LoginReqBody, UserResponse
from utils.response import api_response

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login")
def login(
    body: LoginReqBody,
    auth_service: AuthService = Depends(get_auth_service),
):
    result = auth_service.login_with_user(body.email, body.password)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token, user = result
    return api_response(
        success=True,
        response={
            "access_token": token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user).model_dump(
                mode="json",
                exclude={"is_active", "created_at", "updated_at"},
            ),
        },
    )
    
