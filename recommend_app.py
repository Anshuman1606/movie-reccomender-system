import pandas as pd
import streamlit as st
import pickle
import requests


#import time

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0383b81ddc27b5bf5553774e61ecb3bf&language=en-US".format(
        movie_id)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        print(f"Error fetching poster: {e}")

    # Fallback placeholder image if request fails or poster doesn't exist
    return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"


st.title('Movies Recommender System')
movies=pickle.load(open('movies_dict.pkl', 'rb'))
movies=pd.DataFrame(movies)
similarity=pickle.load(open('similarity.pkl', 'rb'))
movies_list=movies['title'].values

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:5]
    recommended_movies_names= []
    recommended_movies_posters=[]

    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names,recommended_movies_posters


selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
     movies_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])


