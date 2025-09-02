from utils import entrada_numero
import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

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
    per = 4*lado
    area = lado**2
    explicacao = f"""⬛ Quadrado
Perímetro = 4*lado = 4*{lado} = {per}
Área = lado² = {lado}² = {area}
"""
    return {"perímetro": per, "área": area}, explicacao

def retangulo(base, altura):
    if base <= 0 or altura <= 0:
        return {"erro": "Base e altura devem ser positivos!"}, ""
    per = 2*(base+altura)
    area = base*altura
    explicacao = f"""▭ Retângulo
Perímetro = 2*(b+h) = 2*({base}+{altura}) = {per}
Área = b*h = {base}*{altura} = {area}
"""
    return {"perímetro": per, "área": area}, explicacao

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
    # Caso 1: 2 lados + ângulo entre eles → 3º lado + área
    if caso == 1:
        a, b, angC = kwargs["a"], kwargs["b"], math.radians(kwargs["angC"])
        c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(angC))
        area = 0.5*a*b*math.sin(angC)
        explicacao = f"""Caso 1
Lei dos cossenos: c² = a² + b² - 2ab·cos(C)
Área = ½ab·sen(C)
"""
        return {"c": round(c,4), "area": round(area,4)}, explicacao

    # Caso 2: 2 lados + ângulo oposto a um deles → ângulo oposto ao outro
    if caso == 2:
        a, b, angA = kwargs["a"], kwargs["b"], math.radians(kwargs["angA"])
        senB = b*math.sin(angA)/a
        if abs(senB) > 1:
            return {"erro":"Dados inválidos"}, ""
        angB = math.degrees(math.asin(senB))
        explicacao = f"""Caso 2
Lei dos senos: sen(B)/b = sen(A)/a
"""
        return {"angB": round(angB,4)}, explicacao

    # ------------------------------
    # Grupo 2 – Misturando área
    # ------------------------------
    # Caso 3: Área + 2 lados → ângulo entre eles
    if caso == 3:
        a,b,area = kwargs["a"], kwargs["b"], kwargs["area"]
        senC = (2*area)/(a*b)
        if abs(senC) > 1:
            return {"erro":"Área inválida"}, ""
        angC = math.degrees(math.asin(senC))
        explicacao = f"""Caso 3
Área = ½ab·sen(C) → sen(C) = 2A/(ab)
"""
        return {"angC": round(angC,4)}, explicacao

    # Caso 4: Área + 1 lado + ângulo oposto → outro lado
    if caso == 4:
        a, area, angB = kwargs["a"], kwargs["area"], math.radians(kwargs["angB"])
        c = (2*area)/(a*math.sin(angB))
        explicacao = f"""Caso 4
Área = ½ac·sen(B) → c = 2A/(a·sen(B))
"""
        return {"c": round(c,4)}, explicacao

    # Caso 5: Área + 3 ângulos → lados proporcionais
    if caso == 5:
        area = kwargs["area"]
        angA, angB, angC = map(lambda x: math.radians(kwargs[x]), ["angA","angB","angC"])
        # escala aproximada
        k = math.sqrt((4*area)/(math.sin(2*angA)+math.sin(2*angB)+math.sin(2*angC)))
        a = k*math.sin(angA); b = k*math.sin(angB); c = k*math.sin(angC)
        explicacao = f"""Caso 5
3 ângulos + área → apenas semelhança
Escala definida pela área
"""
        return {"a": round(a,4), "b": round(b,4), "c": round(c,4)}, explicacao

    # ------------------------------
    # Grupo 3 – Mistura de ângulos
    # ------------------------------
    # Caso 6: 1 lado + 2 ângulos → outros 2 lados
    if caso == 6:
        a = kwargs["a"]
        angA = math.radians(kwargs["angA"])
        angB = math.radians(kwargs["angB"])
        angC = math.pi-(angA+angB)
        b = a*math.sin(angB)/math.sin(angA)
        c = a*math.sin(angC)/math.sin(angA)
        return {"b": round(b,4),"c": round(c,4)}, "Caso 6 – Lei dos senos"

    # Caso 7: 2 ângulos + área → lados em escala
    if caso == 7:
        area = kwargs["area"]
        angA,angB = map(lambda x: math.radians(kwargs[x]),["angA","angB"])
        angC = math.pi-(angA+angB)
        k = math.sqrt((2*area*math.sin(angA+angB))/(math.sin(angA)*math.sin(angB)*math.sin(angC)))
        a=k*math.sin(angA); b=k*math.sin(angB); c=k*math.sin(angC)
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4)}, "Caso 7 – Escala com área e ângulos"

    # Caso 8: 3 ângulos + perímetro → lados
    if caso == 8:
        P=kwargs["perimetro"]
        angA,angB,angC = map(lambda x: math.radians(kwargs[x]),["angA","angB","angC"])
        k=P/(math.sin(angA)+math.sin(angB)+math.sin(angC))
        a=k*math.sin(angA); b=k*math.sin(angB); c=k*math.sin(angC)
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4)}, "Caso 8 – Escala com perímetro e ângulos"

    # ------------------------------
    # Grupo 4 – Alturas/medianas/bissetrizes
    # ------------------------------
    # Caso 9: 1 lado + altura relativa → área
    if caso == 9:
        a,h=kwargs["a"],kwargs["h"]
        area=0.5*a*h
        return {"area":round(area,4)}, "Caso 9 – Área = ½ah"

    # Caso 10: 3 alturas (complexo – placeholder)
    if caso == 10:
        return {"info":"Necessário resolver sistema – não implementado"}, "Caso 10 – 3 alturas"

    # Caso 11: 1 lado + bissetriz + ângulos
    if caso == 11:
        return {"info":"Cálculo avançado de bissetriz – não implementado"}, "Caso 11 – bissetriz"

    # Caso 12: lado + mediatriz
    if caso == 12:
        return {"info":"Mediatriz → circunrádio – não implementado"}, "Caso 12 – mediatriz"

    # ------------------------------
    # Grupo 5 – Circunferências notáveis
    # ------------------------------
    # Caso 13: r + P → área
    if caso == 13:
        r,P=kwargs["r"],kwargs["P"]
        area=0.5*r*P
        return {"area":round(area,4)}, "Caso 13 – Área = rP/2"

    # Caso 14: R + ângulos → lados
    if caso == 14:
        R=kwargs["R"]
        angA,angB,angC = map(lambda x: math.radians(kwargs[x]),["angA","angB","angC"])
        a=2*R*math.sin(angA); b=2*R*math.sin(angB); c=2*R*math.sin(angC)
        return {"a":round(a,4),"b":round(b,4),"c":round(c,4)}, "Caso 14 – Lei dos senos com R"

    # Caso 15: área + r → perímetro
    if caso == 15:
        area,r=kwargs["area"],kwargs["r"]
        P=2*area/r
        return {"P":round(P,4)}, "Caso 15 – P=2A/r"

    # Caso 16: área + R → lados via trig
    if caso == 16:
        return {"info":"Necessário trig avançada com R – não implementado"}, "Caso 16"

    # ------------------------------
    # Grupo 6 – Retângulo
    # ------------------------------
    # Caso 17: catetos → hipotenusa
    if caso == 17:
        cat1,cat2=kwargs["cat1"],kwargs["cat2"]
        hip=math.sqrt(cat1**2+cat2**2)
        return {"hip":round(hip,4)}, "Caso 17 – Pitágoras"

    # Caso 18: hip + cat → outro cateto
    if caso == 18:
        hip,cat=kwargs["hip"],kwargs["cat"]
        outro=math.sqrt(hip**2-cat**2)
        return {"outro_cat":round(outro,4)}, "Caso 18 – Pitágoras"

    # Caso 19: área + cat → outro cateto
    if caso == 19:
        area,cat=kwargs["area"],kwargs["cat"]
        outro=(2*area)/cat
        return {"outro_cat":round(outro,4)}, "Caso 19 – Área=½ab"

    # Caso 20: perímetro + área → lados
    if caso == 20:
        return {"info":"Sistema de equações (não implementado)"}, "Caso 20"

    return {"erro":"Caso não reconhecido"}, ""
