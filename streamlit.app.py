from utils import entrada_numero
import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import math
import sympy as sp

st.set_page_config(page_title="Calculadora Geométrica", layout="wide")

st.title("📐 Calculadora Geométrica")
st.write("Escolha a figura geométrica e insira os parâmetros para calcular.")

# =========================================================
# Funções de cálculo – Bidimensionais
# =========================================================

def triangulo_master(a=None, b=None, c=None):
    if not (a and b and c):
        return {"erro": "Forneça os 3 lados."}, ""
    if not (a+b>c and a+c>b and b+c>a):
        return {"erro": "Triângulo inválido."}, ""

    perimetro = a+b+c
    s = perimetro/2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))

    explicacao = f"""🔺 Triângulo (fórmula de Heron)
s = (a+b+c)/2 = ({a}+{b}+{c})/2 = {s}
Área = √(s*(s-a)*(s-b)*(s-c))
Área = √({s}*({s}-{a})*({s}-{b})*({s}-{c}))
Área = {area:.4f}
"""

    resultado = {
        "perímetro": round(perimetro,4),
        "área": round(area,4)
    }

    return resultado, explicacao

def circulo(r, theta=None):
    if not r or r <= 0:
        return {"erro": "Raio deve ser positivo!"}, ""

    area = math.pi * r**2
    circ = 2*math.pi*r
    explicacao = f"""⚪ Círculo
Área = πr² = π*{r}² = {area:.4f}
Circunferência = 2πr = 2π*{r} = {circ:.4f}
"""

    resultado = {
        "área": round(area,4),
        "circunferência": round(circ,4)
    }

    if theta:
        arco = 2*math.pi*r*(theta/360)
        setor = math.pi*r**2*(theta/360)
        resultado["arco"] = round(arco,4)
        resultado["setor"] = round(setor,4)
        explicacao += f"Arco = 2πr*(θ/360) = {arco:.4f}\nSetor = πr²*(θ/360) = {setor:.4f}\n"

    return resultado, explicacao

def quadrado(lado):
    if lado <= 0:
        return {"erro": "Forneça lado positivo!"}, ""
    
    per = 4 * lado
    area = lado ** 2
    diag = lado * math.sqrt(2)
    
    explicacao = f"""⬛ Quadrado
Perímetro = 4·lado = 4·{lado} = {per:.4f}
Área = lado² = {lado}² = {area:.4f}
Diagonal = lado·√2 = {lado}·√2 = {diag:.4f}
"""
    return {
        "perímetro": round(per,4),
        "área": round(area,4),
        "diagonal": round(diag,4)
    }, explicacao


def retangulo(base, altura):
    if base <= 0 or altura <= 0:
        return {"erro": "Base e altura devem ser positivos!"}, ""
    
    per = 2 * (base + altura)
    area = base * altura
    diag = math.sqrt(base**2 + altura**2)
    
    explicacao = f"""▭ Retângulo
Perímetro = 2·(b+h) = 2·({base}+{altura}) = {per:.4f}
Área = b·h = {base}·{altura} = {area:.4f}
Diagonal = √(b²+h²) = √({base}²+{altura}²) = {diag:.4f}
"""
    return {
        "perímetro": round(per,4),
        "área": round(area,4),
        "diagonal": round(diag,4)
    }, explicacao


def losango(lado, D, d):
    if lado <= 0 or D <= 0 or d <= 0:
        return {"erro": "Valores devem ser positivos!"}, ""
    area = (D*d)/2
    perimetro = 4*lado
    h = area/D
    explicacao = f"""⬟ Losango
Área = (D*d)/2 = ({D}*{d})/2 = {area}
Perímetro = 4*lado = 4*{lado} = {perimetro}
Altura = área/Diagonal maior = {area}/{D} = {h:.4f}
"""
    return {
        "área": round(area,4),
        "perímetro": round(perimetro,4),
        "altura": round(h,4)
    }, explicacao

def paralelogramo(base, lado, altura=None, angulo=None):
    if base <= 0 or lado <= 0:
        return {"erro": "Base e lado devem ser positivos!"}, ""
    resultado = {"perímetro": round(2*(base+lado),4)}
    explicacao = f"▱ Paralelogramo\nPerímetro = 2*(base+lado) = 2*({base}+{lado}) = {2*(base+lado)}\n"
    if altura:
        area = base*altura
        resultado["área"] = round(area,4)
        explicacao += f"Área = base*altura = {base}*{altura} = {area}\n"
    elif angulo:
        ang_rad = math.radians(angulo)
        area = base*lado*math.sin(ang_rad)
        resultado["área"] = round(area,4)
        explicacao += f"Área = base*lado*sin(ângulo) = {base}*{lado}*sin({angulo}) = {area:.4f}\n"
    return resultado, explicacao

def trapezio(B, b, l1, l2, h=None):
    if B <= 0 or b <= 0 or l1 <= 0 or l2 <= 0:
        return {"erro": "Todos os lados devem ser positivos!"}, ""
    perimetro = B+b+l1+l2
    resultado = {"perímetro": round(perimetro,4)}
    explicacao = f"""Trapézio
Perímetro = B+b+l1+l2 = {B}+{b}+{l1}+{l2} = {perimetro}
"""
    if h:
        area = ((B+b)*h)/2
        resultado["área"] = round(area,4)
        explicacao += f"Área = ((B+b)*h)/2 = (({B}+{b})*{h})/2 = {area}\n"
    return resultado, explicacao

def poligono(n, lado=None, R=None):
    if n < 5 or n > 10:
        return {"erro": "Número de lados deve estar entre 5 e 10!"}, ""
    if lado:
        perimetro = n*lado
        apotema = lado/(2*math.tan(math.pi/n))
        area = (perimetro*apotema)/2
        explicacao = f"""Polígono Regular {n} lados
Perímetro = n*lado = {n}*{lado} = {perimetro}
Apótema = lado / (2*tan(π/n)) = {lado}/(2*tan(π/{n})) = {apotema:.4f}
Área = (perímetro*apótema)/2 = ({perimetro}*{apotema:.4f})/2 = {area:.4f}
"""
    elif R:
        perimetro = 2*n*R*math.sin(math.pi/n)
        apotema = R*math.cos(math.pi/n)
        area = (perimetro*apotema)/2
        explicacao = f"""Polígono Regular {n} lados (usando raio)
Perímetro = 2*n*R*sin(π/n) = 2*{n}*{R}*sin(π/{n}) = {perimetro:.4f}
Apótema = R*cos(π/n) = {R}*cos(π/{n}) = {apotema:.4f}
Área = (perímetro*apótema)/2 = ({perimetro:.4f}*{apotema:.4f})/2 = {area:.4f}
"""
    else:
        return {"erro": "Forneça lado ou raio circunscrito."}, ""

    return {"perímetro": round(perimetro,4), "área": round(area,4), "apotema": round(apotema,4)}, explicacao

# =========================================================
# Função de Plotagem
# =========================================================
def plot_figura(tipo, **params):
    fig, ax = plt.subplots()

    if tipo == "círculo":
        r = params.get("r", 1)
        circ = plt.Circle((0,0), r, fill=False, color="blue")
        ax.add_patch(circ)
        ax.set_aspect("equal")
        ax.set_xlim(-r*1.2, r*1.2)
        ax.set_ylim(-r*1.2, r*1.2)

    elif tipo == "quadrado":
        lado = params.get("lado", 1)
        square = plt.Rectangle((-lado/2,-lado/2), lado, lado, fill=False, color="green")
        ax.add_patch(square)
        ax.set_aspect("equal")
        ax.set_xlim(-lado, lado)
        ax.set_ylim(-lado, lado)

    elif tipo == "retângulo":
        base = params.get("base", 1)
        altura = params.get("altura", 1)
        rect = plt.Rectangle((-base/2,-altura/2), base, altura, fill=False, color="orange")
        ax.add_patch(rect)
        ax.set_aspect("equal")
        ax.set_xlim(-base, base)
        ax.set_ylim(-altura, altura)

    elif tipo == "triângulo":
        a, b, c = params.get("a"), params.get("b"), params.get("c")
        xA, yA = 0, 0
        xB, yB = a, 0
        cos_gamma = (a**2 + b**2 - c**2)/(2*a*b)
        cos_gamma = max(min(cos_gamma,1),-1)
        sin_gamma = (1 - cos_gamma**2)**0.5
        xC, yC = b*cos_gamma, b*sin_gamma
        coords = [(xA,yA), (xB,yB), (xC,yC)]
        poly = plt.Polygon(coords, fill=False, color="red")
        ax.add_patch(poly)
        ax.set_aspect("equal")
        ax.set_xlim(min(xA,xB,xC)-1, max(xA,xB,xC)+1)
        ax.set_ylim(min(yA,yB,yC)-1, max(yA,yB,yC)+1)

    elif tipo == "losango":
        D = params.get("D", 2)
        d = params.get("d", 1)
        coords = [(0, D/2), (d/2, 0), (0, -D/2), (-d/2, 0)]
        poly = plt.Polygon(coords, fill=False, color="purple")
        ax.add_patch(poly)
        ax.set_aspect("equal")
        ax.set_xlim(-D, D)
        ax.set_ylim(-D, D)

    elif tipo == "paralelogramo":
        base = params.get("base", 2)
        lado = params.get("lado", 1)
        ang = math.radians(params.get("angulo", 60))
        coords = [(0,0),(base,0),(base+lado*math.cos(ang), lado*math.sin(ang)),(lado*math.cos(ang),lado*math.sin(ang))]
        poly = plt.Polygon(coords, fill=False, color="brown")
        ax.add_patch(poly)
        ax.set_aspect("equal")
        ax.set_xlim(-base, base*2)
        ax.set_ylim(-lado, lado*2)

    elif tipo == "trapézio":
        B = params.get("B", 4)
        b = params.get("b", 2)
        h = params.get("h", 2)
        x_offset = (B - b)/2
        coords = [(0,0),(B,0),(B-x_offset,h),(x_offset,h)]
        poly = plt.Polygon(coords, fill=False, color="cyan")
        ax.add_patch(poly)
        ax.set_aspect("equal")
        ax.set_xlim(-1, B+1)
        ax.set_ylim(-1, h+1)

    elif tipo == "polígono":
        n = params.get("n", 5)
        R = params.get("R", 1)
        coords = [(R*math.cos(2*math.pi*i/n), R*math.sin(2*math.pi*i/n)) for i in range(n)]
        poly = plt.Polygon(coords, fill=False, color="magenta")
        ax.add_patch(poly)
        ax.set_aspect("equal")
        ax.set_xlim(-R*1.2, R*1.2)
        ax.set_ylim(-R*1.2, R*1.2)

    st.pyplot(fig)

# =========================================================
# Interface Streamlit – Parte 1 (com plots + explicações)
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
        resultado, explicacao = triangulo_master(a, b, c)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura("triângulo", a=a, b=b, c=c)

