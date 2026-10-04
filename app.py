import logging

from handlers.auth_handlers import auth_router
from handlers.users_handlers import user_router
from handlers.teams_handlers import team_router
from handlers.task_handler import task_router
from handlers.comment_handler import comment_router
from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from utils.response import api_response

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return api_response(
        success=False,
        message=str(exc.detail),
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return api_response(
        success=False,
        message=str(exc.errors()),
        status_code=422,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception while processing %s %s", request.method, request.url.path)
    return api_response(
        success=False,
        message=str(exc),
        status_code=500,
    )

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=False,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(team_router)
app.include_router(task_router)
app.include_router(comment_router)