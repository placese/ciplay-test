from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from datetime import date

from . import models, schemas


def get_statistics(db: Session, from_date: date, to_date: date) -> list[schemas.Statistics]:
    """Returns list of statistics object by date"""
    return db.query(models.Statistics).filter(
        and_(models.Statistics.date >= from_date, models.Statistics.date <= to_date)).order_by(models.Statistics.date).all()


def create_statistics(db: Session, statistics_obj: schemas.StatisticsCreate) -> schemas.StatisticsCreate:
    """Creates statistics record in db and returns it"""
    db_statistics_obj = models.Statistics(
        date=statistics_obj.date,
        views=statistics_obj.views,
        clicks=statistics_obj.clicks,
        cost=statistics_obj.cost
    )
    try:
        db.add(db_statistics_obj)
        db.commit()
        db.refresh(db_statistics_obj)
        return db_statistics_obj
    except IntegrityError as e:
        raise e


def update_statistics(db: Session, statistics_obj: schemas.StatisticsCreate) -> schemas.StatisticsCreate | None:
    """Fully updates statistics record and returns it, if record with inputed date does not exists, returns None"""
    db_statistics_obj = db.query(models.Statistics).filter(models.Statistics.date == statistics_obj.date).update({
        models.Statistics.date: statistics_obj.date,
        models.Statistics.views: statistics_obj.views,
        models.Statistics.clicks: statistics_obj.clicks,
        models.Statistics.cost: statistics_obj.cost
    }, synchronize_session=False)
    if not db_statistics_obj:
        return
    db_statistics_obj = models.Statistics(
        date=statistics_obj.date,
        views=statistics_obj.views,
        clicks=statistics_obj.clicks,
        cost=statistics_obj.cost
    )
    db.commit()
    return db_statistics_obj


def delete_statistics(db: Session) -> int:
    """Drops all saved statistics and returns the numbers of deleted rows"""
    result =  db.query(models.Statistics).delete()
    db.commit()
    return result
