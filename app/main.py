from fastapi import FastAPI, Depends, Query
from fastapi import HTTPException, status

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from datetime import date

from database.database import SessionLocal, engine
from database import crud, models, schemas

from services.statistics_handler import calculate_CPC_and_CPM


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/statistics/")
def get_statistics(db: Session = Depends(get_db), from_date: date = Query(date.min), to_date: date = Query(date.today())):
    return calculate_CPC_and_CPM(jsonable_encoder(crud.get_statistics(db=db, from_date=from_date, to_date=to_date)))


@app.post("/statistics/", response_model=schemas.StatisticsCreate)
def save_statistics(statistics: schemas.StatisticsCreate, db: Session = Depends(get_db)):
    return crud.create_statistics(db=db, statistics_obj=statistics)


@app.delete("/statistics/")
def drop_statistics(db: Session = Depends(get_db)):
    return crud.delete_statustics(db=db)
