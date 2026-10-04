from fastapi import APIRouter, Depends
from dependencies.dependencies import get_user_service, require_admin
from services.user_service import UserService
from models.dto import CreateUserReqBody, UpdateUserReqBody, UserResponse
from errors.errors import ApplicationError
from utils.response import api_response


user_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)],
)


@user_router.get("/users", response_model=list[UserResponse])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_all_users()

    return api_response(
        success=True,
        response=[UserResponse.model_validate(user) for user in users],
    )

@user_router.post("/user")
def create_user(body: CreateUserReqBody, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.create_user(body)
        return api_response(success=True, message="successfully created user")
    
    except Exception as e:
        return api_response(
            success=False, message="failed to create user", status_code=500
        )

@user_router.get("/users/active", response_model=list[UserResponse])
def get_active_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_active_users()

    return api_response(
        success=True,
        response=[UserResponse.model_validate(user) for user in users],
    )

@user_router.delete("/user/{id}")
def delete_user(id: str, user_service: UserService = Depends(get_user_service)): 
    try:
        user_service.deactivate_user_by_id(id)
        return api_response(success=True, message="successfully deleted user")

    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as e:
        return api_response(
            success=False, message="failed to delete user", status_code=500
        )

@user_router.put("/user/update/{id}", response_model=UserResponse)
def update_user(id: str, body: UpdateUserReqBody, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.update_user(id, body)
        return api_response(success=True, message="User updated successfully")
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as e:
        return api_response(
            success=False, message="failed to update user", status_code=500
        )

@user_router.get("/user/{id}/activate")
def activate_user(id: str, user_service: UserService = Depends(get_user_service)):
    try: 
        user_service.activate_user_by_id(id)
        return api_response(success=True, message="successfully activated user")

    except ApplicationError as app_error:
            return api_response(
                success=False, message=app_error.message, status_code=app_error.code
            )
    except Exception as e:
            return api_response(
                success=False, message="failed to activate user", status_code=500
            )

    

    