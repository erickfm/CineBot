import streamlit as st
import os
from CineBot.functions import recommend, critique, get_rec_prompt, get_crit_prompt
from CineBot.constants import default_link, alt_link, cinebot_image_path, github_image_path, patreon_image_path, error_response
from tmdbv3api import Movie

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
# os.environ["SERPAPI_API_KEY"] = st.secrets["SERPAPI_API_KEY"]
# os.environ["GOOGLE_CSE_ID"] = st.secrets["GOOGLE_CSE_ID"]
# os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["TMDB_API_KEY"] = st.secrets["TMDB_API_KEY"]
movie = Movie()

st.set_page_config(page_title='CineBot', page_icon="images/cinebot2_small.png", initial_sidebar_state='collapsed')
st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 14rem;}}
    </style>
''', unsafe_allow_html=True)

query_params = st.experimental_get_query_params()

with st.sidebar:
    cinebot_page = st.button('CineBot', use_container_width=1)
    about_page = st.button('About', use_container_width=1)
    if not about_page:
        cinebot_page = True

if 'critic' in query_params:
    if cinebot_page:
        cola, colb = st.columns([2, 9])
        cola.markdown(
            f"""<a target="_self" href="{default_link}"><img src="{cinebot_image_path}" style="display:block;" width="100%" height="100%"></a>""",
            unsafe_allow_html=1)
        colb.markdown('# CineBot \nYour AI Film Critic 😈')
        form = st.form('form')
        film = form.text_input('Your Favorite Film', 'Fight Club (1999)')
        if form.form_submit_button('Submit'):
            prompt = get_crit_prompt(film)
            try:
                critique(prompt)
            except Exception as e:
                critique(prompt)
else:
    if cinebot_page:
        cola, colb = st.columns([2,9])
        cola.markdown(f"""<a target="_self" href="{alt_link}"><img src="{cinebot_image_path}" style="display:block;" width="100%" height="100%"></a>""", unsafe_allow_html=1)
        colb.markdown('# CineBot \nYour AI Film Recommender')
        form = st.form('form')
        film = form.text_input('Film', 'Princess Mononoke (1997)')
        number_of_recs = form.number_input(label='Number of recommendations', min_value=1, value=3, step=1)
        rec_criterion = form.text_input('Recommendation Criterion (optional)')
        if form.form_submit_button('Submit'):
            prompt = get_rec_prompt(film, number_of_recs, rec_criterion)
            try:
                recommend(prompt, movie)
            except Exception as e:
                try:
                    recommend(prompt, movie)
                except Exception as e:
                    st.error(error_response)
if about_page:
    st.markdown('# About \n')
    st.write('Built by [Erick Martinez](https://github.com/erickfm) using OpenAI, LangChain, TMDB, and Streamlit. CineBot icons by [Megan Cerminaro](https://www.megancerminaro.com/)'
             '\n\nModel is tuned for more variety in answers. ChatGPT is trained on data limited to September 2021.')
    st.markdown(f"""<div><a href="https://github.com/erickfm/CineBot"><img src="{github_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a> 
    <a href="https://www.patreon.com/ErickFMartinez"><img src="{patreon_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a></div>""", unsafe_allow_html=1)
