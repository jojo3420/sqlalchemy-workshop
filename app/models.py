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
    username = Column(String(10), nullable=False)
    nickname = Column(String(20))
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    gender = Column(String(1))

    def __repr__(self):
        return f'<User> {self.username}'
