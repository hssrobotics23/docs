import cv2
import numpy as np

def gen_ious(images, truth, results):

    # Assume all same shape
    rea_canvas = np.zeros(images[0].shape[:2], dtype=np.float32)
    res_canvas = np.zeros(images[0].shape[:2], dtype=np.float32)

    for (rea, res) in zip(truth, results):
        rea_canvas[:,:] = 0
        res_canvas[:,:] = 0
        # Render the real bounds
        for box in rea["box"]:
            cv2.fillPoly(rea_canvas, pts =[np.array(box)], color =(1))
        # Render the result bounds
        for box in [r["box"] for r  in res["ocr_all_results"]]:
            cv2.fillPoly(res_canvas, pts =[np.array(box)], color =(1))

        # Calculate the union
        union = np.logical_or(rea_canvas > 0, res_canvas > 0)
        intersection = np.logical_and(rea_canvas > 0, res_canvas > 0)
        yield round(100 * (intersection.sum() / union.sum()))

def to_ious(*args):
    return list(gen_ious(*args))
