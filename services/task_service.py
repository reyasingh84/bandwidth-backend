from repositories.task_repo import TaskRepository
from repositories.user_repo import UserRepository
from repositories.team_repo import TeamRepository
from models.models import Task
from models.dto import CreateTaskReqBody
from models.models import User
import time
from uuid import uuid4
import uuid
from errors.errors import ApplicationError
from models.enums import TaskStatus


class TaskService():
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository, team_repo: TeamRepository):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.team_repo = team_repo

    def create_task(self, jwt_payload: dict, body: CreateTaskReqBody):
        reporter_id = jwt_payload.get("id")
        reporter_username = jwt_payload.get("username")
        reporter_team_id = jwt_payload.get("team_id")
        reporter_role = jwt_payload.get("role")
        task_team_id = None
        current_time = int(time.time())

        if body.deadline < current_time:
            raise ApplicationError(400, "deadline cannot be in past")

        if reporter_role == "manager":
            task_team_id = reporter_team_id
        else: 
            task_team_id = body.team_id

        if not task_team_id: 
            raise ApplicationError(400, "team id for task is required and couldn't be inferred.")
        task = Task(
                    id=str(uuid4()), 
                    team_id=task_team_id,
                    title=body.title,
                    description=body.description,
                    acpt_criteria=body.acpt_criteria,
                    category=body.category,
                    status= TaskStatus.OPEN,
                    reporter_id=reporter_id,
                    reporter_username=reporter_username,
                    assignee_id= body.assignee_id,
                    assignee_username=body.assignee_username,
                    priority=body.priority,
                    proj_name=body.proj_name,
                    history="", 
                    deadline=body.deadline,
                    created_at=current_time,
                    updated_at=current_time
                )
        
        if body.assignee_id and body.assignee_username:
            assignee: User = self.user_repo.get_user_by_id(body.assignee_id)
            if not assignee: 
                raise ApplicationError(400, "assignee doesn't exists")
            if assignee.username != body.assignee_username:
                raise ApplicationError(400, "assignee username doesn't match")
            if assignee.team_id != task.team_id:
                raise ApplicationError(400, "assignee team doesn't match doesn't match")
            


        self.task_repo.add_task(task)


    def get_all_tasks(self, jwt_payload : dict)-> list[Task]:
        user_team_id = jwt_payload.get("team_id")
        user_role = jwt_payload.get("role")
        user_id = jwt_payload.get("id")
        tasks = []

        if user_role == "employee":
            tasks = self.task_repo.get_all_tasks_by_assignee(user_id)
        elif user_role == "manager":
            tasks =self.task_repo.get_all_tasks_by_team(user_team_id)
        elif user_role in ["director", "admin"]:
            tasks = self.task_repo.get_all_tasks()

        return tasks


    def get_all_tasks_by_team_id(self, team_id: str):

        teams = self.team_repo.get_teams()
        team_ids = [team.id for team in teams]

        if team_id not in team_ids:
            raise ApplicationError(400, "not a valid team id")
        
        tasks = self.task_repo.get_all_tasks_by_team(team_id)
        return tasks

    def get_all_tasks_by_user_id(self, user_id: str):
        tasks = self.task_repo.get_all_tasks_by_assignee(user_id)
        return tasks

    def get_all_tasks_from_reporter_id(self, reporter_id: str):
        pass