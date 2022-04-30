from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from datetime import date


def get_statistics(db: Session, from_date: date, to_date: date) -> list[schemas.Statistics]:
    """Returns list of statistics object by date"""
    return db.query(models.Statistics).filter(
        and_(models.Statistics.date >= from_date, models.Statistics.date <= to_date)).order_by(models.Statistics.date).all()


def create_statistics(db: Session, statistics_obj: schemas.StatisticsCreate) -> schemas.StatisticsBase:
    """Creates statistic record in db and returns it as a model"""
    db_statistics_obj = models.Statistics(
        date=statistics_obj.date,
        views=statistics_obj.views,
        clicks=statistics_obj.clicks,
        cost=statistics_obj.cost
        )
    db.add(db_statistics_obj)
    db.commit()
    db.refresh(db_statistics_obj)
    return db_statistics_obj


def delete_statustics(db: Session) -> int:
    """Drops all saved statistics and returns the numbers of deleted rows"""
    result =  db.query(models.Statistics).delete()
    db.commit()
    return result
