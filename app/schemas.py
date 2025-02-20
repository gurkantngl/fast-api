from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    category_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available: bool
    
    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    book_id: int
    borrower_name: str

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool
    
    class Config:
        from_attributes = True 