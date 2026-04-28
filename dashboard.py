from flask import Flask, jsonify, render_template
import threading

app = Flask(__name__)

lock = threading.Lock()

# HISTORIAL GLOBAL POR CLASE
historial = {
    "maduro": set(),
    "verde": set(),
    "defectuoso": set()
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    with lock:
        return jsonify({
            "total": sum(len(v) for v in historial.values()),
            "historial": {
                k: sorted(list(v)) for k, v in historial.items()
            }
        })

def update_dashboard(detecciones):
    """
    detecciones = [
        {"id": 3, "estado": "maduro"},
        ...
    ]
    """
    global historial
    with lock:
        for d in detecciones:
            estado = d["estado"]
            track_id = d["id"]
            if estado in historial:
                historial[estado].add(track_id)

def run_dashboard():
    print("🌐 Dashboard en http://127.0.0.1:5000")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )