from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route("/")
def home():
    return {"msg": "Calculadora Geométrica no ar!"}

# -----------------------------
# Triângulo
# -----------------------------
def validar_triangulo(a, b, c):
    return a + b > c and a + c > b and b + c > a

@app.route("/triangulo_master")
def triangulo_master():
    # -----------------------
    # Entrada de dados
    # -----------------------
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    c = request.args.get("c", type=float)
    A = request.args.get("A", type=float)  # ângulo em graus
    B = request.args.get("B", type=float)
    C = request.args.get("C", type=float)
    h = request.args.get("h", type=float)  # altura opcional

    # -----------------------
    # Reconstrução de lados
    # -----------------------
    # Caso 1: Dois catetos → calcula hipotenusa
    if a and b and not c and not (A or B or C):
        c = math.sqrt(a**2 + b**2)

    # Caso 2: Cateto + hipotenusa → calcula outro cateto
    if a and c and not b:
        if c > a:
            b = math.sqrt(c**2 - a**2)
    if b and c and not a:
        if c > b:
            a = math.sqrt(c**2 - b**2)

    # Caso 3: Dois lados + ângulo entre eles → Lei dos Cossenos
    if a and b and C and not c:
        C_rad = math.radians(C)
        c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(C_rad))
    if a and c and B and not b:
        B_rad = math.radians(B)
        b = math.sqrt(a**2 + c**2 - 2*a*c*math.cos(B_rad))
    if b and c and A and not a:
        A_rad = math.radians(A)
        a = math.sqrt(b**2 + c**2 - 2*b*c*math.cos(A_rad))

    # Caso 4: Um lado + ângulos → Lei dos Senos
    if a and A and B and not b:
        A_rad = math.radians(A)
        B_rad = math.radians(B)
        b = a * math.sin(B_rad)/math.sin(A_rad)
    if a and A and C and not c:
        A_rad = math.radians(A)
        C_rad = math.radians(C)
        c = a * math.sin(C_rad)/math.sin(A_rad)

    # -----------------------
    # Checagem se temos 3 lados
    # -----------------------
    if not (a and b and c):
        return jsonify({"erro": "Não foi possível determinar os 3 lados com as informações fornecidas."}), 400

    # -----------------------
    # Validação existência
    # -----------------------
    if not (a+b>c and a+c>b and b+c>a):
        return jsonify({"erro": "Triângulo inválido (desigualdade triangular não satisfeita)."}), 400

    resultado = {}

    # -----------------------
    # Perímetro e área (Heron)
    # -----------------------
    perimetro = a+b+c
    s = perimetro/2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    resultado["perimetro"] = round(perimetro,4)
    resultado["area"] = round(area,4)

    # -----------------------
    # Alturas
    # -----------------------
    h_a = (2*area)/a
    h_b = (2*area)/b
    h_c = (2*area)/c
    resultado["alturas"] = {"h_a": round(h_a,4), "h_b": round(h_b,4), "h_c": round(h_c,4)}

    # -----------------------
    # Ângulos (Lei dos Cossenos)
    # -----------------------
    A = math.degrees(math.acos((b**2 + c**2 - a**2)/(2*b*c)))
    B = math.degrees(math.acos((a**2 + c**2 - b**2)/(2*a*c)))
    C = 180 - (A+B)
    resultado["angulos"] = {"A": round(A,2), "B": round(B,2), "C": round(C,2)}

    # -----------------------
    # Classificação por lados
    # -----------------------
    if abs(a-b)<1e-6 and abs(b-c)<1e-6:
        tipo_lado = "equilátero"
    elif abs(a-b)<1e-6 or abs(b-c)<1e-6 or abs(a-c)<1e-6:
        tipo_lado = "isósceles"
    else:
        tipo_lado = "escaleno"
    resultado["classificacao_lados"] = tipo_lado

    # -----------------------
    # Classificação por ângulos
    # -----------------------
    if any(abs(x-90) < 1e-3 for x in [A,B,C]):
        tipo_angulo = "retângulo"
    elif all(x < 90 for x in [A,B,C]):
        tipo_angulo = "acutângulo"
    else:
        tipo_angulo = "obtusângulo"
    resultado["classificacao_angulos"] = tipo_angulo

    # -----------------------
    # Ângulos formados pelas alturas
    # -----------------------
    # Exemplo: altura relativa ao lado a divide o ângulo A em dois.
    # Podemos calcular ângulo entre altura h_a e lado b usando trigonometria.
    # tg(theta) = cateto_oposto / cateto_adjacente
    try:
        theta_A = math.degrees(math.atan(h_a / (b - (h_a/math.tan(math.radians(B))))))
    except:
        theta_A = None

    resultado["angulo_altura"] = {
        "altura_relativa_a": round(theta_A,2) if theta_A else "indeterminado"
    }

    return jsonify(resultado)


