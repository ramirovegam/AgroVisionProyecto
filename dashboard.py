from flask import Flask, jsonify, render_template
import threading

app = Flask(__name__)

tomates = []
lock = threading.Lock()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    with lock:
        return jsonify({
            "total": len(tomates),
            "tomates": tomates
        })


def update_dashboard(tracks_estado):
    global tomates
    with lock:
        tomates = tracks_estado.copy()


def run_dashboard():
    print("🌐 Dashboard Flask iniciado en http://127.0.0.1:5000")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
