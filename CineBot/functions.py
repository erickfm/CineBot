from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import streamlit as st
chat = ChatOpenAI(temperature=1, model_name='gpt-3.5-turbo')


def chatgpt(content):
    """Useful knowledgeable assistant. Input should be a search query."""
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=content)
    ]
    return chat(messages).content


def recommend(prompt, movie):
    with st.spinner("Thinking..."):
        response = chatgpt(prompt)
        films = {i.split(' (')[0]: {"release year": i.split(' (')[1].split(')')[0]} for i in response.split(' || ')}
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


def critique(prompt):
    with st.spinner("Thinking..."):
        response = chatgpt(prompt)
        st.write(response)


def get_rec_prompt(film, number_of_recs, rec_criterion):
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
    return prompt


def get_crit_prompt(film):
    prompt = f"""Given a user's favorite film, return an assumptive sarcastic critique of the user except if the user's favorite film is Pride and Prejudice.

    Film: Spirited Away (2001)
    Critique: Are you a baby?
    
    Film: {film}
    Critique:
    """
    return prompt
