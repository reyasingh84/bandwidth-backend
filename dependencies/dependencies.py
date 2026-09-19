from collections.abc import Generator

import mysql.connector
from mysql.connector import MySQLConnection
from fastapi import Depends

from config.config import Config
from repositories.user_repo import UserRepository
from services.auth_service import AuthService


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


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)
