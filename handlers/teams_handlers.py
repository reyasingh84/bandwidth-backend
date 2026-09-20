from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from dependencies.dependencies import require_director, get_team_service
from services.team_service import TeamService
from models.dto import CreateTeamReqBody

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