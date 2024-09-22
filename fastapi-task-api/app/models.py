import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pending")


class ApiCallLog(Base):
    __tablename__ = 'api_call_logs'

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    country = Column(String, nullable=False)
    weather_state = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.date.today)
