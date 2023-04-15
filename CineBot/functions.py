from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature=1, model_name='gpt-3.5-turbo')
def chatgpt(content):
    """Useful knowledgeable assistant. Input should be a search query."""
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=content)
    ]
    return chat(messages).content