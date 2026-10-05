from repositories.task_repo import TaskRepository
from repositories.user_repo import UserRepository
from repositories.team_repo import TeamRepository
from models.models import Task
from models.dto import CreateTaskReqBody, UpdateTaskReqBody
from models.models import User
import time
from uuid import uuid4
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

    @staticmethod
    def _normalize_task_counts(task_counts: dict) -> dict:
        normalized_counts = {
            status.value: task_counts.get(status.value, 0)
            for status in TaskStatus
        }
        normalized_counts["total"] = sum(normalized_counts.values())
        return normalized_counts

    def get_task_statistics(self, jwt_payload: dict) -> dict:
        user_role = jwt_payload.get("role")

        if user_role in ["admin", "director"]:
            task_count = self.task_repo.get_all_tasks_count()
            overdue_task_count = self.task_repo.get_all_overdue_tasks_count()
        elif user_role == "manager":
            team_id = jwt_payload.get("team_id")
            if not team_id:
                raise ApplicationError(400, "team id is required")

            task_count = self.task_repo.get_all_tasks_count_by_team(team_id)
            overdue_task_count = self.task_repo.get_overdue_tasks_count_by_team(team_id)
        elif user_role == "employee":
            assignee_id = jwt_payload.get("id")
            if not assignee_id:
                raise ApplicationError(400, "user id is required")

            task_count = self.task_repo.get_all_tasks_count_by_assignee(assignee_id)
            overdue_task_count = self.task_repo.get_overdue_tasks_count_by_assignee(
                assignee_id
            )
        else:
            raise ApplicationError(403, "invalid user role")

        return {
            "task_count": self._normalize_task_counts(task_count),
            "overdue_task_count": self._normalize_task_counts(overdue_task_count),
        }

    def get_team_task_statistics(self, jwt_payload: dict) -> dict:
        user_role = jwt_payload.get("role")

        if user_role in ["admin", "director"]:
            teams = self.team_repo.get_teams()
            overdue_counts_by_team = (
                self.task_repo.get_overdue_tasks_count_grouped_by_team()
            )
            statistics = []
            for team in teams:
                task_counts = self._normalize_task_counts(
                    self.task_repo.get_all_tasks_count_by_team(team.id)
                )
                overdue_counts = self._normalize_task_counts(
                    overdue_counts_by_team.get(team.id, {})
                )
                task_counts["team_name"] = team.name
                task_counts["team_short_name"] = team.short_name
                task_counts["team_id"] = team.id
                task_counts["overdue"] = overdue_counts["total"]
                statistics.append(task_counts)

            return statistics

        if user_role != "manager":
            raise ApplicationError(403, "only admin, director, and manager roles are allowed")

        team_id = jwt_payload.get("team_id")
        if not team_id:
            raise ApplicationError(400, "team id is required")

        team = self.team_repo.get_by_team_id(team_id)
        if not team:
            raise ApplicationError(400, "not a valid team id")

        team_task_count = self._normalize_task_counts(
            self.task_repo.get_all_tasks_count_by_team(team_id)
        )
        team_overdue_task_count = self._normalize_task_counts(
            self.task_repo.get_overdue_tasks_count_by_team(team_id)
        )
        team_task_count["team_id"] = team_id
        team_task_count["team_name"] = team.name
        team_task_count["team_short_name"] = team.short_name
        team_task_count["overdue"] = team_overdue_task_count["total"]

        return [team_task_count]


    def get_all_tasks_by_team_id(self, team_id: str):

        team = self.team_repo.get_by_team_id(team_id)
        if not team: 
            raise ApplicationError(400, "not a valid team id")
        
        tasks = self.task_repo.get_all_tasks_by_team(team_id)
        return tasks

    def get_all_tasks_by_user_id(self, jwt_payload: dict):
        user_id = jwt_payload.get("id")
        users = self.user_repo.get_users()
        users = self.user_repo.get_user_by_id(user_id)
        user_ids = [user.id for user in users]

        if user_id not in user_ids:
            raise ApplicationError(400, "not a valid user id")

        tasks = self.task_repo.get_all_tasks_by_assignee(user_id)
        
        return tasks

    def get_all_tasks_from_reporter_id(self, reporter_id: str):
        reporters = self.user_repo.get_users()
        reporter_ids = [reporter_id for reporter in reporters]

        if reporter_id not in reporter_ids:
            raise ApplicationError(400, "not a valid reporter id")


        tasks  =  self.task_repo.get_all_tasks_by_reporter(reporter_id)
        return tasks

    def update_task(self, task_id: str, body: UpdateTaskReqBody, jwt_payload: dict):
        task = self.task_repo.get_task_by_id(task_id)
        current_time = int(time.time())
        user_id = jwt_payload.get("id")
        user_role = jwt_payload.get("role")
        user_team_id = jwt_payload.get("team_id")

        if not task:
            raise ApplicationError(404, "invalid task id")

        can_update_all_fields = task.reporter_id == user_id
        if user_role in ["admin", "director"]:
            can_update_status_or_assignee = True
        elif user_role == "manager":
            can_update_status_or_assignee = task.team_id == user_team_id
        elif user_role == "employee":
            can_update_status_or_assignee = (
                task.assignee_id == user_id and body.status is not None
            )
        else:
            can_update_status_or_assignee = False

        if not can_update_all_fields and not can_update_status_or_assignee:
            raise ApplicationError(403, "you do not have permission to update this task")

        if user_role == "employee":
            restricted_fields = (
                body.title,
                body.description,
                body.acpt_criteria,
                body.category,
                body.assignee_id,
                body.assignee_username,
                body.priority,
                body.proj_name,
                body.deadline,
            )
            if any(value is not None for value in restricted_fields):
                raise ApplicationError(
                    403, "employees can only update the status of assigned tasks"
                )
            if task.assignee_id != user_id or body.status is None:
                raise ApplicationError(
                    403, "employees can only update the status of assigned tasks"
                )

        if not can_update_all_fields:
            restricted_fields = (
                body.title,
                body.description,
                body.acpt_criteria,
                body.category,
                body.priority,
                body.proj_name,
                body.deadline,
            )
            if any(value is not None for value in restricted_fields):
                raise ApplicationError(
                    403, "you can only update task status or assignee"
                )

        if body.deadline is not None and body.deadline < current_time:
            raise ApplicationError(400, "deadline cannot be in past")


        if body.title is not None:
            task.title = body.title
        if body.description is not None:
            task.description = body.description
        if body.acpt_criteria is not None:
            task.acpt_criteria = body.acpt_criteria
        if body.category is not None:
            task.category = body.category
        if body.status is not None:
            task.status = body.status
        if body.assignee_id is not None:
            task.assignee_id = body.assignee_id
        if body.assignee_username is not None:
            task.assignee_username = body.assignee_username
        if body.priority is not None:
            task.priority  = body.priority
        if body.proj_name is not None:
            task.proj_name = body.proj_name
        if body.deadline is not None:
            task.deadline =  body.deadline


        task.updated_at = int(time.time())

        self.task_repo.update_task(task)
        return task

    