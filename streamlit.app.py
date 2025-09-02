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

def quadrado(lado):
    if lado <= 0:
        return {"erro": "Forneça lado positivo!"}
    return {"perímetro": 4*lado, "área": lado**2}

def retangulo(base, altura):
    if base <= 0 or altura <= 0:
        return {"erro": "Base e altura devem ser positivos!"}
    return {"perímetro": 2*(base+altura), "área": base*altura}

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

def trapezio(B, b, l1, l2, h=None):
    if B <= 0 or b <= 0 or l1 <= 0 or l2 <= 0:
        return {"erro": "Todos os lados devem ser positivos!"}
    resultado = {"perímetro": round(B+b+l1+l2,4)}
    if h:
        area = ((B+b)*h)/2
        resultado["área"] = round(area,4)
    return resultado

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
# Interface Streamlit – Parte 1 (com plots)
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
        resultado = triangulo_master(a, b, c)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura("triângulo", a=a, b=b, c=c)

with tab2:
    st.header("⚪ Círculo")
    r = entrada_numero("Raio", chave="circ_r")
    theta = entrada_numero("Ângulo θ (graus, opcional)", chave="circ_theta")
    if st.button("Calcular Círculo"):
        resultado = circulo(r, theta if theta else None)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura("círculo", r=r)

with tab3:
    st.header("⬛ Quadrado")
    lado = entrada_numero("Lado", chave="quad_lado")
    if st.button("Calcular Quadrado"):
        resultado = quadrado(lado)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura("quadrado", lado=lado)

with tab4:
    st.header("▭ Retângulo")
    base = entrada_numero("Base", chave="ret_base")
    altura = entrada_numero("Altura", chave="ret_alt")
    if st.button("Calcular Retângulo"):
        resultado = retangulo(base, altura)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura("retângulo", base=base, altura=altura)

with tab5:
    st.header("⬟ Losango")
    lado = entrada_numero("Lado", chave="los_lado")
    D = entrada_numero("Diagonal maior", chave="los_D")
    d = entrada_numero("Diagonal menor", chave="los_d")
    if st.button("Calcular Losango"):
        resultado = losango(lado, D, d)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura("losango", D=D, d=d)

with tab6:
    st.header("▱ Paralelogramo")
    base = entrada_numero("Base", chave="par_base")
    lado = entrada_numero("Lado", chave="par_lado")
    angulo = entrada_numero("Ângulo (graus, opcional)", chave="par_ang")
    if st.button("Calcular Paralelogramo"):
        resultado = paralelogramo(base, lado, angulo=angulo if angulo else 60)
        st.write(resultado)
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
        resultado = trapezio(B, b, l1, l2, h if h else None)
        st.write(resultado)
        if "erro" not in resultado and h:
            plot_figura("trapézio", B=B, b=b, h=h)

with tab8:
    st.header("Polígono Regular")
    n = st.number_input("Número de lados (5 a 10)", min_value=5, max_value=10, step=1)
    lado = entrada_numero("Lado (opcional)", chave="pol_lado")
    R = entrada_numero("Raio circunscrito (opcional)", chave="pol_R")
    if st.button("Calcular Polígono"):
        resultado = poligono(n, lado if lado else None, R if R else None)
        st.write(resultado)
        if "erro" not in resultado:
            R_plot = R if R else lado
            plot_figura("polígono", n=n, R=R_plot)

# =========================================================
# Funções de cálculo – Parte 2 (Tridimensionais)
# =========================================================
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
# Interface Streamlit – Parte 2 (com plots)
# =========================================================
tab8, tab9, tab10, tab11, tab12, tab13, tab14 = st.tabs([
    "Cubo", "Paralelepípedo", "Prisma", "Cilindro", "Cone", "Esfera", "Pirâmide"
])

with tab8:
    st.header("⬛ Cubo")
    lado = entrada_numero("Lado", chave="cubo_lado")
    if st.button("Calcular Cubo"):
        resultado = cubo(lado)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura_3d("cubo", lado=lado)

with tab9:
    st.header("📦 Paralelepípedo")
    c = entrada_numero("Comprimento", chave="par_c")
    l = entrada_numero("Largura", chave="par_l")
    h = entrada_numero("Altura", chave="par_h")
    if st.button("Calcular Paralelepípedo"):
        resultado = paralelepipedo(c, l, h)
        st.write(resultado)
        # (plot básico seria como um cubo esticado, podemos adicionar depois)

with tab10:
    st.header("🔺 Prisma Regular")
    n = st.number_input("Número de lados da base", min_value=3, step=1, key="prisma_n")
    lado = entrada_numero("Lado da base", chave="prisma_lado")
    h = entrada_numero("Altura", chave="prisma_alt")
    if st.button("Calcular Prisma"):
        resultado = prisma(n, lado, h)
        st.write(resultado)
        # (plot pode vir depois)

with tab11:
    st.header("🟠 Cilindro")
    r = entrada_numero("Raio", chave="cil_r")
    h = entrada_numero("Altura", chave="cil_h")
    if st.button("Calcular Cilindro"):
        resultado = cilindro(r, h)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura_3d("cilindro", r=r, h=h)

with tab12:
    st.header("🔻 Cone")
    r = entrada_numero("Raio", chave="cone_r")
    h = entrada_numero("Altura", chave="cone_h")
    if st.button("Calcular Cone"):
        resultado = cone(r, h)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura_3d("cone", r=r, h=h)

with tab13:
    st.header("⚪ Esfera")
    r = entrada_numero("Raio", chave="esf_r")
    h = entrada_numero("Altura da calota (opcional)", chave="esf_h")
    if st.button("Calcular Esfera"):
        resultado = esfera(r, h if h else None)
        st.write(resultado)
        if "erro" not in resultado:
            plot_figura_3d("esfera", r=r)

with tab14:
    st.header("⛏️ Pirâmide Regular")
    n = st.number_input("Número de lados da base (3 a 6)", min_value=3, max_value=6, step=1, key="pir_n")
    lado = entrada_numero("Lado da base", chave="pir_lado")
    h = entrada_numero("Altura", chave="pir_h")
    if st.button("Calcular Pirâmide"):
        resultado = piramide(n, lado, h)
        st.write(resultado)
        # (plot podemos implementar depois)
