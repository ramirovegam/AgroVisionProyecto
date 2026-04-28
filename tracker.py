import numpy as np
from sort import Sort

# ===============================
# CONFIGURACIÓN DEL TRACKER
# ===============================

tracker = Sort(
    max_age=15,
    min_hits=3,
    iou_threshold=0.3
)

# ===============================
# FUNCIÓN PRINCIPAL
# ===============================

def update_tracker(detections):
    """
    Actualiza el tracker SORT usando detecciones YOLO.

    Args:
        detections (list):
        [
            [x1, y1, x2, y2, estado, conf],
            ...
        ]

    Returns:
        tracks (list):
        [
            [x1, y1, x2, y2, track_id],
            ...
        ]
    """

    # SORT SOLO necesita las bounding boxes
    if len(detections) == 0:
        dets = np.empty((0, 4))
    else:
        dets = np.array([
            [d[0], d[1], d[2], d[3]] for d in detections
        ])

    # Actualizar tracker
    tracks = tracker.update(dets)

    # Formatear salida
    formatted_tracks = []
    for trk in tracks:
        x1, y1, x2, y2, track_id = trk
        formatted_tracks.append([
            int(x1),
            int(y1),
            int(x2),
            int(y2),
            int(track_id)
        ])

    return formatted_tracks