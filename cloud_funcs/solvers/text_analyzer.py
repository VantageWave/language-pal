import os
from langchain.chat_models import ChatAnthropic
from langchain.schema import (
    HumanMessage,
)

CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
chat = None

def summarize(context):
    print("context", context)
    global chat

    if chat is None:
        chat = ChatAnthropic(anthropic_api_key = CLAUDE_API_KEY)

    messages = [HumanMessage(content=f"""
        Here is a text, in <text> tags:
        <text>
        {context}
        </text>
        You are a human, and you want to summarize it. Please provide comprehensive summary.
    """)]

    chat_response = chat(messages)

    print(chat_response.content)

    context += chat_response.content

    response = {
        'summary': chat_response.content,
        'context': context
    }

    return response

def ask_question(context, question):
    global chat

    if chat is None:
        chat = ChatAnthropic(anthropic_api_key = CLAUDE_API_KEY)

    messages = [
        HumanMessage(content=context),
        HumanMessage(content=f"""
            You are a human, and I want you to answer a question about this text. Please provide answer for the given question:
            {question}
        """)
    ]

    chat_response = chat(messages)

    print(chat_response.content)

    context += chat_response.content

    response = {
        'question': question,
        'answer': chat_response.content,
        'context': context
    }

    return response
