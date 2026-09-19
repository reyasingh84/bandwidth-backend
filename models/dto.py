from pydantic import BaseModel, EmailStr, Field, field_validator

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