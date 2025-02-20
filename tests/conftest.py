import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid

from app.main import app
from app.database import Base, get_db
from app.models import Category, Book, Loan

# Test veritabanı için SQLite bellek içi veritabanı kullanıyoruz
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_database():
    # Her test için tabloları oluştur
    Base.metadata.create_all(bind=engine)
    yield
    # Her test sonrasında tabloları temizle
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_category(db_session):
    category = Category(name=f"Test Kategori {uuid.uuid4()}", description="Test Açıklama")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category

@pytest.fixture
def test_book(db_session):
    category = Category(name=f"Test Kategori {uuid.uuid4()}", description="Test Açıklama")
    db_session.add(category)
    db_session.commit()
    
    book = Book(
        title="Test Kitap",
        author="Test Yazar",
        isbn="1234567890",
        publication_year=2024,
        category_id=category.id,
        available=True
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book 