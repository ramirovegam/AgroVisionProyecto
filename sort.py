import numpy as np
from filterpy.kalman import KalmanFilter
from scipy.optimize import linear_sum_assignment


def iou(bb_test, bb_gt):
    xx1 = np.maximum(bb_test[0], bb_gt[0])
    yy1 = np.maximum(bb_test[1], bb_gt[1])
    xx2 = np.minimum(bb_test[2], bb_gt[2])
    yy2 = np.minimum(bb_test[3], bb_gt[3])

    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h

    o = wh / (
        (bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1]) +
        (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - wh
    )
    return o


class KalmanBoxTracker:
    count = 0

    def __init__(self, bbox):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([
            [1,0,0,0,1,0,0],
            [0,1,0,0,0,1,0],
            [0,0,1,0,0,0,1],
            [0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0],
            [0,0,0,0,0,1,0],
            [0,0,0,0,0,0,1]
        ])

        self.kf.H = np.array([
            [1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0]
        ])

        self.kf.R[2:,2:] *= 10
        self.kf.P[4:,4:] *= 1000
        self.kf.P *= 10
        self.kf.Q[-1,-1] *= 0.01
        self.kf.Q[4:,4:] *= 0.01

        self.kf.x[:4] = bbox.reshape((4,1))

        self.time_since_update = 0
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.hit_streak = 0
        self.age = 0

    def predict(self):
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        return self.kf.x[:4].reshape((4,))

    def update(self, bbox):
        self.time_since_update = 0
        self.hit_streak += 1
        self.kf.update(bbox.reshape((4,1)))

    def get_state(self):
        return self.kf.x[:4].reshape((4,))


class Sort:
    def __init__(self, max_age=15, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.trackers = []
        self.frame_count = 0

    def update(self, dets):
        self.frame_count += 1

        predictions = []
        for trk in self.trackers:
            predictions.append(trk.predict())
        predictions = np.array(predictions)

        matches = []
        unmatched_dets = list(range(len(dets)))
        unmatched_trks = list(range(len(predictions)))

        if len(predictions) > 0 and len(dets) > 0:
            iou_matrix = np.zeros((len(dets), len(predictions)))

            for d in range(len(dets)):
                for t in range(len(predictions)):
                    iou_matrix[d, t] = iou(dets[d], predictions[t])

            row_ind, col_ind = linear_sum_assignment(-iou_matrix)

            for d, t in zip(row_ind, col_ind):
                if iou_matrix[d, t] >= self.iou_threshold:
                    matches.append((d, t))
                    if d in unmatched_dets:
                        unmatched_dets.remove(d)
                    if t in unmatched_trks:
                        unmatched_trks.remove(t)

        for d, t in matches:
            self.trackers[t].update(dets[d])

        for d in unmatched_dets:
            self.trackers.append(KalmanBoxTracker(dets[d]))

        ret = []
        for trk in list(self.trackers):
            if trk.time_since_update < self.max_age:
                if trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits:
                    ret.append(list(trk.get_state()) + [trk.id])
            else:
                self.trackers.remove(trk)

        return ret