from fractions import Fraction
import streamlit as st   # mantém aqui

def entrada_numero(rotulo, valor_inicial="0", chave=None):
    """
    Entrada de número que aceita frações (ex: 3/4) ou decimais (ex: 2.5).
    Retorna float ou None se inválido.
    """
    valor_str = st.text_input(rotulo, valor_inicial, key=chave)
    try:
        return float(Fraction(valor_str))
    except:
        return None
