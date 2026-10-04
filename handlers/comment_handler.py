from fastapi import APIRouter, Depends
from models.dto import CreateCommentReqBody, UpdateCommentReqBody
from services.comment_service import CommentService
from errors.errors import ApplicationError
from dependencies.dependencies import require_employee, get_comment_repository, get_comment_service
from utils.response import api_response



comment_router = APIRouter()

@comment_router.post("/comment/create")
def create_comment(
      body: CreateCommentReqBody,
      jwt_payload: dict = Depends(require_employee),
      comment_service: CommentService = Depends(get_comment_service),
):
      try:
            comment_service.create_comment(jwt_payload, body)
            return api_response(success=True, message="comment added successfully...")
      except ApplicationError as app_error:
            return api_response(
                success=False, message=app_error.message, status_code=app_error.code
            )
      except Exception as error:
            return api_response(
                  success=False, message="unable to add comment", status_code=500
            )

@comment_router.get("/{task_id}/comments")
def get_all_comments(task_id: str, jwt_payload: dict = Depends(require_employee), comment_service: CommentService = Depends(get_comment_service)):

    try: 
        comments = comment_service.get_comments_by_task_id(task_id)
        return api_response(success=True, response=comments)
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as error:
        return api_response(
                success=False, message="unable to update comment", status_code=500
        )

@comment_router.put("/comment/update/{id}")
def update_comment(id: str, body: UpdateCommentReqBody, jwt_payload:dict = Depends(require_employee), comment_service: CommentService = Depends(get_comment_service)):
    try: 
            comment_service.update_comment(id, body, jwt_payload)
            return api_response(success=True, message="comment updated successfully...")
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as error:
        return api_response(
                success=False, message="unable to update comment", status_code=500
        )
    
