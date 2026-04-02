import numpy as np
from sort import Sort

tracker = Sort(max_age=15, min_hits=3, iou_threshold=0.3)

def update_tracker(detections):
    if len(detections) == 0:
        dets = np.empty((0, 4))
    else:
        dets = np.array([d[:4] for d in detections])

    tracks = tracker.update(dets)

    return [[int(x1), int(y1), int(x2), int(y2), int(tid)]
            for x1, y1, x2, y2, tid in tracks]