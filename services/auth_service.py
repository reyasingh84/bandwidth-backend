from repositories.user_repo import UserRepository
from utils.auth import validate_password_and_hash, issue_token
from models.dto import LoginReqBody

class AuthService: 
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user: 
            return None

        is_valid_pwd = validate_password_and_hash(password, user.password)

        if not is_valid_pwd:
            return None

        token = issue_token(user)

        return token


        
