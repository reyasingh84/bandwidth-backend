from mysql.connector import MySQLConnection
from models.models import Comment

class CommentRepository:

    def __init__(self, connection: MySQLConnection):
        self.connection = connection

    def add_comment(self, comment:Comment):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO comments (id, message, author_id, author_username, task_id, created_at, updated_at)
            VALUES (%s,%s, %s, %s, %s, %s, %s)
        """
        values = (
            comment.id,
            comment.message,
            comment.author_id,
            comment.author_username,
            comment.task_id,
            comment.created_at,
            comment.updated_at
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def get_comments_by_task_id(self, task_id:str):
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM comments
            WHERE task_id = %s
        """

        try:
            cursor.execute(query, (task_id,))
            comments = cursor.fetchall()
            comment_list = []
            for comment in comments:
                comment_obj = Comment(*comment)
                comment_list.append(comment_obj)
            return comment_list
        finally:
            cursor.close()

    def get_comment_by_id(self, id: str):
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM comments
            WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            comment = cursor.fetchone()
            comment_obj = Comment(*comment)
            return comment_obj
        finally:
            cursor.close()

    def update_comment(self, comment_id:str, new_message:str):
        cursor = self.connection.cursor()

        query = """
            UPDATE comments
            SET message=%s
            WHERE id=%s
        """
        try:
            cursor.execute(query, (new_message,comment_id))
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

        
        
    