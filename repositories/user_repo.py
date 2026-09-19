from mysql.connector import MySQLConnection
from models.models import User

class UserRepository:

    def __init__(self, connection: MySQLConnection):
        self.connection = connection

    def add_user(self, user:User):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO users (id, first_name, last_name, email, username, password,
            phone, role, team_id, department, designation, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            user.id, 
            user.first_name,
            user.last_name,
            user.email,
            user.username,
            user.password,
            user.phone,
            user.role.value if hasattr(user.role , "value") else user.role,
            user.team_id,
            user.department.value if hasattr(user.department, "value") else user.department,
            user.designation,
            1 if user.is_active else 0,
            user.created_at,
            user.updated_at
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()


    def get_users(self):
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM users
        """
        try:
            cursor.execute(query)
            users = cursor.fetchall()
            return users
        finally:
            cursor.close()

    def get_active_users(self):
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM users
            WHERE is_active  = TRUE
        """
        try:
            cursor.execute(query)
            active_users = cursor.fetchall()
            return active_users
        finally:
            cursor.close()

    def get_by_email(self, email:str):
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM users
            WHERE email=%s
        """

        try:
            cursor.execute(query, (email,))
            user_by_email = cursor.fetchone()
            return user_by_email
        finally:
            cursor.close()

    def update_user(self, user:User):
        cursor = self.connection.cursor()

        query = """
            UPDATE users
            SET email=%s , password=%s , role=%s , designation=%s , updated_at=%s
            WHERE id = %s 
        """

        values = (
            user.email,
            user.password,
            user.role.value if hasattr(user.role , "value") else user.role,
            user.designation,
            user.updated_at,
            user.id,
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def delete_user(self, user_id: str):
        cursor = self.connection.cursor()

        query = """
            UPDATE users
            SET is_active = FALSE
            WHERE id = %s
        """
        values = (user_id,)

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
