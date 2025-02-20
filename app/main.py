from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app import models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kişisel Kütüphane API",
    description="""
    Bu API, kişisel kütüphane yönetimi için geliştirilmiş bir RESTful servistir.
    
    ## Özellikler
    * 📚 Kitap yönetimi (ekleme, düzenleme, silme)
    * 📋 Kategori yönetimi
    * 📖 Kitap ödünç alma/verme sistemi
    * 🔍 Kategoriye göre kitap filtreleme
    
    ## Kullanım
    API'yi kullanmak için aşağıdaki endpoint'leri kullanabilirsiniz.
    """,
    version="1.0.0",
    contact={
        "name": "Kütüphane Yönetimi",
        "email": "kutuphane@example.com"
    }
)

# Kategori endpoint'leri
@app.post("/categories/", response_model=schemas.Category, tags=["Kategoriler"],
    summary="Yeni kategori oluştur",
    description="Bu endpoint ile kütüphaneye yeni bir kategori ekleyebilirsiniz.")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Yeni bir kategori oluşturur.
    
    - **name**: Kategori adı (zorunlu)
    - **description**: Kategori açıklaması (opsiyonel)
    """
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[schemas.Category], tags=["Kategoriler"],
    summary="Tüm kategorileri listele",
    description="Kütüphanedeki tüm kategorileri listeler.")
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tüm kategorileri listeler.
    
    - **skip**: Atlanacak kayıt sayısı (varsayılan: 0)
    - **limit**: Listelenecek maksimum kayıt sayısı (varsayılan: 100)
    """
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

# Kitap endpoint'leri
@app.post("/books/", response_model=schemas.Book, tags=["Kitaplar"],
    summary="Yeni kitap ekle",
    description="Kütüphaneye yeni bir kitap ekler.")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Yeni bir kitap ekler.
    
    - **title**: Kitap başlığı (zorunlu)
    - **author**: Yazar adı (zorunlu)
    - **isbn**: ISBN numarası (zorunlu)
    - **publication_year**: Yayın yılı (zorunlu)
    - **category_id**: Kategori ID (zorunlu)
    """
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[schemas.Book], tags=["Kitaplar"],
    summary="Kitapları listele",
    description="Tüm kitapları listeler. Opsiyonel olarak kategori ID'ye göre filtrelenebilir.")
def read_books(skip: int = 0, limit: int = 100, category_id: int = None, db: Session = Depends(get_db)):
    """
    Kitapları listeler.
    
    - **skip**: Atlanacak kayıt sayısı (varsayılan: 0)
    - **limit**: Listelenecek maksimum kayıt sayısı (varsayılan: 100)
    - **category_id**: Filtrelenecek kategori ID (opsiyonel)
    """
    query = db.query(models.Book)
    if category_id:
        query = query.filter(models.Book.category_id == category_id)
    books = query.offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=schemas.Book, tags=["Kitaplar"],
    summary="Kitap detaylarını görüntüle",
    description="Belirtilen ID'ye sahip kitabın detaylarını gösterir.")
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Belirli bir kitabın detaylarını gösterir.
    
    - **book_id**: Görüntülenecek kitabın ID'si
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    return book

@app.put("/books/{book_id}", response_model=schemas.Book, tags=["Kitaplar"],
    summary="Kitap bilgilerini güncelle",
    description="Belirtilen ID'ye sahip kitabın bilgilerini günceller.")
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Kitap bilgilerini günceller.
    
    - **book_id**: Güncellenecek kitabın ID'si
    - **book**: Güncellenecek kitap bilgileri
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", tags=["Kitaplar"],
    summary="Kitap sil",
    description="Belirtilen ID'ye sahip kitabı siler.")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Kitabı siler.
    
    - **book_id**: Silinecek kitabın ID'si
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Kitap başarıyla silindi"}

# Ödünç alma endpoint'leri
@app.post("/loans/", response_model=schemas.Loan, tags=["Ödünç İşlemleri"],
    summary="Kitap ödünç al",
    description="Bir kitabı ödünç alma işlemi oluşturur.")
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """
    Kitap ödünç alma işlemi oluşturur.
    
    - **book_id**: Ödünç alınacak kitabın ID'si
    - **borrower_name**: Ödünç alan kişinin adı
    """
    db_book = db.query(models.Book).filter(models.Book.id == loan.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    if not db_book.available:
        raise HTTPException(status_code=400, detail="Kitap şu anda ödünç verilemez")
    
    db_loan = models.Loan(**loan.dict(), loan_date=datetime.now())
    db_book.available = False
    
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@app.put("/loans/{loan_id}/return", tags=["Ödünç İşlemleri"],
    summary="Kitap iade et",
    description="Ödünç alınan bir kitabı iade eder.")
def return_book(loan_id: int, db: Session = Depends(get_db)):
    """
    Kitap iade işlemi gerçekleştirir.
    
    - **loan_id**: İade edilecek ödünç kaydının ID'si
    """
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Ödünç kaydı bulunamadı")
    if db_loan.is_returned:
        raise HTTPException(status_code=400, detail="Bu kitap zaten iade edilmiş")
    
    db_loan.is_returned = True
    db_loan.return_date = datetime.now()
    db_loan.book.available = True
    
    db.commit()
    return {"message": "Kitap başarıyla iade edildi"}

@app.get("/loans/", response_model=List[schemas.Loan], tags=["Ödünç İşlemleri"],
    summary="Ödünç işlemlerini listele",
    description="Tüm ödünç alma işlemlerini listeler.")
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tüm ödünç işlemlerini listeler.
    
    - **skip**: Atlanacak kayıt sayısı (varsayılan: 0)
    - **limit**: Listelenecek maksimum kayıt sayısı (varsayılan: 100)
    """
    loans = db.query(models.Loan).offset(skip).limit(limit).all()
    return loans 