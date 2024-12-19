import pyaudio
import socket

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

SERVER_IP = "192.168.219.196"
SERVER_PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Streaming audio")

try:
    while True:
        data = stream.read(CHUNK)
        
        client_socket.sendall(data)
except KeyboardInterrupt:
    print("Audio streaming stopped.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_socket.close()
