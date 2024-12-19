from delivery_event import detect_delivery_event
from person_handle import detect_person
import mediapipe as mp

pose = mp.solutions.pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def process_frames(frame, prev_gray, roi, save_folder, timestamp, person_start_time, event_triggered, video_writer):
    """
    실시간으로 박스와 사람 감지를 처리.
    """
    prev_gray = detect_delivery_event(frame, prev_gray, roi, save_folder)
    person_start_time, event_triggered, video_writer = detect_person(
        frame, pose, save_folder, timestamp, person_start_time, event_triggered, video_writer
    )
    return prev_gray, person_start_time, event_triggered, video_writer
