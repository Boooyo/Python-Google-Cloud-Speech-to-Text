## Audio Transcription Pipeline

###### 이 저장소는 오디오 파일을 처리하여 WAV 형식으로 변환하고, Google Cloud Speech-to-Text API를 사용하여 텍스트로 변환한 후 결과를 파일에 저장하는 스크립트를 포함하고 있습니다.

## 프로젝트 디렉토리 구조

```
audio-transcription-pipeline/
├── audio_files/               # 원본 오디오 파일을 저장하는 디렉토리
├── transcriptions/            # 생성된 텍스트 파일을 저장하는 디렉토리
├── transcribe.py              # 메인 스크립트 파일
├── requirements.txt           # 필요한 Python 패키지 리스트
├── README.md                  # 리드미 파일
└── .env                       # 환경 변수 파일 (선택 사항)

```
## transcriptions/ 디렉토리 설명

>transcriptions/: 오디오 파일을 텍스트로 변환한 결과를 저장하는 디렉토리입니다. 이 디렉토리는 transcribe.py 스크립트가 실행될 때 자동으로 생성됩니다. 생성된 각 텍스트 파일은 오디오 파일의 이름과 동일하며 .txt 확장자를 갖습니다.

##### transcriptions/ 디렉토리는 다음 코드에서 자동으로 생성됩니다:


```
def main():
    check_environment_variable('GOOGLE_APPLICATION_CREDENTIALS')

    audio_dir = check_environment_variable('AUDIO_DIR', './audio_files')
    output_dir = check_environment_variable('OUTPUT_DIR', './transcriptions')
    os.makedirs(output_dir, exist_ok=True)  # output_dir 디렉토리가 존재하지 않으면 생성

    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(('wav', 'mp3', 'flac', 'm4a'))]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_audio_file, audio_path, os.path.join(output_dir, os.path.basename(audio_path).rsplit('.', 1)[0] + '.txt')) for audio_path in audio_files]
        for future in concurrent.futures.as_completed(futures):
            future.result()
```

위 코드에서 os.makedirs(output_dir, exist_ok=True) 부분이 transcriptions/ 디렉토리를 자동으로 생성합니다.

따라서, 프로젝트 디렉토리 구조를 설정하고 transcribe.py 스크립트를 실행하면, transcriptions/ 디렉토리가 자동으로 생성되고, 그 안에 변환된 텍스트 파일들이 저장됩니다.

## 요구 사항

- Python 3.6+
- 시스템 경로에 설치된 ffmpeg
- Google Cloud SDK 설치 및 Speech-to-Text API 활성화
- requirements.txt 파일에 명시된 Python 패키지

## 설치

##### 저장소를 클론합니다:


```
git clone https://github.com/your-repo/audio-transcription-pipeline.git
cd audio-transcription-pipeline
```

##### 필요한 Python 패키지를 설치합니다:


```
pip install -r requirements.txt
```

##### Google Cloud 인증 설정:
##### Google Cloud 프로젝트에서 Speech-to-Text API를 활성화하고 서비스 계정 키 JSON 파일을 다운로드합니다. 이 JSON 파일의 경로를 환경 변수로 설정합니다:

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
```

##### 환경 변수를 설정합니다:
- AUDIO_DIR: 변환할 오디오 파일이 있는 디렉토리. 기본값은 ./audio_files입니다.
- OUTPUT_DIR: 텍스트 파일이 저장될 디렉토리. 기본값은 ./transcriptions입니다.
##### 이 변수들을 쉘에서 설정하거나 프로젝트 디렉토리에 .env 파일을 생성하여 설정할 수 있습니다:

```
export AUDIO_DIR="./audio_files"
export OUTPUT_DIR="./transcriptions"
```

## 사용법

##### 오디오 파일 준비:

##### 오디오 파일을 AUDIO_DIR 환경 변수로 지정된 디렉토리에 배치합니다. 지원되는 형식은 wav, mp3, flac, m4a입니다.

##### 스크립트 실행:

```
python transcribe.py
```

##### 스크립트는 다음 작업을 수행합니다:

- 오디오 파일을 WAV 형식으로 변환합니다(이미 WAV 형식인 경우 제외).
- WAV 파일이 모노 PCM 형식인지 확인합니다.
- Google Cloud Speech-to-Text API를 사용하여 오디오 파일의 음성을 텍스트로 변환합니다.
- 변환된 텍스트를 OUTPUT_DIR 환경 변수로 지정된 디렉토리에 저장합니다.

## 로깅

##### 스크립트는 진행 상황과 오류를 콘솔에 기록합니다. 기본 로깅 레벨은 INFO로 설정되어 있으며 필요에 따라 조정할 수 있습니다.

## 코드 개요

##### 환경 변수 확인

```
def check_environment_variable(var_name, default_value=None):
    ...

```
##### 오디오 변환

```
def convert_to_wav(audio_path):
    ...
```

##### 오디오 파일 읽기


```
def read_audio_file(audio_path):
    ...
```

##### 오디오 파일 형식 검증


```
def validate_audio_file_format(audio_path):
    ...
```

##### 음성 인식

```
def transcribe_speech(content, language_code="ko-KR", sample_rate_hertz=16000):
    ...
```

##### 텍스트 파일 저장

```
def save_transcription_to_file(response, output_path):
    ...
```

##### 오디오 파일 처리


```
def process_audio_file(audio_path, output_path):
    ...
```

## 라이선스

##### 이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

##### 자세한 내용은 Google Cloud Speech-to-Text 문서를 참조하세요.
