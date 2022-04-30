from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat
from datetime import date


class StatisticsBase(BaseModel):
    """Pydantic base model for statistics"""
    date: date
    views: NonNegativeInt | None = None
    clicks: NonNegativeInt | None = None
    cost: NonNegativeFloat | None = None
    

class StatisticsCreate(StatisticsBase):
    """Pydantic model to create statistics"""
    pass

    class Config:
        orm_mode = True


class Statistics(StatisticsBase):
    """Pydantic model to get statistics"""
    cpc: NonNegativeFloat
    cpm: NonNegativeFloat

    class Config:
        orm_mode = True
