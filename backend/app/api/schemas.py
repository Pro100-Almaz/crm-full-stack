from pydantic import BaseModel


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