@app.route("/circulo")
def circulo():
    try:
        r = float(request.args.get("r"))
    except:
        return jsonify({"erro": "Forneça o raio r!"}), 400
    if r <= 0:
        return jsonify({"erro": "Raio deve ser positivo!"}), 400

    resultado = {}
    resultado["area"] = round(math.pi * r**2, 4)
    resultado["circunferencia"] = round(2*math.pi*r, 4)

    # arco e setor (se informado ângulo θ em graus)
    theta = request.args.get("theta", type=float)
    if theta:
        arco = 2*math.pi*r*(theta/360)
        setor = math.pi*r**2*(theta/360)
        resultado["arco"] = round(arco, 4)
        resultado["setor"] = round(setor, 4)

    # segmento (se informado corda + ângulo central)
    corda = request.args.get("corda", type=float)
    if corda and theta:
        h = r - math.sqrt(r**2 - (corda/2)**2)  # altura do segmento
        segmento = (math.pi*r**2*(theta/360)) - (corda*(r-h)/2)
        resultado["segmento"] = round(segmento, 4)

    resultado["equacao_cartesiana"] = f"(x - 0)² + (y - 0)² = {r}²"
    return jsonify(resultado)

# -----------------------------
# Quadrado
# -----------------------------
@app.route("/quadrado")
def quadrado():
    try:
        lado = float(request.args.get("lado"))
    except:
        return jsonify({"erro": "Forneça o parâmetro lado!"}), 400

    return jsonify({"perimetro": 4*lado, "area": lado**2})

# -----------------------------
# Retângulo
# -----------------------------
@app.route("/retangulo")
def retangulo():
    try:
        base = float(request.args.get("base"))
        altura = float(request.args.get("altura"))
    except:
        return jsonify({"erro": "Forneça base e altura!"}), 400

    return jsonify({"perimetro": 2*(base+altura), "area": base*altura})

# -----------------------------
# Losango
# -----------------------------
@app.route("/losango_avancado")
def losango_avancado():
    try:
        lado = float(request.args.get("lado"))
        D = float(request.args.get("D"))  # diagonal maior
        d = float(request.args.get("d"))  # diagonal menor
    except:
        return jsonify({"erro": "Forneça lado, D e d!"}), 400

    if lado <= 0 or D <= 0 or d <= 0:
        return jsonify({"erro": "Valores devem ser positivos!"}), 400

    resultado = {}

    # Área e perímetro
    area = (D*d)/2
    perimetro = 4*lado
    resultado["area"] = round(area,4)
    resultado["perimetro"] = round(perimetro,4)

    # Consistência dos lados
    if abs(lado**2 - ((D/2)**2 + (d/2)**2)) > 1e-3:
        resultado["aviso"] = "Lado não é compatível com diagonais!"

    # Altura relativa
    h = area / D
    resultado["altura"] = round(h,4)

    # Ângulos internos
    ang_agudo = math.degrees(2*math.atan(d/D))
    resultado["angulos"] = {
        "agudo": round(ang_agudo,2),
        "obtuso": round(180-ang_agudo,2)
    }

    return jsonify(resultado)

# -----------------------------
# Paralelogramo
# -----------------------------
@app.route("/paralelogramo_avancado")
def paralelogramo_avancado():
    try:
        base = float(request.args.get("base"))
        lado = float(request.args.get("lado"))
        altura = request.args.get("altura", type=float)  # opcional
        angulo = request.args.get("angulo", type=float)  # em graus, opcional
    except:
        return jsonify({"erro": "Forneça base, lado e opcionalmente altura ou ângulo!"}), 400

    if base <= 0 or lado <= 0:
        return jsonify({"erro": "Base e lado devem ser positivos!"}), 400

    resultado = {}
    perimetro = 2*(base+lado)
    resultado["perimetro"] = round(perimetro,4)

    # Área pelo que tiver disponível
    if altura:
        area = base*altura
        resultado["area"] = round(area,4)
    elif angulo:
        ang_rad = math.radians(angulo)
        area = base*lado*math.sin(ang_rad)
        resultado["area"] = round(area,4)

        # diagonais
        d1 = math.sqrt(base**2 + lado**2 + 2*base*lado*math.cos(ang_rad))
        d2 = math.sqrt(base**2 + lado**2 - 2*base*lado*math.cos(ang_rad))
        resultado["diagonais"] = {"maior": round(d1,4), "menor": round(d2,4)}

    # classificação
    if abs(base-lado)<1e-6 and angulo==90:
        tipo = "quadrado"
    elif angulo==90:
        tipo = "retângulo"
    elif abs(base-lado)<1e-6:
        tipo = "losango"
    else:
        tipo = "paralelogramo"
    resultado["classificacao"] = tipo

    return jsonify(resultado)

