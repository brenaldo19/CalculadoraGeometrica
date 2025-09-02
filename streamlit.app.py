from utils import entrada_numero
import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora Geométrica", layout="wide")

st.title("📐 Calculadora Geométrica")
st.write("Escolha a figura geométrica e insira os parâmetros para calcular.")

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
        # coloca lado a na base
        xA, yA = 0, 0
        xB, yB = a, 0
        cos_gamma = (a**2 + b**2 - c**2)/(2*a*b)
        cos_gamma = max(min(cos_gamma,1),-1)  # evitar erro numérico
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
            R_plot = R if R else lado  # fallback simples
            plot_figura("polígono", n=n, R=R_plot)

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
    lado = entrada_numero("Lado", chave="cubo_lado")
    if st.button("Calcular Cubo"):
        st.write(cubo(lado))

with tab9:
    st.header("📦 Paralelepípedo")
    c = entrada_numero("Comprimento", chave="par_c")
    l = entrada_numero("Largura", chave="par_l")
    h = entrada_numero("Altura", chave="par_h")
    if st.button("Calcular Paralelepípedo"):
        st.write(paralelepipedo(c, l, h))

with tab10:
    st.header("🔺 Prisma Regular")
    n = st.number_input("Número de lados da base", min_value=3, step=1, key="prisma_n")
    lado = entrada_numero("Lado da base", chave="prisma_lado")
    h = entrada_numero("Altura", chave="prisma_alt")
    if st.button("Calcular Prisma"):
        st.write(prisma(n, lado, h))

with tab11:
    st.header("🟠 Cilindro")
    r = entrada_numero("Raio", chave="cil_r")
    h = entrada_numero("Altura", chave="cil_h")
    if st.button("Calcular Cilindro"):
        st.write(cilindro(r, h))

with tab12:
    st.header("🔻 Cone")
    r = entrada_numero("Raio", chave="cone_r")
    h = entrada_numero("Altura", chave="cone_h")
    if st.button("Calcular Cone"):
        st.write(cone(r, h))

with tab13:
    st.header("⚪ Esfera")
    r = entrada_numero("Raio", chave="esf_r")
    h = entrada_numero("Altura da calota (opcional)", chave="esf_h")
    if st.button("Calcular Esfera"):
        st.write(esfera(r, h if h else None))

with tab14:
    st.header("⛏️ Pirâmide Regular")
    n = st.number_input("Número de lados da base (3 a 6)", min_value=3, max_value=6, step=1, key="pir_n")
    lado = entrada_numero("Lado da base", chave="pir_lado")
    h = entrada_numero("Altura", chave="pir_h")
    if st.button("Calcular Pirâmide"):
        st.write(piramide(n, lado, h))
