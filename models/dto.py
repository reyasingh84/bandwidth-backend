from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from models.enums import Role, UserDepartment, TaskCategory, TaskPriority, TaskStatus

class LoginReqBody(BaseModel):
    email: EmailStr = Field(min_length=6, max_length=50)
    password: str = Field(
        min_length=8,
        max_length=30,
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not any(character.islower() for character in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(character.isupper() for character in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(character.isdigit() for character in password):
            raise ValueError("Password must contain at least one number")
        if not any(not character.isalnum() for character in password):
            raise ValueError("Password must contain at least one special character")
        return password

class CreateUserReqBody(BaseModel): 
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr = Field(min_length=6, max_length=50)
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=8,max_length=30)
    phone: str = Field(None, min_length=10, max_length=13)
    role : Role
    team_id : str = Field(min_length=24, max_length=36)
    department : UserDepartment
    designation : str = Field(None)


    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not any(character.islower() for character in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(character.isupper() for character in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(character.isdigit() for character in password):
            raise ValueError("Password must contain at least one number")
        if not any(not character.isalnum() for character in password):
            raise ValueError("Password must contain at least one special character")
        return password


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    phone: str | None
    role: Role
    team_id: str | None
    department: UserDepartment
    designation: str | None
    is_active: bool
    created_at: int
    updated_at: int

class CreateTeamReqBody(BaseModel):
    name : str
    short_name : str
    description : str

class CreateTaskReqBody(BaseModel):
    team_id : str = Field(None, min_length=24, max_length=36)
    title : str = Field(min_length=5, max_length=250)
    description : str = Field(min_length=10, max_length=1000)
    acpt_criteria : str = Field(None)
    category : TaskCategory
    assignee_id : str = Field(None)
    assignee_username : str = Field(None)
    priority : TaskPriority
    proj_name : str = Field(None)
    deadline : int
    