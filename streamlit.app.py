from utils import entrada_numero
import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

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

def plot_figura_3d(tipo, **params):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if tipo == "paralelepipedo":
        c = params.get("c", 1)
        l = params.get("l", 1)
        h = params.get("h", 1)

        # vértices
        vertices = np.array([
            [0,0,0], [c,0,0], [c,l,0], [0,l,0],  # base inferior
            [0,0,h], [c,0,h], [c,l,h], [0,l,h]   # base superior
        ])

        # faces (cada face é uma lista de índices dos vértices)
        faces = [
            [vertices[j] for j in [0,1,2,3]],  # base inferior
            [vertices[j] for j in [4,5,6,7]],  # base superior
            [vertices[j] for j in [0,1,5,4]],
            [vertices[j] for j in [1,2,6,5]],
            [vertices[j] for j in [2,3,7,6]],
            [vertices[j] for j in [3,0,4,7]],
        ]

        ax.add_collection3d(Poly3DCollection(faces, facecolors="cyan", linewidths=1, edgecolors="r", alpha=.25))

    elif tipo == "prisma":
        n = params.get("n", 5)
        lado = params.get("lado", 1)
        h = params.get("h", 2)

        # raio da circunferência circunscrita da base
        R = lado / (2*math.sin(math.pi/n))

        # base inferior e superior
        base_inf = [(R*math.cos(2*math.pi*i/n), R*math.sin(2*math.pi*i/n), 0) for i in range(n)]
        base_sup = [(x,y,h) for (x,y,_) in base_inf]

        # faces
        faces = []
        faces.append(base_inf)
        faces.append(base_sup)
        for i in range(n):
            faces.append([base_inf[i], base_inf[(i+1)%n], base_sup[(i+1)%n], base_sup[i]])

        ax.add_collection3d(Poly3DCollection(faces, facecolors="lightgreen", linewidths=1, edgecolors="k", alpha=.3))

    # (os outros tipos: cubo, esfera, cilindro, cone, pirâmide já estavam prontos)

    ax.set_box_aspect([1,1,1])
    st.pyplot(fig)

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
# Função de Plotagem 3D
# =========================================================
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_figura_3d(tipo, **params):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if tipo == "cubo":
        lado = params.get("lado",1)
        r = [0, lado]
        # vértices
        vertices = [
            [(x,y,z) for x in r for y in r for z in r]
        ]
        for s, e in [
            ([0,0,0],[0,0,1]),([0,0,0],[0,1,0]),([0,0,0],[1,0,0]),
            ([1,1,1],[1,1,0]),([1,1,1],[1,0,1]),([1,1,1],[0,1,1]),
            ([0,1,1],[0,1,0]),([0,1,1],[1,1,1]),([0,1,1],[0,0,1]),
            ([1,0,1],[1,0,0]),([1,0,1],[1,1,1]),([1,0,1],[0,0,1]),
            ([1,1,0],[0,1,0]),([1,1,0],[1,0,0]),([1,1,0],[1,1,1]),
        ]:
            ax.plot([s[0]*lado, e[0]*lado],[s[1]*lado,e[1]*lado],[s[2]*lado,e[2]*lado],color="b")

    elif tipo == "esfera":
        r = params.get("r",1)
        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x = r*np.outer(np.cos(u), np.sin(v))
        y = r*np.outer(np.sin(u), np.sin(v))
        z = r*np.outer(np.ones_like(u), np.cos(v))
        ax.plot_wireframe(x,y,z,color="r",alpha=0.6)

    elif tipo == "cilindro":
        r = params.get("r",1)
        h = params.get("h",2)
        z = np.linspace(0,h,30)
        theta = np.linspace(0,2*np.pi,30)
        theta,z = np.meshgrid(theta,z)
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        ax.plot_surface(x,y,z,alpha=0.3)

    elif tipo == "cone":
        r = params.get("r",1)
        h = params.get("h",2)
        theta = np.linspace(0,2*np.pi,30)
        R = np.linspace(0,r,30)
        T,R = np.meshgrid(theta,R)
        X = R*np.cos(T)
        Y = R*np.sin(T)
        Z = (h/r)*(r-R)
        ax.plot_surface(X,Y,Z,alpha=0.3)

    elif tipo == "pirâmide":
        n = params.get("n", 4)     # nº de lados da base
        lado = params.get("lado", 1)
        h = params.get("h", 2)

        # Raio da circunferência circunscrita da base
        R = lado / (2 * math.sin(math.pi / n))

        # Vértices da base
        base = [(R * math.cos(2*math.pi*i/n), R * math.sin(2*math.pi*i/n), 0) for i in range(n)]
        topo = (0, 0, h)

        # Desenhar base
        xs, ys, zs = zip(*base, base[0])  # fecha o polígono
        ax.plot(xs, ys, zs, color="g")

        # Desenhar arestas até o topo
        for v in base:
            ax.plot([v[0], topo[0]], [v[1], topo[1]], [v[2], topo[2]], color="g")

        ax.set_box_aspect([1,1,1])  # escala igual

    st.pyplot(fig)


# =========================================================
# Interface Streamlit – Parte 2 (com explicações + plots)
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
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("cubo", lado=lado)

with tab9:
    st.header("📦 Paralelepípedo")
    c = entrada_numero("Comprimento", chave="par_c")
    l = entrada_numero("Largura", chave="par_l")
    h = entrada_numero("Altura", chave="par_h")
    if st.button("Calcular Paralelepípedo"):
        resultado, explicacao = paralelepipedo(c, l, h)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("paralelepipedo", c=c, l=l, h=h)

with tab10:
    st.header("🔺 Prisma Regular")
    n = st.number_input("Número de lados da base", min_value=3, step=1, key="prisma_n")
    lado = entrada_numero("Lado da base", chave="prisma_lado")
    h = entrada_numero("Altura", chave="prisma_alt")
    if st.button("Calcular Prisma"):
        resultado, explicacao = prisma(n, lado, h)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("prisma", n=n, lado=lado, h=h)

with tab11:
    st.header("🟠 Cilindro")
    r = entrada_numero("Raio", chave="cil_r")
    h = entrada_numero("Altura", chave="cil_h")
    if st.button("Calcular Cilindro"):
        resultado, explicacao = cilindro(r, h)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("cilindro", r=r, h=h)

with tab12:
    st.header("🔻 Cone")
    r = entrada_numero("Raio", chave="cone_r")
    h = entrada_numero("Altura", chave="cone_h")
    if st.button("Calcular Cone"):
        resultado, explicacao = cone(r, h)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("cone", r=r, h=h)

with tab13:
    st.header("⚪ Esfera")
    r = entrada_numero("Raio", chave="esf_r")
    h = entrada_numero("Altura da calota (opcional)", chave="esf_h")
    if st.button("Calcular Esfera"):
        resultado, explicacao = esfera(r, h if h else None)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("esfera", r=r)

with tab14:
    st.header("⛏️ Pirâmide Regular")
    n = st.number_input("Número de lados da base (3 a 6)", min_value=3, max_value=6, step=1, key="pir_n")
    lado = entrada_numero("Lado da base", chave="pir_lado")
    h = entrada_numero("Altura", chave="pir_h")
    if st.button("Calcular Pirâmide"):
        resultado, explicacao = piramide(n, lado, h)
        st.write(resultado)
        if explicacao:
            st.code(explicacao, language="")
        if "erro" not in resultado:
            plot_figura_3d("pirâmide", n=n, lado=lado, h=h)
