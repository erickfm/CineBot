import streamlit as st
import os
from CineBot.functions import chatgpt
from tmdbv3api import Movie

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["SERPAPI_API_KEY"] = st.secrets["SERPAPI_API_KEY"]
os.environ["GOOGLE_CSE_ID"] = st.secrets["GOOGLE_CSE_ID"]
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["TMDB_API_KEY"] = st.secrets["TMDB_API_KEY"]
movie = Movie()

st.set_page_config(page_title='CineBot', page_icon="🎞", initial_sidebar_state='collapsed')
st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 14rem;}}
    </style>
''',unsafe_allow_html=True)
with st.sidebar:
    cinebot_page = st.button('CineBot', type='secondary', use_container_width=1)
    about_page = st.button('About', type='secondary', use_container_width=1)
    if not about_page:
        cinebot_page = True
if cinebot_page:
    st.markdown('# CineBot 🤖 \nYour AI Film Recommender')
    form = st.form('form')
    film = form.text_input('Film', 'Princess Mononoke (1997)')
    number_of_recs = form.number_input(label='Number of recommendations', min_value=1, value=3, step=1)
    rec_criterion = form.text_input('Recommendation Criterion (optional)')
    # temperature = form.slider('Variety', 0.0, 1.0, 1.0)
    submit = form.form_submit_button('Submit')

    if submit:
        prompt = f"""Given a film, a number of recommendations desired, and an optional recommendation criterion, return a list of movie recommendations. Do not recommend TV shows like The Walking Dead or Breaking Bad.
    
        Film: Spirited Away (2001)
        Number of Recommendations: 3
        Recommendation Criterion: same/similar director
        Recommendations: My Neighbor Totoro (1988) || Porco Rosso (1992) || Lupin III: The Castle of Cagliostro (1979)
    
        Film: pride and prejudice
        Number of Recommendations: 5
        Recommendation Criterion: 
        Recommendations: Sense and Sensibility (1995) || Emma (2020) || Little Women (2019) || Atonement (2007) || Jane Eyre (2011)
    
        Film: {film}
        Number of Recommendations: {number_of_recs}
        Recommendation Criterion: {rec_criterion}
        Recommendations: 
        """
        try:
            with st.spinner("Thinking..."):
                # st.text(prompt)
                response = chatgpt(prompt)
                # st.write(response)
                films = {i.split(' (')[0]: {"release year": i.split(' (')[1].split(')')[0]} for i in response.split(' || ')}
                # st.text(films)
            with st.spinner("Fetching results..."):
                for film in films:
                    search_results = movie.search(film)
                    n = 0
                    result = search_results[n]
                    while result.release_date.split('-')[0] != films[film]["release year"]:
                        n += 1
                        result = search_results[n]
                    col1, col2 = st.columns([1, 1])
                    col1.image("https://image.tmdb.org/t/p/w500/" + result.poster_path)
                    col2.write(f"### [{result.title}](https://www.themoviedb.org/movie/{result.id}) ({result.release_date.split('-')[0]})")
                    col2.write(result.overview)
        except:
            try:
                with st.spinner("Thinking..."):
                    # st.text(prompt)
                    response = chatgpt(prompt)
                    # st.write(response)
                    films = {i.split(' (')[0]: {"release year": i.split(' (')[1].split(')')[0]} for i in
                             response.split(' || ')}
                    # st.text(films)
                with st.spinner("Fetching results..."):
                    for film in films:
                        search_results = movie.search(film)
                        n = 0
                        result = search_results[n]
                        while result.release_date.split('-')[0] != films[film]["release year"]:
                            n += 1
                            result = search_results[n]
                        col1, col2 = st.columns([1, 1])
                        col1.image("https://image.tmdb.org/t/p/w500/" + result.poster_path)
                        col2.write(f"### [{result.title}](https://www.themoviedb.org/movie/{result.id}) ({result.release_date.split('-')[0]})")
                        col2.write(result.overview)
            except Exception as e:
                st.error("I'm sorry, I got confused somewhere along the way. Please try again, I'll give it another shot.")
if about_page:
    st.markdown('# About 📝 \n')
    st.write('Built by Erick Martinez using OpenAI, LangChain, TMDB, and Streamlit.'
             '\n\nModel is tuned for more variety in answers'
             '\n\nChatGPT is trained on data limited to September 2021'
             '\n\n[Github Repo](https://github.com/erickfm/CineBot)')