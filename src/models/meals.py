from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import Boolean, DateTime, String

from config.database import db


class Meals(db.Model):
    __tablename__ = "meals"

    uuid: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(24), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    is_diet: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __init__(self, name: str, description: str, is_diet: bool):
        self.name = name
        self.description = description
        self.is_diet = is_diet