# =========================================================
# Interface – Triângulo Inverso (20 casos)
# =========================================================
tab_triang_inv = st.tabs(["🔺 Triângulo Inverso"])[0]

with tab_triang_inv:
    st.header("🔺 Triângulo Inverso")

    caso = st.selectbox("Selecione o caso", list(range(1,21)))

    if caso == 1:
        a=entrada_numero("Lado a"); b=entrada_numero("Lado b"); angC=entrada_numero("Ângulo C (graus)")
        if st.button("Calcular"): st.write(*triangulo_inverso(1,a=a,b=b,angC=angC))
    if caso == 2:
        a=entrada_numero("Lado a"); b=entrada_numero("Lado b"); angA=entrada_numero("Ângulo A (graus)")
        if st.button("Calcular"): st.write(*triangulo_inverso(2,a=a,b=b,angA=angA))
    if caso == 3:
        a=entrada_numero("Lado a"); b=entrada_numero("Lado b"); area=entrada_numero("Área")
        if st.button("Calcular"): st.write(*triangulo_inverso(3,a=a,b=b,area=area))
    if caso == 4:
        a=entrada_numero("Lado a"); angB=entrada_numero("Ângulo B (graus)"); area=entrada_numero("Área")
        if st.button("Calcular"): st.write(*triangulo_inverso(4,a=a,angB=angB,area=area))
    if caso == 5:
        angA=entrada_numero("Ângulo A"); angB=entrada_numero("Ângulo B"); angC=entrada_numero("Ângulo C"); area=entrada_numero("Área")
        if st.button("Calcular"): st.write(*triangulo_inverso(5,area=area,angA=angA,angB=angB,angC=angC))
    if caso == 6:
        a=entrada_numero("Lado a"); angA=entrada_numero("Ângulo A"); angB=entrada_numero("Ângulo B")
        if st.button("Calcular"): st.write(*triangulo_inverso(6,a=a,angA=angA,angB=angB))
    if caso == 7:
        area=entrada_numero("Área"); angA=entrada_numero("Ângulo A"); angB=entrada_numero("Ângulo B")
        if st.button("Calcular"): st.write(*triangulo_inverso(7,area=area,angA=angA,angB=angB))
    if caso == 8:
        P=entrada_numero("Perímetro"); angA=entrada_numero("Ângulo A"); angB=entrada_numero("Ângulo B"); angC=entrada_numero("Ângulo C")
        if st.button("Calcular"): st.write(*triangulo_inverso(8,perimetro=P,angA=angA,angB=angB,angC=angC))
    if caso == 9:
        a=entrada_numero("Lado a"); h=entrada_numero("Altura relativa")
        if st.button("Calcular"): st.write(*triangulo_inverso(9,a=a,h=h))
    if caso == 10:
        st.write(*triangulo_inverso(10))
    if caso == 11:
        st.write(*triangulo_inverso(11))
    if caso == 12:
        st.write(*triangulo_inverso(12))
    if caso == 13:
        r=entrada_numero("Raio inscrito"); P=entrada_numero("Perímetro")
        if st.button("Calcular"): st.write(*triangulo_inverso(13,r=r,P=P))
    if caso == 14:
        R=entrada_numero("Raio circunscrito"); angA=entrada_numero("Ângulo A"); angB=entrada_numero("Ângulo B"); angC=entrada_numero("Ângulo C")
        if st.button("Calcular"): st.write(*triangulo_inverso(14,R=R,angA=angA,angB=angB,angC=angC))
    if caso == 15:
        area=entrada_numero("Área"); r=entrada_numero("Raio inscrito")
        if st.button("Calcular"): st.write(*triangulo_inverso(15,area=area,r=r))
    if caso == 16:
        area=entrada_numero("Área"); R=entrada_numero("Raio circunscrito")
        if st.button("Calcular"): st.write(*triangulo_inverso(16,area=area,R=R))
    if caso == 17:
        cat1=entrada_numero("Cateto 1"); cat2=entrada_numero("Cateto 2")
        if st.button("Calcular"): st.write(*triangulo_inverso(17,cat1=cat1,cat2=cat2))
    if caso == 18:
        hip=entrada_numero("Hipotenusa"); cat=entrada_numero("Cateto")
        if st.button("Calcular"): st.write(*triangulo_inverso(18,hip=hip,cat=cat))
    if caso == 19:
        area=entrada_numero("Área"); cat=entrada_numero("Cateto")
        if st.button("Calcular"): st.write(*triangulo_inverso(19,area=area,cat=cat))
    if caso == 20:
        st.write(*triangulo_inverso(20))
