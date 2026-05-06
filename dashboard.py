from flask import Flask, jsonify, render_template
import threading
import json

app = Flask(__name__)

# ===== LOCK PARA SEGURIDAD =====
lock = threading.Lock()

# ===== HISTORIAL DE DETECCIONES (SOLO MONITOREO) =====
historial = {
    "maduro": set(),
    "verde": set(),
    "defectuoso": set()
}

# ===== FUNCIÓN PARA CARGAR MÉTRICAS DEL MODELO =====
def load_metrics():
    try:
        with open("metrics.json") as f:
            return json.load(f)
    except:
        return {
            "mAP50": 0.0,
            "mAP50_95": 0.0,
            "precision": 0.0,
            "recall": 0.0
        }

# ===== RUTA PRINCIPAL =====
@app.route("/")
def index():
    return render_template("index.html")

# ===== API DE DATOS =====
@app.route("/data")
def data():
    with lock:
        total = sum(len(v) for v in historial.values())

        return jsonify({
            "total": total,
            "historial": {
                k: sorted(list(v)) for k, v in historial.items()
            },
            "model_metrics": load_metrics()  # ✅ aquí van las métricas reales
        })

# ===== ACTUALIZAR SOLO HISTORIAL (SIN MÉTRICAS) =====
def update_dashboard(detecciones):
    """
    detecciones = [
        {"id": 3, "estado": "maduro"},
        ...
    ]
    """
    global historial

    if not detecciones:
        return

    with lock:
        for d in detecciones:
            estado = d.get("estado")
            track_id = d.get("id")

            if estado in historial:
                historial[estado].add(track_id)

# ===== EJECUTAR SERVIDOR =====
def run_dashboard():
    print("🌐 Dashboard corriendo en http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )