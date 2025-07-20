import pickle
import streamlit as st
import requests
import os

# Function to download files from Google Drive or other direct link
def download_file(url, destination):
    if not os.path.exists(destination):
        st.write(f"Downloading {destination}...")
        response = requests.get(url)
        with open(destination, 'wb') as f:
            f.write(response.content)
        st.write(f"{destination} downloaded successfully.")
    else:
        st.write(f"{destination} already exists. Skipping download.")

# Download the .pkl files if not present
movies_url = 'https://drive.google.com/uc?export=download&id=1tGjr3L_QbSapZ7hGuiNXpdEhpO9aqW20'

similarity_url = 'https://drive.google.com/uc?export=download&id=1juJfqd1qkw6hoMbtPWqeQUlEHxKFDQ0J' 


download_file(movies_url, 'movies.pkl')
download_file(similarity_url, 'similarity.pkl')


# Load the downloaded pickle files
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Fetch poster from TMDB
def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=55a1eb05ce3d68972a463b781ef08a30&language=en-US".format(id)
    try:
        data = requests.get(url, timeout=10)
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
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
        id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(id))
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
