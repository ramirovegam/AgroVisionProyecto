import cv2
import time

from camera import get_frame, release_camera
from detector import detect_tomatoes
from tracker import update_tracker

# ===============================
# CONFIGURACIÓN
# ===============================
EXIT_KEY = 27  # ESC
FPS_LIMIT = 30

WINDOW_NAME = "AgroVision - Tomates"

COLORS = {
    "maduro": (0, 0, 255),
    "verde": (0, 255, 0),
    "defectuoso": (0, 165, 255),
    "desconocido": (200, 200, 200)
}

# ===============================
# MAIN
# ===============================
def main():
    print("✅ Sistema AgroVision iniciado (sin dashboard)")

    last_time = time.time()

    track_states = {}
    track_conf = {}

    frame_count = 0
    last_detections = []

    # ===============================
    # LOOP PRINCIPAL
    # ===============================
    while True:
        frame = get_frame()

        if frame is None:
            print("❌ No se pudo obtener frame")
            break

        frame_count += 1

        # ===============================
        # DETECCIÓN OPTIMIZADA
        # ===============================
        if frame_count % 2 == 0:
            detections = detect_tomatoes(frame)
            last_detections = detections
        else:
            detections = last_detections

        # ===============================
        # TRACKING
        # ===============================
        tracks = update_tracker(detections)

        # ===============================
        # ASOCIACIÓN
        # ===============================
        for det in detections:
            x1, y1, x2, y2, estado, conf = det

            for trk in tracks:
                tx1, ty1, tx2, ty2, track_id = trk

                if abs(x1 - tx1) < 20 and abs(y1 - ty1) < 20:
                    track_states[track_id] = estado
                    track_conf[track_id] = conf

        # ===============================
        # DIBUJADO
        # ===============================
        for trk in tracks:
            x1, y1, x2, y2, track_id = trk

            estado = track_states.get(track_id, "desconocido")
            conf = track_conf.get(track_id, 0.0)

            color = COLORS.get(estado, COLORS["desconocido"])

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(
                frame,
                f"{estado} ({conf:.2f})",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        # ===============================
        # FPS
        # ===============================
        current_time = time.time()
        fps = 1 / max(current_time - last_time, 1e-6)
        last_time = current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

        # ===============================
        # MOSTRAR
        # ===============================
        cv2.imshow(WINDOW_NAME, frame)

        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("🛑 Ventana cerrada")
            break

        if cv2.waitKey(1) & 0xFF == EXIT_KEY:
            print("🛑 Detenido por ESC")
            break

        time.sleep(max(0, (1 / FPS_LIMIT) - (time.time() - current_time)))

    # ===============================
    # LIMPIEZA
    # ===============================
    cv2.destroyAllWindows()
    release_camera()
    print("✅ Sistema cerrado")

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 CTRL+C")
    finally:
        cv2.destroyAllWindows()
        release_camera()