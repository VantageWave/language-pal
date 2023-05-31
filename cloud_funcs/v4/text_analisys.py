import json
import os
import anthropic
from langchain.chat_models import ChatAnthropic

CLOUDE_API_KEY = os.environ.get('CLOUDE_API_KEY')
anthropic_client =  anthropic.Client(CLOUDE_API_KEY)
# chat = ChatAnthropic(model="claude-v1.3-100k", anthropic_api_key = CLOUDE_API_KEY)

def summarize_text(request):
    data = request.get_json()
    context = data['context']

    prompt = anthropic.HUMAN_PROMPT + context + anthropic.AI_PROMPT

    completion = anthropic_client.completion(
        prompt=prompt, model="claude-v1.3-100k", max_tokens_to_sample=1000
    )["completion"]

    context += completion

    response = {
        'summary': completion,
        'context': context
    }

    return json.dumps(response), 200

def ask_question_text(request):
    data = request.get_json()
    context = data['context']
    problem = data['problem']
    language = data.get('language', 'en') 

    prompt = anthropic.HUMAN_PROMPT + context + problem + " response in" + language + anthropic.AI_PROMPT

    completion = anthropic_client.completion(
        prompt=prompt, model="claude-v1.3-100k", max_tokens_to_sample=1000
    )["completion"]

    context += completion

    response = {
        'question': problem,
        'solution': completion,
        'context': context
    }

    return json.dumps(response), 200
