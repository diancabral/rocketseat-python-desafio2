from uuid import UUID

from sqlalchemy import TypeDecorator
from sqlalchemy.sql.sqltypes import String


class UUIDString(TypeDecorator):
    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(value) if isinstance(value, UUID) else value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return UUID(value) if not isinstance(value, UUID) else value
