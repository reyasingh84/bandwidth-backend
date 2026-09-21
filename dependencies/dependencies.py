from collections.abc import Generator

import mysql.connector
import jwt
from mysql.connector import MySQLConnection
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from config.config import Config
from repositories.user_repo import UserRepository
from repositories.team_repo import TeamRepository
from repositories.task_repo import TaskRepository
from repositories.comment_repo import CommentRepository
from services.team_service import TeamService
from services.user_service import UserService
from services.task_service import TaskService
from services.comment_service import CommentService
from services.auth_service import AuthService
from utils.auth import validate_token

session_token_header = APIKeyHeader(name="session_token", auto_error=False)


def get_connection() -> Generator[MySQLConnection, None, None]:
    connection = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
    )
    try:
        yield connection
    finally:
        if connection.is_connected():
            connection.close()


def get_user_repository(
    connection: MySQLConnection = Depends(get_connection),
) -> UserRepository:
    return UserRepository(connection)

def get_team_repository(
    connection: MySQLConnection = Depends(get_connection)
) -> TeamRepository:
    return TeamRepository(connection)

def get_task_repository(
    connection: MySQLConnection = Depends(get_connection)
)-> TaskRepository:
    return TaskRepository(connection)

def get_comment_repository(
    connection: MySQLConnection = Depends(get_connection)
)-> CommentRepository:
    return CommentRepository(connection)

def get_comment_service(
        comment_repo: CommentRepository = Depends(get_comment_repository),
        task_repo: TaskRepository = Depends(get_task_repository)
)-> CommentService:
    return CommentService(comment_repo, task_repo)
    
def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    team_repo: TeamRepository = Depends(get_team_repository)
)-> TaskService:
    return TaskService(task_repo, user_repo, team_repo)

def get_team_service(
        team_repo: TeamRepository = Depends(get_team_repository)
)-> TeamService:
    return TeamService(team_repo)

def get_user_service(
        user_repo: UserRepository = Depends(get_user_repository),
        team_repo: TeamRepository = Depends(get_team_repository)
)-> UserService:
    return UserService(user_repo, team_repo)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)


def require_admin(
    token: str | None = Depends(session_token_header),
) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = validate_token(token)
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if payload.get("role") not in  ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return payload


def require_director(token: str | None = Depends(session_token_header)) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = validate_token(token)
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if payload.get("role") not in  ["admin","director"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return payload

def require_manager(token: str | None = Depends(session_token_header)) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = validate_token(token)
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if payload.get("role") not in ["admin","director", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return payload

def require_employee(token: str | None = Depends(session_token_header)) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = validate_token(token)
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if payload.get("role") not in ["admin","director", "manager", "employee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return payload
