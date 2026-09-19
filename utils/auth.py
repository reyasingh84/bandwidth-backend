import jwt
import time
import bcrypt
from models.models import User

from config.config import Config

def str_to_bytes(string: str):
    return string.encode("utf-8")

def issue_token(user:User)-> str:

    current_time = int(time.time())

    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role, 
        "team_id": user.team_id,
        "iat": current_time,
        "exp": current_time +int(Config.JWT_EXP_HRS*(60*60))
    }


    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    return token

def validate_token(token: str) -> dict: 

    payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])

    return payload



def generate_hash(password: str) -> str:
    password_encoded = str_to_bytes(password)

    hashed_password = bcrypt.hashpw(password_encoded, bcrypt.gensalt())

    return hashed_password.decode("utf-8")


def validate_password_and_hash(password: str, pwd_hash: str)-> bool:

    is_valid = bcrypt.checkpw(str_to_bytes(password), str_to_bytes(pwd_hash))

    return is_valid