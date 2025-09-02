from fractions import Fraction
import streamlit as st
import math
import re

# Dicionário de constantes matemáticas
CONSTANTES = {
    "pi": math.pi,
    "π": math.pi,
    "e": math.e,
    "phi": (1 + math.sqrt(5)) / 2,  # número de ouro
}

def entrada_numero(rotulo, valor_inicial="0", chave=None):
    """
    Entrada de número que aceita:
    - decimais: 2.5
    - inteiros: 10
    - frações: 3/4
    - raiz quadrada: sqrt(2) ou √2
    - constantes: pi, π, e, phi
    Retorna float ou None se inválido.
    """
    valor_str = st.text_input(rotulo, valor_inicial, key=chave)

    if not valor_str.strip():
        return None

    valor_str = valor_str.strip().lower()

    try:
        # Caso: constante
        if valor_str in CONSTANTES:
            return CONSTANTES[valor_str]

        # Caso: sqrt(2) ou sqrt(3/4)
        if valor_str.startswith("sqrt(") and valor_str.endswith(")"):
            inner = valor_str[5:-1]
            return math.sqrt(float(Fraction(inner)))

        # Caso: √2 ou √(3/4)
        if valor_str.startswith("√"):
            inner = valor_str[1:].strip("()")
            return math.sqrt(float(Fraction(inner)))

        # Caso normal: fração ou decimal
        return float(Fraction(valor_str))

    except Exception:
        return None
