import socket
import pyaudio
from collections import deque
from config import HOST, PORT, CHUNK, CHANNELS, RATE, KEYWORDS, DECIBEL_THRESHOLD, NOISE_THRESHOLD, PROCESS_INTERVAL, LAST_DETECTED
from audio import process_audio
from send_SNS import send_sns_alert

# 스트림 초기화
audio = pyaudio.PyAudio()
buffer = deque(maxlen=RATE // CHUNK * 10)  # 최근 10초간 데이터 저장
last_transcript = ""  # 마지막으로 처리된 Whisper 결과

# 서버 시작
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for connection...")


conn, addr = server_socket.accept()
print(f"Connection from {addr}")

# 스트림 시작
stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

try:
    print("Receiving audio...")
    while True:
        data = conn.recv(CHUNK)
        
        if not data:
            print("Client disconnected.")
            break

        # 스트림 출력 및 버퍼 저장
        stream.write(data)
        buffer.append(data)

        # 버퍼 크기가 일정량을 넘으면 처리
        if len(buffer) == buffer.maxlen:
            process_audio(buffer, KEYWORDS, LAST_DETECTED, PROCESS_INTERVAL, DECIBEL_THRESHOLD, NOISE_THRESHOLD)
            buffer.clear()

except KeyboardInterrupt:
    print("Server stopped.")

finally:
    # 스트림 및 소켓 종료
    stream.stop_stream()
    stream.close()
    audio.terminate()
    conn.close()
    server_socket.close()
    print("Connection closed.")