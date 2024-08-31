from sqlalchemy import Column, String, Integer, Boolean
from db import Base
from flask_login import UserMixin


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, unique=True, nullable=False)
    subject = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    date_created = Column(String, nullable=False)


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
    