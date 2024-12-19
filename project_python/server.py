import socket
import struct
import numpy as np
import cv2
import pyaudio
from collections import deque
import config
from audio import process_audio
import time
#from delivery_event import detect_pixel_changes
# from event_handler import detect_events

from person_handle import detect_hand_in_roi_and_save_video
from person_event import detect_person_and_save_video
from delivery_event import detect_pixel_changes_and_save

# 오디오 서버
def audio_server(host, port, stop_event):
    """오디오 데이터를 수신하는 서버"""
    audio = pyaudio.PyAudio()
    buffer = deque(maxlen=config.RATE // config.CHUNK * 3)  # 최근 3초간 데이터 저장

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, int(port)))
    server_socket.listen(1)
    print(f"Audio server waiting for connection on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Audio connection from {addr}")

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=config.CHANNELS,
        rate=config.RATE,
        output=True,
        frames_per_buffer=config.CHUNK
    )

    try:
        while not stop_event.is_set():
            data = conn.recv(config.CHUNK)
            if not data:
                break

            #print(f"Received audio chunk of size: {len(data)} bytes")
            stream.write(data)
            buffer.append(data)

            if len(buffer) >= config.RATE // config.CHUNK * 3:
                process_audio(
                    buffer,
                    config.KEYWORDS,
                    config.LAST_DETECTED,
                    config.PROCESS_INTERVAL,
                    config.DECIBEL_THRESHOLD,
                    config.NOISE_THRESHOLD,
                )
                buffer.clear()
    except Exception as e:
        print(f"Audio server error: {e}")
    finally:
        print("Closing audio server...")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        conn.close()
        server_socket.close()

#---------------------나영--------------
# def video_server(host, port, latest_frame, stop_event):
#     """비디오 데이터를 수신하고 이벤트 감지를 수행하는 서버"""
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((host, int(port)))
#     server_socket.listen(1)
#     print(f"📡 Video server waiting for connection on {host}:{port}...")

#     conn, addr = server_socket.accept()
#     print(f"✅ Connected to {addr}")

#     try:
#         while not stop_event():
#             # 프레임 길이 수신
#             frame_size_data = conn.recv(8)
#             if not frame_size_data:
#                 break
#             frame_size = struct.unpack("!Q", frame_size_data)[0]

#             # 프레임 데이터 수신
#             frame_data = b""
#             while len(frame_data) < frame_size:
#                 packet = conn.recv(min(4096, frame_size - len(frame_data)))
#                 if not packet:
#                     print("❌ Connection lost while receiving frame data.")
#                     break
#                 frame_data += packet

#             if len(frame_data) != frame_size:
#                 print(f"❌ Frame size mismatch: expected {frame_size}, got {len(frame_data)}")
#                 continue

#             # 프레임 디코딩
#             frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
#             if frame is None or frame.size == 0:
#                 print("❌ Decoded frame is empty! Skipping...")
#                 continue
            
#             # 이벤트 처리에 사용할 변수 업데이트
#             # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             # if prev_gray is None:  # 초기 프레임
#             #     prev_gray = gray_frame

#             # 최신 프레임 업데이트
#             _, buffer = cv2.imencode('.jpg', frame)
#             latest_frame.value = buffer.tobytes()

#             # 이벤트 실행 (하나씩 주석 제거하여 실행)

#             # 사람 감지 이벤트 실행
#             # print("👤 Executing detect_person_and_save_video...")
#             detect_person_and_save_video(frame, 30, frame.shape[1], frame.shape[0], config.SAVE_FOLDER, str(int(time.time())))

#             # 손 감지 이벤트 실행
#             # print("✋ Executing detect_hand_in_roi_and_save_video...")
#             # detect_hand_in_roi_and_save_video(frame, 30, frame.shape[1], frame.shape[0], config.SAVE_FOLDER, str(int(time.time())), config.HAND_ROI)

#             # 픽셀 변화 감지 이벤트 실행
#             # print("🔔 Executing detect_pixel_changes_and_save...")
#             # detect_pixel_changes_and_save(frame, config.SAVE_FOLDER, config.HAND_ROI)

