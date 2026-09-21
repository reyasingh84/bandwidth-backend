from mysql.connector import MySQLConnection
from models.models import Task

class TaskRepository:

    def __init__(self, connection: MySQLConnection):
        self.connection = connection

    def add_task(self, task:Task):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO tasks(id, team_id, title, description, acpt_criteria,
            category, status, reporter_id, reporter_username, assignee_id, 
            assignee_username, priority, proj_name, history, deadline, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            task.id,
            task.team_id,
            task.title,
            task.description,
            task.acpt_criteria,
            task.category.value if hasattr(task.category, "value") else task.category,
            task.status.value if hasattr(task.status, "value") else task.status,
            task.reporter_id,
            task.reporter_username,
            task.assignee_id,
            task.assignee_username,
            task.priority.value if hasattr(task.priority, "value") else task.priority,
            task.proj_name,
            task.history,
            task.deadline,
            task.created_at,
            task.updated_at
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def get_all_tasks(self)-> list[Task]:
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM tasks
        """
        try:
            cursor.execute(query)
            tasks = cursor.fetchall()
            tasks_list = []
            for task in tasks: 
                task_obj = Task(*task)
                tasks_list.append(task_obj)
            
            return tasks_list
        finally:
            cursor.close()

    def get_task_by_id(self, task_id: str) -> Task | None:
        cursor = self.connection.cursor()

        query = """
            SELECT * FROM tasks
            WHERE id = %s
        """
        try:
            cursor.execute(query, (task_id,))
            task = cursor.fetchone()
            return Task(*task) if task else None
        finally:
            cursor.close()

    def get_all_tasks_by_team(self, team_id: str):
        cursor = self.connection.cursor()

        query = """
            SELECT * from tasks where team_id= %s
        """

        try:
            cursor.execute(query, (team_id,) )
            tasks = cursor.fetchall()
            tasks_list = []
            for task in tasks: 
                task_obj = Task(*task)
                tasks_list.append(task_obj)
            
            return tasks_list
        finally:
            cursor.close()

    def get_all_tasks_by_assignee(self, assignee_id: str):
        cursor = self.connection.cursor()
        
        query = """
            SELECT * from tasks where assignee_id = %s
        """

        try:
            cursor.execute(query, (assignee_id,) )
            tasks = cursor.fetchall()
            tasks_list = []
            for task in tasks: 
                task_obj = Task(*task)
                tasks_list.append(task_obj)
            
            return tasks_list
        finally:
            cursor.close()

    def get_all_tasks_by_reporter(self, reporter_id: str):
            cursor = self.connection.cursor()
            
            query = """
                SELECT * from tasks where reporter_id = %s
            """
    
            try:
                cursor.execute(query, (reporter_id,) )
                tasks = cursor.fetchall()
                tasks_list = []
                for task in tasks: 
                    task_obj = Task(*task)
                    tasks_list.append(task_obj)
                
                return tasks_list
            finally:
                cursor.close()

    def update_task(self, task:Task):
        cursor = self.connection.cursor()

        query = """
            UPDATE tasks
            SET title=%s , description=%s , acpt_criteria=%s , category=%s, status=%s, assignee_id=%s ,
                assignee_username=%s, priority=%s, proj_name=%s, history=%s, deadline=%s, updated_at=%s
            WHERE id = %s
        """
        values = (
            task.title,
            task.description,
            task.acpt_criteria,
            task.category.value if hasattr(task.category, "value") else task.category,
            task.status.value if hasattr(task.status, "value") else task.status,
            task.assignee_id,
            task.assignee_username,
            task.priority.value if hasattr(task.priority, "value") else task.priority,
            task.proj_name,
            task.history,
            task.deadline,
            task.updated_at,
            task.id
        )

        try:
            cursor.execute(query,values)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()


    


    


   
  
    
