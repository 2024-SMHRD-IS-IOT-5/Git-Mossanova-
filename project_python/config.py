from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# 서버 설정
HOST = os.getenv("HOST") 
AUDIO_PORT = os.getenv("AUDIO_PORT")
VIDEO_PORT = os.getenv("VIDEO_PORT")
CHUNK = int(os.getenv("CHUNK"))
CHANNELS = int(os.getenv("CHANNELS"))
RATE = int(os.getenv("RATE"))

# DataBase
DB_HOST = os.getenv("DB_HOST")  
DB_USER = os.getenv("DB_USER")      
DB_PASSWORD = os.getenv("DB_PASSWORD")  
DB_NAME = os.getenv("DB_NAME")    
DB_PORT = int(os.getenv("DB_PORT"))    

# AWS 설정
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION") 
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")


# 키워드 목록
KEYWORDS = os.getenv("KEYWORDS")

# 마이크 설정 및 오디오 임계값
MIC_SENSITIVITY_DB = float(os.getenv("MIC_SENSITIVITY_DB"))
MIC_SENSITIVITY = 10 ** (MIC_SENSITIVITY_DB / 20)
REFERENCE_PRESSURE =  float(os.getenv("REFERENCE_PRESSURE"))
DECIBEL_THRESHOLD = float(os.getenv("DECIBEL_THRESHOLD"))
NOISE_THRESHOLD = float(os.getenv("NOISE_THRESHOLD"))

# 키워드 처리 간격
PROCESS_INTERVAL = timedelta(seconds=10)

# 키워드 처리 시간 기록 초기화
LAST_DETECTED = {keyword: datetime.min for keyword in KEYWORDS}

# 사진, 동영상 저장 경로 설정
SAVE_FOLDER = '.\save_data'
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ROI 영역 (x, y, width, height)
BOX_ROI = (270, 200, 70, 110)
HAND_ROI = (200, 130, 50, 130)

# 사람 감지 임계값 (초)
PERSON_DETECT_THRESHOLD = 30

# 비디오 저장 형식
VIDEO_FOURCC = 'mp4v'
FPS = 30

# 알람 내용
audio_message = os.getenv("audio_message")
delivery_message = os.getenv("delivery_message")
video_30s_message = os.getenv("video_30s_message")
video_door_message = os.getenv("video_door_message")
