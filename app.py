import streamlit as st
import pickle as pk
import pandas as pd 
import numpy as np
# import imdb
import requests

# ia = imdb.IMDb()

with open('similarity.pkl', 'rb') as f:  # 'rb' stands for read binary mode
    similarity = pk.load(f)
        
with open('movies.pkl', 'rb') as f:  # 'rb' stands for read binary mode
    db = pk.load(f)

# similarity = pd.DataFrame(sim)
movies = pd.DataFrame(db)

# def fetch_poster(movie_title):
#     search_results = ia.search_movie(movie_title)

#     # Get the first search result (assuming it's the most relevant)
#     if search_results:
#         movie_id = search_results[0].movieID
#         movie = ia.get_movie(movie_id)

#         # Get the poster URL
#         if 'cover url' in movie:
#             return movie['cover url']
def fetch_poster(movie_title):
    # Construct the OMDB API request URL
    # omdb_api_key = "YOUR_OMDB_API_KEY"  # Replace with your OMDB API key
    omdb_url = f"http://www.omdbapi.com/?apikey=abc4c56c&t={movie_title}"

    # Send a request to the OMDB API
    response = requests.get(omdb_url)
    data = response.json()

    # Check if the response contains a valid poster URL
    # if "Poster" in data and data["Poster"] != "N/A":
        
    # else:
    #     return None
    return data["Poster"]
        
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    dist = similarity[index]
    movies_list = sorted(list(enumerate(dist)),reverse = True,key = lambda x : x[1])[1:9]
    recommend_movies = []
    recommend_movies_poster  = []
    for i in movies_list:
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movies.iloc[i[0]].title))
    return  recommend_movies,recommend_movies_poster



st.title("Movies Recommendation system")


movies_list = movies['title'].values

selected_movie = st.selectbox(
    'Enter Movie for Other Recommendation',
    movies_list)

st.button("Reset", type="primary")

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])