import functions_framework
from v4.text_analysis import summarize_text, ask_question_text

@functions_framework.http
def v4_summarizeText(request):
    return summarize_text(request)
    
@functions_framework.http
def v4_askQuestionText(request):
    return ask_question_text(request)
