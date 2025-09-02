from fractions import Fraction

def entrada_numero(rotulo, valor_inicial="0", chave=None):
    valor_str = st.text_input(rotulo, valor_inicial, key=chave)
    try:
        return float(Fraction(valor_str))
    except:
        return None
