import openai
from api_key import openai_api_key  # api_key.py dosyasından değişkeni içe aktarıyoruz

# OpenAI API anahtarını ayarlayın
openai.api_key = openai_api_key


def get_movie_recommendations(genres, genre_selection_method, optional_details):
    """
    Bu fonksiyon, OpenAI API kullanarak kullanıcının tercihlerine göre film önerisi yapar.

    :param genres: Kullanıcının zorunlu olarak belirttiği film türleri listesi
    :param genre_selection_method: Kullanıcının film türü seçiminde kullandığı yöntem ("ve" veya "veya")
    :param optional_details: Kullanıcının opsiyonel olarak belirttiği ek bilgiler (filmler, diziler, kitaplar, vb.)
    :return: Önerilen filmler hakkında tablo formatında bilgi içeren metin
    """
    # Tür seçim mantığına göre prompt oluşturma
    if genre_selection_method == 've':
        # Kullanıcı "ve" seçtiyse, tüm türleri içeren filmler önerilecek
        genre_condition = f"Tüm türler: {', '.join(genres)}"
    else:
        # Kullanıcı "veya" seçtiyse, herhangi bir türü içeren filmler önerilecek
        genre_condition = f"Herhangi bir tür: {', '.join(genres)}"

    # Opsiyonel bilgiler için prompt oluşturma
    prompt_parts = [genre_condition]

    if optional_details.get('favorite_movies'):
        prompt_parts.append(f"Sevdiği Filmler: {', '.join(optional_details['favorite_movies'])}")
    if optional_details.get('favorite_books'):
        prompt_parts.append(f"Beğendiği Kitaplar: {', '.join(optional_details['favorite_books'])}")
    if optional_details.get('favorite_series'):
        prompt_parts.append(f"Beğendiği Diziler: {', '.join(optional_details['favorite_series'])}")
    if optional_details.get('imdb_score'):
        prompt_parts.append(f"Minimum IMDb Puanı: {optional_details['imdb_score']}")
    if optional_details.get('rotten_tomatoes_score'):
        prompt_parts.append(f"Minimum Rotten Tomatoes Puanı: {optional_details['rotten_tomatoes_score']}")
    if optional_details.get('age_rating'):
        prompt_parts.append(f"Yaş Sınırı: {optional_details['age_rating']}")
    if optional_details.get('release_year'):
        prompt_parts.append(f"Filmin Çıkış Yılı: {optional_details['release_year']}")
    if optional_details.get('director_preference'):
        prompt_parts.append(f"Tercih Edilen Yönetmen: {optional_details['director_preference']}")

    # Promptu oluşturma
    prompt = (
            "Kullanıcının tercihlerine göre 5 film önerisi yap ve her film için tablo formatında şu bilgileri ver: "
            "Film Adı, Türü, IMDb Puanı, Süresi, Yapım Ülkesi, Genel Konusu, IMDb Linki ve Bu filmin neden önerildiği."
            " İşte kullanıcının tercihleri: " + ". ".join(prompt_parts) + "."
    )

    # OpenAI API çağrısı
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that provides detailed movie recommendations in a table format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return response['choices'][0]['message']['content'].strip()
