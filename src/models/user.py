from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from config.database import db


class User(db.Model):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(24), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False, default="user")

    def __init__(self, username: str, password: bytes, role: str):
        self.username = username
        self.password = password
        self.role = role

    def get_checkpw_password(self):
        return str.encode(str(self.password))