with tab2:
    st.header("⚪ Círculo")
    r = entrada_numero("Raio", chave="circ_r")
    theta = entrada_numero("Ângulo θ (graus, opcional)", chave="circ_theta")
    if st.button("Calcular Círculo"):
        resultado, explicacao = circulo(r, theta if theta else None)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura("círculo", r=r)

with tab3:
    st.header("⬛ Quadrado")
    lado = entrada_numero("Lado", chave="quad_lado")
    if st.button("Calcular Quadrado"):
        resultado, explicacao = quadrado(lado)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura("quadrado", lado=lado)

with tab4:
    st.header("▭ Retângulo")
    base = entrada_numero("Base", chave="ret_base")
    altura = entrada_numero("Altura", chave="ret_alt")
    if st.button("Calcular Retângulo"):
        resultado, explicacao = retangulo(base, altura)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura("retângulo", base=base, altura=altura)

with tab5:
    st.header("⬟ Losango")
    lado = entrada_numero("Lado", chave="los_lado")
    D = entrada_numero("Diagonal maior", chave="los_D")
    d = entrada_numero("Diagonal menor", chave="los_d")
    if st.button("Calcular Losango"):
        resultado, explicacao = losango(lado, D, d)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura("losango", D=D, d=d)

with tab6:
    st.header("▱ Paralelogramo")
    base = entrada_numero("Base", chave="par_base")
    lado = entrada_numero("Lado", chave="par_lado")
    angulo = entrada_numero("Ângulo (graus, opcional)", chave="par_ang")
    if st.button("Calcular Paralelogramo"):
        resultado, explicacao = paralelogramo(base, lado, angulo=angulo if angulo else 60)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura("paralelogramo", base=base, lado=lado, angulo=angulo if angulo else 60)

with tab7:
    st.header("Trapézio")
    B = entrada_numero("Base maior", chave="trap_B")
    b = entrada_numero("Base menor", chave="trap_b")
    l1 = entrada_numero("Lado 1", chave="trap_l1")
    l2 = entrada_numero("Lado 2", chave="trap_l2")
    h = entrada_numero("Altura (opcional)", chave="trap_h")
    if st.button("Calcular Trapézio"):
        resultado, explicacao = trapezio(B, b, l1, l2, h if h else None)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado and h:
            plot_figura("trapézio", B=B, b=b, h=h)

with tab8:
    st.header("Polígono Regular")
    n = st.number_input("Número de lados (5 a 10)", min_value=5, max_value=10, step=1)
    lado = entrada_numero("Lado (opcional)", chave="pol_lado")
    R = entrada_numero("Raio circunscrito (opcional)", chave="pol_R")
    if st.button("Calcular Polígono"):
        resultado, explicacao = poligono(n, lado if lado else None, R if R else None)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            R_plot = R if R else lado
            plot_figura("polígono", n=n, R=R_plot)

# =========================================================
# Funções de cálculo – Parte 2 (Tridimensionais)
# =========================================================
# =========================================================
# Funções de cálculo – Tridimensionais
# =========================================================
# =========================================================
# Funções de cálculo – Tridimensionais
# =========================================================

def cubo(lado):
    if not lado or lado <= 0:
        return {"erro": "Forneça lado > 0"}, ""

    volume = lado**3
    area = 6*lado**2
    diag_face = lado*math.sqrt(2)
    diag_cubo = lado*math.sqrt(3)
    r_in = lado/2
    r_out = (lado*math.sqrt(3))/2

    explicacao = f"""⬛ Cubo
Volume = lado³ = {lado}³ = {volume}
Área superficial = 6*lado² = 6*{lado}² = {area}
Diagonal da face = lado*√2 = {diag_face:.4f}
Diagonal do cubo = lado*√3 = {diag_cubo:.4f}
Raio inscrito = lado/2 = {r_in:.4f}
Raio circunscrito = (lado*√3)/2 = {r_out:.4f}
"""

    return {
        "volume": round(volume,4),
        "área_superfície": round(area,4),
        "diagonal_face": round(diag_face,4),
        "diagonal_cubo": round(diag_cubo,4),
        "raio_inscrito": round(r_in,4),
        "raio_circunscrito": round(r_out,4)
    }, explicacao


def paralelepipedo(c, l, h):
    if c <= 0 or l <= 0 or h <= 0:
        return {"erro": "Todos os lados devem ser positivos"}, ""

    volume = c*l*h
    area = 2*(c*l + c*h + l*h)
    diag = math.sqrt(c**2 + l**2 + h**2)

    explicacao = f"""📦 Paralelepípedo
Volume = c*l*h = {c}*{l}*{h} = {volume}
Área superficial = 2*(cl+ch+lh) = 2*({c}*{l}+{c}*{h}+{l}*{h}) = {area}
Diagonal espacial = √(c²+l²+h²) = √({c}²+{l}²+{h}²) = {diag:.4f}
"""

    return {
        "volume": round(volume,4),
        "área_superfície": round(area,4),
        "diagonal_espacial": round(diag,4)
    }, explicacao


def prisma(n, lado, h):
    if n < 3:
        return {"erro": "Prisma precisa base com pelo menos 3 lados"}, ""
    if lado <= 0 or h <= 0:
        return {"erro": "Lado e altura devem ser positivos"}, ""

    perimetro = n*lado
    apotema = lado/(2*math.tan(math.pi/n))
    area_base = (perimetro*apotema)/2
    area_lateral = perimetro*h
    area_total = 2*area_base + area_lateral
    volume = area_base*h

    explicacao = f"""🔺 Prisma Regular {n} lados
Perímetro base = n*lado = {n}*{lado} = {perimetro}
Apótema = {lado}/(2*tan(π/{n})) = {apotema:.4f}
Área base = (perímetro*apótema)/2 = {area_base:.4f}
Área lateral = perímetro*altura = {perimetro}*{h} = {area_lateral}
Área total = 2*área base + área lateral = {area_total}
Volume = área base*altura = {area_base:.4f}*{h} = {volume:.4f}
"""

    return {
        "perímetro_base": round(perimetro,4),
        "área_base": round(area_base,4),
        "apotema_base": round(apotema,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }, explicacao


def cilindro(r, h):
    if r <= 0 or h <= 0:
        return {"erro": "Raio e altura devem ser positivos"}, ""

    area_base = math.pi*r**2
    area_lateral = 2*math.pi*r*h
    area_total = 2*area_base + area_lateral
    volume = area_base*h

    explicacao = f"""🟠 Cilindro
Área base = πr² = π*{r}² = {area_base:.4f}
Área lateral = 2πrh = 2π*{r}*{h} = {area_lateral:.4f}
Área total = 2*área base + área lateral = {area_total:.4f}
Volume = área base*altura = {area_base:.4f}*{h} = {volume:.4f}
"""

    return {
        "área_base": round(area_base,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }, explicacao


def cone(r, h):
    if r <= 0 or h <= 0:
        return {"erro": "Raio e altura devem ser positivos"}, ""

    g = math.sqrt(r**2 + h**2)
    area_base = math.pi*r**2
    area_lateral = math.pi*r*g
    area_total = area_base + area_lateral
    volume = (math.pi*r**2*h)/3

    explicacao = f"""🔻 Cone
Geratriz = √(r²+h²) = √({r}²+{h}²) = {g:.4f}
Área base = πr² = π*{r}² = {area_base:.4f}
Área lateral = πrg = π*{r}*{g:.4f} = {area_lateral:.4f}
Área total = base + lateral = {area_total:.4f}
Volume = (πr²h)/3 = (π*{r}²*{h})/3 = {volume:.4f}
"""

    return {
        "geratriz": round(g,4),
        "área_base": round(area_base,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }, explicacao


def esfera(r, h=None):
    if r <= 0:
        return {"erro": "Raio deve ser positivo"}, ""

    area = 4*math.pi*r**2
    volume = (4/3)*math.pi*r**3
    circ_max = 2*math.pi*r

    explicacao = f"""⚪ Esfera
Área superfície = 4πr² = 4π*{r}² = {area:.4f}
Volume = 4/3πr³ = (4/3)*π*{r}³ = {volume:.4f}
Circunferência máxima = 2πr = 2π*{r} = {circ_max:.4f}
"""

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
        explicacao += f"Calota: área = 2πrh = {area_calota:.4f}, volume = (πh²(3r-h))/3 = {volume_calota:.4f}\n"

    return resultado, explicacao


def piramide(n, lado, h):
    if n < 3 or n > 6:
        return {"erro": "Pirâmide só aceita base de 3 a 6 lados"}, ""
    if lado <= 0 or h <= 0:
        return {"erro": "Lado e altura devem ser positivos"}, ""

    perimetro_base = n*lado
    apotema_base = lado/(2*math.tan(math.pi/n))
    area_base = (perimetro_base*apotema_base)/2
    apotema_lateral = math.sqrt(h**2 + apotema_base**2)
    area_lateral = (perimetro_base*apotema_lateral)/2
    area_total = area_base + area_lateral
    volume = (area_base*h)/3
    nomes = {3:"triangular",4:"quadrada",5:"pentagonal",6:"hexagonal"}

    explicacao = f"""⛏️ Pirâmide {nomes[n]}
Perímetro base = n*lado = {n}*{lado} = {perimetro_base}
Apótema base = {apotema_base:.4f}
Área base = (perímetro*apótema)/2 = {area_base:.4f}
Apótema lateral = √(h²+apotema_base²) = {apotema_lateral:.4f}
Área lateral = (perímetro*apotema_lateral)/2 = {area_lateral:.4f}
Área total = base + lateral = {area_total:.4f}
Volume = (área base*h)/3 = ({area_base:.4f}*{h})/3 = {volume:.4f}
"""

    return {
        "figura": f"pirâmide regular {nomes[n]}",
        "perímetro_base": round(perimetro_base,4),
        "apotema_base": round(apotema_base,4),
        "área_base": round(area_base,4),
        "apotema_lateral": round(apotema_lateral,4),
        "área_lateral": round(area_lateral,4),
        "área_total": round(area_total,4),
        "volume": round(volume,4)
    }, explicacao


# =========================================================
# Função de Plotagem 3D (todos os sólidos)
# =========================================================
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# =========================================================
# Função de Plotagem 3D (todos os sólidos) – com Plotly
# =========================================================
import plotly.graph_objects as go

def plot_figura_3d(tipo, **params):
    fig = go.Figure()

    if tipo == "cubo":
        lado = params.get("lado",1)
        vertices = [(x,y,z) for x in [0,lado] for y in [0,lado] for z in [0,lado]]
        edges = [(i,j) for i,v1 in enumerate(vertices)
                        for j,v2 in enumerate(vertices)
                        if sum(a!=b for a,b in zip(v1,v2))==1]
        for (i,j) in edges:
            x,y,z = zip(vertices[i], vertices[j])
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="cyan")))

    elif tipo == "paralelepipedo":
        c = params.get("c",1); l = params.get("l",1); h = params.get("h",1)
        vertices = [
            (0,0,0),(c,0,0),(c,l,0),(0,l,0),
            (0,0,h),(c,0,h),(c,l,h),(0,l,h)
        ]
        edges = [(0,1),(1,2),(2,3),(3,0),
                 (4,5),(5,6),(6,7),(7,4),
                 (0,4),(1,5),(2,6),(3,7)]
        for (i,j) in edges:
            x,y,z = zip(vertices[i], vertices[j])
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="orange")))

    elif tipo == "prisma":
        n = params.get("n",5); lado = params.get("lado",1); h = params.get("h",2)
        R = lado/(2*math.sin(math.pi/n))
        base_inf = [(R*math.cos(2*math.pi*i/n), R*math.sin(2*math.pi*i/n), 0) for i in range(n)]
        base_sup = [(x,y,h) for (x,y,_) in base_inf]
        # bases
        for i in range(n):
            x,y,z = zip(base_inf[i], base_inf[(i+1)%n])
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="green")))
            x,y,z = zip(base_sup[i], base_sup[(i+1)%n])
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="green")))
            x,y,z = zip(base_inf[i], base_sup[i])
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="green")))

    elif tipo == "cilindro":
        r = params.get("r",1); h = params.get("h",2)
        z = np.linspace(0,h,30); theta = np.linspace(0,2*np.pi,30)
        theta,z = np.meshgrid(theta,z)
        x = r*np.cos(theta); y = r*np.sin(theta)
        fig.add_trace(go.Surface(x=x,y=y,z=z,opacity=0.5,colorscale="Blues"))

    elif tipo == "cone":
        r = params.get("r",1); h = params.get("h",2)
        theta = np.linspace(0,2*np.pi,30); R = np.linspace(0,r,30)
        T,R = np.meshgrid(theta,R)
        X = R*np.cos(T); Y = R*np.sin(T); Z = (h/r)*(r-R)
        fig.add_trace(go.Surface(x=X,y=Y,z=Z,opacity=0.5,colorscale="Reds"))

    elif tipo == "esfera":
        r = params.get("r",1)
        u = np.linspace(0,2*np.pi,60); v = np.linspace(0,np.pi,30)
        x = r*np.outer(np.cos(u), np.sin(v))
        y = r*np.outer(np.sin(u), np.sin(v))
        z = r*np.outer(np.ones_like(u), np.cos(v))
        fig.add_trace(go.Surface(x=x,y=y,z=z,opacity=0.5,colorscale="Viridis"))

    elif tipo == "pirâmide":
        n = params.get("n",4); lado = params.get("lado",1); h = params.get("h",2)
        R = lado/(2*math.sin(math.pi/n))
        base = [(R*math.cos(2*math.pi*i/n), R*math.sin(2*math.pi*i/n), 0) for i in range(n)]
        topo = (0,0,h)
        # base
        for i in range(n):
            x,y,z = zip(base[i], base[(i+1)%n])
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="yellow")))
        # laterais
        for i in range(n):
            x,y,z = zip(base[i], topo)
            fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(color="yellow")))

    fig.update_layout(scene=dict(aspectmode="data"))
    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# Interface Streamlit – Parte 2 (3D)
