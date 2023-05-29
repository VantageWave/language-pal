import json
import os
from flask import Flask, request
import anthropic
import unittest
import pytest
from dotenv import load_dotenv

load_dotenv()

CLOUDE_API_KEY = os.getenv('CLOUDE_API_KEY')
anthropic_client =  anthropic.Client(CLOUDE_API_KEY)

PRICE_PROMPT = 1.102E-5
PRICE_COMPLETION = 3.268E-5

app = firebase_admin.initialize_app()

# to be removed
def count_used_tokens(prompt, completion):
    prompt_token_count = anthropic.count_tokens(prompt)
    completion_token_count = anthropic.count_tokens(completion)

    prompt_cost = prompt_token_count * PRICE_PROMPT
    completion_cost = completion_token_count * PRICE_COMPLETION

    total_cost = prompt_cost + completion_cost

    return (
        "🟡 Used tokens this round: "
        + f"Prompt: {prompt_token_count} tokens, "
        + f"Completion: {completion_token_count} tokens - "
        + f"{format(total_cost, '.5f')} USD)"
    )


app = Flask(__name__)

@app.route('/v4_summarizeText', methods=['POST'])
def v4_summarizeText():
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

    return json.dumps(response)  

@app.route('/v4_askQuestionText', methods=['POST'])
def v4_askQuestionText():
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

    return json.dumps(response)  

if __name__ == '__main__':
    app.run()