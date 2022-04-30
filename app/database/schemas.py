from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat, validator, Field
from datetime import date


class StatisticsBase(BaseModel):
    """Pydantic base model for statistics"""
    date: date
    views: NonNegativeInt | None = Field(None)
    clicks: NonNegativeInt | None = Field(None)
    cost: NonNegativeFloat | None = Field(None)


class StatisticsCreate(StatisticsBase):
    """Pydantic model to create statistics"""

    class Config:
        validate_assignment = True
        orm_mode = True
    
    @validator("views")
    def set_name(cls, views):
        return views or 0

    @validator("clicks")
    def set_clicks(cls, clicks):
        return clicks or 0

    @validator("cost")
    def set_cost(cls, cost):
        return cost or 0


class Statistics(StatisticsBase):
    """Pydantic model to get statistics"""
    cpc: NonNegativeFloat
    cpm: NonNegativeFloat

    class Config:
        orm_mode = True