# -----------------------------
# Trapézio
# -----------------------------
@app.route("/trapezio_avancado")
def trapezio_avancado():
    try:
        B = float(request.args.get("B"))  # base maior
        b = float(request.args.get("b"))  # base menor
        l1 = float(request.args.get("l1"))
        l2 = float(request.args.get("l2"))
        h = request.args.get("h", type=float)  # altura opcional
    except:
        return jsonify({"erro": "Forneça B, b, l1, l2 e opcionalmente h!"}), 400

    if B <= 0 or b <= 0 or l1 <= 0 or l2 <= 0:
        return jsonify({"erro": "Todos os lados devem ser positivos!"}), 400

    resultado = {}

    # altura (se não foi passada)
    if not h:
        # só funciona se trapézio isósceles (l1 = l2)
        if abs(l1 - l2) < 1e-6:
            h = math.sqrt(l1**2 - ((B - b)/2)**2)
            resultado["altura_calc"] = round(h,4)

    if h:
        area = ((B+b)*h)/2
        resultado["area"] = round(area,4)

    perimetro = B+b+l1+l2
    resultado["perimetro"] = round(perimetro,4)

    # classificação
    if abs(l1-l2)<1e-6:
        tipo = "isósceles"
    elif l1 == h or l2 == h:
        tipo = "retângulo"
    else:
        tipo = "escaleno"
    resultado["classificacao"] = tipo

    return jsonify(resultado)

# -----------------------------
# Polígonos Regulares
# -----------------------------
@app.route("/poligono_detalhado")
def poligono_detalhado():
    try:
        n = int(request.args.get("n"))
    except:
        return jsonify({"erro": "Forneça n (5 a 10)!"}), 400

    lado = request.args.get("lado", type=float)
    R = request.args.get("R", type=float)   # raio circunscrito opcional

    if n < 5 or n > 10:
        return jsonify({"erro": "Número de lados deve estar entre 5 e 10!"}), 400

    resultado = {"n_lados": n}
    perimetro = None
    area = None
    apotema = None

    # -------------------
    # Pentágono
    # -------------------
    if n == 5:
        resultado["nome"] = "pentágono"
        if lado:
            perimetro = 5*lado
            area = (5/4)*lado**2*(1/math.tan(math.pi/5))
            apotema = lado/(2*math.tan(math.pi/5))
        elif R:
            perimetro = 10*R*math.sin(math.pi/5)
            area = (5/2)*R**2*math.sin(math.radians(72))
            apotema = R*math.cos(math.pi/5)
        else:
            return jsonify({"erro": "Pentágono precisa de lado ou raio circunscrito (R)."}), 400

    # -------------------
    # Hexágono
    # -------------------
    elif n == 6:
        resultado["nome"] = "hexágono"
        if lado:
            perimetro = 6*lado
            area = (3*math.sqrt(3)/2)*lado**2
            apotema = (math.sqrt(3)/2)*lado
        elif R:
            perimetro = 6*R
            area = (3*math.sqrt(3)/2)*R**2
            apotema = (math.sqrt(3)/2)*R
        else:
            return jsonify({"erro": "Hexágono precisa de lado ou raio circunscrito (R)."}), 400

    # -------------------
    # Heptágono
    # -------------------
    elif n == 7:
        resultado["nome"] = "heptágono"
        if not lado:
            return jsonify({"erro": "Heptágono precisa do lado."}), 400
        perimetro = 7*lado
        apotema = lado/(2*math.tan(math.pi/7))
        area = (perimetro*apotema)/2

    # -------------------
    # Octógono
    # -------------------
    elif n == 8:
        resultado["nome"] = "octógono"
        if lado:
            perimetro = 8*lado
            area = 2*(1+math.sqrt(2))*lado**2
            apotema = lado/(2*math.tan(math.pi/8))
        elif R:
            lado = R*math.sqrt(2-2*math.cos(2*math.pi/8)) # lado a partir de R
            perimetro = 8*lado
            apotema = R*math.cos(math.pi/8)
            area = (perimetro*apotema)/2
        else:
            return jsonify({"erro": "Octógono precisa de lado ou raio circunscrito (R)."}), 400

    # -------------------
    # Eneágono
    # -------------------
    elif n == 9:
        resultado["nome"] = "eneágono"
        if not lado:
            return jsonify({"erro": "Eneágono precisa do lado."}), 400
        perimetro = 9*lado
        apotema = lado/(2*math.tan(math.pi/9))
        area = (perimetro*apotema)/2

    # -------------------
    # Decágono
    # -------------------
    elif n == 10:
        resultado["nome"] = "decágono"
        if lado:
            perimetro = 10*lado
            apotema = lado/(2*math.tan(math.pi/10))
            area = (perimetro*apotema)/2
        elif R:
            perimetro = 20*R*math.sin(math.pi/10)
            area = (5/2)*R**2*math.sin(math.radians(72))
            apotema = R*math.cos(math.pi/10)
        else:
            return jsonify({"erro": "Decágono precisa de lado ou raio circunscrito (R)."}), 400

    resultado["perimetro"] = round(perimetro,4)
    resultado["area"] = round(area,4)
    if apotema:
        resultado["apotema"] = round(apotema,4)

    return jsonify(resultado)

