import os
import wave
import mysql.connector
from config import DB_HOST,DB_PASSWORD,DB_NAME,DB_PORT,DB_USER

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

# def trigger_audio_details(file_path):
#     """오디오관련 트리거 데이터 """
#     try:
#         trg_type = "위급상황-불법침입"
#         trg_info = "현관 문 앞에서 특정 키워드의 소리가 감지되었습니다."
        
#         # trg_image 값 추출
#         trg_image = file_path
        
#         video_idx = 1
      
#         return trg_type, trg_info, trg_image, video_idx
    
#     except Exception as e:
#         print(f"Error trigger_audio details: {e}")
#         return None, None, None, None   
              

def save_audio_to_db(file_path):
    """db 저장 : 오디오 및 트리거 테이블 """
    conn = get_db_connection()
    if conn is None:
        return
    audio_name, audio_size, audio_ext, audio_length = extract_audio_details(file_path)
    #trg_type, trg_info, trg_image, video_idx = trigger_audio_details(file_path)
    
    try:
        cursor = conn.cursor()
        
        # audio 테이블에 값 저장
        query = """
        INSERT INTO audios (audio_name, audio_size, audio_ext, audio_length, user_id)
        VALUES (%s, %s, %s, %s, 'smhrd1')
        """
        cursor.execute(query, (audio_name, audio_size, audio_ext, audio_length))
        
        # # triggers 테이블에 값 저장
        # query = """
        # SELECT audio_idx FROM audios WHERE audio_name= %s 
        # """
        # cursor.execute(query, (audio_name,))
        # audio_idx_db = cursor.fetchone()
        
        # query = """
        # INSERT INTO triggers (user_id, trg_type, trg_info, trg_image, video_idx, audio_idx)
        # VALUES ('smhrd1', %s, %s, %s, %s, %s)
        # """
        # cursor.execute(query, (trg_type, trg_info, trg_image, video_idx, audio_idx_db))
        
        conn.commit()
        print("Data saved to database successfully.")
    except mysql.connector.Error as err:
        print(f"Error saving to database: {err}")
    finally:
        cursor.close()
        conn.close()


################################################# 비디오 관련(트리거 포함) #####################################################    
# def extract_video_details(file_path):
#     """ 비디오 데이터 추출 """
#     try:
#         # audio db 값들 추출하기
#         video_name = os.path.basename(file_path)
#         video_size = os.path.getsize(file_path) 
#         video_ext = os.path.splitext(file_path)[1] 

#         # video_length
#         with wave.open(file_path, "rb") as wf:
#             n_frames = wf.getnframes() 
#             frame_rate = wf.getframerate() 
#             video_length = n_frames / float(frame_rate)  # Length in seconds

#         return video_name, video_size, video_ext, video_length
    
#     except Exception as e:
#         print(f"Error extracting _video details: {e}")
#         return None, None, None, None              

# def trigger_video_details(file_path):
#     """비디오관련 트리거 데이터 """
#     try:
#         trg_type = "위급상황-불법침입"   # 객체나 리스트 사용해야할듯. 
#         trg_info = "현관 문 앞에서 특정 키워드의 소리가 감지되었습니다." # 객체나 리스트 사용해야할듯. 
        
#         # trg_image 값 추출
#         trg_image = file_path
      
#         return trg_type, trg_info, trg_image
    
#     except Exception as e:
#         print(f"Error trigger_audio details: {e}")
#         return None, None, None, None   

# def save_video_to_db(file_path):
#     """db 저장 : 비디오 및 트리거 테이블 """
    
#     conn = get_db_connection()
#     if conn is None:
#         return
#     video_name, video_size, video_ext, video_length = extract_video_details(file_path)
#     #trg_type, trg_info, trg_image = trigger_video_details(file_path)
    
#     try:
#         cursor = conn.cursor()
        
#         query = """
#         INSERT INTO videos (video_name, video_size, video_ext, video_length, user_id)
#         VALUES (%s, %s, %s, %s, 'smhrd1')
#         """
#         cursor.execute(query, (video_name, video_size, video_ext, video_length))
        
#         # # triggers 테이블에 값 저장
#         # query = """
#         # SELECT video_idx FROM videos WHERE video_name= %s 
#         # """
#         # cursor.execute(query, (video_name,))
#         # video_idx_db = cursor.fetchone()
        
#         # query = """
#         # INSERT INTO triggers (user_id, trg_type, trg_info, trg_image, video_idx)
#         # VALUES ('smhrd1', %s, %s, %s, %s)
#         # """
#         # cursor.execute(query, (trg_type, trg_info, trg_image, video_idx_db))
        
#         conn.commit()
#         print("Data saved to database successfully.")
#     except mysql.connector.Error as err:
#         print(f"Error saving to database: {err}")
#     finally:
#         cursor.close()
#         conn.close()