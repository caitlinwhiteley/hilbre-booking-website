from sqlmodel import Field, SQLModel, Relationship
from pydantic import validator, ConfigDict
from pydantic.alias_generators import to_camel
from fastapi import HTTPException

class BaseSchema(SQLModel):
    """
    Use an alias generator to receive json with attributes in camelcase
    and convert them to snake_case on serialisation
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        json_schema_extra={"examples": []},
    )
    
class User(BaseSchema, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=20)  
    email: str = Field(max_length=100, unique=True, index=True)
    phone_number: str = Field(max_length=20, unique=True, index=True)
    admin: bool = Field(default=False)
    bookings: list["Booking"] = Relationship(back_populates="user")

    @validator("phone_number")
    def validate_phone_number(cls, v):
        # Remove any non-digit characters
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError("Phone number must have at least 10 digits")
        return cleaned

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone_number": "1234567890",
                    "admin": False
                }
            ]
        }
    )
