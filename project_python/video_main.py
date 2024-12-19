import signal
import sys
from server import video_server
from config import VIDEO_PORT, HOST
from multiprocessing import Manager
import cv2
import numpy as np

# import cv2
# import time
# import signal
# import os
# import sys
# from multiprocessing import Manager
# from person_handle import detect_person_and_save_video
# from person_event import detect_hand_in_roi_and_save_video
# from delivery_event import detect_pixel_changes_and_save
# from server import video_server  # 비디오 서버 함수 가져오기
# from config import HOST, VIDEO_PORT  # 서버 설정 값
# import numpy as np

# # 공통 설정
# save_folder = './save_data'
# os.makedirs(save_folder, exist_ok=True)

# # ROI 영역 설정
# roi = (67, 175, 22, 86)  # 손 감지 ROI
# box_roi = (58, 208, 292, 227)  # 픽셀 변화 감지 ROI

# # 타임스탬프
# timestamp = str(int(time.time()))


# def extract_frame(latest_frame):
#     """latest_frame에서 이미지를 추출"""
#     frame_data = np.frombuffer(latest_frame.value, dtype=np.uint8)
#     frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
#     return frame


# def main():
#     """비디오 서버 실행 및 이벤트 감지"""
#     print("🚀 Starting video server...")

#     stop_event = False  # 종료 플래그

#     def signal_handler(sig, frame):
#         """Ctrl+C 신호 감지 시 종료"""
#         nonlocal stop_event
#         print("\n🛑 Stopping video server...")
#         stop_event = True

#     signal.signal(signal.SIGINT, signal_handler)  # 종료 시그널 핸들러 등록

#     try:
#         with Manager() as manager:  # Manager 사용
#             latest_frame = manager.Value('bytes', b'')  # latest_frame 초기화

#             # 비디오 서버 실행
#             video_server(HOST, VIDEO_PORT, latest_frame, lambda: stop_event)

#             while not stop_event:
#                 frame = extract_frame(latest_frame)
#                 if frame is None or frame.size == 0:
#                     print("❌ Failed to decode frame. Skipping...")
#                     continue

#                 # 주석을 제거하여 각각의 이벤트를 실행하세요

#                 # 사람 감지 이벤트 실행
#                 print("👤 Executing detect_person_and_save_video...")
#                 detect_person_and_save_video(
#                     frame, 30, frame.shape[1], frame.shape[0], save_folder, timestamp
#                 )

#                 # 손 감지 이벤트 실행
#                 # print("✋ Executing detect_hand_in_roi_and_save_video...")
#                 # detect_hand_in_roi_and_save_video(
#                 #     frame, 30, frame.shape[1], frame.shape[0], save_folder, timestamp, roi
#                 # )

#                 # 픽셀 변화 감지 이벤트 실행
#                 # print("🔔 Executing detect_pixel_changes_and_save...")
#                 # detect_pixel_changes_and_save(frame, save_folder, box_roi)

#     except KeyboardInterrupt:
#         print("\nShutting down video server...")
#     finally:
#         print("✅ Video server stopped.")
#         sys.exit(0)


# if __name__ == "__main__":
#     main()


#----- 기존 코드
def main():
    """비디오 서버 실행"""
    print("🚀 Starting video server...")

    stop_event = False  # 종료 플래그

    def signal_handler(sig, frame):
        """Ctrl+C 신호 감지 시 종료"""
        nonlocal stop_event
        print("\n🛑 Stopping video server...")
        stop_event = True

    signal.signal(signal.SIGINT, signal_handler)  # 종료 시그널 핸들러 등록

    try:
        with Manager() as manager:  # Manager 사용
            latest_frame = manager.Value('bytes', b'')  # latest_frame 초기화

            # 비디오 서버 실행
            video_server(HOST, VIDEO_PORT, latest_frame, lambda: stop_event)

    except KeyboardInterrupt:
        print("\nShutting down video server...")
    finally:
        print("✅ Video server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()



# ------------------------------플라스크서버와 멀티프로세싱-----------------
# import signal
# import sys
# from multiprocessing import Process, Manager, Event
# from server import video_server
# from flask_server import run_flask_server
# import time
# from config import VIDEO_PORT, HOST

# def main():
#     """Flask 서버와 비디오 서버 실행"""
#     print("🚀 Starting Flask server and video server...")

#     stop_event = Event()
#     signal.signal(signal.SIGINT, lambda sig, frame: stop_event.set())

#     try:
#         with Manager() as manager:
#             latest_frame = manager.Value('bytes', b'')

#             # Flask 서버 프로세스
#             flask_process = Process(target=run_flask_server, args=(latest_frame, stop_event))
#             flask_process.start()

#             # 비디오 서버 프로세스 (이벤트 감지 포함)
#             video_process = Process(target=video_server, args=(HOST, VIDEO_PORT, latest_frame, stop_event))
#             video_process.start()

#             # 메인 프로세스에서 기다리기
#             while not stop_event.is_set():
#                 time.sleep(1)

#     except KeyboardInterrupt:
#         print("Shutting down servers...")
#         stop_event.set()
#     finally:
#         flask_process.terminate()
#         video_process.terminate()
#         flask_process.join()
#         video_process.join()
#         sys.exit(0)

# if __name__ == "__main__":
#     main()
