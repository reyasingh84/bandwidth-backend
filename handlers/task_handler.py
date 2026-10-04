from fastapi import APIRouter, Depends
from models.dto import CreateTaskReqBody, UpdateTaskReqBody
from dependencies.dependencies import get_task_service, require_manager, require_director, require_employee
from services.task_service import TaskService
from errors.errors import ApplicationError
from utils.response import api_response


task_router = APIRouter()

@task_router.post("/tasks/create")
def create_task(body: CreateTaskReqBody, jwt_payload = Depends(require_manager), task_service: TaskService= Depends(get_task_service)):
    try:
        task_service.create_task(jwt_payload, body)
        return api_response(
            success=True,
            message="created task successfully please check team's board",
        )
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as e: 
        return api_response(
            success=False, message="Unexpected Error Occured", status_code=500
        )

@task_router.get("/tasks/all")
def get_all_tasks(jwt_payload = Depends(require_employee), task_service: TaskService= Depends(get_task_service)):
    tasks = task_service.get_all_tasks(jwt_payload)

    return api_response(success=True, response=tasks)

@task_router.get("/tasks/team/{team_id}")
def get_all_task_by_team(team_id: str, jwt_payload = Depends(require_director), task_service: TaskService= Depends(get_task_service)):
    tasks = task_service.get_all_tasks_by_team_id(team_id)

    return api_response(success=True, response=tasks)

@task_router.get("/tasks/assignee")
def get_all_task_by_assignee(jwt_payload = Depends(require_employee), task_service: TaskService= Depends(get_task_service)):
    tasks = task_service.get_all_tasks_by_user_id(jwt_payload)

    return api_response(success=True, response=tasks)

@task_router.put("/task/update/{id}")
def update_task(id:str, body:UpdateTaskReqBody , jwt_payload: dict = Depends(require_manager), task_service: TaskService= Depends(get_task_service)):
    try:
        task_service.update_task(id, body, jwt_payload)
        return api_response(success=True, message="Task updated successfully")
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as e: 
        return api_response(
            success=False, message="Unexpected Error Occured", status_code=500
        )