# =========================================================
tab8, tab9, tab10, tab11, tab12, tab13, tab14 = st.tabs([
    "Cubo", "Paralelepípedo", "Prisma", "Cilindro", "Cone", "Esfera", "Pirâmide"
])

with tab8:
    st.header("⬛ Cubo")
    lado = entrada_numero("Lado", chave="cubo_lado")
    if st.button("Calcular Cubo"):
        resultado, explicacao = cubo(lado)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("cubo", lado=lado)

with tab9:
    st.header("📦 Paralelepípedo")
    c = entrada_numero("Comprimento", chave="par_c")
    l = entrada_numero("Largura", chave="par_l")
    h = entrada_numero("Altura", chave="par_h")
    if st.button("Calcular Paralelepípedo"):
        resultado, explicacao = paralelepipedo(c, l, h)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("paralelepipedo", c=c, l=l, h=h)

with tab10:
    st.header("🔺 Prisma Regular")
    n = st.number_input("Número de lados da base", min_value=3, step=1, key="prisma_n")
    lado = entrada_numero("Lado da base", chave="prisma_lado")
    h = entrada_numero("Altura", chave="prisma_alt")
    if st.button("Calcular Prisma"):
        resultado, explicacao = prisma(n, lado, h)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("prisma", n=n, lado=lado, h=h)

with tab11:
    st.header("🟠 Cilindro")
    r = entrada_numero("Raio", chave="cil_r")
    h = entrada_numero("Altura", chave="cil_h")
    if st.button("Calcular Cilindro"):
        resultado, explicacao = cilindro(r, h)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("cilindro", r=r, h=h)

with tab12:
    st.header("🔻 Cone")
    r = entrada_numero("Raio", chave="cone_r")
    h = entrada_numero("Altura", chave="cone_h")
    if st.button("Calcular Cone"):
        resultado, explicacao = cone(r, h)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("cone", r=r, h=h)

with tab13:
    st.header("⚪ Esfera")
    r = entrada_numero("Raio", chave="esf_r")
    h = entrada_numero("Altura da calota (opcional)", chave="esf_h")
    if st.button("Calcular Esfera"):
        resultado, explicacao = esfera(r, h if h else None)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("esfera", r=r)

with tab14:
    st.header("⛏️ Pirâmide Regular")
    n = st.number_input("Número de lados da base (3 a 6)", min_value=3, max_value=6, step=1, key="pir_n")
    lado = entrada_numero("Lado da base", chave="pir_lado")
    h = entrada_numero("Altura", chave="pir_h")
    if st.button("Calcular Pirâmide"):
        resultado, explicacao = piramide(n, lado, h)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado: plot_figura_3d("pirâmide", n=n, lado=lado, h=h)

# =========================================================
# Funções de Cálculo – 4D (Policoros)
# =========================================================
def simplex_4d(lado):
    if not lado or lado <= 0:
        return {"erro": "Forneça lado > 0"}, ""

    hipervolume = (math.sqrt(5)/96) * (lado**4)
    area_hipersuperficie = (math.sqrt(3)/2) * (lado**3) * 5

    explicacao = f"""🔺 Simplexo 4D (5-célula)
Hipervolume = (√5/96)*a⁴ = {hipervolume:.4f}
Área da hipersuperfície = 5*(√3/2)*a³ = {area_hipersuperficie:.4f}
"""

    return {
        "hipervolume": round(hipervolume,4),
        "área_hipersuperfície": round(area_hipersuperficie,4)
    }, explicacao


def tesseract(lado):
    if not lado or lado <= 0:
        return {"erro": "Forneça lado > 0"}, ""

    hipervolume = lado**4
    area_hipersuperficie = 8*lado**3
    diagonal = lado*2

    explicacao = f"""🔷 Tesseract (8-célula)
Hipervolume = a⁴ = {hipervolume}
Área da hipersuperfície = 8*a³ = {area_hipersuperficie}
Diagonal 4D = 2a = {diagonal}
"""

    return {
        "hipervolume": round(hipervolume,4),
        "área_hipersuperfície": round(area_hipersuperficie,4),
        "diagonal_4d": round(diagonal,4)
    }, explicacao


def sixteen_cell(lado):
    if not lado or lado <= 0:
        return {"erro": "Forneça lado > 0"}, ""

    hipervolume = (2/3) * (lado**4)
    area_hipersuperficie = 16 * (math.sqrt(3)/4) * (lado**3)

    explicacao = f"""🔶 16-célula
Hipervolume = (2/3)*a⁴ = {hipervolume:.4f}
Área da hipersuperfície = 16*(√3/4)*a³ = {area_hipersuperficie:.4f}
"""

    return {
        "hipervolume": round(hipervolume,4),
        "área_hipersuperfície": round(area_hipersuperficie,4)
    }, explicacao


def twentyfour_cell(lado):
    if not lado or lado <= 0:
        return {"erro": "Forneça lado > 0"}, ""

    hipervolume = (2/3) * (lado**4) * math.sqrt(2)
    area_hipersuperficie = 24 * (math.sqrt(3)/2) * (lado**3)

    explicacao = f"""🔷 24-célula
Hipervolume = (2√2/3)*a⁴ = {hipervolume:.4f}
Área da hipersuperfície = 24*(√3/2)*a³ = {area_hipersuperficie:.4f}
"""

    return {
        "hipervolume": round(hipervolume,4),
        "área_hipersuperfície": round(area_hipersuperficie,4)
    }, explicacao


def hiperesfera(r):
    if not r or r <= 0:
        return {"erro": "Forneça raio > 0"}, ""

    hipervolume = 0.5 * (math.pi**2) * (r**4)
    area_hipersuperficie = 2 * (math.pi**2) * (r**3)

    explicacao = f"""⚪ Hiperesfera
Hipervolume = (1/2)*π²*r⁴ = {hipervolume:.4f}
Área da hipersuperfície = 2*π²*r³ = {area_hipersuperficie:.4f}
"""

    return {
        "hipervolume": round(hipervolume,4),
        "área_hipersuperfície": round(area_hipersuperficie,4)
    }, explicacao


# =========================================================
# Plotagem Policoros 4D → 3D
# =========================================================
def project_4d_to_3d(vertices4d):
    vertices3d = []
    for (x,y,z,w) in vertices4d:
        denom = (w+2)
        if abs(denom) < 1e-6:  # evita divisão por zero
            k = 1  # fallback: projeção ortográfica
        else:
            k = 2/denom
        vertices3d.append((x*k, y*k, z*k))
    return vertices3d



def plot_poliedro_4d(vertices4d, edges, color="blue"):
    vertices3d = project_4d_to_3d(vertices4d)
    fig = go.Figure()
    for (i,j) in edges:
        x,y,z = zip(vertices3d[i], vertices3d[j])
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=color)))
    fig.update_layout(scene=dict(aspectmode="data"))
    st.plotly_chart(fig, use_container_width=True)


