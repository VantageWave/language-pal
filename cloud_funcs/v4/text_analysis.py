from solvers.text_analyzer import summarize, ask_question

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

def ask_question_text(request):
    request_json = request.get_json()

    if request_json and 'context' in request_json and 'question' in request_json:
        context = request_json['context']
        question = request_json['question']
    else:
        raise ValueError("JSON is invalid, or missing a 'context' or 'question' property")
    
    # TODO user validation
    # TODO check if user has enough requests in pool

    try:
        response = ask_question(context, question)
        return {
            'question': response['question'],
            'answer': response['answer'],
            'context': response['context']
        }, 200
    except Exception as e:
        return {
            'code': 'Could not answer the question.',
            'message': 'Could not answer the question.',
            'error': str(e)
        }, 500
