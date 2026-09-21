from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from dependencies.dependencies import require_director, get_team_service
from services.team_service import TeamService
from models.dto import CreateTeamReqBody, UpdateTeamReqBody
from errors.errors import ApplicationError

team_router = APIRouter(
    prefix = "/teams",
    dependencies=[Depends(require_director)]
)


@team_router.get("")
def get_all_teams(team_service: TeamService = Depends(get_team_service)):
    teams = team_service.get_all_teams()

    return teams

@team_router.post("/team")
def create_team(body: CreateTeamReqBody, team_service: TeamService = Depends(get_team_service)):
    try: 
        team_service.create_team(body)
        return JSONResponse({
            "message" : "Team created successfully"
        }, 200)
    except Exception as e:
        return JSONResponse({
            "message" : "failed to create team",
            "error" : str(e)
        }, 500)

@team_router.put("/update/{id}")
def update_team(id:str, body: UpdateTeamReqBody, team_service: TeamService = Depends(get_team_service)):
    try:
        team_service.update_team(id, body)
        return JSONResponse({"message": "Team updated successfully"}, 200)
    except ApplicationError as app_error:
        return JSONResponse({"message" : app_error.message}, app_error.code)
    except Exception as e:
        return JSONResponse({
            "message" : "unexcepted error occur",
            "error" : str(e)
        }, 400)