def plot_figura_4d(tipo, **params):
    if tipo == "tesseract":
        lado = params.get("lado",1)
        vertices4d = [(x,y,z,w) for x in [0,lado] for y in [0,lado] for z in [0,lado] for w in [0,lado]]
        edges = [(i,j) for i,v1 in enumerate(vertices4d) for j,v2 in enumerate(vertices4d) if sum(a!=b for a,b in zip(v1,v2))==1]
        plot_poliedro_4d(vertices4d, edges, "blue")

    elif tipo == "simplex":
        vertices4d = [
            (1,1,1,-1/math.sqrt(5)),
            (1,-1,-1,-1/math.sqrt(5)),
            (-1,1,-1,-1/math.sqrt(5)),
            (-1,-1,1,-1/math.sqrt(5)),
            (0,0,0, math.sqrt(5)-1/math.sqrt(5))
        ]
        edges = [(i,j) for i in range(len(vertices4d)) for j in range(i+1,len(vertices4d))]
        plot_poliedro_4d(vertices4d, edges, "red")

    elif tipo == "sixteen":
        lado = params.get("lado",1)
        vertices4d = []
        for i in range(4):
            for s in [-lado, lado]:
                coord = [0,0,0,0]
                coord[i] = s
                vertices4d.append(tuple(coord))
        edges = []
        for i,v1 in enumerate(vertices4d):
            for j,v2 in enumerate(vertices4d):
                if i<j:
                    dist = math.sqrt(sum((a-b)**2 for a,b in zip(v1,v2)))
                    if abs(dist - math.sqrt(2)*lado) < 1e-6:
                        edges.append((i,j))
        plot_poliedro_4d(vertices4d, edges, "green")

    elif tipo == "twentyfour":
        vals = [-1,1]
        vertices4d = []
        for i in range(4):
            for j in range(i+1,4):
                for s1 in vals:
                    for s2 in vals:
                        coord = [0,0,0,0]
                        coord[i] = s1
                        coord[j] = s2
                        vertices4d.append(tuple(coord))
        edges = []
        for i,v1 in enumerate(vertices4d):
            for j,v2 in enumerate(vertices4d):
                if i<j:
                    dist = math.sqrt(sum((a-b)**2 for a,b in zip(v1,v2)))
                    if abs(dist - math.sqrt(2)) < 1e-6:
                        edges.append((i,j))
        plot_poliedro_4d(vertices4d, edges, "purple")

    elif tipo == "hiperesfera":
        r = params.get("r",1)
        u = np.linspace(0, 2*np.pi, 60)
        v = np.linspace(0, np.pi, 30)
        x = r*np.outer(np.cos(u), np.sin(v))
        y = r*np.outer(np.sin(u), np.sin(v))
        z = r*np.outer(np.ones_like(u), np.cos(v))
        fig = go.Figure(data=[go.Surface(x=x,y=y,z=z,colorscale="Viridis",opacity=0.7)])
        fig.update_layout(scene=dict(aspectmode="data"))
        st.plotly_chart(fig, use_container_width=True)


# =========================================================
# Interface Streamlit – Parte 3 (4D)
# =========================================================
tab15, tab16, tab17, tab18, tab19 = st.tabs([
    "5-célula (Simplexo)", "8-célula (Tesseract)", 
    "16-célula", "24-célula", "Hiperesfera"
])

with tab15:
    st.header("🔺 5-célula (Simplexo 4D)")
    lado = entrada_numero("Lado", chave="simp_lado")
    if st.button("Calcular Simplexo 4D"):
        resultado, explicacao = simplex_4d(lado)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        plot_figura_4d("simplex", lado=lado)

with tab16:
    st.header("🔷 8-célula (Tesseract)")
    lado = entrada_numero("Lado", chave="tess_lado")
    if st.button("Calcular Tesseract"):
        resultado, explicacao = tesseract(lado)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_4d("tesseract", lado=lado)

with tab17:
    st.header("🔶 16-célula")
    lado = entrada_numero("Lado", chave="sixteen_lado")
    if st.button("Calcular 16-célula"):
        resultado, explicacao = sixteen_cell(lado)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_4d("sixteen", lado=lado)

with tab18:
    st.header("🔷 24-célula")
    lado = entrada_numero("Lado", chave="twentyfour_lado")
    if st.button("Calcular 24-célula"):
        resultado, explicacao = twentyfour_cell(lado)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_4d("twentyfour", lado=lado)

with tab19:
    st.header("⚪ Hiperesfera")
    r = entrada_numero("Raio", chave="hiper_r")
    if st.button("Calcular Hiperesfera"):
        resultado, explicacao = hiperesfera(r)
        st.write(resultado)
        if explicacao: st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_4d("hiperesfera", r=r)

# =========================================================
# Triângulo Inverso – todos os 20 casos
# =========================================================

