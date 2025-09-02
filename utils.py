from fractions import Fraction
import streamlit as st
import math
import re

def entrada_numero(rotulo, valor_inicial="0", chave=None):
    """
    Entrada de número que aceita:
    - decimais: 2.5
    - inteiros: 10
    - frações: 3/4
    - raiz quadrada: sqrt(2) ou √2
    Retorna float ou None se inválido.
    """
    valor_str = st.text_input(rotulo, valor_inicial, key=chave)

    if not valor_str.strip():
        return None

    try:
        # caso: sqrt(2)
        if valor_str.lower().startswith("sqrt(") and valor_str.endswith(")"):
            inner = valor_str[5:-1]
            return math.sqrt(float(Fraction(inner)))

        # caso: √2 (ou √(3/4))
        if valor_str.startswith("√"):
            inner = valor_str[1:]
            # remove parênteses opcionais
            inner = inner.strip("()")
            return math.sqrt(float(Fraction(inner)))

        # caso normal: fração ou decimal
        return float(Fraction(valor_str))

    except Exception:
        return None
