import cv2
import numpy as np

def process_video_stream(packet, latest_frame):
    try:
        # 소켓에서 수신한 데이터를 Numpy 배열로 변환
        frame_data = np.frombuffer(packet, dtype=np.uint8)
        
        # Numpy 배열을 OpenCV 형식으로 디코딩
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
        if frame is None:
            print("Error: Failed to decode frame.")  # 디코딩 실패 메시지
            return

        # 디코딩 성공 로그
        print("Frame decoded successfully.")

        # JPEG로 다시 인코딩하여 Flask 서버와 React에서 사용할 수 있도록 변환
        _, buffer = cv2.imencode('.jpg', frame)

        # latest_frame 변수 업데이트
        latest_frame.value = buffer.tobytes()

        # 디버깅용 로그: 업데이트된 프레임 크기 출력
        print(f"Updated latest_frame with size: {len(latest_frame.value)} bytes")

    except Exception as e:
        print(f"Error in process_video_stream: {e}")
