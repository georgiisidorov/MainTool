import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, Boolean, Integer, BigInteger, String, DateTime, Float, sql

from utils.db_api.db_gino import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    fullname = Column(String(100))
    balance = Column(Float)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    test_3k = Column(Integer)
    message_id = Column(BigInteger)


    query: sql.Select
