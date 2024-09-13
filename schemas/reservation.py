from pydantic import BaseModel
from datetime import date, time


class ReservationBase(BaseModel):
    coworking_id: int
    user_id: int
    date: date
    start_time: time
    end_time: time


class Reservation(ReservationBase):
    id: int
