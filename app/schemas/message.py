from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

if TYPE_CHECKING:
    from .chat import Chat


class Message(SQLModel, table=True):
    __tablename__: str = "messages"

    id: uuid.UUID = Field(default=None, primary_key=True)
    chat_id: uuid.UUID = Field(foreign_key="chats.id")
    role: str
    content: str
    created_at: datetime

    chat: Optional["Chat"] = Relationship(back_populates="messages")
