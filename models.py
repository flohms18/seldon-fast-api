from sqlalchemy import Column, Integer, String
from database import Base



class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    tag = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)