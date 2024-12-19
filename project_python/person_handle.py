# import cv2
# import os
# import time
# from db import save_video_to_db, save_photo_to_db

# def detect_person(frame, pose, save_folder, timestamp, person_start_time, event_triggered, video_writer_person):
#     """
#     사람 감지 및 30초 이상 감지 시 이벤트 처리.
#     """
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results_pose = pose.process(rgb_frame)

#     if results_pose.pose_landmarks:
#         if person_start_time is None:
#             person_start_time = time.time()
#             print("👤 Person detected!")

#         if not event_triggered and time.time() - person_start_time >= 30:
#             print("📹 30 seconds of person detection! Saving video and photo...")
#             event_triggered = True
#             photo_path = os.path.join(save_folder, f"person_detected_{timestamp}.jpg")
#             video_writer_person = cv2.VideoWriter(
#                 os.path.join(save_folder, f"person_detected_{timestamp}.mp4"),
#                 cv2.VideoWriter_fourcc(*'mp4v'),
#                 30,
#                 (frame.shape[1], frame.shape[0]),
#             )
#             cv2.imwrite(photo_path, frame)
#             save_photo_to_db(photo_path)

#     if event_triggered:
#         video_writer_person.write(frame)

#         if time.time() - person_start_time >= 45:  # 15초 후 저장 종료
#             print("✅ Stopping person video recording...")
#             video_writer_person.release()
#             save_video_to_db(video_writer_person.filename, photo_path)
#             event_triggered = False
#             person_start_time = None

#     return person_start_time, event_triggered, video_writer_person



import cv2
import os
import time
import mediapipe as mp  # MediaPipe 임포트
from db import save_video_to_db
from config import video_door_message
from send_SNS import send_sns_alert

# MediaPipe Pose Estimation 초기화
pose = mp.solutions.pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

hand_touch_time = None
video_writer_hand = None

def detect_hand_in_roi_and_save_video(frame, fps, frame_width, frame_height, save_folder, timestamp, roi):
    """실시간 손 감지 및 ROI 이벤트 처리"""
    global hand_touch_time, video_writer_hand, video_path
    
    video_out_path_hand = os.path.join(save_folder, f"hand_in_roi_{timestamp}.mp4")
    photo_path_hand = os.path.join(save_folder, f"hand_in_roi_{timestamp}.jpg")
    roi_x, roi_y, roi_w, roi_h = roi

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(rgb_frame)

    
    if results_pose.pose_landmarks:
        for id in [15, 16]:
            h, w, _ = frame.shape
            hand_x = int(results_pose.pose_landmarks.landmark[id].x * w)
            hand_y = int(results_pose.pose_landmarks.landmark[id].y * h)

            if roi_x < hand_x < roi_x + roi_w and roi_y < hand_y < roi_y + roi_h:
                if hand_touch_time is None:
                    hand_touch_time = time.time()
                    print("✋ Hand detected in ROI! Starting video recording...")
                    
                    video_writer_hand = cv2.VideoWriter(
                        video_out_path_hand, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height)
                    )
                    video_path = video_out_path_hand
                    cv2.imwrite(photo_path_hand, frame)

    if hand_touch_time:
        video_writer_hand.write(frame)
        # print('💔time/ hand_touch_time ', time.time(), hand_touch_time)

        if time.time() - hand_touch_time > 10:
            print("✅ Stopping hand video recording...")
            
            video_writer_hand.release()
            # Reset variables
            video_writer_hand = None  # Reset the video writer
            hand_touch_time = None    # Reset the touch time
            
            # Ensure the video file exists before saving to DB
            if os.path.exists(video_path):
                send_sns_alert(video_door_message)
                save_video_to_db(video_path, photo_path_hand)
            else:
                print(f"❌ Video file not found: {video_path}. Skipping database save.")
            
            
            # save_video_to_db(video_out_path_hand, photo_path_hand)
            # video_writer_hand = None
            # hand_touch_time = None
