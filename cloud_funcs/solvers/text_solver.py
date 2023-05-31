from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

templates_pl = {
    "main": "Jesteś nauczycielem matematyki, pomagającym w rozwiązywaniu zadań matematycznych. Rozwiąż zadanie i przedstaw dokładnie swój tok rozumowania.",
    "human-main": "Q: {mathProblemText}\nA: Rozwiąż zadanie krok po kroku.",
}

templates_en = {
    "main": "You are a math teacher, helping with solving math problems. Your task is to solve the problem and present the solution step by step.",
    "human-main": "Q: {mathProblemText}\nA: Solve step by step",
}

def get_template(template_name, language):
    if language == "pl":
        return templates_pl[template_name]
    elif language == "en":
        return templates_en[template_name]
    else:
        raise ValueError("Language not supported")

def get_prompt(math_problem_text, language):
    template = get_template("main", language)
    system_message = SystemMessagePromptTemplate.from_template(template)
    human_template = get_template("human-main", language)
    human_message = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    return chat_prompt.format_messages(mathProblemText=math_problem_text)

def get_solution(chat_model, problem_text, language="pl"):
    result = chat_model.generate([get_prompt(problem_text, language)])
    result_text = result.generations[0][0].text if result.generations and len(result.generations) == 1 else ""
    if result_text != "":
        return {
            'answer': result_text,
            'error': ''
        }
    return {
        'answer': '',
        'error': 'Could not generate solution'
    }
