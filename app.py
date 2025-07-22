import pickle
import streamlit as st
import gdown
import os
import requests

# Function to download files from Google Drive using gdown
def download_file_from_drive(file_id, destination):
    if not os.path.exists(destination):
        # st.write(f"Downloading {destination}...")
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, destination, quiet=False)
        # st.write(f"{destination} downloaded successfully. Size: {os.path.getsize(destination)} bytes.")
    #else:
       #  st.write(f"{destination} already exists. Skipping download.")

# Download the .pkl files if not present
movies_file_id = '1Cdi5TbnaPbp5lDjKiZ8KWkAO8P0YJ6fY'
similarity_file_id = '1eVHczxlSOz-aKZqW_1A2KhE61SmNNaxX'

download_file_from_drive(movies_file_id, 'new_movies.pkl')
download_file_from_drive(similarity_file_id, 'new_similarity.pkl')

# Load the downloaded pickle files
movies = pickle.load(open('new_movies.pkl', 'rb'))
similarity = pickle.load(open('new_similarity.pkl', 'rb'))

# Fetch poster from TMDB
def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=55a1eb05ce3d68972a463b781ef08a30&language=en-US"
    try:
        data = requests.get(url, timeout=10)
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for movie ID {id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
