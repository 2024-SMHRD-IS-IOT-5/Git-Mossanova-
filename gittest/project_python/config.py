from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# 서버 설정
HOST = "0.0.0.0"
PORT = 5000
CHUNK = 1024
CHANNELS = 1
RATE = 44100

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
KEYWORDS = ["도와주세요", "살려주세요"]

# 임계값
DECIBEL_THRESHOLD = 50
NOISE_THRESHOLD = 40

# 키워드 처리 간격
PROCESS_INTERVAL = timedelta(seconds=10)

# 키워드 처리 시간 기록 초기화
LAST_DETECTED = {keyword: datetime.min for keyword in KEYWORDS}
