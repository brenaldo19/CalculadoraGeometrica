from fractions import Fraction
import streamlit as st
import math
import re
import ast

# Dicionário de constantes matemáticas
CONSTANTES = {
    "pi": math.pi,
    "π": math.pi,
    "e": math.e,
    "phi": (1 + math.sqrt(5)) / 2,  # número de ouro
}

# Operadores e funções permitidas
ALLOWED_NAMES = {
    **CONSTANTES,
    "sqrt": math.sqrt,
}

ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub
}

def eval_expr(expr: str):
    """
    Avalia expressão matemática de forma segura.
    Suporta:
    - +, -, *, /
    - ^ ou ** (potência)
    - sqrt(x), √x
    - constantes (pi, e, phi)
    - frações (ex: 3/4)
    """

    # Substitui símbolos comuns
    expr = expr.replace("^", "**")
    expr = expr.replace("√", "sqrt")

    # Se for fração pura tipo "3/4", trata separado
    if re.fullmatch(r"\d+/\d+", expr):
        return float(Fraction(expr))

    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        elif isinstance(n, ast.Num):  # números
            return n.n
        elif isinstance(n, ast.BinOp) and type(n.op) in ALLOWED_OPERATORS:
            return _eval(n.left) ** _eval(n.right) if isinstance(n.op, ast.Pow) else eval(compile(ast.Expression(n), "", "eval"), {"__builtins__":{}}, ALLOWED_NAMES)
        elif isinstance(n, ast.UnaryOp) and type(n.op) in ALLOWED_OPERATORS:
            return -_eval(n.operand)
        elif isinstance(n, ast.Name) and n.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[n.id]
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ALLOWED_NAMES:
            args = [_eval(arg) for arg in n.args]
            return ALLOWED_NAMES[n.func.id](*args)
        else:
            raise ValueError("Expressão inválida")

    return float(_eval(node))


def entrada_numero(label, valor_padrao=0.0, key=None):
    if key is None:
        # gera chave única a partir do label
        key = f"{label}_{str(id(label))}"
    return st.number_input(label, value=float(valor_padrao), format="%.4f", key=key)

    """
    Entrada de número que aceita:
    - decimais: 2.5
    - inteiros: 10
    - frações: 3/4
    - raízes: sqrt(2), √2
    - constantes: pi, e, phi
    - operações: +, -, *, /
    - potência: ^ ou **
    Retorna float ou None se inválido.
    """
    valor_str = st.text_input(rotulo, valor_inicial, key=chave)

    if not valor_str.strip():
        return None

    try:
        return eval_expr(valor_str.strip().lower())
    except Exception:
        return None
