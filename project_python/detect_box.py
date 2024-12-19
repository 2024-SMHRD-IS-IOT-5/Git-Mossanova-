import cv2
import numpy as np
import os
import time
from db import save_photo_to_db
from config import BOX_ROI

def detect_box_changes(frame, prev_gray, roi, save_folder):
    """
    ROI(박스) 영역에서 픽셀 변화 감지 및 사진 저장.
    """
    x, y, w, h = BOX_ROI
    current_roi = frame[y:y+h, x:x+w]
    curr_gray = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)

    # 이전 프레임과 비교
    if prev_gray is not None:
        frame_diff = cv2.absdiff(prev_gray, curr_gray)
        _, threshold_diff = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

        # 변화 감지
        if (np.sum(threshold_diff) > 33000)&(np.sum(threshold_diff)<50000):
            print("📦 Box change detected! Saving photo...")
            photo_path = os.path.join(save_folder, f"box_change_{int(time.time())}.jpg")
            cv2.imwrite(photo_path, frame)
            save_photo_to_db(photo_path)

    return curr_gray
