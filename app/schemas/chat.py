from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .message import Message


class Chat(SQLModel):
    __tablename__: str = "chats"

    id: uuid.UUID = Field(default=None, primary_key=True)
    title: str | None = None
    model: str | None = None
    created_at: datetime
    last_activity_at: datetime

    messages: list["Message"] = Relationship(back_populates="chat")
