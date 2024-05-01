from sqlalchemy import Column, Integer, String, sql

from utils.db_api.db_gino import BaseModel


class Settings(BaseModel):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    action = Column(String(10))
    service_id = Column(String(4))

    query: sql.Select
