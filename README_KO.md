# CleanTempMail API - Python 예제

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | 한국어 | [Español](README_ES.md)

[CleanTempMail](https://cleantempmail.com) 공식 Python 예제 - 강력한 API가 있는 무료 임시 이메일 서비스.

## 🚀 특징

- **임시 이메일을 즉시 생성**
- **실시간으로 이메일 수신**
- **주소당 최근 500개 이메일 액세스**
- **분석을 위한 통계 API**
- **완전 무료** - 넉넉한 속도 제한

## 📦 설치

외부 종속성 필요 없음! 모든 예제는 Python 표준 라이브러리만 사용합니다.

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
```

## 🔑 API 키

[CleanTempMail API](https://cleantempmail.com/api)에서 무료 API 키 받기

테스트용: `ct-test`

## 🎯 빠른 시작

```python
import requests

API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# 이메일 생성
response = requests.get(
    f"{BASE_URL}/generate-email",
    headers={"X-API-Key": API_KEY}
)
email = response.json()["data"]["email"]
print(f"✅ 생성됨: {email}")
```

## 📚 예제

| 파일 | 설명 |
|------|------|
| [`demo.py`](demo.py) | 🎬 모든 기능의 전체 데모 |
| [`01_generate_email.py`](01_generate_email.py) | 랜덤 임시 이메일 생성 |
| [`02_custom_email.py`](02_custom_email.py) | 사용자 정의 접두사로 이메일 생성 |
| [`03_receive_email.py`](03_receive_email.py) | 수신 이메일 읽기 |
| [`04_auto_polling.py`](04_auto_polling.py) | 새 이메일 자동 폴링 |
| [`09_verification_code.py`](09_verification_code.py) | 인증 코드 추출 |
| [`cleantempmail.py`](cleantempmail.py) | 재사용 가능한 Python 클라이언트 클래스 |
| [`example_client.py`](example_client.py) | 클라이언트 클래스 사용 방법 |

## 🔧 사용 사례

- **테스트** - 이메일 인증 플로우 테스트
- **자동화** - 가입 프로세스 자동화
- **개인정보 보호** - 실제 이메일 보호
- **개발** - SMTP 없이 이메일 기능 테스트
- **QA** - 이메일 전송 확인

## 🌐 링크

- 🌍 웹사이트: [cleantempmail.com](https://cleantempmail.com)
- 📚 API 문서: [cleantempmail.com/api](https://cleantempmail.com/api)
- 💬 Issues: [GitHub Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues)

---

❤️로 제작 by [CleanTempMail](https://cleantempmail.com)
