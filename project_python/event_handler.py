import cv2
import numpy as np
from save_photo_video import save_photo
from person_event import detect_person_and_hand
from config import ROI, delivery_message
from db import save_photo_to_db
from send_SNS import send_sns_alert
import time

# delivery 이벤트를 막기 위한 타이머 변수
last_delivery_time = 0  # 초기화

def detect_events(frame, prev_gray, frame_size, person_start_time, hand_start_time, 
                  video_writer_person, video_writer_hand):
    """픽셀 변화 및 person_event를 동시에 실행"""
    x, y, w, h = ROI
    current_roi = frame[y:y+h, x:x+w]
    curr_gray = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)
    
    global last_delivery_time  # 타이머 변수 전역 선언
    current_time = time.time()
    
    # 10초 동안 delivery 이벤트 차단
    if current_time - last_delivery_time < 10:  # 10초 이내일 경우
        print("⏳ Skipping delivery event (10-second cooldown)")
        return curr_gray, person_start_time, hand_start_time, video_writer_person, video_writer_hand
    
    # 픽셀 변화 감지
    change_detected = False
    if prev_gray is not None:
        frame_diff = cv2.absdiff(prev_gray, curr_gray)
        _, threshold_diff = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        change_detected = (np.sum(threshold_diff) > 33000)&(np.sum(threshold_diff)<50000)
        print("💕💕 Pixel sum:", np.sum(threshold_diff))

    # 이벤트 실행
    if change_detected:
        print("🔍 Pixel change detected!")
        photo_path = save_photo(frame, "delivery")
        save_photo_to_db(photo_path)
        send_sns_alert(delivery_message)
        
        # delivery 이벤트 실행 후 시간 갱신
        last_delivery_time = current_time  # 현재 시간을 저장
    
    print("🚨 Triggering person_event...")
    person_start_time, hand_start_time, video_writer_person, video_writer_hand = detect_person_and_hand(
    frame, frame_size, person_start_time, hand_start_time, video_writer_person, video_writer_hand)
    
    return curr_gray, person_start_time, hand_start_time, video_writer_person, video_writer_hand