def triangulo_inverso(caso, **kwargs):
    # ------------------------------
    # Grupo 1 – Básicos (Lados + Ângulos)
    # ------------------------------
    if caso == 1:
        a, b, angC = kwargs["a"], kwargs["b"], math.radians(kwargs["angC"])
        c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(angC))
        area = 0.5*a*b*math.sin(angC)
        exp = f"c² = a² + b² - 2ab·cos(C)\nc = {c:.4f}\nÁrea = ½ab·sen(C) = {area:.4f}"
        return {"c": round(c,4), "area": round(area,4)}, exp

    if caso == 2:
        a, b, angA = kwargs["a"], kwargs["b"], math.radians(kwargs["angA"])
        senB = b*math.sin(angA)/a
        if abs(senB) > 1: return {"erro":"Dados inválidos"}, ""
        angB = math.degrees(math.asin(senB))
        exp = f"Lei dos senos: sen(B)/b = sen(A)/a → B = {angB:.4f}°"
        return {"angB": round(angB,4)}, exp

    # ------------------------------
    # Grupo 2 – Misturando área
    # ------------------------------
    if caso == 3:
        a,b,area = kwargs["a"], kwargs["b"], kwargs["area"]
        senC = (2*area)/(a*b)
        if abs(senC)>1: return {"erro":"Área inválida"}, ""
        angC = math.degrees(math.asin(senC))
        exp = f"Área = ½ab·sen(C) → C = {angC:.4f}°"
        return {"angC": round(angC,4)}, exp

    if caso == 4:
        a, area, angB = kwargs["a"], kwargs["area"], math.radians(kwargs["angB"])
        c = (2*area)/(a*math.sin(angB))
        exp = f"Área = ½ac·sen(B) → c = {c:.4f}"
        return {"c": round(c,4)}, exp

    if caso == 5:
        area = kwargs["area"]
        angA, angB, angC = map(lambda x: math.radians(kwargs[x]), ["angA","angB","angC"])
        k = math.sqrt((4*area)/(math.sin(2*angA)+math.sin(2*angB)+math.sin(2*angC)))
        a = k*math.sin(angA); b = k*math.sin(angB); c = k*math.sin(angC)
        exp = f"3 ângulos + área → semelhança escalada pelos senos\n a={a:.4f}, b={b:.4f}, c={c:.4f}"
        return {"a": round(a,4), "b": round(b,4), "c": round(c,4)}, exp

    # ------------------------------
    # Grupo 3 – Mistura de ângulos
    # ------------------------------
    if caso == 6:
        a=kwargs["a"]; angA=math.radians(kwargs["angA"]); angB=math.radians(kwargs["angB"])
        angC=math.pi-(angA+angB)
        b=a*math.sin(angB)/math.sin(angA); c=a*math.sin(angC)/math.sin(angA)
        exp = f"Lei dos senos: b={b:.4f}, c={c:.4f}"
        return {"b":round(b,4),"c":round(c,4)}, exp

    if caso == 7:
        area=kwargs["area"]; angA=math.radians(kwargs["angA"]); angB=math.radians(kwargs["angB"])
        angC=math.pi-(angA+angB)
        k=math.sqrt((2*area*math.sin(angA+angB))/(math.sin(angA)*math.sin(angB)*math.sin(angC)))
        a=k*math.sin(angA); b=k*math.sin(angB); c=k*math.sin(angC)
        exp = f"Escala com área e ângulos → a={a:.4f}, b={b:.4f}, c={c:.4f}"
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4)}, exp

    if caso == 8:
        P=kwargs["perimetro"]
        angA,angB,angC=map(lambda x: math.radians(kwargs[x]),["angA","angB","angC"])
        k=P/(math.sin(angA)+math.sin(angB)+math.sin(angC))
        a=k*math.sin(angA); b=k*math.sin(angB); c=k*math.sin(angC)
        exp = f"Escala com perímetro → a={a:.4f}, b={b:.4f}, c={c:.4f}"
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4)}, exp

    # ------------------------------
    # Grupo 4 – Alturas/medianas/bissetrizes
    # ------------------------------
    if caso == 9:
        a,h=kwargs["a"],kwargs["h"]
        area=0.5*a*h
        exp=f"Área = ½·a·h = {area:.4f}"
        return {"area":round(area,4)}, exp

    if caso == 10:
        ha,hb,hc=kwargs["ha"],kwargs["hb"],kwargs["hc"]
        # sistema simbólico: ha=2A/a etc.
        A=sp.symbols('A', positive=True)
        a=2*A/ha; b=2*A/hb; c=2*A/hc
        s=(a+b+c)/2
        eq=sp.Eq(A, sp.sqrt(s*(s-a)*(s-b)*(s-c)))
        sol=sp.nsolve(eq, 10)  # chute inicial
        A_val=float(sol)
        a=2*A_val/ha; b=2*A_val/hb; c=2*A_val/hc
        exp=f"Resolução numérica com Heron: a={a:.4f}, b={b:.4f}, c={c:.4f}"
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4),"area":round(A_val,4)}, exp

    if caso == 11:
        return {"info":"Bissetriz requer sistema trigonométrico avançado"}, "Caso 11 – não implementado"

    if caso == 12:
        return {"info":"Mediatriz requer circunrádio"}, "Caso 12 – não implementado"

    # ------------------------------
    # Grupo 5 – Circunferências
    # ------------------------------
    if caso == 13:
        r,P=kwargs["r"],kwargs["P"]
        area=0.5*r*P
        exp=f"A = rP/2 = {area:.4f}"
        return {"area":round(area,4)}, exp

    if caso == 14:
        R=kwargs["R"]
        angA,angB,angC=map(lambda x: math.radians(kwargs[x]),["angA","angB","angC"])
        a=2*R*math.sin(angA); b=2*R*math.sin(angB); c=2*R*math.sin(angC)
        exp=f"a=2R·senA → a={a:.4f}, b={b:.4f}, c={c:.4f}"
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4)}, exp

    if caso == 15:
        area,r=kwargs["area"],kwargs["r"]
        P=2*area/r
        exp=f"P = 2A/r = {P:.4f}"
        return {"P":round(P,4)}, exp

    if caso == 16:
        return {"info":"Área+R → sistema trigonométrico"}, "Caso 16 – não implementado"

    # ------------------------------
    # Grupo 6 – Retângulo
    # ------------------------------
    if caso == 17:
        cat1,cat2=kwargs["cat1"],kwargs["cat2"]
        hip=math.sqrt(cat1**2+cat2**2)
        exp=f"Pitágoras: hip²=cat1²+cat2² → {hip:.4f}"
        return {"hip":round(hip,4)}, exp

    if caso == 18:
        hip,cat=kwargs["hip"],kwargs["cat"]
        outro=math.sqrt(hip**2-cat**2)
        exp=f"Pitágoras: outro=√(hip²-cat²)={outro:.4f}"
        return {"outro_cat":round(outro,4)}, exp

    if caso == 19:
        area,cat=kwargs["area"],kwargs["cat"]
        outro=(2*area)/cat
        exp=f"A=½ab → b=2A/a={outro:.4f}"
        return {"outro_cat":round(outro,4)}, exp

    if caso == 20:
        A,P=kwargs["area"],kwargs["perimetro"]
        a,b=sp.symbols('a b', positive=True)
        eqs=[
            sp.Eq(a*b/2, A),
            sp.Eq(a+b+sp.sqrt(a**2+b**2), P)  # usar sp.sqrt
]
        sol=sp.nsolve(eqs, [a,b], [3,4])  # chute inicial
        a_val=float(sol[0]); b_val=float(sol[1])
        c_val=math.sqrt(a_val**2+b_val**2)  # aqui pode ser math.sqrt pq já virou float

        exp=f"Solução numérica: a={a_val:.4f}, b={b_val:.4f}, c={c_val:.4f}"
        return {"a":round(a_val,4),"b":round(b_val,4),"c":round(c_val,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""
# =========================================================
# Interface – Triângulo Inverso (20 casos com nomes)
# =========================================================
tab_triang_inv = st.tabs(["🔺 Triângulo Inverso"])[0]

casos_lista = [
    "1. Dois lados + ângulo entre eles → 3º lado e área",
    "2. Dois lados + ângulo oposto a um deles → outro ângulo",
    "3. Área + dois lados → ângulo entre eles",
    "4. Área + um lado + ângulo oposto → outro lado",
    "5. Área + três ângulos → lados proporcionais",
    "6. Um lado + dois ângulos → outros lados",
    "7. Dois ângulos + área → lados escalados",
    "8. Três ângulos + perímetro → lados",
    "9. Um lado + altura relativa → área",
    "10. Três alturas → triângulo definido",
    "11. Um lado + bissetriz relativa + ângulos → outros lados",
    "12. Um lado + mediatriz → circunrádio e lados",
    "13. Raio inscrito + perímetro → área",
    "14. Raio circunscrito + ângulos → lados",
    "15. Área + raio inscrito → perímetro",
    "16. Área + raio circunscrito → lados via trigonometria",
    "17. Catetos → hipotenusa",
    "18. Hipotenusa + cateto → outro cateto",
    "19. Área + cateto → outro cateto",
    "20. Perímetro + área → lados via sistema"
]

with tab_triang_inv:
    st.header("🔺 Triângulo Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_lista)
    caso = int(caso_txt.split(".")[0])

    # ---------------------------------------
    # Grupo 1
    # ---------------------------------------
    if caso == 1:
        a = entrada_numero("Lado a")
        b = entrada_numero("Lado b")
        angC = entrada_numero("Ângulo C (graus)")
        if st.button("Calcular Caso 1"):
            r,exp = triangulo_inverso(caso,a=a,b=b,angC=angC)
            st.write(r); st.code(exp)

    if caso == 2:
        a = entrada_numero("Lado a")
        b = entrada_numero("Lado b")
        angA = entrada_numero("Ângulo A (graus)")
        if st.button("Calcular Caso 2"):
            r,exp = triangulo_inverso(caso,a=a,b=b,angA=angA)
            st.write(r); st.code(exp)

    # ---------------------------------------
    # Grupo 2
    # ---------------------------------------
    if caso == 3:
        a = entrada_numero("Lado a")
        b = entrada_numero("Lado b")
        area = entrada_numero("Área")
        if st.button("Calcular Caso 3"):
            r,exp = triangulo_inverso(caso,a=a,b=b,area=area)
            st.write(r); st.code(exp)

    if caso == 4:
        a = entrada_numero("Lado a")
        angB = entrada_numero("Ângulo B (graus)")
        area = entrada_numero("Área")
        if st.button("Calcular Caso 4"):
            r,exp = triangulo_inverso(caso,a=a,angB=angB,area=area)
            st.write(r); st.code(exp)

    if caso == 5:
        angA = entrada_numero("Ângulo A (graus)")
        angB = entrada_numero("Ângulo B (graus)")
        angC = entrada_numero("Ângulo C (graus)")
        area = entrada_numero("Área")
        if st.button("Calcular Caso 5"):
            r,exp = triangulo_inverso(caso,area=area,angA=angA,angB=angB,angC=angC)
            st.write(r); st.code(exp)

    # ---------------------------------------
    # Grupo 3
    # ---------------------------------------
    if caso == 6:
        a = entrada_numero("Lado a")
        angA = entrada_numero("Ângulo A (graus)")
        angB = entrada_numero("Ângulo B (graus)")
        if st.button("Calcular Caso 6"):
            r,exp = triangulo_inverso(caso,a=a,angA=angA,angB=angB)
            st.write(r); st.code(exp)

    if caso == 7:
        area = entrada_numero("Área")
        angA = entrada_numero("Ângulo A (graus)")
        angB = entrada_numero("Ângulo B (graus)")
        if st.button("Calcular Caso 7"):
            r,exp = triangulo_inverso(caso,area=area,angA=angA,angB=angB)
            st.write(r); st.code(exp)

    if caso == 8:
        P = entrada_numero("Perímetro")
        angA = entrada_numero("Ângulo A (graus)")
        angB = entrada_numero("Ângulo B (graus)")
        angC = entrada_numero("Ângulo C (graus)")
        if st.button("Calcular Caso 8"):
            r,exp = triangulo_inverso(caso,perimetro=P,angA=angA,angB=angB,angC=angC)
            st.write(r); st.code(exp)

    # ---------------------------------------
    # Grupo 4
    # ---------------------------------------
    if caso == 9:
        a = entrada_numero("Lado a")
        h = entrada_numero("Altura relativa")
        if st.button("Calcular Caso 9"):
            r,exp = triangulo_inverso(caso,a=a,h=h)
            st.write(r); st.code(exp)

    if caso == 10:
        ha = entrada_numero("Altura ha")
        hb = entrada_numero("Altura hb")
        hc = entrada_numero("Altura hc")
        if st.button("Calcular Caso 10"):
            r,exp = triangulo_inverso(caso,ha=ha,hb=hb,hc=hc)
            st.write(r); st.code(exp)

    if caso == 11:
        a = entrada_numero("Lado a")
        bissetriz = entrada_numero("Bissetriz")
        angA = entrada_numero("Ângulo A (graus)")
        angB = entrada_numero("Ângulo B (graus)")
        if st.button("Calcular Caso 11"):
            r,exp = triangulo_inverso(caso,a=a,bissetriz=bissetriz,angA=angA,angB=angB)
            st.write(r); st.code(exp)

    if caso == 12:
        a = entrada_numero("Lado a")
        mediatriz = entrada_numero("Mediatriz")
        if st.button("Calcular Caso 12"):
            r,exp = triangulo_inverso(caso,a=a,mediatriz=mediatriz)
            st.write(r); st.code(exp)

    # ---------------------------------------
    # Grupo 5
    # ---------------------------------------
    if caso == 13:
        r = entrada_numero("Raio inscrito r")
        P = entrada_numero("Perímetro")
        if st.button("Calcular Caso 13"):
            r,exp = triangulo_inverso(caso,r=r,P=P)
            st.write(r); st.code(exp)

    if caso == 14:
        R = entrada_numero("Raio circunscrito R")
        angA = entrada_numero("Ângulo A (graus)")
        angB = entrada_numero("Ângulo B (graus)")
        angC = entrada_numero("Ângulo C (graus)")
        if st.button("Calcular Caso 14"):
            r,exp = triangulo_inverso(caso,R=R,angA=angA,angB=angB,angC=angC)
            st.write(r); st.code(exp)

    if caso == 15:
        area = entrada_numero("Área")
        r = entrada_numero("Raio inscrito r")
        if st.button("Calcular Caso 15"):
            r,exp = triangulo_inverso(caso,area=area,r=r)
            st.write(r); st.code(exp)

    if caso == 16:
        area = entrada_numero("Área")
        R = entrada_numero("Raio circunscrito R")
        if st.button("Calcular Caso 16"):
            r,exp = triangulo_inverso(caso,area=area,R=R)
            st.write(r); st.code(exp)

    # ---------------------------------------
    # Grupo 6
    # ---------------------------------------
    if caso == 17:
        cat1 = entrada_numero("Cateto 1")
        cat2 = entrada_numero("Cateto 2")
        if st.button("Calcular Caso 17"):
            r,exp = triangulo_inverso(caso,cat1=cat1,cat2=cat2)
            st.write(r); st.code(exp)

    if caso == 18:
        hip = entrada_numero("Hipotenusa")
        cat = entrada_numero("Cateto")
        if st.button("Calcular Caso 18"):
            r,exp = triangulo_inverso(caso,hip=hip,cat=cat)
            st.write(r); st.code(exp)

    if caso == 19:
        area = entrada_numero("Área")
        cat = entrada_numero("Cateto")
        if st.button("Calcular Caso 19"):
            r,exp = triangulo_inverso(caso,area=area,cat=cat)
            st.write(r); st.code(exp)

    if caso == 20:
        area = entrada_numero("Área")
        P = entrada_numero("Perímetro")
        if st.button("Calcular Caso 20"):
            r,exp = triangulo_inverso(caso,area=area,perimetro=P)
            st.write(r); st.code(exp)
# =========================================================
# Quadrado Inverso – 3 casos
# =========================================================

def quadrado_inverso(caso, **kwargs):
    # Caso 1 – Área → lado, perímetro, diagonal
    if caso == 1:
        A = kwargs["area"]
        if A <= 0: 
            return {"erro":"Área inválida"}, ""
        a = math.sqrt(A)
        P = 4*a
        d = a*math.sqrt(2)
        exp = f"Lado = √A = {a:.4f}\nPerímetro = 4a = {P:.4f}\nDiagonal = a√2 = {d:.4f}"
        return {"lado":round(a,4),"perimetro":round(P,4),"diagonal":round(d,4)}, exp

    # Caso 2 – Perímetro → lado, área, diagonal
    if caso == 2:
        P = kwargs["perimetro"]
        if P <= 0: 
            return {"erro":"Perímetro inválido"}, ""
        a = P/4
        A = a**2
        d = a*math.sqrt(2)
        exp = f"Lado = P/4 = {a:.4f}\nÁrea = a² = {A:.4f}\nDiagonal = a√2 = {d:.4f}"
        return {"lado":round(a,4),"area":round(A,4),"diagonal":round(d,4)}, exp

    # Caso 3 – Diagonal → lado, área, perímetro
    if caso == 3:
        d = kwargs["diagonal"]
        if d <= 0:
            return {"erro":"Diagonal inválida"}, ""
        a = d/math.sqrt(2)
        A = a**2
        P = 4*a
        exp = f"Lado = d/√2 = {a:.4f}\nÁrea = a² = {A:.4f}\nPerímetro = 4a = {P:.4f}"
        return {"lado":round(a,4),"area":round(A,4),"perimetro":round(P,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""

# =========================================================
# Interface – Quadrado Inverso (3 casos)
# =========================================================
tab_quad_inv = st.tabs(["⬜ Quadrado Inverso"])[0]

casos_quad = [
    "1. Área → lado, perímetro, diagonal",
    "2. Perímetro → lado, área, diagonal",
    "3. Diagonal → lado, área, perímetro"
]

with tab_quad_inv:
    st.header("⬜ Quadrado Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_quad)
    caso = int(caso_txt.split(".")[0])

    # Caso 1
    if caso == 1:
        A = entrada_numero("Área")
        if st.button("Calcular Caso 1"):
            r,exp = quadrado_inverso(caso, area=A)
            st.write(r); st.code(exp)

    # Caso 2
    if caso == 2:
        P = entrada_numero("Perímetro")
        if st.button("Calcular Caso 2"):
            r,exp = quadrado_inverso(caso, perimetro=P)
            st.write(r); st.code(exp)

    # Caso 3
    if caso == 3:
        d = entrada_numero("Diagonal")
        if st.button("Calcular Caso 3"):
            r,exp = quadrado_inverso(caso, diagonal=d)
            st.write(r); st.code(exp)

# =========================================================
# Retângulo Inverso – 3 casos
# =========================================================

def retangulo_inverso(caso, **kwargs):
    # Caso 1 – Área + lado → outro lado, perímetro, diagonal
    if caso == 1:
        A, b = kwargs["area"], kwargs["lado"]
        if A <= 0 or b <= 0: 
            return {"erro":"Valores inválidos"}, ""
        h = A / b
        P = 2 * (b + h)
        d = math.sqrt(b**2 + h**2)
        exp = f"h = A/b = {h:.4f}\nP = 2(b+h) = {P:.4f}\nDiagonal = √(b²+h²) = {d:.4f}"
        return {"altura":round(h,4),"perimetro":round(P,4),"diagonal":round(d,4)}, exp

    # Caso 2 – Perímetro + lado → outro lado, área, diagonal
    if caso == 2:
        P, b = kwargs["perimetro"], kwargs["lado"]
        if P <= 0 or b <= 0: 
            return {"erro":"Valores inválidos"}, ""
        h = P/2 - b
        if h <= 0: 
            return {"erro":"Perímetro incompatível com o lado"}, ""
        A = b * h
        d = math.sqrt(b**2 + h**2)
        exp = f"h = P/2 - b = {h:.4f}\nÁrea = b·h = {A:.4f}\nDiagonal = √(b²+h²) = {d:.4f}"
        return {"altura":round(h,4),"area":round(A,4),"diagonal":round(d,4)}, exp

    # Caso 3 – Diagonal + lado → outro lado, área, perímetro
    if caso == 3:
        d, b = kwargs["diagonal"], kwargs["lado"]
        if d <= 0 or b <= 0 or d <= b: 
            return {"erro":"Valores inválidos"}, ""
        h = math.sqrt(d**2 - b**2)
        A = b * h
        P = 2 * (b + h)
        exp = f"h = √(d² - b²) = {h:.4f}\nÁrea = b·h = {A:.4f}\nPerímetro = 2(b+h) = {P:.4f}"
        return {"altura":round(h,4),"area":round(A,4),"perimetro":round(P,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""


# =========================================================
# Interface – Retângulo Inverso (3 casos)
# =========================================================
tab_ret_inv = st.tabs(["▭ Retângulo Inverso"])[0]

casos_ret = [
    "1. Área + lado → outro lado, perímetro, diagonal",
    "2. Perímetro + lado → outro lado, área, diagonal",
    "3. Diagonal + lado → outro lado, área, perímetro"
]

with tab_ret_inv:
    st.header("▭ Retângulo Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_ret)
    caso = int(caso_txt.split(".")[0])

    # Caso 1
    if caso == 1:
        A = entrada_numero("Área")
        b = entrada_numero("Lado conhecido (base ou altura)")
        if st.button("Calcular Caso 1"):
            r,exp = retangulo_inverso(caso, area=A, lado=b)
            st.write(r); st.code(exp)

    # Caso 2
    if caso == 2:
        P = entrada_numero("Perímetro")
        b = entrada_numero("Lado conhecido (base ou altura)")
        if st.button("Calcular Caso 2"):
            r,exp = retangulo_inverso(caso, perimetro=P, lado=b)
            st.write(r); st.code(exp)

    # Caso 3
    if caso == 3:
        d = entrada_numero("Diagonal")
        b = entrada_numero("Lado conhecido (base ou altura)")
        if st.button("Calcular Caso 3"):
            r,exp = retangulo_inverso(caso, diagonal=d, lado=b)
            st.write(r); st.code(exp)


# =========================================================
# Losango Inverso – 5 casos
# =========================================================

def losango_inverso(caso, **kwargs):
    # Caso 1 – Duas diagonais
    if caso == 1:
        D, d = kwargs["D"], kwargs["d"]
        if D <= 0 or d <= 0:
            return {"erro":"Diagonais inválidas"}, ""
        A = (D * d) / 2
        L = math.sqrt((D/2)**2 + (d/2)**2)
        P = 4*L
        exp = f"A=(D·d)/2={A:.4f}\nL=√((D/2)²+(d/2)²)={L:.4f}\nP=4L={P:.4f}"
        return {"area":round(A,4),"lado":round(L,4),"perimetro":round(P,4)}, exp

    # Caso 2 – Área + diagonal maior
    if caso == 2:
        A, D = kwargs["area"], kwargs["D"]
        if A <= 0 or D <= 0:
            return {"erro":"Valores inválidos"}, ""
        d = (2*A)/D
        L = math.sqrt((D/2)**2 + (d/2)**2)
        P = 4*L
        exp = f"d=2A/D={d:.4f}\nL=√((D/2)²+(d/2)²)={L:.4f}\nP=4L={P:.4f}"
        return {"diagonal_menor":round(d,4),"lado":round(L,4),"perimetro":round(P,4)}, exp

    # Caso 3 – Área + diagonal menor
    if caso == 3:
        A, d = kwargs["area"], kwargs["d"]
        if A <= 0 or d <= 0:
            return {"erro":"Valores inválidos"}, ""
        D = (2*A)/d
        L = math.sqrt((D/2)**2 + (d/2)**2)
        P = 4*L
        exp = f"D=2A/d={D:.4f}\nL=√((D/2)²+(d/2)²)={L:.4f}\nP=4L={P:.4f}"
        return {"diagonal_maior":round(D,4),"lado":round(L,4),"perimetro":round(P,4)}, exp

    # Caso 4 – Lado + ângulo
    if caso == 4:
        L, ang = kwargs["lado"], math.radians(kwargs["angulo"])
        if L <= 0 or ang <= 0 or ang >= math.pi:
            return {"erro":"Valores inválidos"}, ""
        A = L**2 * math.sin(ang)
        D = 2*L*math.cos(ang/2)
        d = 2*L*math.sin(ang/2)
        P = 4*L
        exp = f"A=L²·senθ={A:.4f}\nD=2L·cos(θ/2)={D:.4f}\nd=2L·sen(θ/2)={d:.4f}\nP=4L={P:.4f}"
        return {"area":round(A,4),"D":round(D,4),"d":round(d,4),"perimetro":round(P,4)}, exp

    # Caso 5 – Área + lado
    if caso == 5:
        A, L = kwargs["area"], kwargs["lado"]
        if A <= 0 or L <= 0 or A > L**2:
            return {"erro":"Valores inválidos"}, ""
        sen_t = A / (L**2)
        ang = math.degrees(math.asin(sen_t))
        D = 2*L*math.cos(math.radians(ang/2))
        d = 2*L*math.sin(math.radians(ang/2))
        P = 4*L
        exp = f"senθ=A/L²={sen_t:.4f} → θ={ang:.4f}°\nD=2L·cos(θ/2)={D:.4f}\nd=2L·sen(θ/2)={d:.4f}\nP=4L={P:.4f}"
        return {"angulo":round(ang,4),"D":round(D,4),"d":round(d,4),"perimetro":round(P,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""


# =========================================================
# Interface – Losango Inverso (5 casos)
# =========================================================
tab_los_inv = st.tabs(["♦️ Losango Inverso"])[0]

casos_los = [
    "1. Duas diagonais → área, lado, perímetro",
    "2. Área + diagonal maior → diagonal menor, lado, perímetro",
    "3. Área + diagonal menor → diagonal maior, lado, perímetro",
    "4. Lado + ângulo → área, diagonais, perímetro",
    "5. Área + lado → ângulo, diagonais, perímetro"
]

with tab_los_inv:
    st.header("♦️ Losango Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_los)
    caso = int(caso_txt.split(".")[0])

    if caso == 1:
        D = entrada_numero("Diagonal maior (D)")
        d = entrada_numero("Diagonal menor (d)")
        if st.button("Calcular Caso 1"):
            r,exp = losango_inverso(caso, D=D, d=d)
            st.write(r); st.code(exp)

    if caso == 2:
        A = entrada_numero("Área")
        D = entrada_numero("Diagonal maior (D)")
        if st.button("Calcular Caso 2"):
            r,exp = losango_inverso(caso, area=A, D=D)
            st.write(r); st.code(exp)

    if caso == 3:
        A = entrada_numero("Área")
        d = entrada_numero("Diagonal menor (d)")
        if st.button("Calcular Caso 3"):
            r,exp = losango_inverso(caso, area=A, d=d)
            st.write(r); st.code(exp)

    if caso == 4:
        L = entrada_numero("Lado")
        ang = entrada_numero("Ângulo interno (graus)")
        if st.button("Calcular Caso 4"):
            r,exp = losango_inverso(caso, lado=L, angulo=ang)
            st.write(r); st.code(exp)

    if caso == 5:
        A = entrada_numero("Área")
        L = entrada_numero("Lado")
        if st.button("Calcular Caso 5"):
            r,exp = losango_inverso(caso, area=A, lado=L)
            st.write(r); st.code(exp)
# =========================================================
# Trapézio Inverso – 6 casos
# =========================================================

def trapezio_inverso(caso, **kwargs):
    # Caso 1 – Bases + altura
    if caso == 1:
        B,b,h = kwargs["B"],kwargs["b"],kwargs["h"]
        if B<=0 or b<=0 or h<=0:
            return {"erro":"Valores inválidos"}, ""
        A=((B+b)*h)/2
        L=math.sqrt(((B-b)/2)**2+h**2)
        P=B+b+2*L
        exp=f"A=((B+b)·h)/2={A:.4f}\nL=√(((B-b)/2)²+h²)={L:.4f}\nP=B+b+2L={P:.4f}"
        return {"area":round(A,4),"lado_obliquo":round(L,4),"perimetro":round(P,4)}, exp

    # Caso 2 – Área + bases
    if caso == 2:
        A,B,b = kwargs["area"],kwargs["B"],kwargs["b"]
        if A<=0 or B<=0 or b<=0:
            return {"erro":"Valores inválidos"}, ""
        h=(2*A)/(B+b)
        exp=f"h=2A/(B+b)={h:.4f}"
        return {"altura":round(h,4)}, exp

    # Caso 3 – Bases + lados oblíquos
    if caso == 3:
        B,b,L = kwargs["B"],kwargs["b"],kwargs["lado"]
        if B<=0 or b<=0 or L<=0 or B<=b:
            return {"erro":"Valores inválidos"}, ""
        h=math.sqrt(L**2-((B-b)/2)**2)
        A=((B+b)*h)/2
        P=B+b+2*L
        exp=f"h=√(L²-((B-b)/2)²)={h:.4f}\nA=((B+b)·h)/2={A:.4f}\nP=B+b+2L={P:.4f}"
        return {"altura":round(h,4),"area":round(A,4),"perimetro":round(P,4)}, exp

    # Caso 4 – Bases + ângulo
    if caso == 4:
        B,b,ang = kwargs["B"],kwargs["b"],math.radians(kwargs["angulo"])
        if B<=0 or b<=0 or ang<=0 or ang>=math.pi/2:
            return {"erro":"Valores inválidos"}, ""
        h=((B-b)/2)*math.tan(ang)
        L=h/math.sin(ang)
        A=((B+b)*h)/2
        P=B+b+2*L
        exp=f"h=((B-b)/2)·tanθ={h:.4f}\nL=h/senθ={L:.4f}\nA=((B+b)·h)/2={A:.4f}\nP=B+b+2L={P:.4f}"
        return {"altura":round(h,4),"lado_obliquo":round(L,4),"area":round(A,4),"perimetro":round(P,4)}, exp

    # Caso 5 – Área + altura + base maior
    if caso == 5:
        A,h,B=kwargs["area"],kwargs["h"],kwargs["B"]
        if A<=0 or h<=0 or B<=0:
            return {"erro":"Valores inválidos"}, ""
        b=(2*A)/h - B
        exp=f"b=2A/h-B={b:.4f}"
        return {"base_menor":round(b,4)}, exp

    # Caso 6 – Bases + diagonais
    if caso == 6:
        B,b,d1,d2=kwargs["B"],kwargs["b"],kwargs["d1"],kwargs["d2"]
        if B<=0 or b<=0 or d1<=0 or d2<=0:
            return {"erro":"Valores inválidos"}, ""
        # Fórmula via Brahmagupta adaptada (trapézio = quadrilátero cíclico quando isósceles)
        # Aproximação: média geométrica
        h=math.sqrt(d1**2 - ((B-b)/2)**2)
        A=((B+b)*h)/2
        exp=f"h≈√(d1²-((B-b)/2)²)={h:.4f}\nA=((B+b)·h)/2={A:.4f}"
        return {"altura":round(h,4),"area":round(A,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""


# =========================================================
# Interface – Trapézio Inverso (6 casos)
# =========================================================
tab_trap_inv = st.tabs(["⏢ Trapézio Inverso"])[0]

casos_trap = [
    "1. Bases + altura → área, perímetro (isósceles)",
    "2. Área + bases → altura",
    "3. Bases + lados oblíquos → altura, área, perímetro",
    "4. Bases + ângulo → altura, lados, área, perímetro",
    "5. Área + altura + base maior → base menor",
    "6. Bases + diagonais → altura, área"
]

with tab_trap_inv:
    st.header("⏢ Trapézio Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_trap)
    caso = int(caso_txt.split(".")[0])

    if caso == 1:
        B=entrada_numero("Base maior (B)")
        b=entrada_numero("Base menor (b)")
        h=entrada_numero("Altura (h)")
        if st.button("Calcular Caso 1"):
            r,exp=trapezio_inverso(caso,B=B,b=b,h=h)
            st.write(r); st.code(exp)

    if caso == 2:
        A=entrada_numero("Área")
        B=entrada_numero("Base maior (B)")
        b=entrada_numero("Base menor (b)")
        if st.button("Calcular Caso 2"):
            r,exp=trapezio_inverso(caso,area=A,B=B,b=b)
            st.write(r); st.code(exp)

    if caso == 3:
        B=entrada_numero("Base maior (B)")
        b=entrada_numero("Base menor (b)")
        L=entrada_numero("Lado oblíquo (isósceles)")
        if st.button("Calcular Caso 3"):
            r,exp=trapezio_inverso(caso,B=B,b=b,lado=L)
            st.write(r); st.code(exp)

    if caso == 4:
        B=entrada_numero("Base maior (B)")
        b=entrada_numero("Base menor (b)")
        ang=entrada_numero("Ângulo com a base maior (graus)")
        if st.button("Calcular Caso 4"):
            r,exp=trapezio_inverso(caso,B=B,b=b,angulo=ang)
            st.write(r); st.code(exp)

    if caso == 5:
        A=entrada_numero("Área")
        h=entrada_numero("Altura (h)")
        B=entrada_numero("Base maior (B)")
        if st.button("Calcular Caso 5"):
            r,exp=trapezio_inverso(caso,area=A,h=h,B=B)
            st.write(r); st.code(exp)

    if caso == 6:
        B=entrada_numero("Base maior (B)")
        b=entrada_numero("Base menor (b)")
        d1=entrada_numero("Diagonal 1")
        d2=entrada_numero("Diagonal 2")
        if st.button("Calcular Caso 6"):
            r,exp=trapezio_inverso(caso,B=B,b=b,d1=d1,d2=d2)
            st.write(r); st.code(exp)
# =========================================================
# Paralelogramo Inverso – 6 casos
# =========================================================

def paralelogramo_inverso(caso, **kwargs):
    # Caso 1 – Base + altura
    if caso == 1:
        b,h = kwargs["base"],kwargs["altura"]
        if b<=0 or h<=0: return {"erro":"Valores inválidos"}, ""
        A=b*h
        P=2*(b+h)
        exp=f"A=b·h={A:.4f}\nP=2(b+h)={P:.4f}"
        return {"area":round(A,4),"perimetro":round(P,4)}, exp

    # Caso 2 – Dois lados + ângulo
    if caso == 2:
        a,b,ang = kwargs["a"],kwargs["b"],math.radians(kwargs["angulo"])
        if a<=0 or b<=0 or ang<=0 or ang>=math.pi:
            return {"erro":"Valores inválidos"}, ""
        A=a*b*math.sin(ang)
        h=A/b
        d1=math.sqrt(a**2+b**2+2*a*b*math.cos(ang))
        d2=math.sqrt(a**2+b**2-2*a*b*math.cos(ang))
        P=2*(a+b)
        exp=f"A=a·b·senθ={A:.4f}\nh=A/b={h:.4f}\nd1=√(a²+b²+2abcosθ)={d1:.4f}\nd2=√(a²+b²-2abcosθ)={d2:.4f}\nP=2(a+b)={P:.4f}"
        return {"area":round(A,4),"altura":round(h,4),"d1":round(d1,4),"d2":round(d2,4),"perimetro":round(P,4)}, exp

    # Caso 3 – Dois lados + diagonal
    if caso == 3:
        a,b,d=kwargs["a"],kwargs["b"],kwargs["diag"]
        if a<=0 or b<=0 or d<=0: return {"erro":"Valores inválidos"}, ""
        cos_t=(d**2 - a**2 - b**2)/(2*a*b)
        if cos_t<-1 or cos_t>1: return {"erro":"Valores incompatíveis"}, ""
        ang=math.degrees(math.acos(cos_t))
        A=a*b*math.sin(math.acos(cos_t))
        exp=f"cosθ=(d²-a²-b²)/(2ab)={cos_t:.4f} → θ={ang:.4f}°\nA=a·b·senθ={A:.4f}"
        return {"angulo":round(ang,4),"area":round(A,4)}, exp

    # Caso 4 – Área + lado
    if caso == 4:
        A,b=kwargs["area"],kwargs["lado"]
        if A<=0 or b<=0: return {"erro":"Valores inválidos"}, ""
        h=A/b
        exp=f"h=A/b={h:.4f}"
        return {"altura":round(h,4)}, exp

    # Caso 5 – Área + dois lados
    if caso == 5:
        A,a,b=kwargs["area"],kwargs["a"],kwargs["b"]
        if A<=0 or a<=0 or b<=0 or A>(a*b): return {"erro":"Valores inválidos"}, ""
        sen_t=A/(a*b)
        ang=math.degrees(math.asin(sen_t))
        exp=f"senθ=A/(a·b)={sen_t:.4f} → θ={ang:.4f}°"
        return {"angulo":round(ang,4)}, exp

    # Caso 6 – Altura + lado
    if caso == 6:
        b,h=kwargs["base"],kwargs["altura"]
        if b<=0 or h<=0: return {"erro":"Valores inválidos"}, ""
        A=b*h
        P=2*(b+h)
        exp=f"A=b·h={A:.4f}\nP=2(b+h)={P:.4f}"
        return {"area":round(A,4),"perimetro":round(P,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""


# =========================================================
# Interface – Paralelogramo Inverso (6 casos)
# =========================================================
tab_par_inv = st.tabs(["⬛ Paralelogramo Inverso"])[0]

casos_par = [
    "1. Base + altura → área, perímetro",
    "2. Dois lados + ângulo → área, altura, diagonais, perímetro",
    "3. Dois lados + diagonal → ângulo, área",
    "4. Área + lado → altura",
    "5. Área + dois lados → ângulo",
    "6. Altura + lado → área, perímetro"
]

with tab_par_inv:
    st.header("⬛ Paralelogramo Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_par)
    caso = int(caso_txt.split(".")[0])

    if caso == 1:
        b=entrada_numero("Base")
        h=entrada_numero("Altura")
        if st.button("Calcular Caso 1"):
            r,exp=paralelogramo_inverso(caso,base=b,altura=h)
            st.write(r); st.code(exp)

    if caso == 2:
        a=entrada_numero("Lado a")
        b=entrada_numero("Lado b")
        ang=entrada_numero("Ângulo (graus)")
        if st.button("Calcular Caso 2"):
            r,exp=paralelogramo_inverso(caso,a=a,b=b,angulo=ang)
            st.write(r); st.code(exp)

    if caso == 3:
        a=entrada_numero("Lado a")
        b=entrada_numero("Lado b")
        d=entrada_numero("Diagonal")
        if st.button("Calcular Caso 3"):
            r,exp=paralelogramo_inverso(caso,a=a,b=b,diag=d)
            st.write(r); st.code(exp)

    if caso == 4:
        A=entrada_numero("Área")
        b=entrada_numero("Lado")
        if st.button("Calcular Caso 4"):
            r,exp=paralelogramo_inverso(caso,area=A,lado=b)
            st.write(r); st.code(exp)

    if caso == 5:
        A=entrada_numero("Área")
        a=entrada_numero("Lado a")
        b=entrada_numero("Lado b")
        if st.button("Calcular Caso 5"):
            r,exp=paralelogramo_inverso(caso,area=A,a=a,b=b)
            st.write(r); st.code(exp)

    if caso == 6:
        b=entrada_numero("Base")
        h=entrada_numero("Altura")
        if st.button("Calcular Caso 6"):
            r,exp=paralelogramo_inverso(caso,base=b,altura=h)
            st.write(r); st.code(exp)
# =========================================================
# Círculo Inverso – 6 casos
# =========================================================

def circulo_inverso(caso, **kwargs):
    # Caso 1 – Raio
    if caso == 1:
        r=kwargs["raio"]
        if r<=0: return {"erro":"Raio inválido"}, ""
        d=2*r
        A=math.pi*r**2
        P=2*math.pi*r
        exp=f"d=2r={d:.4f}\nA=πr²={A:.4f}\nP=2πr={P:.4f}"
        return {"diametro":round(d,4),"area":round(A,4),"perimetro":round(P,4)}, exp

    # Caso 2 – Diâmetro
    if caso == 2:
        d=kwargs["diametro"]
        if d<=0: return {"erro":"Diâmetro inválido"}, ""
        r=d/2
        A=math.pi*r**2
        P=2*math.pi*r
        exp=f"r=d/2={r:.4f}\nA=πr²={A:.4f}\nP=2πr={P:.4f}"
        return {"raio":round(r,4),"area":round(A,4),"perimetro":round(P,4)}, exp

    # Caso 3 – Área
    if caso == 3:
        A=kwargs["area"]
        if A<=0: return {"erro":"Área inválida"}, ""
        r=math.sqrt(A/math.pi)
        d=2*r
        P=2*math.pi*r
        exp=f"r=√(A/π)={r:.4f}\nd=2r={d:.4f}\nP=2πr={P:.4f}"
        return {"raio":round(r,4),"diametro":round(d,4),"perimetro":round(P,4)}, exp

    # Caso 4 – Perímetro
    if caso == 4:
        P=kwargs["perimetro"]
        if P<=0: return {"erro":"Perímetro inválido"}, ""
        r=P/(2*math.pi)
        d=2*r
        A=math.pi*r**2
        exp=f"r=P/(2π)={r:.4f}\nd=2r={d:.4f}\nA=πr²={A:.4f}"
        return {"raio":round(r,4),"diametro":round(d,4),"area":round(A,4)}, exp

    # Caso 5 – Ângulo central + raio
    if caso == 5:
        ang,r=kwargs["angulo"],kwargs["raio"]
        if r<=0 or ang<=0 or ang>360: return {"erro":"Valores inválidos"}, ""
        A=(ang/360)*math.pi*r**2
        C=(ang/360)*2*math.pi*r
        exp=f"A_setor=(θ/360)πr²={A:.4f}\nC_arco=(θ/360)2πr={C:.4f}"
        return {"area_setor":round(A,4),"comprimento_arco":round(C,4)}, exp

    # Caso 6 – Arco + raio
    if caso == 6:
        C,r=kwargs["arco"],kwargs["raio"]
        if C<=0 or r<=0: return {"erro":"Valores inválidos"}, ""
        ang=(C/(2*math.pi*r))*360
        A=(ang/360)*math.pi*r**2
        exp=f"θ=(C/(2πr))·360={ang:.4f}°\nA_setor=(θ/360)πr²={A:.4f}"
        return {"angulo":round(ang,4),"area_setor":round(A,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""


# =========================================================
# Interface – Círculo Inverso (6 casos)
# =========================================================
tab_circ_inv = st.tabs(["⚪ Círculo Inverso"])[0]

casos_circ = [
    "1. Raio → diâmetro, área, perímetro",
    "2. Diâmetro → raio, área, perímetro",
    "3. Área → raio, diâmetro, perímetro",
    "4. Perímetro → raio, diâmetro, área",
    "5. Ângulo central + raio → área do setor, comprimento do arco",
    "6. Arco + raio → ângulo central, área do setor"
]

with tab_circ_inv:
    st.header("⚪ Círculo Inverso")
    caso_txt = st.selectbox("Selecione o caso", casos_circ)
    caso = int(caso_txt.split(".")[0])

    if caso == 1:
        r=entrada_numero("Raio")
        if st.button("Calcular Caso 1"):
            r,exp=circulo_inverso(caso,raio=r)
            st.write(r); st.code(exp)

    if caso == 2:
        d=entrada_numero("Diâmetro")
        if st.button("Calcular Caso 2"):
            r,exp=circulo_inverso(caso,diametro=d)
            st.write(r); st.code(exp)

    if caso == 3:
        A=entrada_numero("Área")
        if st.button("Calcular Caso 3"):
            r,exp=circulo_inverso(caso,area=A)
            st.write(r); st.code(exp)

    if caso == 4:
        P=entrada_numero("Perímetro (circunferência)")
        if st.button("Calcular Caso 4"):
            r,exp=circulo_inverso(caso,perimetro=P)
            st.write(r); st.code(exp)

    if caso == 5:
        ang=entrada_numero("Ângulo central (graus)")
        r=entrada_numero("Raio")
        if st.button("Calcular Caso 5"):
            r,exp=circulo_inverso(caso,angulo=ang,raio=r)
            st.write(r); st.code(exp)

    if caso == 6:
        C=entrada_numero("Comprimento do arco")
        r=entrada_numero("Raio")
        if st.button("Calcular Caso 6"):
            r,exp=circulo_inverso(caso,arco=C,raio=r)
            st.write(r); st.code(exp)
# =========================================================
# Polígono Regular Inverso – 6 casos
# =========================================================

def poligono_inverso(caso, **kwargs):
    n = kwargs.get("n")
    if not n or n < 5 or n > 10:
        return {"erro":"Número de lados deve estar entre 5 e 10"}, ""

    # Caso 1 – lado + n
    if caso == 1:
        a=kwargs["lado"]
        if a<=0: return {"erro":"Lado inválido"}, ""
        P=n*a
        r=a/(2*math.tan(math.pi/n))
        A=(n*a**2)/(4*math.tan(math.pi/n))
        R=a/(2*math.sin(math.pi/n))
        exp=f"P=n·a={P:.4f}\nr=a/(2tan(π/n))={r:.4f}\nA=n·a²/(4tan(π/n))={A:.4f}\nR=a/(2sen(π/n))={R:.4f}"
        return {"perimetro":round(P,4),"apotema":round(r,4),"area":round(A,4),"raio_circ":round(R,4)}, exp

    # Caso 2 – apótema + n
    if caso == 2:
        r=kwargs["apotema"]
        if r<=0: return {"erro":"Apótema inválido"}, ""
        a=2*r*math.tan(math.pi/n)
        P=n*a
        A=(P*r)/2
        R=a/(2*math.sin(math.pi/n))
        exp=f"a=2r·tan(π/n)={a:.4f}\nP=n·a={P:.4f}\nA=P·r/2={A:.4f}\nR=a/(2sen(π/n))={R:.4f}"
        return {"lado":round(a,4),"perimetro":round(P,4),"area":round(A,4),"raio_circ":round(R,4)}, exp

    # Caso 3 – perímetro + n
    if caso == 3:
        P=kwargs["perimetro"]
        if P<=0: return {"erro":"Perímetro inválido"}, ""
        a=P/n
        r=a/(2*math.tan(math.pi/n))
        A=(P*r)/2
        R=a/(2*math.sin(math.pi/n))
        exp=f"a=P/n={a:.4f}\nr=a/(2tan(π/n))={r:.4f}\nA=P·r/2={A:.4f}\nR=a/(2sen(π/n))={R:.4f}"
        return {"lado":round(a,4),"apotema":round(r,4),"area":round(A,4),"raio_circ":round(R,4)}, exp

    # Caso 4 – área + n
    if caso == 4:
        A=kwargs["area"]
        if A<=0: return {"erro":"Área inválida"}, ""
        a=math.sqrt((4*A*math.tan(math.pi/n))/n)
        P=n*a
        r=a/(2*math.tan(math.pi/n))
        R=a/(2*math.sin(math.pi/n))
        exp=f"a=√(4A·tan(π/n)/n)={a:.4f}\nP=n·a={P:.4f}\nr=a/(2tan(π/n))={r:.4f}\nR=a/(2sen(π/n))={R:.4f}"
        return {"lado":round(a,4),"perimetro":round(P,4),"apotema":round(r,4),"raio_circ":round(R,4)}, exp

    # Caso 5 – raio circunscrito + n
    if caso == 5:
        R=kwargs["raio_circ"]
        if R<=0: return {"erro":"Raio circunscrito inválido"}, ""
        a=2*R*math.sin(math.pi/n)
        r=R*math.cos(math.pi/n)
        P=n*a
        A=(P*r)/2
        exp=f"a=2R·sen(π/n)={a:.4f}\nr=R·cos(π/n)={r:.4f}\nP=n·a={P:.4f}\nA=P·r/2={A:.4f}"
        return {"lado":round(a,4),"apotema":round(r,4),"perimetro":round(P,4),"area":round(A,4)}, exp

    # Caso 6 – raio inscrito (apótema) + n
    if caso == 6:
        r=kwargs["raio_insc"]
        if r<=0: return {"erro":"Raio inscrito inválido"}, ""
        a=2*r*math.tan(math.pi/n)
        R=r/math.cos(math.pi/n)
        P=n*a
        A=(P*r)/2
        exp=f"a=2r·tan(π/n)={a:.4f}\nR=r/cos(π/n)={R:.4f}\nP=n·a={P:.4f}\nA=P·r/2={A:.4f}"
        return {"lado":round(a,4),"raio_circ":round(R,4),"perimetro":round(P,4),"area":round(A,4)}, exp

    return {"erro":"Caso não reconhecido"}, ""


# =========================================================
# Interface – Polígono Regular Inverso (6 casos)
# =========================================================
tab_pol_inv = st.tabs(["🔷 Polígono Regular Inverso"])[0]

casos_pol = [
    "1. Lado + n → perímetro, apótema, área, raio circunscrito",
    "2. Apótema + n → lado, perímetro, área, raio circunscrito",
    "3. Perímetro + n → lado, apótema, área, raio circunscrito",
    "4. Área + n → lado, perímetro, apótema, raio circunscrito",
    "5. Raio circunscrito + n → lado, apótema, perímetro, área",
    "6. Raio inscrito (apótema) + n → lado, raio circunscrito, perímetro, área"
]

with tab_pol_inv:
    st.header("🔷 Polígono Regular Inverso (5 a 10 lados)")
    caso_txt = st.selectbox("Selecione o caso", casos_pol)
    caso = int(caso_txt.split(".")[0])
    n = entrada_numero("Número de lados (5 a 10)",5)

    if caso == 1:
        a=entrada_numero("Lado")
        if st.button("Calcular Caso 1"):
            r,exp=poligono_inverso(caso,lado=a,n=n)
            st.write(r); st.code(exp)

    if caso == 2:
        r=entrada_numero("Apótema")
        if st.button("Calcular Caso 2"):
            r,exp=poligono_inverso(caso,apotema=r,n=n)
            st.write(r); st.code(exp)

    if caso == 3:
        P=entrada_numero("Perímetro")
        if st.button("Calcular Caso 3"):
            r,exp=poligono_inverso(caso,perimetro=P,n=n)
            st.write(r); st.code(exp)

    if caso == 4:
        A=entrada_numero("Área")
        if st.button("Calcular Caso 4"):
            r,exp=poligono_inverso(caso,area=A,n=n)
            st.write(r); st.code(exp)

    if caso == 5:
        R=entrada_numero("Raio circunscrito")
        if st.button("Calcular Caso 5"):
            r,exp=poligono_inverso(caso,raio_circ=R,n=n)
            st.write(r); st.code(exp)

    if caso == 6:
        r=entrada_numero("Raio inscrito (apótema)")
        if st.button("Calcular Caso 6"):
            r,exp=poligono_inverso(caso,raio_insc=r,n=n)
            st.write(r); st.code(exp)
