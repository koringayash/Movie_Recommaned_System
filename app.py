import streamlit as st
import pickle
import requests

st.title('Movie Recommender System')
movie_list = pickle.load(open('movies.pkl','rb'))
# similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2e1a8cb17a1f3803c906e5635f4ccfa9&language=en-US'.format(movie_id))
    data = response.json()
    if 'poster_path' not in data.keys():
        return 'images.jpg'
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']

similarity1 = pickle.load(open('similarity1.pkl','rb'))
similarity2 = pickle.load(open('similarity2.pkl','rb'))
similarity3 = pickle.load(open('similarity3.pkl','rb'))
similarity4 = pickle.load(open('similarity4.pkl','rb'))
similarity5 = pickle.load(open('similarity5.pkl','rb'))

def recommendOnGenres(movie):
    movie_index = movie_list[movie_list['title']==movie].index[0]
    distances = similarity1[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    movies = []
    for i in movies_list:
        movies.append(movie_list.iloc[i[0]].title)
        
    return movies

def recommendOnKeywords(movie):
    movie_index = movie_list[movie_list['title']==movie].index[0]
    distances = similarity2[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    movies = []
    for i in movies_list:
        movies.append(movie_list.iloc[i[0]].title)
        
    return movies

def recommendOnCast(movie):
    movie_index = movie_list[movie_list['title']==movie].index[0]
    distances = similarity3[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    movies = []
    for i in movies_list:
        movies.append(movie_list.iloc[i[0]].title)
        
    return movies
        
def recommendOnDirector(movie):
    movie_index = movie_list[movie_list['title']==movie].index[0]
    distances = similarity4[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    movies = []
    for i in movies_list:
        movies.append(movie_list.iloc[i[0]].title)
        
    return movies
        
def recommendOnProducer(movie):
    movie_index = movie_list[movie_list['title']==movie].index[0]
    distances = similarity5[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    movies = []
    for i in movies_list:
        movies.append(movie_list.iloc[i[0]].title)
        
    return movies

def function(movieList,movieDictionary,weight):
    for movie in movieList:
        if movie not in movieDictionary:
            movieDictionary[movie] = 0
        movieDictionary[movie] = movieDictionary[movie] + weight
        
    return movieDictionary

def recommend(movie_name,genresW,keywordsW,castW,directorW,producerW):
    # movie_index = movie_list[movie_list['title'] == movie].index[0]
    # distances = similarity[movie_index]
    # movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # genresW = 4
    # keywordsW = 3
    # castW = 3
    # directorW = 2
    # producerW = 1

    movieDictionary = {}

    movieDictionary = function(recommendOnGenres(movie_name),movieDictionary,genresW)
    movieDictionary = function(recommendOnKeywords(movie_name),movieDictionary,keywordsW)
    movieDictionary = function(recommendOnCast(movie_name),movieDictionary,castW)
    movieDictionary = function(recommendOnDirector(movie_name),movieDictionary,directorW)
    movieDictionary = function(recommendOnProducer(movie_name),movieDictionary,producerW)

    movieDictionary = sorted(movieDictionary.items(), key=lambda x: x[1], reverse=True)

    reco_movies = []
    for movie in movieDictionary:
        reco_movies.append(movie[0])
        if len(reco_movies)==5:
            break
            

    recommend_movies = []
    recommend_movies_posters = []
    for i in reco_movies:
        recommend_movies_posters.append(fetch_poster(movie_list.loc[movie_list['title']==i]['movie_id'].values[0]))
        recommend_movies.append(i)

    return recommend_movies,recommend_movies_posters

selected_movie_name = st.selectbox("Enter movie's name...",(list(movie_list['title'].values)))

genresW = st.slider('Genres', 1, 5, 4)
keywordsW = st.slider('Story', 1, 5, 3)
castW = st.slider('Cast', 1, 5, 3)
directorW = st.slider('Director', 1, 5, 2)
producerW = st.slider('Producer', 1, 5, 1)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name,genresW,keywordsW,castW,directorW,producerW)
    col1,col2,col3,col4,col5 = st.columns(5)
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