from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    func,
    Text,
    ForeignKey,
    Table,
)
from app.database import Base
from sqlalchemy.orm import relationship


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
    """sqlalchemy model USER Table
    User, Role 1:N 관계
    """

    __tablename__ = "user"

    email = Column(String(255), unique=True, index=True)
    username = Column(String(10), nullable=False)
    nickname = Column(String(20))
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    gender = Column(String(1))

    # 참조할 table.column(PK)
    role_id = Column(Integer, ForeignKey('role.id'))

    def __repr__(self):
        return f'<User> {self.username}'


class Role(IDMixin, Base):
    __tablename__ = 'role'
    title = Column(String(15), unique=True)

    # 참조할 class 명, 참조할 클래스 User가 참조하는 테이블명, ...
    users = relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role> {self.title}'


class Parent(IDMixin, Base):
    __tablename__ = 'parent'
    username = Column(String(15), nullable=False)
    children = relationship('Child', backref='parent', lazy='dynamic')


class Child(IDMixin, Base):
    __tablename__ = 'child'
    name = Column(String(20))
    age = Column(Integer)
    gender = Column(String(1))

    parent_id = Column(Integer, ForeignKey('parent.id'))


class Member(IDMixin, Base):
    __tablename__ = 'member'
    name = Column(String(20))

    # N:M
    projects = relationship('Project', secondary='member_project', backref='member', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Project(IDMixin, Base):
    __tablename__ = 'project'
    name = Column(String(20))
    dead_line = Column(DateTime)

    # N:M
    members = relationship('Member', secondary='member_project', backref='project', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


# N:M Many to Many
# Member - Project
association_table = Table('member_project',
                          Base.metadata,
                          Column('member_id', Integer, ForeignKey('member.id')),
                          Column('project_id', Integer, ForeignKey('project.id'))
                          )



class Human(IDMixin, Base):
    __tablename__ = 'human'
    name = Column(String(25))
    age = Column(Integer)
    human_info = relationship('HumanInfo', back_populates='human', uselist=False)


class HumanInfo(IDMixin, Base):
    __tablename__ = 'human_info'
    address = Column(String(200))
    zipcode = Column(String(5))
    human_id = Column(Integer, ForeignKey('human.id'))

    human = relationship('Human', back_populates='human_info')


