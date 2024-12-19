import os
import wave
import mysql.connector
from config import DB_HOST,DB_PASSWORD,DB_NAME,DB_PORT,DB_USER
import cv2

def get_db_connection():
    """MySQL 데이터베이스 연결"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

################################################# 오디오 관련(트리거 포함) #####################################################    
def extract_audio_details(file_path):
    """오디오 데이터 추출 """
    try:
        # audio db 값들 추출하기
        audio_name = os.path.basename(file_path)
        audio_size = os.path.getsize(file_path) 
        audio_ext = os.path.splitext(file_path)[1] 

        # audio_length
        with wave.open(file_path, "rb") as wf:
            n_frames = wf.getnframes() 
            frame_rate = wf.getframerate() 
            audio_length = n_frames / float(frame_rate)  # Length in seconds

        return audio_name, audio_size, audio_ext, audio_length
    
    except Exception as e:
        print(f"Error extracting audio details: {e}")
        return None, None, None, None

def trigger_audio_details(file_path):
    """오디오관련 트리거 데이터 """
    try:
        trg_type = "위급상황-불법침입"
        trg_info = "현관 문 앞에서 특정 키워드의 소리가 감지되었습니다."
        
        # trg_image 값 추출
        trg_image = file_path
        
        video_idx = 1
      
        return trg_type, trg_info, trg_image, video_idx
    
    except Exception as e:
        print(f"Error trigger_audio details: {e}")
        return None, None, None, None   
              

def save_audio_to_db(file_path):
    """db 저장 : 오디오 및 트리거 테이블 """
    conn = get_db_connection()
    if conn is None:
        return
    audio_name, audio_size, audio_ext, audio_length = extract_audio_details(file_path)
    trg_type, trg_info, trg_image, video_idx = trigger_audio_details(file_path)
    
    try:
        cursor = conn.cursor()
        
        # audio 테이블에 값 저장
        query = """
        INSERT INTO audios (audio_name, audio_size, audio_ext, audio_length, user_id)
        VALUES (%s, %s, %s, %s, 'smhrd1')
        """
        cursor.execute(query, (audio_name, audio_size, audio_ext, audio_length))
        
        # triggers 테이블에 값 저장
        query = """
        SELECT audio_idx FROM audios WHERE audio_name= %s 
        """
        cursor.execute(query, (audio_name,))
        audio_idx_db = cursor.fetchone()
        
        query = """
        INSERT INTO triggers (user_id, trg_type, trg_info, trg_image, video_idx, audio_idx)
        VALUES ('smhrd1', %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (trg_type, trg_info, trg_image, video_idx, audio_idx_db))
        
        conn.commit()
        print("Data saved to database successfully.")
    except mysql.connector.Error as err:
        print(f"Error saving to database: {err}")
    finally:
        cursor.close()
        conn.close()


################################################# 비디오 관련(트리거 포함) #####################################################    
def extract_video_details(file_path):
    """ 비디오 데이터 추출 """
    try:
        # audio db 값들 추출하기
        video_name = os.path.basename(file_path)
        video_size = os.path.getsize(file_path) 
        video_ext = os.path.splitext(file_path)[1] 
        video_path = os.path.abspath(file_path)  # 절대 경로로 변환

       # video_length (초 단위로 비디오 길이 추출)
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {file_path}")

        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 총 프레임 수
        fps = cap.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수 (fps)
        video_length = frame_count / fps  # 비디오 길이 (초 단위)
        
        # 캡처 객체 해제
        cap.release()
        
        print("💞 : ", video_name, video_size, video_ext, video_length, video_path)

        return video_name, video_size, video_ext, video_length, video_path

    except Exception as e:
        print(f"Error extracting _video details: {e}")
        return None, None, None, None, None              

def trigger_video_details(photo_path):
    """비디오관련 트리거 데이터 """
    try:
        # trg_image 값 추출
        trg_image = os.path.abspath(photo_path)
        
        return trg_image

    except Exception as e:
        print(f"Error trigger_audio details: {e}")
        return None   

def save_photo_to_db(photo_path):
    conn = get_db_connection()
    
    if conn is None:
        return
    
    trg_image = trigger_video_details(photo_path)

    try:
        cursor = conn.cursor()
        
        # triggers 테이블에 값 저장
        photo_name = os.path.basename(photo_path)
        
        if 'delivery_' in photo_name :
            trg_type = '택배 및 배달'
            trg_info = '(딩동) 택배/배달음식이 도착했습니다~!'
        else :
            trg_type =None
            trg_info = None
            
        query = """
        INSERT INTO triggers (user_id, trg_type,  trg_info, trg_image)
        VALUES ('smhrd1', %s, %s, %s)
        """
        cursor.execute(query, (trg_type, trg_info, trg_image))
    
        conn.commit()
        print("Data saved to database successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error saving to database: {err}")

def save_video_to_db(file_path, photo_path):
    """db 저장 : 비디오 및 트리거 테이블 """
    
    conn = get_db_connection()
    if conn is None:
        return
    video_name, video_size, video_ext, video_length, video_path = extract_video_details(file_path)
    trg_image = trigger_video_details(photo_path)
    
    try:
        cursor = conn.cursor()
    
        query = """
        INSERT INTO videos (video_name, video_size, video_ext, video_length, user_id, video_path)
        VALUES (%s, %s, %s, %s, 'smhrd1',%s)
        """
        cursor.execute(query, (video_name, video_size, video_ext, video_length, video_path))
    
        # triggers 테이블에 값 저장
        query = """
        SELECT video_idx FROM videos WHERE video_name= %s 
        """
        cursor.execute(query, (video_name,))
        video_idx_db = cursor.fetchone()
        
        if video_idx_db is None:
            print("Error: Video index not found.")
            return
        
        video_idx_db = video_idx_db[0]  # 튜플에서 첫 번째 값만 가져옴

        photo_name = os.path.basename(photo_path)
            
        print("photo_name",photo_name)
        if 'hand_in_roi_' in photo_name:
            trg_type = '이상탐지 도어락'
            trg_info = '누군가 도어락을 잡았습니다...'
        elif 'person_30sec_' in photo_name:
            trg_type = '이상탐지 30초'
            trg_info = '어떤사람 30초 이상 문 앞에 머물렀습니다...'
        else :
            trg_type = None
            trg_info = None
            
        query = """
        INSERT INTO triggers (user_id, trg_type,  trg_info, trg_image, video_idx)
        VALUES ('smhrd1', %s, %s, %s, %s)
        """
        cursor.execute(query, (trg_type, trg_info, trg_image, video_idx_db))
    
        conn.commit()
        print("Data saved to database successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error saving to database: {err}")
        
    finally:
        # 쿼리 실행 후 커서 닫기 전에 항상 결과를 모두 읽어야 합니다.
        cursor.fetchall() # 결과가 있을 경우 모두 읽어들입니다.
        cursor.close()
        conn.close()