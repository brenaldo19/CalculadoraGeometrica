from utils import entrada_numero
import streamlit as st
import math

st.set_page_config(page_title="Calculadora Geométrica", layout="wide")

st.title("📐 Calculadora Geométrica")
st.write("Escolha a figura geométrica e insira os parâmetros para calcular.")

# =========================================================
# Funções de cálculo
# =========================================================

# -----------------------------
# Triângulo (apenas lados)
# -----------------------------
def triangulo_master(a=None, b=None, c=None):
    if not (a and b and c):
        return {"erro": "Forneça os 3 lados."}
    if not (a+b>c and a+c>b and b+c>a):
        return {"erro": "Triângulo inválido."}

    resultado = {}
    perimetro = a+b+c
    s = perimetro/2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    resultado["perímetro"] = round(perimetro,4)
    resultado["área"] = round(area,4)

    h_a = (2*area)/a
    h_b = (2*area)/b
    h_c = (2*area)/c
    resultado["alturas"] = {"h_a": round(h_a,4), "h_b": round(h_b,4), "h_c": round(h_c,4)}

    A = math.degrees(math.acos((b**2 + c**2 - a**2)/(2*b*c)))
    B = math.degrees(math.acos((a**2 + c**2 - b**2)/(2*a*c)))
    C = 180 - (A+B)
    resultado["ângulos"] = {"A": round(A,2), "B": round(B,2), "C": round(C,2)}

    if abs(a-b)<1e-6 and abs(b-c)<1e-6:
        resultado["classificação_lados"] = "equilátero"
    elif abs(a-b)<1e-6 or abs(b-c)<1e-6 or abs(a-c)<1e-6:
        resultado["classificação_lados"] = "isósceles"
    else:
        resultado["classificação_lados"] = "escaleno"

    if any(abs(x-90) < 1e-3 for x in [A,B,C]):
        resultado["classificação_ângulos"] = "retângulo"
    elif all(x < 90 for x in [A,B,C]):
        resultado["classificação_ângulos"] = "acutângulo"
    else:
        resultado["classificação_ângulos"] = "obtusângulo"

    return resultado


# -----------------------------
# Círculo (sem corda)
# -----------------------------
def circulo(r, theta=None):
    if not r or r <= 0:
        return {"erro": "Raio deve ser positivo!"}

    resultado = {}
    resultado["área"] = round(math.pi * r**2, 4)
    resultado["circunferência"] = round(2*math.pi*r, 4)

    if theta:
        arco = 2*math.pi*r*(theta/360)
        setor = math.pi*r**2*(theta/360)
        resultado["arco"] = round(arco, 4)
        resultado["setor"] = round(setor, 4)

    return resultado


# -----------------------------
# Quadrado
# -----------------------------
def quadrado(lado):
    return {"perímetro": 4*lado, "área": lado**2}


# -----------------------------
# Retângulo
# -----------------------------
def retangulo(base, altura):
    return {"perímetro": 2*(base+altura), "área": base*altura}


# -----------------------------
# Losango
# -----------------------------
def losango(lado, D, d):
    if lado <= 0 or D <= 0 or d <= 0:
        return {"erro": "Valores devem ser positivos!"}
    area = (D*d)/2
    perimetro = 4*lado
    h = area/D
    ang_agudo = math.degrees(2*math.atan(d/D))
    return {
        "área": round(area,4),
        "perímetro": round(perimetro,4),
        "altura": round(h,4),
        "ângulos": {"agudo": round(ang_agudo,2), "obtuso": round(180-ang_agudo,2)}
    }


# -----------------------------
# Paralelogramo
# -----------------------------
def paralelogramo(base, lado, altura=None, angulo=None):
    if base <= 0 or lado <= 0:
        return {"erro": "Base e lado devem ser positivos!"}
    resultado = {"perímetro": round(2*(base+lado),4)}
    if altura:
        resultado["área"] = round(base*altura,4)
    elif angulo:
        ang_rad = math.radians(angulo)
        area = base*lado*math.sin(ang_rad)
        resultado["área"] = round(area,4)
    return resultado


