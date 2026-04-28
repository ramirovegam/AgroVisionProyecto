import cv2
from ultralytics import YOLO

# ===============================
# CONFIGURACIÓN
# ===============================

# Ruta a tu modelo entrenado en Roboflow
MODEL_PATH = "models/tomate_yolov8.pt"  

# Confianza mínima para aceptar detecciones
CONF_THRESHOLD = 0.4

# Tamaño de inferencia YOLO
YOLO_IMG_SIZE = 640

# ===============================
# CARGAR MODELO
# ===============================

print("📦 Cargando modelo YOLO...")
model = YOLO(MODEL_PATH)
print("✅ Modelo YOLO cargado correctamente")

# ===============================
# FUNCIÓN PRINCIPAL
# ===============================

def detect_tomatoes(frame):
    """
    Detecta y clasifica tomates usando YOLOv8 entrenado.
    
    Args:
        frame (numpy array): Frame original de la cámara (BGR)

    Returns:
        detections (list):
        [
            [x1, y1, x2, y2, estado, confidence],

        ]
        donde estado ∈ {"maduro", "verde", "defectuoso"}
    """

    detections = []

    # Inferencia YOLO (YOLO hace resize y letterbox internamente)
    results = model(
        frame,
        imgsz=YOLO_IMG_SIZE,
        conf=CONF_THRESHOLD,
        verbose=False
    )

    # Procesar resultados
    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            # Confianza
            conf = float(box.conf[0])
            if conf < CONF_THRESHOLD:
                continue

            # Coordenadas (ya están en tamaño original)
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Clase detectada
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            detections.append([
                x1,
                y1,
                x2,
                y2,
                class_name,  # ← ESTADO DIRECTO DE YOLO
                conf
            ])

    return detections