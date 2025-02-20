from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    books = relationship("Book", back_populates="category")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    publication_year = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    available = Column(Boolean, default=True)
    
    category = relationship("Category", back_populates="books")
    loans = relationship("Loan", back_populates="book")

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    borrower_name = Column(String)
    loan_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    
    book = relationship("Book", back_populates="loans") 