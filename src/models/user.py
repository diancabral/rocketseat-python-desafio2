from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from config.database import db

from .utils.type_decorator_uuid import UUIDString

if TYPE_CHECKING:
    from models.meals import Meals


class User(db.Model, UserMixin):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(UUIDString, primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(24), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False, default="user")

    meals: Mapped[list["Meals"]] = relationship("Meals", back_populates="user")

    def get_id(self):
        return str(self.uuid)
