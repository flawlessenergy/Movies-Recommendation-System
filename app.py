import pickle
import streamlit as st
import pandas as pd
import requests
movies_dict=pickle.load(open("movie_dict.pkl",'rb'))
movies=pd.DataFrame(movies_dict)
st.title("Movies Recommendor System")
similarity = pickle.load(open('similarity.pkl','rb'))

select_movie_name=st.selectbox("How would you like to be contacted",movies['title'].values)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()

    full_path = "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances=similarity[index]
    movies_list =sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster


if st.button('Recommend'):
    names,poster= recommend(select_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.header(names[0])
        st.image(poster[0])
    with col2:
        st.header(names[1])
        st.image(poster[1])
    with col3:
        st.header(names[2])
        st.image(poster[2])
    with col4:
        st.header(names[3])
        st.image(poster[3])
    with col5:
        st.header(names[4])
        st.image(poster[4])

