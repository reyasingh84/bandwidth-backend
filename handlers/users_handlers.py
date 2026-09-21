from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies.dependencies import get_user_service, require_admin
from services.user_service import UserService
from models.dto import CreateUserReqBody, UpdateUserReqBody, UserResponse
from errors.errors import ApplicationError


user_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)],
)


@user_router.get("/users", response_model=list[UserResponse])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_all_users()

    return users

@user_router.post("/user")
def create_user(body: CreateUserReqBody, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.create_user(body)
        return JSONResponse({
                "message": "successfully created user"
            }, 200)
    
    except Exception as e:
        return JSONResponse({
            "message": "failed to create user",
            "error": str(e)
        }, 500)

@user_router.get("/users/active", response_model=list[UserResponse])
def get_active_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_active_users()

    return users

@user_router.delete("/user/{id}")
def delete_user(id: str, user_service: UserService = Depends(get_user_service)): 
    try:
        user_service.deactivate_user_by_id(id)
        return JSONResponse({
                "message": "successfully deleted user"
            }, 200)

    except ApplicationError as app_error:
        return JSONResponse(
            {"message": app_error.message},
            app_error.code
        )
    except Exception as e:
        return JSONResponse({
            "message": "failed to delete user",
            "error": str(e)
        }, 500)

@user_router.put("/user/update/{id}", response_model=UserResponse)
def update_user(id: str, body: UpdateUserReqBody, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.update_user(id, body)
        return JSONResponse({"message" : "User updated successfully"}, 200)
    except ApplicationError as app_error:
        return JSONResponse({"message": app_error.message}, app_error.code)
    except Exception as e:
        return JSONResponse({
            "message": "failed to update user",
            "error": str(e)
        }, 500)

@user_router.get("/user/{id}/activate")
def activate_user(id: str, user_service: UserService = Depends(get_user_service)):
    try: 
        user_service.activate_user_by_id(id)
        return JSONResponse({
                "message": "successfully activated user"
            }, 200)

    except ApplicationError as app_error:
            return JSONResponse(
                {"message": app_error.message},
                app_error.code
            )
    except Exception as e:
            return JSONResponse({
                "message": "failed to activate user",
                "error": str(e)
            }, 500)

    

    