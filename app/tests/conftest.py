from venv import create
import pytest

from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import schemas
from database.database import Base

from environs import Env

@pytest.fixture(scope="function")
def SessionLocal():
    env = Env()
    env.read_env('tests/test.env')

    DB_NAME=env.str("DB_NAME_TEST")
    DB_USER=env.str("DB_USER")
    DB_PASS=env.str("DB_PASS")
    DB_HOST=env.str("DB_HOST")
    DB_PORT=env.int("DB_PORT")

    TEST_SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

    assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."
    create_database(TEST_SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield SessionLocal

    drop_database(TEST_SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="function")
def get_statistics():
    statistics: schemas.StatisticsCreate = {
        "date": "2015-04-30",
        "views": 15,
        "clicks": 16,
        "cost": 17.52
    }
    return statistics

@pytest.fixture(scope="function")
def get_statistics_before_list():
    statistics_before: list[schemas.StatisticsCreate] = [{
        "date": "2015-04-30",
        "views": 15,
        "clicks": 16,
        "cost": 17.52
    },
    {
        "date": "2014-04-30",
        "views": 0,
        "clicks": 0,
        "cost": 500
    }]
    return statistics_before

@pytest.fixture(scope="function")
def get_expected_statistics_list():
    expected_statistics: list[schemas.Statistics] = [{
        "date": "2015-04-30",
        "views": 15,
        "clicks": 16,
        "cost": 17.52,
        "cpc": 1.09,
        "cpm": 1168,
    },
    {
        "date": "2014-04-30",
        "views": 0,
        "clicks": 0,
        "cost": 500,
        "cpc": 0,
        "cpm": 0,
    }]
    return expected_statistics
