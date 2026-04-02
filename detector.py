import cv2
from ultralytics import YOLO

# ===============================
# CONFIGURACIÓN
# ===============================

# MODEL_PATH = "models/yolov8_tomates.pt"  # o yolov8n.pt si estás probando
MODEL_PATH = "yolov8n.pt"
YOLO_IMG_SIZE = 640                      # tamaño de entrada YOLO
CONF_THRESHOLD = 0.4                    # confianza mínima


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
    Detecta tomates en un frame usando YOLOv8.

    Args:
        frame (numpy array): Frame original de la cámara

    Returns:
        detections (list): [[x1, y1, x2, y2, confidence], ...]
    """

    original_h, original_w = frame.shape[:2]

    # -------------------------------
    # 1. Redimensionar para YOLO
    # -------------------------------
    resized_frame = cv2.resize(frame, (YOLO_IMG_SIZE, YOLO_IMG_SIZE))

    # -------------------------------
    # 2. Inferencia YOLO
    # -------------------------------
    results = model(resized_frame, verbose=False)

    detections = []

    # -------------------------------
    # 3. Procesar resultados
    # -------------------------------
    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            conf = float(box.conf[0])
            if conf < CONF_THRESHOLD:
                continue

            # Coordenadas en imagen 640x640
            x1, y1, x2, y2 = box.xyxy[0]

            # -------------------------------
            # 4. Escalar a tamaño original
            # -------------------------------
            x1 = int(x1 * original_w / YOLO_IMG_SIZE)
            x2 = int(x2 * original_w / YOLO_IMG_SIZE)
            y1 = int(y1 * original_h / YOLO_IMG_SIZE)
            y2 = int(y2 * original_h / YOLO_IMG_SIZE)

            detections.append([x1, y1, x2, y2, conf])

    return detections