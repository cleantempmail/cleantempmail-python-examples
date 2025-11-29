# CleanTempMail API - Python サンプル

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | 日本語 | [한국어](README_KO.md) | [Español](README_ES.md)

[CleanTempMail](https://cleantempmail.com) 公式 Python サンプル - 強力な API を備えた無料の一時メールサービス。

## 🚀 機能

- **一時メールアドレスを即座に生成**
- **リアルタイムでメールを受信**
- **アドレスごとに最新500件のメールにアクセス**
- **統計API** で分析
- **完全無料** - 寛大な制限で無料

## 📦 インストール

外部依存関係は不要！すべてのサンプルは Python 標準ライブラリのみを使用します。

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
```

## 🔑 API キー

無料の API キーを [CleanTempMail API](https://cleantempmail.com/api) で取得

テスト用： `ct-test`

## 🎯 クイックスタート

```python
import requests

API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# メールを生成
response = requests.get(
    f"{BASE_URL}/generate-email",
    headers={"X-API-Key": API_KEY}
)
email = response.json()["data"]["email"]
print(f"✅ 生成されました: {email}")
```

## 📚 サンプル

| ファイル | 説明 |
|----------|------|
| [`demo.py`](demo.py) | 🎬 全機能の完全なデモ |
| [`01_generate_email.py`](01_generate_email.py) | ランダムな一時メールを生成 |
| [`02_custom_email.py`](02_custom_email.py) | カスタムプレフィックスでメールを作成 |
| [`03_receive_email.py`](03_receive_email.py) | 受信メールを読む |
| [`04_auto_polling.py`](04_auto_polling.py) | 新しいメールを自動ポーリング |
| [`09_verification_code.py`](09_verification_code.py) | 確認コードを抽出 |
| [`cleantempmail.py`](cleantempmail.py) | 再利用可能な Python クライアントクラス |
| [`example_client.py`](example_client.py) | クライアントクラスの使用方法 |

## 🔧 ユースケース

- **テスト** - メール認証フローをテスト
- **自動化** - サインアッププロセスを自動化
- **プライバシー** - 本物のメールを保護
- **開発** - SMTP なしでメール機能をテスト
- **QA** - メール配信を検証

## 🌐 リンク

- 🌍 ウェブサイト：[cleantempmail.com](https://cleantempmail.com)
- 📚 API ドキュメント：[cleantempmail.com/api](https://cleantempmail.com/api)
- 💬 Issues：[GitHub Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues)

---

❤️ で作成 by [CleanTempMail](https://cleantempmail.com)
