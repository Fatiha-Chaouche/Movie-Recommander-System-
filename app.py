import pickle
import streamlit as st
import requests

# Custom CSS for background and styling
st.markdown(
    """
    <style>
    body {
        background-color: #4D1408; /* Light blue background color */
        background-size: cover;
        background-attachment: fixed;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
    }
    .block-container {
        padding: 2rem;
        border-radius: 10px;
    }
    h1 {
        font-family: 'Trebuchet MS', sans-serif;
        color: #333;
    }
    p {
        font-family: 'Trebuchet MS', sans-serif;
        color: #666;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.title('MovieMatch')
st.markdown("""
## Welcome to MovieMatch

MovieMatch is a movie recommendation system that helps you discover new movies based on your preferences. Just select a movie you like, and we'll recommend five movies you'll love!

""")

try:
    movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")

if 'movies' in globals() and 'similarity' in globals():
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movies['title'].values
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            st.markdown(f"### {name}")
            st.image(poster, use_column_width=True)
