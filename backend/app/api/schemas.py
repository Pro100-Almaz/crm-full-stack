from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Branch(BaseModel):
    id: str = None
    name: str
    internal_name: str = None
    abbreviation: str = "Основной филиал"
    address: str = None
    newsletter_address: str = None
    address_note: str = None
    time_zone: str = "UTC+5:00"
    group_id: str = None
    workdays: str = "Monday,Tuesday,Wednesday,Thursday,Friday"
    holidays: str = "Saturday,Sunday"
    work_hours: str = "9:00-18:00"
    responsible_for_aa: str = None
    display_color: str = None
    send_notification: dict = {}


class EventBase(BaseModel):
    title: str = Field(..., example="Team Meeting")
    description: str = Field(None, example="Discuss project milestones")
    start_time: datetime = Field(..., example="2024-05-01T10:00:00")
    end_time: datetime = Field(..., example="2024-05-01T11:00:00")
    user_id: str = None
    room: int = 1

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: str = None
    description: str = None
    start_time: datetime = "2024-05-01T12:00:00"
    end_time: datetime = "2024-05-01T13:00:00"
    user_id: str = None
    room: int = 1




