from solvers.text_analyzer import summarize

def summarize_text(request):
    request_json = request.get_json()

    if request_json and 'context' in request_json:
        context = request_json['context']
    else:
        raise ValueError("JSON is invalid, or missing a 'context' property")
    
    # TODO user validation
    # TODO check if user has enough requests in pool

    try:
        response = summarize(context)
        return {
            'summary': response['summary'],
            'context': response['context']
        }, 200
    except Exception as e:
        return {
            'code': 'Could not summarize the text.',
            'message': 'Could not summarize the text.',
            'error': str(e)
        }, 500

# def ask_question_text(request):
#     data = request.get_json()
#     context = data['context']
#     problem = data['problem']
#     language = data.get('language', 'en') 

#     prompt = anthropic.HUMAN_PROMPT + context + problem + " response in" + language + anthropic.AI_PROMPT

#     completion = anthropic_client.completion(
#         prompt=prompt, model="claude-v1.3-100k", max_tokens_to_sample=1000
#     )["completion"]

#     context += completion

#     response = {
#         'question': problem,
#         'solution': completion,
#         'context': context
#     }

#     return json.dumps(response), 200
