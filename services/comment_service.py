from repositories.comment_repo import CommentRepository
from repositories.task_repo import TaskRepository
from models.dto import CreateCommentReqBody, UpdateCommentReqBody
from models.models import Comment
from errors.errors import ApplicationError
from uuid import uuid4
import time

class CommentService():
    def __init__(self, comment_repo: CommentRepository, task_repo: TaskRepository):
        self.comment_repo = comment_repo
        self.task_repo  = task_repo

    def create_comment(self,jwt_payload : dict, body:CreateCommentReqBody):
        author_id = jwt_payload.get("id")
        author_username = jwt_payload.get("username")
        user_team_id = jwt_payload.get("team_id")
        role = jwt_payload.get("role")
        task_id = body.task_id


        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            raise ApplicationError(400, "not a valid task id that you entered!")

        if role in ["admin", "director"]:
            pass
        elif role in ["manager", "employee"]:
            if user_team_id != task.team_id:
                raise ApplicationError(403, "you donot have permission to perform this action")

        if not task_id: 
            raise ApplicationError(400, "task id is required.")
        
        current_time = int(time.time())
        comment = Comment(
            id = str(uuid4()),
            message= body.message,
            author_id= author_id,
            author_username= author_username,
            task_id=body.task_id,
            created_at= current_time,
            updated_at= current_time
        )

        self.comment_repo.add_comment(comment)

    def get_comments_by_task_id(self, task_id:str):

        comments = self.comment_repo.get_comments_by_task_id(task_id)
        return comments

    def update_comment(self, comment_id: str, body: UpdateCommentReqBody, jwt_payload: dict):
        user_id = jwt_payload.get("id")
        comment = self.comment_repo.get_comment_by_id(comment_id)

        if not comment:
            raise ApplicationError(404, "comment not found")

        if user_id != comment.author_id:
            raise ApplicationError(403, "you donot have permission to perform this action")

        comment.message = body.message
        comment.updated_at = int(time.time())
        self.comment_repo.update_comment(comment.id, comment.message)






