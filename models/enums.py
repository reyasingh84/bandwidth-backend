from enum import StrEnum, IntEnum

class Role(StrEnum):
    ADMIN = "admin"
    DIRECTOR = "director"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class TaskPriority(IntEnum):
    VERY_HIGH = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    VERY_LOW = 1

class TaskCategory(StrEnum):
    BUG = "bug"
    QA = "testing"
    TASK = "task"

class TaskStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    TESTING = "testing"
    CLOSED = "closed"
    ON_HOLD = "on_hold"

class UserDepartment(StrEnum):
    IT = "it"
    ENGINEERING = "engineering"
    QA = "qa"
    SECURITY = "security"
    DEVOPS = "devops"
    