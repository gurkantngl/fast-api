# Kişisel Kütüphane API

Bu proje, FastAPI kullanılarak geliştirilmiş bir kişisel kütüphane yönetim sistemidir.

## Özellikler

- Kitap ekleme, düzenleme ve silme
- Kategori yönetimi
- Kitap ödünç alma ve iade etme sistemi
- Kategoriye göre kitap filtreleme

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
uvicorn app.main:app --reload
```

3. Tarayıcınızda aşağıdaki adresi açın:
```
http://localhost:8000/docs
```

## API Endpoint'leri

### Kategoriler
- `GET /categories/`: Tüm kategorileri listele
- `POST /categories/`: Yeni kategori ekle

### Kitaplar
- `GET /books/`: Tüm kitapları listele
- `POST /books/`: Yeni kitap ekle
- `GET /books/{book_id}`: Belirli bir kitabı görüntüle
- `PUT /books/{book_id}`: Kitap bilgilerini güncelle
- `DELETE /books/{book_id}`: Kitap sil

### Ödünç İşlemleri
- `GET /loans/`: Tüm ödünç işlemlerini listele
- `POST /loans/`: Yeni ödünç verme işlemi oluştur
- `PUT /loans/{loan_id}/return`: Kitap iade işlemi 