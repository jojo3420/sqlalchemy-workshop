from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    func,
    Text,
    ForeignKey,
)
from app.database import Base


class IDMixin:
    id = Column(Integer, primary_key=True, index=True)


class DateTimeMixin:
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )


class User(IDMixin, DateTimeMixin, Base):
    """sqlalchemy model USER Table"""

    __tablename__ = "user"

    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User> {self.username}'
