# CleanTempMail API — Python 예제

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

[CleanTempMail API](https://cleantempmail.com/ko/api)의 공식 예제와 재사용 가능한 클라이언트입니다. 자신의 애플리케이션 테스트에서 임시 주소 생성, 메일 수신, 인증 코드 추출, 첨부 파일 다운로드에 사용할 수 있습니다.

**Python 3.10 이상 · 표준 라이브러리만 사용 · MIT 라이선스**

## 설정
```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

PowerShell에서는 `$env:CLEANTEMPMAIL_API_KEY = 'YOUR_API_KEY'`를 사용하세요. 비동기 예제도 별도 패키지를 설치할 필요가 없습니다. 기본 URL은 `https://cleantempmail.com/api`이며, 자체 서버는 `CLEANTEMPMAIL_BASE_URL`로 지정할 수 있습니다. 로컬 개발 외에는 HTTPS를 사용하세요. 스크립트는 환경 변수만 읽고 `.env` 파일을 자동으로 로드하지 않습니다. [.env.example](.env.example)을 참고하세요.

## 키와 사용량

- [API 페이지](https://cleantempmail.com/ko/api)에서 키를 구매하세요. 고정된 총 요청량을 한 번 결제하며 자동 갱신이나 추가 충전은 없습니다. 현재 가격은 웹사이트에서 확인하세요.
- 환경 변수를 설정하지 않으면 `ct-test`를 사용합니다. 모두가 한도를 공유하는 제한된 테스트 키이므로 이미 소진되었을 수 있습니다. 프로덕션용이 아니며 API가 무료 또는 무제한이라는 뜻도 아닙니다.
- 키는 `X-API-Key` 헤더로 전송합니다. Git, URL, 로그 등에 키를 넣지 마세요. 클라이언트는 리디렉션을 거부합니다.
- 인증된 보호 API 요청마다 1회가 차감됩니다. 빈 받은 편지함 조회, 생성, 본문 읽기, 첨부 다운로드, 삭제와 키를 사용하는 통계 조회도 포함됩니다. 처리 전에 차감하므로 실패나 재시도도 사용량을 소모할 수 있습니다.
- `get_usage()`는 사용량을 차감하지 않습니다. 공개 API인 `get_domains()`는 키를 보내지 않습니다. 이 클라이언트의 통계 메서드는 키를 전송하므로 차감됩니다.
- `remaining_total`은 총 잔여량, `remaining_today`는 오늘의 잔여량입니다. limit이 `0`, remaining이 `-1`이면 해당 사용량 한도가 없다는 뜻이지만 요청 빈도와 동시 실행 제한은 유지됩니다. `Retry-After`를 따르세요.

## 사용 예시
```python
from cleantempmail import CleanTempMailClient

client = CleanTempMailClient.from_env()
print(client.get_usage())
address = client.generate_email()
print(address)
message = client.wait_for_email(address, timeout=120, interval=10)
if message:
    full = client.get_email(message["id"])
    print(full["subject"], full["content"])
```

대기는 즉시 편지함을 확인하고 이미 도착한 메일도 포함합니다. 기존 메일을 제외하려면 `seen_ids={...}`, 조건을 지정하려면 `predicate=lambda message: ...`를 전달하세요. 결과는 요약이며, 시간 내에 메일이 없으면 `None`을 반환하고 복구할 수 없는 API 오류는 예외를 발생시킵니다. `summary=1`은 짧은 미리보기와 함께 최근 최대 100개, 일반 `get_emails(address)`는 전체 내용이 있는 최근 최대 500개를 반환합니다. 영구 보관함이 아닙니다.

## 예제 파일
| Python | |
| --- | --- |
| [demo.py](demo.py) | 기본 데모. 기다리려면 `--wait` 추가 |
| [01_generate_email.py](01_generate_email.py) | 무작위 주소 생성 |
| [02_custom_email.py](02_custom_email.py) | 사용자 지정 접두사와 활성 도메인 |
| [03_receive_email.py](03_receive_email.py) | 편지함의 전체 메일 조회 |
| [04_auto_polling.py](04_auto_polling.py) | 시간 제한을 두고 10초마다 조회 |
| [05_delete_email.py](05_delete_email.py) | `--yes`로 메일 1개 삭제 |
| [06_clear_inbox.py](06_clear_inbox.py) | `--yes`로 편지함 비우기 |
| [07_statistics.py](07_statistics.py) | 통계 조회: 요청 5회 |
| [08_async_client.py](08_async_client.py) | `asyncio.to_thread`로 주소 3개 생성 |
| [09_verification_code.py](09_verification_code.py) | 코드 추출 및 `--keyword` 필터 |
| [10_multiple_addresses.py](10_multiple_addresses.py) | 여러 주소 생성 및 조회 |
| [11_key_usage.py](11_key_usage.py) | 차감 없이 키 사용량 확인 |
| [12_download_attachment.py](12_download_attachment.py) | 지정 경로에 다운로드, 덮어쓰기 금지 |
| [13_list_domains.py](13_list_domains.py) | 공개 도메인 페이지 조회, `--query` 필터 |

## 오류 처리와 안전

`APIError`에는 `status`, `message`, `usage`, `retry_after`, `quota_exhausted`가 있습니다. `TransportError`는 네트워크 오류나 시간 초과를 나타냅니다. 요청 실패를 빈 편지함으로 표시하지 않습니다. 기본 HTTP 시간 제한은 15초입니다.

400은 입력 수정, 401은 키 확인, 403은 비공개 편지함 접근 중단, 404는 없거나 만료된 ID 갱신, 409는 활성 도메인 재선택이 필요합니다. 429는 사용량 소진과 일시적인 빈도 제한을 구분하세요. 5xx는 일시적 장애일 수 있습니다. 일반 요청은 자동 재전송하지 않습니다. 폴링만 대기 시간을 늘리고 `Retry-After`를 따르며, 연속 3회 실패하거나 재시도할 시간이 부족하면 예외를 발생시킵니다. 재시도도 사용량을 소모할 수 있습니다.

사용자 지정 생성은 JSON POST를 사용합니다. 지정한 도메인을 사용할 수 없으면 409를 반환하며 다른 주소로 자동 변경하지 않습니다. GPTMail의 비공개 도메인은 이 API로 접근할 수 없습니다. 첨부 응답은 JSON이 아닌 바이트이며 오류는 일반 텍스트일 수 있습니다. 삭제 스크립트에는 `--yes`가 필요합니다. 코드 추출은 추정에 기반하므로 메일 형식에 맞게 조정하세요. HTML은 로컬에서 텍스트로 분석하며 외부 이미지를 로드하지 않습니다.

전체 엔드포인트와 JSON 필드는 [영문 참조](README.md#http-api-reference) 및 [API 문서](https://cleantempmail.com/ko/api)를 참고하세요. [QUICK_START.md](QUICK_START.md)와 [CONTRIBUTING.md](CONTRIBUTING.md)도 제공합니다.

## 검증
```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

테스트는 로컬 모의 API와 가상 메일을 사용합니다. GitHub Actions는 프로덕션 키 없이 Python 3.10–3.14를 검사합니다.
