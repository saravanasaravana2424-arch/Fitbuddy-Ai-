from sqlalchemy import Column, Integer, String, Text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    fitness_level = Column(String)
    goal = Column(String)
    fitness_plan = Column(Text)
    feedback = Column(Text, nullable=True)