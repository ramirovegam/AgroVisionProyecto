import cv2
import time
import threading

from camera import get_frame
from detector import detect_tomatoes
from tracker import update_tracker
from classifier import classify_tomato

from dashboard import update_dashboard, run_dashboard


# ===============================
# CONFIGURACIÓN
# ===============================

EXIT_KEY = 27  # ESC
FPS_LIMIT = 30

COLORS = {
    "Maduro": (0, 0, 255),
    "No maduro": (0, 255, 0),
    "Desconocido": (200, 200, 200),
}


# ===============================
# MAIN
# ===============================

def main():
    print("✅ Sistema de visión iniciado...")

    # -------------------------------------------------
    # INICIAR DASHBOARD WEB (ANTES DE OPENCV)
    # -------------------------------------------------
    dashboard_thread = threading.Thread(
        target=run_dashboard,
        daemon=True
    )
    dashboard_thread.start()

    last_time = time.time()

    # -------------------------------------------------
    # LOOP PRINCIPAL
    # -------------------------------------------------
    while True:
        frame = get_frame()
        if frame is None:
            print("❌ No se pudo obtener frame de la cámara")
            break

        # 1. Detección
        detections = detect_tomatoes(frame)

        # 2. Seguimiento
        tracks = update_tracker(detections)

        # 3. Clasificación + dibujo
        datos_dashboard = []

        for track in tracks:
            x1, y1, x2, y2, track_id = track

            if x2 <= x1 or y2 <= y1:
                estado = "Desconocido"
            else:
                estado = classify_tomato(frame, track)

            color = COLORS.get(estado, (255, 255, 255))

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                f"ID {track_id} - {estado}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

            datos_dashboard.append({
                "id": track_id,
                "estado": estado
            })

        # 4. Actualizar dashboard
        update_dashboard(datos_dashboard)

        # 5. Mostrar FPS
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
            2,
        )

        # 6. Ventana OpenCV
        cv2.imshow("AgroVision - Tomates", frame)

        if cv2.waitKey(1) & 0xFF == EXIT_KEY:
            print("🛑 Sistema detenido por el usuario")
            break

        time.sleep(max(0, (1 / FPS_LIMIT) - (time.time() - current_time)))

    cv2.destroyAllWindows()
    print("✅ Sistema cerrado correctamente")


# ===============================
# ENTRY POINT
# ===============================

if __name__ == "__main__":
    main()