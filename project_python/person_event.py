# import cv2
# import os
# import time
# from db import save_video_to_db, save_photo_to_db
# from config import HAND_ROI

# def detect_hand_event(frame, pose, roi, save_folder, timestamp, hand_start_time, video_writer_hand):
#     """
#     손이 ROI에 감지되면 이벤트 처리.
#     """
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results_pose = pose.process(rgb_frame)

#     x, y, w, h = HAND_ROI
#     if results_pose.pose_landmarks:
#         for id in [15, 16]:  # 왼손, 오른손
#             h, w, _ = frame.shape
#             hand_x = int(results_pose.pose_landmarks.landmark[id].x * w)
#             hand_y = int(results_pose.pose_landmarks.landmark[id].y * h)

#             if x < hand_x < x + w and y < hand_y < y + h:  # ROI 내부 감지
#                 if hand_start_time is None:
#                     hand_start_time = time.time()
#                     print("✋ Hand detected in ROI! Starting video recording...")
#                     video_writer_hand = cv2.VideoWriter(
#                         os.path.join(save_folder, f"hand_detected_{timestamp}.mp4"),
#                         cv2.VideoWriter_fourcc(*'mp4v'),
#                         30,
#                         (frame.shape[1], frame.shape[0]),
#                     )
#                     photo_path = os.path.join(save_folder, f"hand_detected_{timestamp}.jpg")
#                     cv2.imwrite(photo_path, frame)
#                     save_photo_to_db(photo_path)

#     if hand_start_time:
#         video_writer_hand.write(frame)

#         if time.time() - hand_start_time >= 10:
#             print("✅ Stopping hand video recording...")
#             video_writer_hand.release()
#             save_video_to_db(video_writer_hand.filename, photo_path)
#             hand_start_time = None

#     return hand_start_time, video_writer_hand

import cv2
import os
import time
from db import save_video_to_db
import mediapipe as mp
from config import video_30s_message
from send_SNS import send_sns_alert

# MediaPipe Pose Estimation 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3)


# frame, 30, frame.shape[1], frame.shape[0], './save_data', str(int(time.time()))
# frame, fps, frame_width, frame_height, save_folder, timestamp

# 전역 변수 초기화
person_detected_start_time = None
event_triggered = False
video_writer_person = None
video_path = None

def detect_person_and_save_video(frame, fps, frame_width, frame_height, save_folder, timestamp):
    """실시간 사람 감지 및 30초 이상 감지 시 이벤트 처리"""
    global person_detected_start_time, event_triggered, video_writer_person

    photo_path_person = os.path.join(save_folder, f"person_30sec_{timestamp}.jpg")
    video_out_path_person = os.path.join(save_folder, f"person_30sec_{timestamp}.mp4")
    
    if frame is None or frame.size == 0:
        print("❌ Invalid frame received. Skipping...")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(rgb_frame)  # Pose Estimation 수행
    
    # 사람 감지
    if not event_triggered and results_pose.pose_landmarks:
        if person_detected_start_time is None:
            person_detected_start_time = time.time()
            print("👤 Person detected! Starting 30-second timer...")

        # 30초 이상 감지되었는지 확인
        if time.time() - person_detected_start_time >= 30:
            # print("📹 30 seconds of person detection! Saving video and photo...")
            event_triggered = True
            
            cv2.imwrite(photo_path_person, frame)
            
            video_writer_person = cv2.VideoWriter(
                video_out_path_person, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height)
            )
            
            video_path = video_out_path_person
            
    elif not results_pose.pose_landmarks:
        print("🖤 No person detected. Resetting timer...")
        person_detected_start_time = None
        
    if video_writer_person and event_triggered:
        video_writer_person.write(frame)
        print('time / person_time : ', time.time(),person_detected_start_time)
        
        if time.time() - person_detected_start_time > 40:
            print("✅ Stopping person video recording...")
            video_writer_person.release()
            video_writer_person = None
            person_detected_start_time = None
            event_triggered = False
            
            if video_path and os.path.exists(video_path):
                save_video_to_db(video_path, photo_path_person)
                send_sns_alert(video_30s_message)
            else:
                print(f"❌ Video file not found: {video_path}. Skipping database save.")

