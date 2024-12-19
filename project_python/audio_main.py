from server import audio_server
import config
import signal
import sys
from multiprocessing import Event

def main():
    """오디오 서버 실행 및 종료 처리"""
    print("Starting audio server...")
    stop_event = Event()

    def signal_handler(sig, frame):
        """Ctrl+C 신호 처리"""
        print("\nCtrl+C detected. Shutting down audio server...")
        stop_event.set()

    # Ctrl+C 신호 핸들링
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # 서버 실행
        audio_server(config.HOST, config.AUDIO_PORT, stop_event)
    except KeyboardInterrupt:
        print("Shutting down audio server...")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
