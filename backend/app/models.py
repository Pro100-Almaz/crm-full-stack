import uuid
from typing import List, Optional, Dict  # noqa: UP035

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class BranchGroup(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    branches: List["Branch"] = Relationship(back_populates="group")


class Branch(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    internal_name: Optional[str] = Field(default=None, max_length=100)
    abbreviation: Optional[str] = Field(default=None, max_length=100)
    address: str = Field(min_length=1, max_length=200)
    newsletter_address: Optional[str] = Field(default=None, max_length=200)
    address_note: Optional[str] = Field(default=None, max_length=500)
    time_zone: str = Field(min_length=1, max_length=100)
    send_notification: Optional[Dict] = Field(default=None, sa_column_kwargs={"type_": "JSONB"})
    work_hours: str = Field(default="8:00-18:00", min_length=1, max_length=100)
    responsible_user_for_authomative_actions: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    display_color: str = Field(min_length=1, max_length=50)
    group_id: Optional[uuid.UUID] = Field(default=None, foreign_key="branchgroup.id")
    group: Optional["BranchGroup"] = Relationship(back_populates="branches")
    workdays: str = Field(default="")
    holidays: str = Field(default="")

    @property
    def workdays_list(self) -> List[str]:
        return self.workdays.split(",") if self.workdays else []

    @property
    def holidays_list(self) -> List[str]:
        return self.holidays.split(",") if self.holidays else []

