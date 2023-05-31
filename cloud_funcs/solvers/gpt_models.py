from langchain.chat_models import ChatOpenAI

def get_text_solver_models(api_key):
    chat = ChatOpenAI(
        openai_api_key=api_key,
        client="gpt-3.5-turbo",
        temperature=0.25,
        n=1,
        max_tokens=1200,
    )

    answer_extractor = ChatOpenAI(
        openai_api_key=api_key,
        client="gpt-3.5-turbo",
        temperature=0.0,
        n=1,
        max_tokens=1200,
    )
    return chat, answer_extractor
