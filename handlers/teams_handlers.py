from fastapi import APIRouter, Depends
from dependencies.dependencies import require_director, require_employee, get_team_service
from services.team_service import TeamService
from models.dto import CreateTeamReqBody, UpdateTeamReqBody
from errors.errors import ApplicationError
from utils.response import api_response

team_router = APIRouter(
    prefix="/teams",
)


@team_router.get("")
def get_all_teams(
    jwt_payload: dict = Depends(require_director),
    team_service: TeamService = Depends(get_team_service),
):
    teams = team_service.get_all_teams()

    return api_response(success=True, response=teams)

@team_router.post("/team")
def create_team(
    body: CreateTeamReqBody,
    jwt_payload: dict = Depends(require_director),
    team_service: TeamService = Depends(get_team_service),
):
    try: 
        team_service.create_team(body)
        return api_response(success=True, message="Team created successfully")
    except Exception as e:
        return api_response(
            success=False, message="failed to create team", status_code=500
        )

@team_router.put("/update/{id}")
def update_team(
    id: str,
    body: UpdateTeamReqBody,
    jwt_payload: dict = Depends(require_director),
    team_service: TeamService = Depends(get_team_service),
):
    try:
        team_service.update_team(id, body)
        return api_response(success=True, message="Team updated successfully")
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception as e:
        return api_response(
            success=False, message="unexcepted error occur", status_code=400
        )


@team_router.get("/{team_id}")
def get_team_by_id(
    team_id: str,
    jwt_payload: dict = Depends(require_employee),
    team_service: TeamService = Depends(get_team_service),
):
    try:
        team = team_service.get_team_by_id(team_id)
        return api_response(success=True, response=team)
    except ApplicationError as app_error:
        return api_response(
            success=False, message=app_error.message, status_code=app_error.code
        )
    except Exception:
        return api_response(
            success=False, message="failed to fetch team", status_code=500
        )