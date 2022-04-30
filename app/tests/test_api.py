from urllib import response
from fastapi.testclient import TestClient
from server.main import app, get_db
from services.statistics_handler import calculate_CPC_and_CPM
client = TestClient(app)


def temp_db(f):
    def func(SessionLocal, get_statistics, *args, **kwargs):
        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()
        app.dependency_overrides[get_db] = override_get_db
        f(get_statistics, *args, **kwargs)
        app.dependency_overrides[get_db] = get_db
    return func


@temp_db
def test_create_statistics(get_statistics):
    response = client.post(
        "/statistics/",
        json=get_statistics
    )
    
    assert response.status_code == 201
    assert response.json() == get_statistics
    response = client.post(
        "/statistics/",
        json=get_statistics
    )
    assert response.status_code == 409

@temp_db
def test_get_statistics(get_statistics):
    client.post(
        "/statistics/",
        json=get_statistics
    )
    response = client.get(
        "/statistics",
        params=get_statistics["date"]
    )
    assert response.status_code == 200
    assert response.json() == calculate_CPC_and_CPM([get_statistics])

@temp_db
def test_drop_statistics(get_statistics):
    client.post(
        "/statistics/",
        json=get_statistics
    )
    response = client.delete(
        "/statistics/"
    )
    assert response.status_code == 200
    assert response.text == "1"

@temp_db
def test_update_statistics(get_statistics):
    response = client.put(
        "/statistics/",
        json=get_statistics
    )
    response.status_code == 201
    assert response.json() == get_statistics
    