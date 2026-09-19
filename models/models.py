from dataclasses import dataclass
from enums import Role, TaskCategory, TaskPriority, TaskStatus, UserDepartment

@dataclass
class User:
    id : str
    first_name : str
    last_name : str
    email : str
    username : str
    password : str
    phone : str
    role : Role
    team_id : str
    department : UserDepartment
    designation : str
    is_active : bool
    created_at : int
    updated_at : int


@dataclass
class Team:
    id : str
    name : str
    short_name : str
    description : str
    created_at : int
    updated_at : int

@dataclass
class Task:
    id : str
    team_id : str
    title : str
    description : str
    acpt_criteria : str
    category : TaskCategory
    status : TaskStatus
    reporter_id : str
    reporter_username : str
    assignee_id : str
    assignee_username : str
    priority : TaskPriority
    proj_name : str
    history : str
    deadline : int
    created_at : int
    updated_at : int

@dataclass
class Comment:
    id : str
    message : str
    author_id : str
    author_username : str
    task_id : str
    created_at : int
    updated_at : int