# -----------------------------
# Trapézio
# -----------------------------
def trapezio(B, b, l1, l2, h=None):
    if B <= 0 or b <= 0 or l1 <= 0 or l2 <= 0:
        return {"erro": "Todos os lados devem ser positivos!"}
    resultado = {"perímetro": round(B+b+l1+l2,4)}
    if h:
        area = ((B+b)*h)/2
        resultado["área"] = round(area,4)
    return resultado


# -----------------------------
# Polígono Regular
# -----------------------------
def poligono(n, lado=None, R=None):
    if n < 5 or n > 10:
        return {"erro": "Número de lados deve estar entre 5 e 10!"}
    perimetro, area, apotema = None, None, None
    if lado:
        perimetro = n*lado
        apotema = lado/(2*math.tan(math.pi/n))
        area = (perimetro*apotema)/2
    elif R:
        perimetro = 2*n*R*math.sin(math.pi/n)
        apotema = R*math.cos(math.pi/n)
        area = (perimetro*apotema)/2
    else:
        return {"erro": "Forneça lado ou raio circunscrito."}
    return {"perímetro": round(perimetro,4), "área": round(area,4), "apotema": round(apotema,4)}


# =========================================================
# Interface Streamlit – Parte 1 (com frações)
# =========================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Triângulo", "Círculo", "Quadrado", "Retângulo", "Losango", "Paralelogramo", "Trapézio", "Polígono Regular"
])

with tab1:
    st.header("🔺 Triângulo")
    a = entrada_numero("Lado a", chave="tri_a")
    b = entrada_numero("Lado b", chave="tri_b")
    c = entrada_numero("Lado c", chave="tri_c")
    if st.button("Calcular Triângulo"):
        st.write(triangulo_master(a, b, c))

with tab2:
    st.header("⚪ Círculo")
    r = entrada_numero("Raio", chave="circ_r")
    theta = entrada_numero("Ângulo θ (graus, opcional)", chave="circ_theta")
    if st.button("Calcular Círculo"):
        st.write(circulo(r, theta if theta else None))

with tab3:
    st.header("⬛ Quadrado")
    lado = entrada_numero("Lado", chave="quad_lado")
    if st.button("Calcular Quadrado"):
        st.write(quadrado(lado))

with tab4:
    st.header("▭ Retângulo")
    base = entrada_numero("Base", chave="ret_base")
    altura = entrada_numero("Altura", chave="ret_alt")
    if st.button("Calcular Retângulo"):
        st.write(retangulo(base, altura))

with tab5:
    st.header("⬟ Losango")
    lado = entrada_numero("Lado", chave="los_lado")
    D = entrada_numero("Diagonal maior", chave="los_D")
    d = entrada_numero("Diagonal menor", chave="los_d")
    if st.button("Calcular Losango"):
        st.write(losango(lado, D, d))

with tab6:
    st.header("▱ Paralelogramo")
    base = entrada_numero("Base", chave="par_base")
    lado = entrada_numero("Lado", chave="par_lado")
    altura = entrada_numero("Altura (opcional)", chave="par_alt")
    angulo = entrada_numero("Ângulo (graus, opcional)", chave="par_ang")
    if st.button("Calcular Paralelogramo"):
        st.write(paralelogramo(base, lado, altura if altura else None, angulo if angulo else None))

with tab7:
    st.header("Trapézio")
    B = entrada_numero("Base maior", chave="trap_B")
    b = entrada_numero("Base menor", chave="trap_b")
    l1 = entrada_numero("Lado 1", chave="trap_l1")
    l2 = entrada_numero("Lado 2", chave="trap_l2")
    h = entrada_numero("Altura (opcional)", chave="trap_h")
    if st.button("Calcular Trapézio"):
        st.write(trapezio(B, b, l1, l2, h if h else None))

