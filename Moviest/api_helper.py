import streamlit as st
import pandas as pd
from api_helper import get_movie_recommendations  # api_helper.py dosyasından fonksiyonu içe aktarıyoruz

# Streamlit Arayüzü
st.title('Moviest: Film Öneri Sistemi')
st.write('Sevdiğiniz film türlerini seçin ve opsiyonel olarak ek bilgileri girin. Size özel film önerileri alın!')

# Kullanıcıdan Girdi Alma

# Zorunlu: Film Türleri ve Seçim Yöntemi
st.subheader('Film Türü Seçimi')
genres = st.multiselect(
    'Film Türleri (Zorunlu)',
    ['Aksiyon', 'Komedi', 'Drama', 'Bilim Kurgu', 'Korku', 'Fantastik', 'Animasyon', 'Anime', 'Donghua'],
    help="Öneri almak için en az bir tür seçin."
)

genre_selection_method = st.radio(
    'Film Türü Seçim Yöntemi (Zorunlu)',
    ['ve', 'veya'],
    help="Seçilen türler arasında 've' veya 'veya' bağlantısı kurarak öneri yapabilirsiniz."
)

# Opsiyonel Bilgiler
st.subheader('Ek Özellikler (Opsiyonel)')
favorite_movies = st.text_area('Sevdiğiniz Filmler', placeholder='Örnek: Inception, Matrix')
favorite_books = st.text_area('Beğendiğiniz Kitaplar', placeholder='Örnek: Harry Potter, Yüzüklerin Efendisi')
favorite_series = st.text_area('Beğendiğiniz Diziler', placeholder='Örnek: Game of Thrones, Breaking Bad')
imdb_score = st.slider('Minimum IMDb Puanı', 0.0, 10.0, 0.0)
rotten_tomatoes_score = st.slider('Minimum Rotten Tomatoes Puanı', 0, 100, 0)
age_rating = st.selectbox('Yaş Sınırı', ['', 'G', 'PG', 'PG-13', 'R', 'NC-17'])
release_year = st.slider('Filmin Çıkış Yılı (Opsiyonel)', 1900, 2024, (1990, 2024))
director_preference = st.text_input('Tercih Edilen Yönetmen (Opsiyonel)', placeholder='Örnek: Christopher Nolan, Quentin Tarantino')

if st.button('Öneriler Al'):
    if not genres:
        st.error('Lütfen en az bir film türü seçin.')
    else:
        # Kullanıcıdan gelen bilgileri bir sözlükte topluyoruz
        optional_details = {
            'favorite_movies': favorite_movies.split(', ') if favorite_movies else None,
            'favorite_books': favorite_books.split(', ') if favorite_books else None,
            'favorite_series': favorite_series.split(', ') if favorite_series else None,
            'imdb_score': imdb_score if imdb_score > 0 else None,
            'rotten_tomatoes_score': rotten_tomatoes_score if rotten_tomatoes_score > 0 else None,
            'age_rating': age_rating if age_rating else None,
            'release_year': release_year if release_year else None,
            'director_preference': director_preference if director_preference else None
        }

        recommendations = get_movie_recommendations(genres, genre_selection_method, optional_details)

        # Önerilen filmleri tablo formatında görüntüleme
        st.write('Önerilen Filmler:')
        st.markdown(recommendations)
