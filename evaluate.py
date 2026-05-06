from ultralytics import YOLO
import json

# Cargar modelo
model = YOLO("models/best.pt")

# Evaluar modelo
metrics = model.val(data="tomates_yolo.v5i.yolov8/data.yaml")

# Extraer métricas
resultados = {
    "mAP50": float(metrics.box.map50),
    "mAP50_95": float(metrics.box.map),
    "precision": float(metrics.box.mp),
    "recall": float(metrics.box.mr)
}

# Guardar archivo
with open("metrics.json", "w") as f:
    json.dump(resultados, f, indent=4)

print("✅ MÉTRICAS GUARDADAS:")
print(resultados)