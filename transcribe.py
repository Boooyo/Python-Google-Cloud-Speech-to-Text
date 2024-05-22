import os
import io
import wave
import logging
import concurrent.futures
from google.cloud import speech_v1p1beta1 as speech
import subprocess

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_environment_variable(var_name, default_value=None):
    value = os.getenv(var_name, default_value)
    if not value:
        logging.error(f"The {var_name} environment variable is not set.")
        exit(1)
    return value

def convert_to_wav(audio_path):
    wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
    try:
        subprocess.run(['ffmpeg', '-i', audio_path, wav_path], check=True)
        return wav_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting file to WAV: {e}")
        return None

def read_audio_file(audio_path):
    try:
        with io.open(audio_path, "rb") as audio_file:
            return audio_file.read()
    except IOError as e:
        logging.error(f"Error reading audio file: {e}")
        return None

def validate_audio_file_format(audio_path):
    try:
        with wave.open(audio_path, 'rb') as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                logging.error("Audio file must be WAV format mono PCM.")
                return False
    except wave.Error as e:
        logging.error(f"Error reading audio file format: {e}")
        return False
    return True

def transcribe_speech(content, language_code="ko-KR", sample_rate_hertz=16000):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    try:
        return client.recognize(config=config, audio=audio)
    except Exception as e:
        logging.error(f"Error during speech recognition: {e}")
        return None

def save_transcription_to_file(response, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                logging.info(f"Transcript: {transcript}")
                output_file.write(f"{transcript}\n")
    except IOError as e:
        logging.error(f"Error writing to output file: {e}")

def process_audio_file(audio_path, output_path):
    wav_path = convert_to_wav(audio_path)
    if not wav_path:
        return

    if not validate_audio_file_format(wav_path):
        return

    content = read_audio_file(wav_path)
    if content is None:
        return

    response = transcribe_speech(content)
    if response is not None:
        save_transcription_to_file(response, output_path)

def main():
    check_environment_variable('GOOGLE_APPLICATION_CREDENTIALS')

    audio_dir = check_environment_variable('AUDIO_DIR', './audio_files')
    output_dir = check_environment_variable('OUTPUT_DIR', './transcriptions')
    os.makedirs(output_dir, exist_ok=True)

    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(('wav', 'mp3', 'flac', 'm4a'))]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_audio_file, audio_path, os.path.join(output_dir, os.path.basename(audio_path).rsplit('.', 1)[0] + '.txt')) for audio_path in audio_files]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
