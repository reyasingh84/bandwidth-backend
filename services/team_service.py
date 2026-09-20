from repositories.team_repo import TeamRepository
from models.models import Team
from models.dto import CreateTeamReqBody
import time
from uuid import uuid4

class TeamService:
    def __init__(self, team_repo: TeamRepository):
        self.team_repo = team_repo

    def create_team(self, body: CreateTeamReqBody):
        current_time = int(time.time())

        team = Team(
            id = str(uuid4()),
            name = body.name,
            short_name = body.short_name,
            description = body.description,
            created_at = current_time,
            updated_at = current_time,
        )

        self.team_repo.add_team(team)

    def get_all_teams(self):
        teams = self.team_repo.get_teams()
        return teams

    def get_team_by_name(self, name:str):
        team = self.team_repo.get_by_name(name)

        if not team:
            return None
        return team

    

    
