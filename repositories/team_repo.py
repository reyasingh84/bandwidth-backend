from mysql.connector import MySQLConnection
from models.models import Team

class TeamRepository:

    def __init__(self, connection: MySQLConnection):
        self.connection = connection

    def add_team(self, team:Team):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO teams(id, name, short_name, description, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            team.id,
            team.name,
            team.short_name,
            team.description,
            team.created_at,
            team.updated_at
        )

        try:
            cursor.execute(query,values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def get_teams(self)-> list[Team]:
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM teams
        """

        try:
            cursor.execute(query)
            teams = cursor.fetchall()
            teams_list = []
            for team in teams: 
                teams_list.append(Team(*team))
            return teams_list
        finally:
            cursor.close()

    def get_by_name(self, team_name:str):
        cursor = self.connection.cursor()
        
        query = """
            SELECT * FROM teams
            WHERE name=%s
        """
        
        try:
            cursor.execute(query, (team_name,))
            team = cursor.fetchone()
            return Team(*team) if team else None
        finally:
            cursor.close()

    def get_by_team_id(self, team_id:str):
            cursor = self.connection.cursor()
            
            query = """
                SELECT * FROM teams
                WHERE id=%s
            """
            
            try:
                cursor.execute(query, (team_id,))
                team = cursor.fetchone()
                return Team(*team) if team else None
            finally:
                cursor.close()
    
    
    def update_team(self, team:Team):
        cursor = self.connection.cursor()

        query = """
            UPDATE teams
            SET name=%s , short_name=%s ,  description=%s , updated_at = %s
            WHERE id = %s
        """

        values = (
            team.name,
            team.short_name,
            team.description,
            team.updated_at,
            team.id
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()
