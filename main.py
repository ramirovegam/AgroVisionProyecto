import cv2
import time
import threading

from camera import get_frame, release_camera
from detector import detect_tomatoes
from tracker import update_tracker
from dashboard import update_dashboard, run_dashboard

# ===============================
# CONFIGURACIÓN
# ===============================
EXIT_KEY = 27  # ESC
FPS_LIMIT = 30

WINDOW_NAME = "AgroVision - Tomates"

COLORS = {
    "maduro": (0, 0, 255),       # rojo
    "verde": (0, 255, 0),        # verde
    "defectuoso": (0, 165, 255), # naranja
    "desconocido": (200, 200, 200)
}

# ===============================
# MAIN
# ===============================
def main():
    print("✅ Sistema AgroVision iniciado")

    # ===== INICIAR DASHBOARD =====
    dashboard_thread = threading.Thread(
        target=run_dashboard,
        daemon=True
    )
    dashboard_thread.start()

    last_time = time.time()

    # Diccionario para guardar estado por ID
    track_states = {}
    track_conf = {}

    # ===============================
    # LOOP PRINCIPAL
    # ===============================
    while True:
        frame = get_frame()

        if frame is None:
            print("❌ No se pudo obtener frame de la cámara")
            break

        # ===== 1. DETECCIÓN =====
        detections = detect_tomatoes(frame)

        # ===== 2. TRACKING =====
        tracks = update_tracker(detections)

        # ===== 3. ASOCIAR DETECCIONES CON TRACK IDs =====
        for det in detections:
            x1, y1, x2, y2, estado, conf = det

            for trk in tracks:
                tx1, ty1, tx2, ty2, track_id = trk

                # Asociación simple (cercanía)
                if abs(x1 - tx1) < 20 and abs(y1 - ty1) < 20:
                    track_states[track_id] = estado
                    track_conf[track_id] = conf

        # ===== 4. DIBUJAR + PREPARAR DASHBOARD =====
        datos_dashboard = []

        for trk in tracks:
            x1, y1, x2, y2, track_id = trk

            estado = track_states.get(track_id, "desconocido")
            conf = track_conf.get(track_id, 0.0)

            color = COLORS.get(estado, COLORS["desconocido"])

            # Dibujar bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(
                frame,
                f"ID {track_id} - {estado} ({conf:.2f})",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            # Datos para dashboard
            datos_dashboard.append({
                "id": track_id,
                "estado": estado,
                "conf": conf
            })

        # ===== 5. ACTUALIZAR DASHBOARD =====
        update_dashboard(datos_dashboard)

        # ===== 6. FPS =====
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

        # ===== 7. MOSTRAR VENTANA =====
        cv2.imshow(WINDOW_NAME, frame)

        # 🔴 Detectar cierre con la X
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("🛑 Ventana cerrada por el usuario")
            break

        # 🔴 Detectar tecla ESC
        if cv2.waitKey(1) & 0xFF == EXIT_KEY:
            print("🛑 Sistema detenido por ESC")
            break

        # Limitar FPS
        time.sleep(max(0, (1 / FPS_LIMIT) - (time.time() - current_time)))

    # ===============================
    # LIMPIEZA
    # ===============================
    cv2.destroyAllWindows()
    release_camera()
    print("✅ Sistema cerrado correctamente")


# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Programa interrumpido con CTRL+C")
    finally:
        cv2.destroyAllWindows()
        release_camera()