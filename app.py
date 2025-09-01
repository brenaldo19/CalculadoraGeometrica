from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Rota inicial (teste rápido)
@app.route("/")
def home():
    return {"msg": "Calculadora Geométrica no ar!"}

# -----------------------------
# Funções de cálculo
# -----------------------------
def validar_triangulo(a, b, c):
    return a + b > c and a + c > b and b + c > a

@app.route("/triangulo", methods=["GET"])
def triangulo():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        c = float(request.args.get("c"))
    except:
        return jsonify({"erro": "Forneça os parâmetros a, b, c corretamente!"}), 400

    if not validar_triangulo(a, b, c):
        return jsonify({"erro": "Triângulo inválido!"}), 400

    perimetro = a + b + c
    s = perimetro / 2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))  # Fórmula de Heron

    return jsonify({"perimetro": perimetro, "area": round(area, 2)})

@app.route("/quadrado", methods=["GET"])
def quadrado():
    try:
        lado = float(request.args.get("lado"))
    except:
        return jsonify({"erro": "Forneça o parâmetro lado!"}), 400

    perimetro = 4 * lado
    area = lado**2
    return jsonify({"perimetro": perimetro, "area": round(area, 2)})

@app.route("/retangulo", methods=["GET"])
def retangulo():
    try:
        base = float(request.args.get("base"))
        altura = float(request.args.get("altura"))
    except:
        return jsonify({"erro": "Forneça os parâmetros base e altura!"}), 400

    perimetro = 2 * (base + altura)
    area = base * altura
    return jsonify({"perimetro": perimetro, "area": round(area, 2)})

@app.route("/poligono", methods=["GET"])
def poligono():
    try:
        n = int(request.args.get("n"))
        lado = float(request.args.get("lado"))
    except:
        return jsonify({"erro": "Forneça os parâmetros n (lados) e lado!"}), 400

    if n < 5 or n > 10:
        return jsonify({"erro": "Só aceitamos polígonos regulares de 5 a 10 lados!"}), 400

    perimetro = n * lado
    apotema = lado / (2 * math.tan(math.pi/n))
    area = (perimetro * apotema) / 2

    return jsonify({"perimetro": perimetro, "area": round(area, 2)})

# -----------------------------
# Main (para rodar localmente)
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
