import cv2

# ===============================
# CONFIGURACIÓN DE CÁMARA
# ===============================

CAMERA_INDEX = 0        # 0 = webcam por defecto
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# ===============================
# INICIALIZACIÓN
# ===============================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError("❌ No se pudo abrir la cámara")

# Configurar resolución
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)


# ===============================
# FUNCIÓN PRINCIPAL
# ===============================

def get_frame():
    """
    Captura un frame de la cámara.

    Returns:
        frame (numpy array) o None si falla
    """
    ret, frame = cap.read()

    if not ret:
        return None

    return frame


# ===============================
# LIBERAR CÁMARA (opcional)
# ===============================

def release_camera():
    cap.release()
