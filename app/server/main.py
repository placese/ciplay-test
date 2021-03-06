from fastapi import FastAPI, Depends, Query
from fastapi import HTTPException, status, Response

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from datetime import date

from database.database import SessionLocal, engine
from database import crud, models, schemas

from services.statistics_handler import calculate_CPC_and_CPM, sort_statistics_list


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/statistics/", response_model=list[schemas.Statistics])
def get_statistics(
    db: Session = Depends(get_db),
    from_date: date = Query(date.min, alias="from", title="from date", description="Start date of period."),
    to_date: date = Query(date.today(), alias="to", title="to date", description="End date of period."),
    sort: str = Query('date', alias="sort", title="sort", description="Field to sort by: date, view, clicks or cost. Date set as default."),
    ):
    """Returns list of statistics by date"""
    return sort_statistics_list(calculate_CPC_and_CPM(jsonable_encoder(crud.get_statistics(db=db, from_date=from_date, to_date=to_date))), sort)


@app.post("/statistics/", response_model=schemas.StatisticsCreate, status_code=status.HTTP_201_CREATED)
def create_statistics(statistics: schemas.StatisticsCreate, db: Session = Depends(get_db)):
    """Create statistics records and returns it"""
    try:
        return crud.create_statistics(db=db, statistics_obj=statistics)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Statistics with this date already exists. Try to use PUT or PATCH methods to update information."
        )


@app.put("/statistics/", response_model=schemas.StatisticsCreate)
def update_statistics(response: Response, statistics: schemas.StatisticsCreate, db: Session = Depends(get_db)):
    """Updates statistics record if exists, or creates if doesn't exist and returns it"""
    result = crud.update_statistics(db=db, statistics_obj=statistics)
    if result:
        response.status_code = status.HTTP_200_OK
        return result
    else:
        result = crud.create_statistics(db=db, statistics_obj=statistics)
        response.status_code = status.HTTP_201_CREATED
        return result


@app.delete("/statistics/", response_model=int, status_code=status.HTTP_200_OK)
def drop_statistics(db: Session = Depends(get_db)):
    """Drop all statistics"""
    return crud.delete_statistics(db=db)
