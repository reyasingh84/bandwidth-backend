from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.dto import CreateCommentReqBody, UpdateCommentReqBody
from services.comment_service import CommentService
from errors.errors import ApplicationError
from dependencies.dependencies import require_employee, get_comment_repository, get_comment_service



comment_router = APIRouter()

@comment_router.post("/comment/create")
def create_comment(
      body: CreateCommentReqBody,
      jwt_payload: dict = Depends(require_employee),
      comment_service: CommentService = Depends(get_comment_service),
):
      try:
            comment_service.create_comment(jwt_payload, body)
            return JSONResponse({"message": "comment added successfully..."}, 200)
      except ApplicationError as app_error:
            return JSONResponse({"message": app_error.message}, status_code=app_error.code)
      except Exception as error:
            return JSONResponse(
                  {"message": "unable to add comment", "error": str(error)},
                  status_code=500,
            )

@comment_router.get("/{task_id}/comments")
def get_all_comments(task_id: str, jwt_payload: dict = Depends(require_employee), comment_service: CommentService = Depends(get_comment_service)):

    try: 
        comments = comment_service.get_comments_by_task_id(task_id)
        return comments
    except ApplicationError as app_error:
        return JSONResponse({"message": app_error.message}, status_code=app_error.code)
    except Exception as error:
        return JSONResponse(
                {"message": "unable to update comment", "error": str(error)},
                status_code=500,
        )

@comment_router.put("/comment/update/{id}")
def update_comment(id: str, body: UpdateCommentReqBody, jwt_payload:dict = Depends(require_employee), comment_service: CommentService = Depends(get_comment_service)):
    try: 
            comment_service.update_comment(id, body, jwt_payload)
            return JSONResponse({"message": "comment updated successfully..."}, 200)
    except ApplicationError as app_error:
        return JSONResponse({"message": app_error.message}, status_code=app_error.code)
    except Exception as error:
        return JSONResponse(
                {"message": "unable to update comment", "error": str(error)},
                status_code=500,
        )
    

