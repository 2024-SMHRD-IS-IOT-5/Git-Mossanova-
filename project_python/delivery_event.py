# import cv2
# import numpy as np
# import os
# import time
# from db import save_photo_to_db
# from config import BOX_ROI

# def detect_delivery_event(frame, prev_gray, roi, save_folder):
#     """
#     픽셀 변화 감지 및 이벤트 발생 시 사진 저장.
#     """
#     x, y, w, h = BOX_ROI
#     current_roi = frame[y:y+h, x:x+w]
#     curr_gray = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)

#     if prev_gray is not None:
#         frame_diff = cv2.absdiff(prev_gray, curr_gray)
#         _, threshold_diff = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

#         if (np.sum(threshold_diff) > 33000)&(np.sum(threshold_diff)<50000):
#             print("🔔 Delivery event detected! Saving photo...")
#             photo_path = os.path.join(save_folder, f"delivery_event_{int(time.time())}.jpg")
#             cv2.imwrite(photo_path, frame)
#             save_photo_to_db(photo_path)

#     return curr_gray

# import cv2
# import numpy as np
# from save_photo_video import save_photo
# from person_event import detect_person_and_hand  # person_event 함수 불러오기
# from config import ROI, delivery_message
# from db import save_photo_to_db
# from send_SNS import send_sns_alert


# def detect_pixel_changes(frame, prev_gray, frame_size, person_start_time, hand_start_time, video_writer_person, video_writer_hand):
#     """ROI 픽셀 변화 감지 및 person_event 실행"""
#     x, y, w, h = ROI
#     current_roi = frame[y:y+h, x:x+w]
#     curr_gray = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)

#     if prev_gray is not None:
#         # 픽셀 차이 계산
#         frame_diff = cv2.absdiff(prev_gray, curr_gray)
#         _, threshold_diff = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
#         change_detected = np.sum(threshold_diff)<=35000
        
#         print('💕💕pixel',np.sum(threshold_diff))

#         if change_detected:
#             print("🔍 Pixel change detected!")
#             photo_path = save_photo(frame, "delivery")
#             save_photo_to_db(photo_path)
#             send_sns_alert(delivery_message)

#             # person_event 실행
#             print("🚨 Triggering person_event...")
#             person_start_time, hand_start_time, video_writer_person, video_writer_hand = detect_person_and_hand(
#                 frame, frame_size, person_start_time, hand_start_time, video_writer_person, video_writer_hand
#             )
#             return curr_gray, person_start_time, hand_start_time, video_writer_person, video_writer_hand

#     return curr_gray, person_start_time, hand_start_time, video_writer_person, video_writer_hand

# import cv2
# import numpy as np
# import os
# import time
# from db import save_photo_to_db


# def detect_pixel_changes_and_save(cap, save_folder, roi):
#     """실시간 픽셀 변화 감지 및 이벤트 처리"""
#     x, y, w, h = roi
#     prev_gray = None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         current_roi = frame[y:y+h, x:x+w]
#         curr_gray = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)

#         if prev_gray is not None:
#             frame_diff = cv2.absdiff(prev_gray, curr_gray)
#             _, threshold_diff = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

#             if (np.sum(threshold_diff) > 33000)&(np.sum(threshold_diff)<50000):
#                 print("🔔 Pixel change detected! Saving photo...")
#                 photo_path = os.path.join(save_folder, f"pixel_change_{int(time.time())}.jpg")
#                 cv2.imwrite(photo_path, frame)
#                 save_photo_to_db(photo_path)

#         prev_gray = curr_gray
#         cv2.imshow("Pixel Change Detection", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

import cv2
import numpy as np
import os
import time
from db import save_photo_to_db
from config import video_30s_message
from send_SNS import send_sns_alert

# 타이머 변수
# last_event_time = 0  # 마지막 이벤트 실행 시간 초기화

# 전역 변수 초기화
prev_gray = None  # 이전 프레임의 흑백 이미지
last_event_time = 0  # 마지막 이벤트 실행 시간 초기화

def detect_pixel_changes_and_save(frame, save_folder, roi):
    """픽셀 변화 감지 및 이벤트 처리"""
    global last_event_time  # 전역 타이머 변수 선언
    global prev_gray
    
    event_time = False
    
    x, y, w, h = roi
    current_roi = frame[y:y+h, x:x+w]
    curr_gray = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)

    # 현재 시간 확인
    current_time = time.time()
    
    # prev_gray가 초기화되지 않았다면 현재 프레임으로 초기화
    if prev_gray is None:
        prev_gray = curr_gray
        print("🟡 Initialized prev_gray with the first frame.")
        return  # 초기화 후 다음 프레임으로 넘어감

    if not event_time and prev_gray is not None :
        frame_diff = cv2.absdiff(prev_gray, curr_gray)
        _, threshold_diff = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

        if (np.sum(threshold_diff) > 33000) & (np.sum(threshold_diff) < 50000):
            print("🔔 Pixel change detected! Saving photo...")
            photo_path = os.path.join(save_folder, f"delivery_{int(time.time())}.jpg")
            cv2.imwrite(photo_path, frame)
            save_photo_to_db(photo_path)
            send_sns_alert(video_30s_message)
            event_time = True

            # 이벤트 실행 후 시간 갱신
            last_event_time = current_time
            
    # 20초 동안 이벤트 차단
    if event_time and current_time - last_event_time < 20:
        print("⏳ Skipping event (20-second cooldown)")
        event_time = False
        return

    prev_gray = curr_gray

