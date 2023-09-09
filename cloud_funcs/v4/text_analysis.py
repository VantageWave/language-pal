from solvers.text_analyzer import summarize, ask_question
from utils.utils import verify_user, check_user_tokens, update_user_token

def summarize_text(request):
    request_json = request.get_json()

    if request_json and 'context' in request_json:
        context = request_json['context']
        lang = request_json['lang']
    else:
        raise ValueError("JSON is invalid, or missing a 'context' property")

    if request_json and 'lang' in request_json:
        language = request_json['lang']
    else:
        language = 'en'
    
    user = verify_user(request)
    if isinstance(user, (tuple)):
        return user

    checkTokens = check_user_tokens(user)
    if isinstance(checkTokens, (tuple)):
        print(checkTokens)
        return checkTokens

    try:
        response = summarize(context, lang)
        update_user_token(user)
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
        lang = request_json['lang']
    else:
        raise ValueError("JSON is invalid, or missing a 'context' or 'question' property")
    
    user = verify_user(request)
    if isinstance(user, (tuple)):
        return user

    checkTokens = check_user_tokens(user)
    if isinstance(checkTokens, (tuple)):
        return checkTokens

    try:
        response = ask_question(context, question, lang)
        update_user_token(user)
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
