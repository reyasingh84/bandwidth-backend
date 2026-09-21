from uuid import uuid4
from repositories.user_repo import UserRepository
from models.dto import CreateUserReqBody, UpdateUserReqBody
from models.models import User
from utils.auth import generate_hash
from repositories.team_repo import TeamRepository
from errors.errors import ApplicationError
import time

class UserService:
    def __init__(self, user_repo: UserRepository, team_repo:TeamRepository ):
        self.user_repo = user_repo
        self.team_repo = team_repo


    def create_user(self, body: CreateUserReqBody):
        current_time = int(time.time())
        user = User(
            id = str(uuid4()),
            first_name=body.first_name,
            last_name=body.last_name,
            email= body.email,
            username= body.username, 
            password= generate_hash(body.password),
            phone= body.phone, 
            role= body.role,
            team_id= body.team_id, 
            department= body.department,
            designation= body.designation,
            is_active=True,
            created_at=current_time,
            updated_at=current_time
        )

        team = self.team_repo.get_by_team_id(body.team_id)

        if not team: 
            raise ApplicationError("400", "Not a valid team id")


        self.user_repo.add_user(user)

    def get_all_users(self):
        users = self.user_repo.get_users()

        return users

    def get_active_users(self):
            users = self.user_repo.get_active_users()
            return users

    def get_user_by_email(self, email: str):
        user = self.user_repo.get_by_email(email=email)


        if not user: 
            return None

        return user

    def deactivate_user_by_id(self, user_id: str):

        user = self.user_repo.get_user_by_id(user_id)
        if not user: 
            raise ApplicationError(404, "user not found")
        self.user_repo.delete_user(user_id)

    def activate_user_by_id(self, user_id: str):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ApplicationError(404, "user not found")
        self.user_repo.retrieve_user(user_id)


    def get_user_by_id(self, user_id:str) -> User:
        user = self.user_repo.get_user_by_id(user_id)

        if not user: 
            return None

        return user

    def update_user(self, user_id: str, body: UpdateUserReqBody) -> User:
        user= self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ApplicationError(404, "user not found")

        if body.email is not None:
            user.email = body.email
        if body.password is not None:
            user.password = generate_hash(body.password)
        if body.role is not None:
            user.role = body.role
        if body.designation is not None:
            user.designation = body.designation

        user.updated_at = int(time.time())
        self.user_repo.update_user(user)
        return user

        