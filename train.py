from ultralytics import YOLO

# Ruta correcta
data = "tomates_yolo.v5i.yolov8/data.yaml"

# Cargar modelo
model = YOLO("yolov8n.pt")

# Entrenar
model.train(
    data=data,   # ✅ aquí corregido
    epochs=50,
    imgsz=640,
    batch=8,
    name="tomates_modelo_v5",
    device="cpu"
)

print("✅ Entrenamiento terminado")