#             # prev_gray = gray_frame  # 현재 프레임을 다음 루프의 이전 프레임으로 설정
            
#     except Exception as e:
#         print(f"❗ Video server error: {e}")
#     finally:
#         conn.close()
#         server_socket.close()
#         print("✅ Video server stopped.")
#---------------------나영--------------

# def video_server(host, port, latest_frame, stop_event):
#     """비디오 데이터를 수신하고 이벤트 감지를 수행하는 서버"""
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((host, int(port)))
#     server_socket.listen(1)
#     print(f"📡 Video server waiting for connection on {host}:{port}...")

#     conn, addr = server_socket.accept()
#     print(f"✅ Connected to {addr}")

#     prev_gray = None
#     person_start_time = None
#     hand_start_time = None
#     video_writer_person = None
#     video_writer_hand = None

#     try:
#         while not stop_event():
#             # 프레임 길이 수신
#             frame_size_data = conn.recv(8)
#             if not frame_size_data:
#                 break
#             frame_size = struct.unpack("!Q", frame_size_data)[0]

#             # 프레임 데이터 수신
#             frame_data = b""
#             while len(frame_data) < frame_size:
#                 packet = conn.recv(min(4096, frame_size - len(frame_data)))
#                 if not packet:
#                     print("❌ Connection lost while receiving frame data.")
#                     break
#                 frame_data += packet

#             if len(frame_data) != frame_size:
#                 print(f"❌ Frame size mismatch: expected {frame_size}, got {len(frame_data)}")
#                 continue

#             # 프레임 디코딩
#             frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
#             if frame is None or frame.size == 0:
#                 print("❌ Decoded frame is empty! Skipping this frame...")
#                 continue
            
#             if frame is not None:
#                 print(" Failed to decode frame or empty frame received")
#                 # 이벤트 실행 (동시에 delivery 및 person_event)
#                 prev_gray, person_start_time, hand_start_time, video_writer_person, video_writer_hand = detect_events(
#                     frame, prev_gray, (frame.shape[1], frame.shape[0]), person_start_time, hand_start_time, 
#                     video_writer_person, video_writer_hand
#                 )

#                 # 최신 프레임 업데이트
#                 _, buffer = cv2.imencode('.jpg', frame)
#                 latest_frame.value = buffer.tobytes()

#                 # 비디오 저장
#                 if video_writer_person:
#                     video_writer_person.write(frame)
#                 if video_writer_hand:
#                     video_writer_hand.write(frame)
#             else:
#                 print("❌ Failed to decode frame!")

#     except Exception as e:
#         print(f"❗ Video server error: {e}")
#     finally:
#         # 비디오 저장 객체 해제
#         if video_writer_person:
#             video_writer_person.release()
#             print("🎥 Person video writer released.")
#         if video_writer_hand:
#             video_writer_hand.release()
#             print("🎥 Hand video writer released.")
#         conn.close()
#         server_socket.close()
#         print("✅ Video server stopped.")


#비디오 서버
def video_server(host, port, latest_frame, stop_event):
    """비디오 데이터를 수신하고 이벤트 감지를 수행하는 서버"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, int(port)))
    server_socket.listen(1)
    print(f"📡 Video server waiting for connection on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"✅ Connected to {addr}")

    try:
        while not stop_event():  # stop_event()로 호출
            # 프레임 수신 및 처리 로직
            frame_size_data = conn.recv(8)
            if not frame_size_data:
                break
            frame_size = struct.unpack("!Q", frame_size_data)[0]

            frame_data = b""
            while len(frame_data) < frame_size:
                packet = conn.recv(min(4096, frame_size - len(frame_data)))
                if not packet:
                    break
                frame_data += packet

            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                latest_frame.value = buffer.tobytes()
            else:
                print("❌ Failed to decode frame!")

    except Exception as e:
        print(f"❗ Video server error: {e}")
    finally:
        conn.close()
        server_socket.close()
        print("✅ Video server stopped.")
