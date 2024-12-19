import subprocess

def run_video_stream():
    subprocess.run(["python3", "video.py"])

if __name__ == "__main__":
    print("Starting video stream...")
    try:
        run_video_stream()
    except KeyboardInterrupt:
        print("Video streaming stopped.")
    


