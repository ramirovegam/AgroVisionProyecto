import cv2
import numpy as np


# ===============================
# CONFIGURACIÓN
# ===============================

# Umbrales HSV aproximados (ajustables)
RED_LOWER_1 = np.array([0, 80, 60])
RED_UPPER_1 = np.array([10, 255, 255])

RED_LOWER_2 = np.array([170, 80, 60])
RED_UPPER_2 = np.array([180, 255, 255])

GREEN_LOWER = np.array([25, 50, 50])
GREEN_UPPER = np.array([75, 255, 255])

# Porcentaje mínimo de color para decidir estado
RED_THRESHOLD = 0.35
GREEN_THRESHOLD = 0.35

# Tamaño mínimo de ROI (evita errores)
MIN_ROI_SIZE = 20


# ===============================
# FUNCIÓN PRINCIPAL
# ===============================

def classify_tomato(frame, track):
    """
    Clasifica el estado del tomate usando color (HSV).

    Args:
        frame (numpy array): frame original
        track (list): [x1, y1, x2, y2, id]

    Returns:
        estado (str): "Maduro", "No maduro" o "Desconocido"
    """

    x1, y1, x2, y2, _ = map(int, track)

    # -------------------------------
    # 1. Validar ROI
    # -------------------------------
    if x2 - x1 < MIN_ROI_SIZE or y2 - y1 < MIN_ROI_SIZE:
        return "Desconocido"

    roi = frame[y1:y2, x1:x2]

    if roi is None or roi.size == 0:
        return "Desconocido"

    # -------------------------------
    # 2. Convertir a HSV
    # -------------------------------
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # -------------------------------
    # 3. Detectar color rojo (maduro)
    # -------------------------------
    mask_red1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
    mask_red2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    red_ratio = cv2.countNonZero(mask_red) / (roi.shape[0] * roi.shape[1])

    # -------------------------------
    # 4. Detectar color verde
    # -------------------------------
    mask_green = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    green_ratio = cv2.countNonZero(mask_green) / (roi.shape[0] * roi.shape[1])

    # -------------------------------
    # 5. Decisión final
    # -------------------------------
    if red_ratio > RED_THRESHOLD:
        return "Maduro"

    if green_ratio > GREEN_THRESHOLD:
        return "No maduro"

    return "Desconocido"