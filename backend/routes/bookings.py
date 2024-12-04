from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from sqlmodel import select
from services.database import SessionDep
from services.models.booking_requests_model import Booking, BookingCreate
from services.models.users_model import User

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

@router.post("/")
def create_booking(booking_data: BookingCreate, session: SessionDep) -> Booking:
    print("Py - Received booking data:", booking_data.model_dump(by_alias=True))
    
    # Verify that the user exists
    user = session.get(User, booking_data.user_id)
    if not user:
        print("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create new booking from validated data
    booking = Booking.from_orm(booking_data)
    print("Created booking:", booking.model_dump(by_alias=True))
    
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking

@router.get("/")
def read_bookings(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Booking]:
    bookings = session.exec(select(Booking).offset(offset).limit(limit)).all()
    return bookings

@router.get("/{booking_id}")
def read_booking(booking_id: int, session: SessionDep) -> Booking:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.get("/user/{user_id}")
def read_user_bookings(
    user_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Booking]:
    # Verify that the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    bookings = session.exec(
        select(Booking)
        .where(Booking.user_id == user_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return bookings

@router.put("/{booking_id}")
def update_booking(booking_id: int, updated_booking: BookingCreate, session: SessionDep) -> Booking:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Update booking fields
    booking_data = updated_booking.dict(exclude_unset=True)
    for key, value in booking_data.items():
        setattr(booking, key, value)
    
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, session: SessionDep):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(booking)
    session.commit()
    return {"ok": True}
