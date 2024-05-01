from sqlalchemy import Column, Integer, BigInteger, String, ARRAY, Float, sql

from utils.db_api.db_gino import BaseModel


class Auto(BaseModel):
    __tablename__ = 'auto'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    user_id = Column(BigInteger)
    service = Column(String(5))
    amount = Column(Integer)

    query: sql.Select
