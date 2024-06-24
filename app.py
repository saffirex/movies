import streamlit as st
import pickle
import pandas as pd
import requests

top_n = 10
request_url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
poster_base_url = "https://image.tmdb.org/t/p/w500"

movie_dict = pickle.load(open("./movies.pkl", "rb"))
similarity_matrix = pickle.load(open("./similarity_matrix.pkl", "rb"))

available_movies = movie_dict["title"].values()
mov_df = pd.DataFrame(movie_dict)


def get_poster(movie_id):
    response = requests.get(request_url.format(movie_id = str(movie_id), api_key = st.secrets["api_key"]))
    data = response.json()
    poster_path = data["poster_path"]

    return poster_base_url + poster_path

def get_recommendations(movie_name):
    #.index returns all the indices. In this case, all the indices in the subsetted mov_df, essentially giving the index for movie_name
    movie_index = mov_df[mov_df["title"] == movie_name].index[0]
    similarities_for_movie_name = similarity_matrix[movie_index]
    top_similar_movies = sorted(list(enumerate(similarities_for_movie_name)), reverse=True, key= lambda x: x[1])[:top_n]

    recommendation_titles = []
    recommendation_posters =[]
    for i in top_similar_movies:
        index = i[0]
        movie_id = mov_df.iloc[i[0]].id
        recommendation_posters.append(get_poster(movie_id))
        recommendation_titles.append(mov_df.iloc[index].title)
    
    return recommendation_titles, recommendation_posters


st.title("Get Movie Recommendations")
choice = st.selectbox(
    "Choose a movie",
    available_movies)

st.write("You Selected: ", choice)
get_button = st.button("Get Recommendations", type="primary")
st.write("")
st.write("Recommendations: ")

if get_button:
    recommendation_titles, recommendation_posters = get_recommendations(choice)
    
    for row_num in range(3):
        cols = st.columns(3, vertical_alignment="bottom")

        for i, col in enumerate(cols, start=1): #start at 1 because we shouldnt be showing the choice movie itself
            with col:
                st.subheader(recommendation_titles[row_num*3+i])
                st.image(recommendation_posters[row_num*3+i])

    
    
