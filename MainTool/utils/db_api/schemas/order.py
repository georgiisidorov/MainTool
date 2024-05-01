from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ARRAY, Float, sql

from utils.db_api.db_gino import BaseModel


class Order(BaseModel):
    __tablename__ = 'order'
    order_id = Column(String(20), primary_key=True)
    user_id = Column(BigInteger)
    action = Column(String(20))
    amount = Column(Integer)
    service_id = Column(String(4))
    description = Column(String(100))
    status = Column(String(20))
    money = Column(Float)
    created_at = Column(DateTime(timezone=True))

    query: sql.Select
