import streamlit as st
import requests
from datetime import datetime

# API URL'si
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Kütüphane Yönetim Sistemi",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Kütüphane Yönetim Sistemi")

# Sidebar menüsü
menu = st.sidebar.selectbox(
    "Menü",
    ["Ana Sayfa", "Kitaplar", "Kategoriler", "Ödünç İşlemleri"]
)

if menu == "Ana Sayfa":
    st.header("Hoş Geldiniz!")
    st.write("""
    Bu uygulama ile kütüphanenizi kolayca yönetebilirsiniz.
    
    ### Özellikler:
    - 📖 Kitap ekleme, düzenleme ve silme
    - 📑 Kategori yönetimi
    - 📌 Kitap ödünç alma ve iade etme
    - 🔍 Kategoriye göre kitap filtreleme
    """)

elif menu == "Kitaplar":
    st.header("Kitap Yönetimi")
    
    tab1, tab2 = st.tabs(["Kitap Listesi", "Yeni Kitap Ekle"])
    
    with tab1:
        # Kategori filtresi
        try:
            categories = requests.get(f"{API_URL}/categories/").json()
            category_filter = st.selectbox(
                "Kategoriye Göre Filtrele",
                ["Tümü"] + [cat["name"] for cat in categories]
            )
            
            # Kitapları listele
            if category_filter == "Tümü":
                books = requests.get(f"{API_URL}/books/").json()
            else:
                selected_category = next(cat for cat in categories if cat["name"] == category_filter)
                books = requests.get(f"{API_URL}/books/?category_id={selected_category['id']}").json()
            
            for book in books:
                with st.expander(f"{book['title']} - {book['author']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ISBN:** {book['isbn']}")
                        st.write(f"**Yayın Yılı:** {book['publication_year']}")
                    with col2:
                        st.write(f"**Durum:** {'Müsait' if book['available'] else 'Ödünç Verilmiş'}")
                        if st.button("Sil", key=f"delete_{book['id']}"):
                            response = requests.delete(f"{API_URL}/books/{book['id']}")
                            if response.status_code == 200:
                                st.success("Kitap başarıyla silindi!")
                                st.rerun()
                            
        except Exception as e:
            st.error(f"Kitaplar yüklenirken bir hata oluştu: {str(e)}")
    
    with tab2:
        try:
            categories = requests.get(f"{API_URL}/categories/").json()
            with st.form("new_book_form"):
                title = st.text_input("Kitap Adı")
                author = st.text_input("Yazar")
                isbn = st.text_input("ISBN")
                publication_year = st.number_input("Yayın Yılı", min_value=1000, max_value=datetime.now().year)
                category_id = st.selectbox(
                    "Kategori",
                    options=[cat["id"] for cat in categories],
                    format_func=lambda x: next(cat["name"] for cat in categories if cat["id"] == x)
                )
                
                if st.form_submit_button("Kitap Ekle"):
                    response = requests.post(
                        f"{API_URL}/books/",
                        json={
                            "title": title,
                            "author": author,
                            "isbn": isbn,
                            "publication_year": publication_year,
                            "category_id": category_id
                        }
                    )
                    if response.status_code == 200:
                        st.success("Kitap başarıyla eklendi!")
                    else:
                        st.error("Kitap eklenirken bir hata oluştu!")
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

elif menu == "Kategoriler":
    st.header("Kategori Yönetimi")
    
    tab1, tab2 = st.tabs(["Kategori Listesi", "Yeni Kategori Ekle"])
    
    with tab1:
        try:
            categories = requests.get(f"{API_URL}/categories/").json()
            for category in categories:
                with st.expander(category["name"]):
                    st.write(f"**Açıklama:** {category['description']}")
        except Exception as e:
            st.error(f"Kategoriler yüklenirken bir hata oluştu: {str(e)}")
    
    with tab2:
        with st.form("new_category_form"):
            name = st.text_input("Kategori Adı")
            description = st.text_area("Açıklama")
            
            if st.form_submit_button("Kategori Ekle"):
                response = requests.post(
                    f"{API_URL}/categories/",
                    json={
                        "name": name,
                        "description": description
                    }
                )
                if response.status_code == 200:
                    st.success("Kategori başarıyla eklendi!")
                else:
                    st.error("Kategori eklenirken bir hata oluştu!")

elif menu == "Ödünç İşlemleri":
    st.header("Ödünç İşlemleri")
    
    tab1, tab2, tab3 = st.tabs(["Ödünç Al", "İade Et", "Ödünç Kayıtları"])
    
    with tab1:
        try:
            books = requests.get(f"{API_URL}/books/").json()
            available_books = [book for book in books if book["available"]]
            
            with st.form("loan_form"):
                book_id = st.selectbox(
                    "Kitap",
                    options=[book["id"] for book in available_books],
                    format_func=lambda x: next(book["title"] for book in available_books if book["id"] == x)
                )
                borrower_name = st.text_input("Ödünç Alan Kişi")
                
                if st.form_submit_button("Ödünç Ver"):
                    response = requests.post(
                        f"{API_URL}/loans/",
                        json={
                            "book_id": book_id,
                            "borrower_name": borrower_name
                        }
                    )
                    if response.status_code == 200:
                        st.success("Kitap başarıyla ödünç verildi!")
                    else:
                        st.error("Ödünç verme işlemi başarısız oldu!")
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")
    
    with tab2:
        try:
            loans = requests.get(f"{API_URL}/loans/").json()
            active_loans = [loan for loan in loans if not loan["is_returned"]]
            
            if active_loans:
                for loan in active_loans:
                    book = requests.get(f"{API_URL}/books/{loan['book_id']}").json()
                    with st.expander(f"{book['title']} - {loan['borrower_name']}"):
                        st.write(f"Ödünç Alma Tarihi: {loan['loan_date']}")
                        if st.button("İade Et", key=f"return_{loan['id']}"):
                            response = requests.put(f"{API_URL}/loans/{loan['id']}/return")
                            if response.status_code == 200:
                                st.success("Kitap başarıyla iade edildi!")
                                st.rerun()
            else:
                st.info("İade edilmemiş ödünç kayıt bulunmamaktadır.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")
    
    with tab3:
        try:
            loans = requests.get(f"{API_URL}/loans/").json()
            for loan in loans:
                book = requests.get(f"{API_URL}/books/{loan['book_id']}").json()
                with st.expander(f"{book['title']} - {loan['borrower_name']}"):
                    st.write(f"**Ödünç Alma Tarihi:** {loan['loan_date']}")
                    st.write(f"**İade Tarihi:** {loan['return_date'] if loan['return_date'] else 'İade Edilmemiş'}")
                    st.write(f"**Durum:** {'İade Edildi' if loan['is_returned'] else 'Ödünç Verilmiş'}")
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}") 