import cv2
import time

# ===============================
# CONFIGURACIÓN DE CÁMARA
# ===============================

CAMERA_INDEX = 0
FRAME_WIDTH = 1920    # 1080p
FRAME_HEIGHT = 1080
TARGET_FPS = 30

# ===============================
# INICIALIZACIÓN
# ===============================

# En Windows: usar DirectShow mejora mucho el rendimiento
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

if not cap.isOpened():
    raise RuntimeError("❌ No se pudo abrir la cámara")

# Resolución
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# FPS solicitado
cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)

# Evitar acumulación de frames
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# ===============================
# FUNCIÓN PRINCIPAL
# ===============================

def get_frame():
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

# ===============================
# PRUEBA DE FPS REAL
# ===============================

def test_fps(duration=5):
    start = time.time()
    frames = 0

    while time.time() - start < duration:
        frame = get_frame()
        if frame is None:
            break
        frames += 1

    fps = frames / duration
    print(f"FPS reales: {fps:.2f}")

# ===============================
# LIBERAR CÁMARA
# ===============================

def release_camera():
    cap.release()

# ===============================
# EJECUCIÓN DE PRUEBA
# ===============================

if __name__ == "__main__":
    test_fps()
    release_camera()
