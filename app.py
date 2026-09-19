# starting development

# import mysql
# from repositories.user_repo import UserRepository
# from config.config import Config

# conn = mysql.connector.connect(
#     host=Config.DB_HOST,
#     user=Config.DB_USER,
#     password=Config.DB_PASSWORD,
#     database=Config.DB_NAME,
# )

from handlers.auth_handlers import auth_router
from fastapi import FastAPI 

app = FastAPI()

app.include_router(auth_router)