# -----------------------------
# Cubo
# -----------------------------
@app.route("/cubo_detalhado")
def cubo_detalhado():
    lado = request.args.get("lado", type=float)
    if not lado or lado <= 0:
        return jsonify({"erro": "Forneça o lado > 0"}), 400

    resultado = {"figura": "cubo"}
    resultado["volume"] = round(lado**3,4)
    resultado["area_superficie"] = round(6*lado**2,4)
    resultado["diagonal_face"] = round(lado*math.sqrt(2),4)
    resultado["diagonal_cubo"] = round(lado*math.sqrt(3),4)
    resultado["raio_inscrito"] = round(lado/2,4)
    resultado["raio_circunscrito"] = round((lado*math.sqrt(3))/2,4)

    return jsonify(resultado)

# -----------------------------
# Paralelepípedo
# -----------------------------
@app.route("/paralelepipedo_detalhado")
def paralelepipedo_detalhado():
    try:
        c = float(request.args.get("c"))
        l = float(request.args.get("l"))
        h = float(request.args.get("h"))
    except:
        return jsonify({"erro": "Forneça c, l e h"}), 400

    if c <= 0 or l <= 0 or h <= 0:
        return jsonify({"erro": "Todos os lados devem ser positivos"}), 400

    resultado = {"figura": "paralelepípedo"}
    resultado["volume"] = round(c*l*h,4)
    resultado["area_superficie"] = round(2*(c*l + c*h + l*h),4)
    resultado["diagonal_espacial"] = round(math.sqrt(c**2 + l**2 + h**2),4)
    resultado["diagonais_faces"] = {
        "cl": round(math.sqrt(c**2 + l**2),4),
        "ch": round(math.sqrt(c**2 + h**2),4),
        "lh": round(math.sqrt(l**2 + h**2),4),
    }

    if abs(c-l)<1e-6 and abs(l-h)<1e-6:
        resultado["classificacao"] = "cubo (caso especial)"

    return jsonify(resultado)

# -----------------------------
# Prisma regular
# -----------------------------
@app.route("/prisma_detalhado")
def prisma_detalhado():
    try:
        n = int(request.args.get("n"))
        lado = float(request.args.get("lado"))
        h = float(request.args.get("h"))
    except:
        return jsonify({"erro": "Forneça n, lado e h"}), 400

    if n < 3:
        return jsonify({"erro": "Prisma precisa de base com pelo menos 3 lados"}), 400
    if lado <= 0 or h <= 0:
        return jsonify({"erro": "Lado e altura devem ser positivos"}), 400

    resultado = {"figura": f"prisma regular de base {n}-gonal"}
    perimetro = n*lado
    apotema = lado/(2*math.tan(math.pi/n))
    area_base = (perimetro*apotema)/2
    area_lateral = perimetro*h
    area_total = 2*area_base + area_lateral
    volume = area_base*h

    resultado["perimetro_base"] = round(perimetro,4)
    resultado["area_base"] = round(area_base,4)
    resultado["apotema_base"] = round(apotema,4)
    resultado["area_lateral"] = round(area_lateral,4)
    resultado["area_total"] = round(area_total,4)
    resultado["volume"] = round(volume,4)

    return jsonify(resultado)

