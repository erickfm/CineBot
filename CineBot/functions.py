from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import streamlit as st
chat = ChatOpenAI(temperature=1, model_name='gpt-3.5-turbo')


def chatgpt(content, sys="You are a helpful assistant."):
    """Useful knowledgeable assistant. Input should be a search query."""
    messages = [
        SystemMessage(content=sys),
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
        response = chatgpt(prompt, sys="You are a sarcastic critic.")
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
    prompt = f"""Given a user's favorite film, return a sarcastic critique of the user except if the user's favorite film is Pride and Prejudice (2005).

    Favorite film: spirited away
    Critique of user: Oh how cute.
    
    Favorite film: the matrix
    Critique of user: Are you one of those people who think they're living in a simulation? Because if so, you might want to take a break from sci-fi films and step outside for a bit.
    
    Favorite film: pulp fiction
    Critique of user: Another Tarantino fanboy? How original.
    
    Favorite film: Pokemon: The First Movie (1998)
    Critique of user: Sorry, I didn't realize I was assisting a 7-year-old.
    
    Favorite film: the mummy
    Critique of user: Wow, a film that accurately reflects your taste in ancient history - outdated and corny.
    
    Favorite film: {film}
    Critique of user:
    """
    return prompt
