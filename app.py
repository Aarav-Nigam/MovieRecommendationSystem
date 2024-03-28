import pickle
import streamlit as st
import os
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('API')}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to recommend movies
def recommend(movie, distance):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:distance+1]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(layout="centered")
st.title('Movie Recommender System')


# Custom CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://t4.ftcdn.net/jpg/02/71/50/69/360_F_271506927_WWFfd92jDIIDx6DgMflakU14o5jRPgBm.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load movie data and similarity matrix
with st.spinner('Loading...'):
    movies = pickle.load(open('saved_models/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('saved_models/similarity.pkl', 'rb'))

# Movie selection dropdown
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

distance = st.slider("Select number of Recommendations", min_value=3, max_value=20, value=6)

# Button to show recommendations
if st.button('Show Recommendation'):
    with st.spinner('Fetching Recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, distance)
    num_movies = len(recommended_movie_names)
    num_columns = min(num_movies, 4)  # Limit to a maximum of 5 columns
    num_rows = -(-num_movies // num_columns)  # Ceiling division to calculate the number of rows
    
    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_movies:
                with cols[j]:
                    st.subheader(recommended_movie_names[index])
                    st.image(recommended_movie_posters[index], use_column_width=True)

# Define the footer HTML content with CSS for sticky positioning
footer = '''
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
}
</style>
<div class="footer">
    <p>Developed  by <a style='display: block; text-align: center; color:orange ;font-weight: bold; font-size:20px' href="https://portfolio-aarav.netlify.app/" target="_blank">~Aarav Nigam</a></p>
</div>
'''

# Display the footer using st.markdown
st.markdown(footer, unsafe_allow_html=True)
