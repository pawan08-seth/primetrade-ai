from sqlalchemy import Column, Integer, String,Text,DateTime,ForeignKey,Date,JSON
from datetime import datetime
from typing import Literal
from Database.database import Base

class Users(Base):
    __tablename__="Users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String(50), unique=True, index=True)
    hashed_Password=Column(String(255))
    roles = Column(JSON, default=list)


class Task(Base):
    __tablename__="Task"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    category=Column(String, nullable=False)
    Date=Column(Date, nullable=False)
    owner_id=Column(Integer,ForeignKey("Users.id"), index=True)
    notes = Column(String, nullable=True)
