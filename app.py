from handlers.auth_handlers import auth_router
from handlers.users_handlers import user_router
from handlers.teams_handlers import team_router
from handlers.task_handler import task_router
from fastapi import FastAPI 

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(team_router)
app.include_router(task_router)