# -----------------------------
# Cilindro
# -----------------------------
@app.route("/cilindro_detalhado")
def cilindro_detalhado():
    try:
        r = float(request.args.get("r"))
        h = float(request.args.get("h"))
    except:
        return jsonify({"erro": "Forneça r e h"}), 400

    if r <= 0 or h <= 0:
        return jsonify({"erro": "Raio e altura devem ser positivos"}), 400

    resultado = {"figura": "cilindro"}
    area_base = math.pi*r**2
    area_lateral = 2*math.pi*r*h
    area_total = 2*area_base + area_lateral
    volume = area_base*h

    resultado["area_base"] = round(area_base,4)
    resultado["area_lateral"] = round(area_lateral,4)
    resultado["area_total"] = round(area_total,4)
    resultado["volume"] = round(volume,4)

    if abs(r-h)<1e-6:
        resultado["classificacao"] = "cilindro equilátero (raio = altura)"

    return jsonify(resultado)
# -----------------------------
# Cone
# -----------------------------
@app.route("/cone_detalhado")
def cone_detalhado():
    try:
        r = float(request.args.get("r"))
        h = float(request.args.get("h"))
    except:
        return jsonify({"erro": "Forneça r e h"}), 400

    if r <= 0 or h <= 0:
        return jsonify({"erro": "Raio e altura devem ser positivos"}), 400

    resultado = {"figura": "cone"}
    g = math.sqrt(r**2 + h**2)
    area_base = math.pi*r**2
    area_lateral = math.pi*r*g
    area_total = area_base + area_lateral
    volume = (math.pi*r**2*h)/3

    resultado["geratriz"] = round(g,4)
    resultado["area_base"] = round(area_base,4)
    resultado["area_lateral"] = round(area_lateral,4)
    resultado["area_total"] = round(area_total,4)
    resultado["volume"] = round(volume,4)

    if abs(r-h)<1e-6:
        resultado["classificacao"] = "cone equilátero (raio = altura)"

    return jsonify(resultado)

# -----------------------------
# Esfera
# -----------------------------
@app.route("/esfera_detalhada")
def esfera_detalhada():
    try:
        r = float(request.args.get("r"))
    except:
        return jsonify({"erro": "Forneça o raio r"}), 400

    if r <= 0:
        return jsonify({"erro": "Raio deve ser positivo"}), 400

    resultado = {"figura": "esfera"}
    area = 4*math.pi*r**2
    volume = (4/3)*math.pi*r**3
    circ_max = 2*math.pi*r

    resultado["diametro"] = round(2*r,4)
    resultado["area_superficie"] = round(area,4)
    resultado["volume"] = round(volume,4)
    resultado["circunferencia_maxima"] = round(circ_max,4)

    # Calota esférica (opcional, se altura fornecida)
    h = request.args.get("h", type=float)
    if h and 0 < h < 2*r:
        area_calota = 2*math.pi*r*h
        volume_calota = (math.pi*h**2*(3*r-h))/3
        resultado["calota"] = {
            "altura": h,
            "area": round(area_calota,4),
            "volume": round(volume_calota,4)
        }

    return jsonify(resultado)

# -----------------------------
# Pirâmide
# -----------------------------
@app.route("/piramide_detalhada")
def piramide_detalhada():
    try:
        n = int(request.args.get("n"))       # lados da base
        lado = float(request.args.get("lado"))
        h = float(request.args.get("h"))
    except:
        return jsonify({"erro": "Forneça n (3 a 6), lado e h"}), 400

    if n < 3 or n > 6:
        return jsonify({"erro": "Pirâmide só aceita base de 3 a 6 lados"}), 400
    if lado <= 0 or h <= 0:
        return jsonify({"erro": "Lado e altura devem ser positivos"}), 400

    # Perímetro e apótema da base
    perimetro_base = n*lado
    apotema_base = lado/(2*math.tan(math.pi/n))
    area_base = (perimetro_base*apotema_base)/2

    # Apótema lateral
    apotema_lateral = math.sqrt(h**2 + apotema_base**2)

    # Áreas e volume
    area_lateral = (perimetro_base*apotema_lateral)/2
    area_total = area_base + area_lateral
    volume = (area_base*h)/3

    nomes = {3:"triangular",4:"quadrada",5:"pentagonal",6:"hexagonal"}

    resultado = {"figura": f"pirâmide regular {nomes[n]}"}
    resultado["perimetro_base"] = round(perimetro_base,4)
    resultado["apotema_base"] = round(apotema_base,4)
    resultado["area_base"] = round(area_base,4)
    resultado["apotema_lateral"] = round(apotema_lateral,4)
    resultado["area_lateral"] = round(area_lateral,4)
    resultado["area_total"] = round(area_total,4)
    resultado["volume"] = round(volume,4)

    return jsonify(resultado)

# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
