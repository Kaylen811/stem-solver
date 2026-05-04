from flask import Flask, request, jsonify, render_template_string
from sympy import symbols, diff, integrate, sympify
import numpy as np

app = Flask(__name__)
x = symbols('x')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>STEM Solver</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body style="font-family: Arial; text-align:center;">

<h1>STEM Solver 🚀</h1>

<input id="problem" placeholder="Enter expression like x^2 + 3*x">
<br><br>

<button onclick="solve('derivative')">Derivative</button>
<button onclick="solve('integral')">Integral</button>
<button onclick="graph()">Graph</button>

<h3>Result:</h3>
<div id="result"></div>

<canvas id="chart" width="400" height="200"></canvas>

<script>
async function solve(type){
    let problem = document.getElementById("problem").value;

    let response = await fetch("/solve", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({problem: problem, type: type})
    });

    let data = await response.json();
    document.getElementById("result").innerText = data.result;
}

async function graph(){
    let problem = document.getElementById("problem").value;

    let response = await fetch("/graph", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({problem: problem})
    });

    let data = await response.json();

    new Chart(document.getElementById("chart"), {
        type: 'line',
        data: {
            labels: data.x,
            datasets: [{
                label: "f(x)",
                data: data.y
            }]
        }
    });
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    expr = sympify(data["problem"])
    mode = data["type"]

    if mode == "derivative":
        result = diff(expr, x)
    else:
        result = integrate(expr, x)

    return jsonify({"result": str(result)})

@app.route("/graph", methods=["POST"])
def graph():
    data = request.json
    expr = sympify(data["problem"])

    xs = np.linspace(-10, 10, 50)
    ys = [float(expr.subs(x, val)) for val in xs]

    return jsonify({"x": xs.tolist(), "y": ys})

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)