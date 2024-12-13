import wave
import os
import numpy as np
import whisper
from datetime import datetime
from send_SNS import send_sns_alert
from db import save_audio_to_db

# Whisper 모델 로드
model = whisper.load_model("small")

# Whisper 지연로딩 방법------------
# _model = None
# def get_whisper_model():
#     global _model
#     if _model is None:
#         _model = whisper.load_model("small")
#     return _model
#-----------------------------------------

# 오디오 처리 파라미터
MIC_SENSITIVITY_DB = -32
MIC_SENSITIVITY = 10 ** (MIC_SENSITIVITY_DB / 20)
REFERENCE_PRESSURE = 2e-5
CHANNELS = 1
RATE = 44100


def transcribe_audio(buffer, temp_file="temp_stream_audio.wav"):
    """오디오 데이터를 텍스트로 변환"""
    with wave.open(temp_file, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(RATE)
        wf.writeframes(b"".join(buffer))

    try:
        # whisper 지연로딩 할 때
        #model = get_whisper_model()
        result = model.transcribe(temp_file, language="ko")
        print(result["text"])
        os.remove(temp_file)  # 임시 파일 삭제
        return result["text"].strip()
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def calculate_decibel(buffer, noise_threshold):
    """버퍼 데이터를 기반으로 데시벨을 계산"""
    try:
        audio_data = np.frombuffer(b"".join(buffer), dtype=np.int16)
        rms = np.sqrt(np.mean(audio_data ** 2))
        if rms < noise_threshold:
            return None
        max_adc_value = 32768
        mic_output_voltage = rms / max_adc_value
        sound_pressure = mic_output_voltage / MIC_SENSITIVITY
        return 20 * np.log10(sound_pressure / REFERENCE_PRESSURE) if sound_pressure > 0 else 0
    except Exception as e:
        print(f"Error calculating decibel: {e}")
        return None


def save_audio_file(buffer, identifier, audio_directory = "audio_files"):
    """오디오 데이터를 파일로 저장."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(audio_directory, exist_ok=True)
    file_path = os.path.join(audio_directory, f"audio_{identifier}_{timestamp}.wav")
    
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b"".join(buffer))
    
    print(f"Audio saved as {file_path}")
    save_audio_to_db(file_path)
    return file_path


def detect_keywords(transcript, keywords):
    """텍스트에서 키워드 감지."""
    return [kw for kw in keywords if kw in transcript]

def process_audio(buffer, keywords, last_detected, process_interval, decibel_threshold, noise_threshold):
    """
    오디오 데이터를 처리하여 키워드 탐지, 파일 저장, 및 알림 전송을 수행합니다.
    """
    # 데시벨 계산 , 데시벨 임계값 보다 적으면 무시
    decibel = calculate_decibel(buffer, noise_threshold)
    if decibel is None or decibel < decibel_threshold:
        return None, None, None

    # 텍스트 변환
    transcript = transcribe_audio(buffer)
    if not transcript:
        return None, None, None

    # 키워드 감지
    detected_keywords = detect_keywords(transcript, keywords)

    if not detected_keywords:
        return transcript, None, None  # 키워드가 없는 경우

    now = datetime.now()
    keywords_to_notify = []

    for keyword in detected_keywords:
        if keyword not in last_detected or (now - last_detected[keyword] > process_interval):
            if decibel >= decibel_threshold:
                keywords_to_notify.append(keyword)
                last_detected[keyword] = now

    if keywords_to_notify:
        alert_message = (
            f"위급상황 발생!!\n"
            f"탐지 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"주소: 스마트인재 개발원 301호"
        )
        send_sns_alert(alert_message)
        saved_file = save_audio_file(buffer, "_".join(keywords_to_notify))
        return transcript, keywords_to_notify, saved_file

    return transcript, None, None

