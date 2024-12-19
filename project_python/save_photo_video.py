import cv2
import os
import time
from config import SAVE_FOLDER, VIDEO_FOURCC, FPS


def save_photo(frame, prefix):
    """사진 저장 함수"""
    timestamp = int(time.time())
    photo_path = os.path.join(SAVE_FOLDER, f"{prefix}_{timestamp}.jpg")
    cv2.imwrite(photo_path, frame)
    print(f"📸 Photo saved: {photo_path}")
    return photo_path

def init_video_writer(video_name, frame_size):
    """비디오 저장 객체 초기화"""
    fourcc = cv2.VideoWriter_fourcc(*VIDEO_FOURCC)
    video_path = os.path.join(SAVE_FOLDER, f"{video_name}_{int(time.time())}.mp4v")
    return cv2.VideoWriter(video_path, fourcc, FPS, frame_size), video_path
