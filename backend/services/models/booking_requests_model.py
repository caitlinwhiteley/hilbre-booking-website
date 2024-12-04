from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional
from pydantic import validator, ConfigDict
from pydantic.alias_generators import to_camel
from .users_model import User

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

class BookingBase(BaseSchema):
    date: str  # datetime // TODO add validator
    number_of_days: int = Field(gt=0)
    number_of_people: int = Field(gt=0)
    price: float = Field(gt=0)
    has_paid: bool = Field(default=False)
    other_attendees: str | None = None
    booking_status: str = Field(default="pending")
    booking_comments: str | None = None
    user_id: int = Field(foreign_key="user.id")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "date": "2024-01-01",
                    "numberOfDays": 7,
                    "numberOfPeople": 2,
                    "price": 100.0,
                    "hasPaid": False,
                    "otherAttendees": "John, Jane",
                    "bookingStatus": "pending",
                    "bookingComments": "Special request",
                    "userId": 12
                }
            ]
        }
    )

class Booking(BookingBase, table=True):
    booking_id: Optional[int] = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="bookings")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "bookingId": 1,
                    "date": "2024-01-01",
                    "numberOfDays": 7,
                    "numberOfPeople": 2,
                    "price": 100.0,
                    "hasPaid": False,
                    "otherAttendees": "John, Jane",
                    "bookingStatus": "pending",
                    "bookingComments": "Special request",
                    "userId": 12
                }
            ]
        }
    )

class BookingCreate(BookingBase):
    """
    Model for creating a new booking.
    Inherits all fields from BookingBase but adds specific validation for creation.
    """
    @validator("date")
    def validate_date(cls, v):
        try:
            date = datetime.fromisoformat(v)
            if date < datetime.now():
                raise ValueError("Booking date must be in the future")
            return v
        except ValueError as e:
            raise ValueError(f"Invalid date format: {str(e)}")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "date": "2024-01-01",
                    "numberOfDays": 7,
                    "numberOfPeople": 2,
                    "price": 100.0,
                    "hasPaid": False,
                    "otherAttendees": "John, Jane",
                    "bookingStatus": "pending",
                    "bookingComments": "Special request",
                    "userId": 12
                }
            ]
        }
    )