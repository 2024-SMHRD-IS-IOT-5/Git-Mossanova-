import cv2
import socket
import struct

SERVER_IP = "192.168.219.196"
SERVER_PORT = 6000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
camera.set(cv2.CAP_PROP_FPS, 30)

print("Streaming video")

try:
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to capture frame.")
            continue

        _, buffer = cv2.imencode('.jpg', frame,[int(cv2.IMWRITE_JPEG_QUALITY), 50])
        frame_data =buffer.tobytes()
        
        frame_size = struct.pack("!Q", len(frame_data))
        client_socket.sendall(frame_size)
        
        print(f"Sending frame of size: {frame_size} bytes")  # ??? ?? ??
        client_socket.sendall(frame_data)
except KeyboardInterrupt:
    print("Video streaming stopped.")
finally:
    camera.release()
    client_socket.close()