with tab8:
    st.header("Polígono Regular")
    n = entrada_numero("Número de lados (5 a 10)", min_value=5, max_value=10, step=1)
    lado = entrada_numero("Lado (opcional)", chave="pol_lado")
    R = entrada_numero("Raio circunscrito (opcional)", chave="pol_R")
    if st.button("Calcular Polígono"):
        st.write(poligono(n, lado if lado else None, R if R else None))

# =========================================================
# Funções de cálculo – Parte 2
# =========================================================

# -----------------------------
# Cubo
# -----------------------------
def cubo(lado):
    if not lado or lado <= 0:
        return {"erro": "Forneça lado > 0"}
    return {
        "volume": round(lado**3,4),
        "área_superfície": round(6*lado**2,4),
        "diagonal_face": round(lado*math.sqrt(2),4),
        "diagonal_cubo": round(lado*math.sqrt(3),4),
        "raio_inscrito": round(lado/2,4),
        "raio_circunscrito": round((lado*math.sqrt(3))/2,4)
    }

# -----------------------------
# Paralelepípedo
# -----------------------------
def paralelepipedo(c, l, h):
    if c <= 0 or l <= 0 or h <= 0:
        return {"erro": "Todos os lados devem ser positivos"}
    resultado = {
        "volume": round(c*l*h,4),
        "área_superfície": round(2*(c*l + c*h + l*h),4),
        "diagonal_espacial": round(math.sqrt(c**2 + l**2 + h**2),4),
        "diagonais_faces": {
            "cl": round(math.sqrt(c**2 + l**2),4),
            "ch": round(math.sqrt(c**2 + h**2),4),
            "lh": round(math.sqrt(l**2 + h**2),4),
        }
    }
    if abs(c-l)<1e-6 and abs(l-h)<1e-6:
        resultado["classificação"] = "cubo (caso especial)"
    return resultado

