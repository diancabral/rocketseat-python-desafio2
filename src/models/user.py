from uuid import UUID, uuid4

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from config.database import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(24), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False, default="user")

    def get_id(self):
        return str(self.uuid)
