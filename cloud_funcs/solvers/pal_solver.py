from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
import re
import string
import numpy as np
from sympy import solve, sympify, Symbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def reformat_equations_from_peano(eq_list):
    result = ''
    for eq in eq_list.split(','):
        if 'eq' in eq:
            if len(result) == 0:
                result += eq[eq.index('eq') + 2:]
            else:
                result += ', ' + eq[eq.index('eq') + 2:]
        elif 'answer' in eq:
            if len(result) == 0:
                result += eq[eq.index('answer') + 6:].strip() + ' = ?'
            else:
                result += ', ' + eq[eq.index('answer') + 6:].strip() + ' = ?'     
    return result

def reformat_incre_equations(x):
    result = ''
    if len(x) >= 1:
        for eq in x:
            if len(result) == 0:
                result += eq[2 : -2]
            else:
                result += ', ' + eq[2 : -2]
    return result

def get_declarative_equations(result):
    eq_list = re.findall(r'\[\[.*?\]\]', result)
    if len(eq_list) > 0:            
        return reformat_equations_from_peano(reformat_incre_equations(eq_list))
    return ''

def get_final_using_sympy(equations):
    try:
        transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
        if str(equations) == 'nan':
            return np.nan
        equation_list = equations.split(',')
        for eq in equation_list:
            for c in range(len(eq)):
                if c < len(eq) - 2:
                    if eq[c].isalpha() and eq[c+1].isalpha() and eq[c+2].isalpha():
                        return 'invalid equations'

        goal_var = None
        goal_expression_list = []
            
        if equation_list[-1].split('=')[0].strip().isalpha() or len(equation_list[-1].split('=')[0].strip()) == 2:
            goal_var = equation_list[-1].split('=')[0].strip()
        elif '=' in equation_list[-1]:
            for l in list(string.ascii_lowercase) + list(string.ascii_uppercase):
                if l not in equation_list[-1]:
                    goal_var = l
                    break
            if goal_var is not None:
                goal_expression = goal_var + ' - (' + equation_list[-1].split('=')[0].strip() + ')'
                goal_expression = parse_expr(goal_expression, transformations=transformations)
                goal_expression = sympify(goal_expression)
                try:
                    return float(solve(goal_expression)[0])
                except Exception as e:
                    pass
                goal_expression_list.append(goal_expression)
            else:
                return 'invalid equations'

        if len(equation_list) == 1:
            try:
                goal_expression = parse_expr(equation_list[0].split('=')[0], transformations=transformations)
                return float(sympify(goal_expression))
            except Exception as e:
                return 'invalid equations'

        if goal_var == None:
            return 'no goal found'

        for i in range(len(equation_list) - 1):
            sub_eqs = equation_list[i]  
            if '?' not in sub_eqs:
                try:    
                    sub_eqs_split = sub_eqs.split('=')
                    sub_eqs = sub_eqs_split[0].strip() + ' - (' + sub_eqs_split[1].strip() + ')'
                    sub_eqs = parse_expr(sub_eqs, transformations=transformations)
                    sub_eqs = sympify(sub_eqs)
                except Exception as e:
                    return 'invalid equations'
                goal_expression_list.append(sub_eqs)

                try:
                    try:
                        return float(solve(goal_expression_list)[Symbol(goal_var)])
                    except Exception as e:
                        return float(solve(goal_expression_list)[0][Symbol(goal_var)])
                except Exception as e:
                    pass

        return 'no solution'
    except Exception as e:
        print(e)
        return 'bug'

templates_pl = {
    "main": f"""Rozwiążesz zadanie matematyczne krok po kroku, w uważny i formalny sposób. Rozwiązanie przedstawisz w formacie Peano.
        Zasady:
        1 - Kaźda zmienna lub równanie będzie zapisane w formacie Peano czyli np. [[eq a = b]] lub [[var a]]
        2 - Ostatnie zdanie przedstawi w formacie Peano, która zmienna jest rozwiązaniem zadania.
        3 - Każde nowe równanie będzie używało tylko zmiennych wprowadzonych wcześniej.
    """,
    "human-main": """
        Q: {mathProblemText}
        A: Rozwiąż zadanie krok po kroku w powyżej przedstawiony sposób.
    """,
}

templates_en = {
    "main": f""""You will solve a math problem step by step, in a careful and formal way. You will present the solution in Peano format.
        Rules:
        1 - Each variable or equation will be written in Peano format, i.e. [[eq a = b]] or [[var a]]
        2 - The last sentence will present in Peano format which variable is the solution to the problem.
        3 - Each new equation will use only variables introduced earlier.
    """,
    "human-main": """
        Q: {mathProblemText}
        A: Solve the problem step by step in the way presented above.
    """,
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
    human_template= get_template("human-main", language)
    system_message = SystemMessagePromptTemplate.from_template(template)
    human_message = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    return chat_prompt.format_messages(mathProblemText=math_problem_text)

def get_solution(chat_model, problem_text, language="pl"):
    result = chat_model.generate([get_prompt(problem_text, language)])
    result_text = result.generations[0][0].text if result.generations and len(result.generations) == 1 else ""
    print(result_text)
    eq_list = get_declarative_equations(result_text)
    print(eq_list)
    answer = get_final_using_sympy(eq_list)
    if answer != "":
        return {
            'answer': answer,
            'error': ''
        }
    return {
        'answer': '',
        'error': 'Could not generate solution'
    }
