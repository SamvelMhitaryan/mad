import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.memes.main import app
from app.memes.database import Base, get_db_memes
from app.memes.settings import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_database(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(autouse=True)
async def clear_database():
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
    yield


@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db_memes] = override_get_db

client = TestClient(app)


def test_create_meme(db_session):
    response = client.post(
        "/memes", json={"title": "Test Meme", "image_url": "http://example.com/test.jpg"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Meme"
    assert response.json()["image_url"] == "http://example.com/test.jpg"


def test_read_memes(db_session):
    client.post("/memes", json={"title": "Test Meme 1",
                "image_url": "http://example.com/test1.jpg"})
    client.post("/memes", json={"title": "Test Meme 2",
                "image_url": "http://example.com/test2.jpg"})

    response = client.get("/memes")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_meme(db_session):
    response_create = client.post(
        "/memes", json={"title": "Test Meme", "image_url": "http://example.com/test.jpg"})
    meme_id = response_create.json()["id"]

    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["id"] == meme_id
