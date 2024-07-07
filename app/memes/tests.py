from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


async def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_meme():
    response = client.post(
        "/memes", json={"title": "Test Meme", "image_url": "http://example.com/test.jpg"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Meme"
    assert response.json()["image_url"] == "http://example.com/test.jpg"


def test_read_memes():
    response = client.get("/memes")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_meme():
    response = client.get("/memes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
