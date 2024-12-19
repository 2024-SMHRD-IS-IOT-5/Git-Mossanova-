import subprocess

def run_audio_stream():
    subprocess.run(["python3", "audio.py"])

if __name__ == "__main__":
    print("Starting audio stream...")
    try:
        run_audio_stream()
    except KeyboardInterrupt:
        print("Audio streaming stopped.")
