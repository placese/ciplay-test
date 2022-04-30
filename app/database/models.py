from database.database import Base
from sqlalchemy import Column, Integer, Date, Float

class Statistics(Base):
    """SQLAlchemy ORM model for statistics"""
    __tablename__ = 'statistics'

    date = Column(Date, primary_key=True, index=True)
    views = Column(Integer, nullable=True)
    clicks = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
