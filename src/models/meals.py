from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime, String

from config.database import db

from .utils.type_decorator_uuid import UUIDString

if TYPE_CHECKING:
    from models.user import User


class Meals(db.Model):
    __tablename__ = "meals"

    uuid: Mapped[UUID] = mapped_column(UUIDString, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(24), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    is_diet: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_id: Mapped[UUID] = mapped_column(
        UUIDString, ForeignKey("users.uuid"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="meals")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def get_id(self):
        return str(self.uuid)
