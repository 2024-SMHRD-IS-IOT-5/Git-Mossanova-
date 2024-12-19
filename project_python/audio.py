import wave
import os
import numpy as np
import whisper
from datetime import datetime
from send_SNS import send_sns_alert
from db import save_audio_to_db
from config import CHANNELS, RATE, MIC_SENSITIVITY, REFERENCE_PRESSURE, audio_message
import warnings

# FutureWarning 무시
warnings.filterwarnings("ignore", category=FutureWarning)
# Whisper 모델 로드
model = whisper.load_model("small")

def transcribe_audio(buffer, temp_file="temp_stream_audio.wav"):
    """오디오 데이터를 텍스트로 변환"""
    with wave.open(temp_file, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(RATE)
        wf.writeframes(b"".join(buffer))

    try:
        result = model.transcribe(temp_file, language="ko")
        print(result["text"])
        os.remove(temp_file)  # 임시 파일 삭제
        return result["text"].strip()
    except Exception as e:
        with open("audio_errors.log", "a") as log_file:
            log_file.write(f"Error during transcription: {e}\n")
        return None


def calculate_decibel(buffer, noise_threshold):
    """버퍼 데이터를 기반으로 데시벨을 계산"""
    try:
        audio_data = np.frombuffer(b"".join(buffer), dtype=np.int16)
        rms = np.sqrt(np.mean(audio_data ** 2))
        print(f"RMS Value: {rms}, Noise Threshold: {noise_threshold}")  # 디버깅 로그
        
        if rms < noise_threshold:
            print("RMS is below the noise threshold. Returning None.") # 디버깅 로그
            return None
        max_adc_value = 32768
        mic_output_voltage = rms / max_adc_value
        sound_pressure = mic_output_voltage / MIC_SENSITIVITY
        print(f"Sound Pressure: {sound_pressure}")  # 디버깅 로그
        
        decibel = 20 * np.log10(sound_pressure / REFERENCE_PRESSURE) if sound_pressure > 0 else 0
        print(f"Calculated Decibel: {decibel} dB")
        return decibel
    except Exception as e:
        with open("audio_errors.log", "a") as log_file:
            log_file.write(f"Error calculating decibel: {e}\n")
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
            decibel = calculate_decibel(buffer, noise_threshold)
            print(decibel,"db")
            if decibel is None or decibel < decibel_threshold:
                continue  # 데시벨 기준 미달 시 이 키워드를 건너뜀

            keywords_to_notify.append(keyword)
            last_detected[keyword] = now

    if keywords_to_notify:
        send_sns_alert(audio_message)
        saved_file = save_audio_file(buffer, "_".join(keywords_to_notify))
        return transcript, keywords_to_notify, saved_file

    return transcript, None, None