# -----------------------------
# Prisma Regular
# -----------------------------
def prisma(n, lado, h):
    if n < 3:
        return {"erro": "Prisma precisa base com pelo menos 3 lados"}
    if lado <= 0 or h <= 0:
        return {"erro": "Lado e altura devem ser positivos"}
    perimetro = n*lado
    apotema = lado/(2*math.tan(math.pi/n))
    area_base = (perimetro*apotema)/2
    area_lateral = perimetro*h
    area_total = 2*area_base + area_lateral
    volume = area_base*h
    return {
        "perímetro_base": round(perimetro,4),
        "área_base": round(area_base,4),
        "apotema_base": round(apotema,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }

# -----------------------------
# Cilindro
# -----------------------------
def cilindro(r, h):
    if r <= 0 or h <= 0:
        return {"erro": "Raio e altura devem ser positivos"}
    area_base = math.pi*r**2
    area_lateral = 2*math.pi*r*h
    area_total = 2*area_base + area_lateral
    volume = area_base*h
    resultado = {
        "área_base": round(area_base,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }
    if abs(r-h)<1e-6:
        resultado["classificação"] = "cilindro equilátero (raio = altura)"
    return resultado

# -----------------------------
# Cone
# -----------------------------
def cone(r, h):
    if r <= 0 or h <= 0:
        return {"erro": "Raio e altura devem ser positivos"}
    g = math.sqrt(r**2 + h**2)
    area_base = math.pi*r**2
    area_lateral = math.pi*r*g
    area_total = area_base + area_lateral
    volume = (math.pi*r**2*h)/3
    resultado = {
        "geratriz": round(g,4),
        "área_base": round(area_base,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }
    if abs(r-h)<1e-6:
        resultado["classificação"] = "cone equilátero (raio = altura)"
    return resultado

# -----------------------------
# Esfera
# -----------------------------
def esfera(r, h=None):
    if r <= 0:
        return {"erro": "Raio deve ser positivo"}
    area = 4*math.pi*r**2
    volume = (4/3)*math.pi*r**3
    circ_max = 2*math.pi*r
    resultado = {
        "diâmetro": round(2*r,4),
        "área_superfície": round(area,4),
        "volume": round(volume,4),
        "circunferência_máxima": round(circ_max,4)
    }
    if h and 0 < h < 2*r:
        area_calota = 2*math.pi*r*h
        volume_calota = (math.pi*h**2*(3*r-h))/3
        resultado["calota"] = {
            "altura": h,
            "área": round(area_calota,4),
            "volume": round(volume_calota,4)
        }
    return resultado

# -----------------------------
# Pirâmide
# -----------------------------
def piramide(n, lado, h):
    if n < 3 or n > 6:
        return {"erro": "Pirâmide só aceita base de 3 a 6 lados"}
    if lado <= 0 or h <= 0:
        return {"erro": "Lado e altura devem ser positivos"}
    perimetro_base = n*lado
    apotema_base = lado/(2*math.tan(math.pi/n))
    area_base = (perimetro_base*apotema_base)/2
    apotema_lateral = math.sqrt(h**2 + apotema_base**2)
    area_lateral = (perimetro_base*apotema_lateral)/2
    area_total = area_base + area_lateral
    volume = (area_base*h)/3
    nomes = {3:"triangular",4:"quadrada",5:"pentagonal",6:"hexagonal"}
    return {
        "figura": f"pirâmide regular {nomes[n]}",
        "perímetro_base": round(perimetro_base,4),
        "apotema_base": round(apotema_base,4),
        "área_base": round(area_base,4),
        "apotema_lateral": round(apotema_lateral,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }


# =========================================================
# Interface Streamlit – Parte 2
# =========================================================
tab8, tab9, tab10, tab11, tab12, tab13, tab14 = st.tabs([
    "Cubo", "Paralelepípedo", "Prisma", "Cilindro", "Cone", "Esfera", "Pirâmide"
])

with tab8:
    st.header("⬛ Cubo")
    lado = entrada_numero("Lado", min_value=0.0, step=0.1, key="cubo_lado")
    if st.button("Calcular Cubo"):
        st.write(cubo(lado))

with tab9:
    st.header("📦 Paralelepípedo")
    c = entrada_numero("Comprimento", min_value=0.0, step=0.1)
    l = entrada_numero("Largura", min_value=0.0, step=0.1)
    h = entrada_numero("Altura", min_value=0.0, step=0.1)
    if st.button("Calcular Paralelepípedo"):
        st.write(paralelepipedo(c, l, h))

with tab10:
    st.header("🔺 Prisma Regular")
    n = entrada_numero("Número de lados da base", min_value=3, step=1)
    lado = entrada_numero("Lado da base", min_value=0.0, step=0.1, key="prisma_lado")
    h = entrada_numero("Altura", min_value=0.0, step=0.1, key="prisma_alt")
    if st.button("Calcular Prisma"):
        st.write(prisma(n, lado, h))

with tab11:
    st.header("🟠 Cilindro")
    r = entrada_numero("Raio", min_value=0.0, step=0.1, key="cil_r")
    h = entrada_numero("Altura", min_value=0.0, step=0.1, key="cil_h")
    if st.button("Calcular Cilindro"):
        st.write(cilindro(r, h))

with tab12:
    st.header("🔻 Cone")
    r = entrada_numero("Raio", min_value=0.0, step=0.1, key="cone_r")
    h = entrada_numero("Altura", min_value=0.0, step=0.1, key="cone_h")
    if st.button("Calcular Cone"):
        st.write(cone(r, h))

with tab13:
    st.header("⚪ Esfera")
    r = entrada_numero("Raio", min_value=0.0, step=0.1, key="esf_r")
    h = entrada_numero("Altura da calota (opcional)", min_value=0.0, step=0.1)
    if st.button("Calcular Esfera"):
        st.write(esfera(r, h if h>0 else None))

with tab14:
    st.header("⛏️ Pirâmide Regular")
    n = entrada_numero("Número de lados da base (3 a 6)", min_value=3, max_value=6, step=1)
    lado = entrada_numero("Lado da base", min_value=0.0, step=0.1, key="pir_lado")
    h = entrada_numero("Altura", min_value=0.0, step=0.1, key="pir_h")
    if st.button("Calcular Pirâmide"):
        st.write(piramide(n, lado, h))
