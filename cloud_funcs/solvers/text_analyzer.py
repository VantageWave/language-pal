import os
import json
from langchain.chat_models import ChatAnthropic
from langchain.schema import (
    HumanMessage,
)

CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
chat = None

def summarize(context, lang = "en"):
    print("context", context)
    global chat

    messagesFile = open(f"./i18n/${lang}.json")
    messages = json.load(messagesFile)

    if chat is None:
        chat = ChatAnthropic(anthropic_api_key = CLAUDE_API_KEY)

    message = [HumanMessage(content=f"""
        {messages["textSummarize1"]}
        <text>
        {context}
        </text>
       {messages["textSummarize2"]}
    """)]

    chat_response = chat(message)

    print(chat_response.content)

    context += chat_response.content

    messages.close()

    response = {
        'summary': chat_response.content,
        'context': context
    }

    return response

def ask_question(context, question, lang = "en"):
    global chat

    messagesFile = open(f"./i18n/${lang}.json")
    messages = json.load(messagesFile)

    if chat is None:
        chat = ChatAnthropic(anthropic_api_key = CLAUDE_API_KEY)

    message = [
        HumanMessage(content=context),
        HumanMessage(content=f"""
            {messages["askQuestion"]}
            {question}
        """)
    ]

    chat_response = chat(message)

    print(chat_response.content)

    context += chat_response.content

    messages.close()

    response = {
        'question': question,
        'answer': chat_response.content,
        'context': context
    }

    return response
