# CleanTempMail API — Python サンプル

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

[CleanTempMail API](https://cleantempmail.com/ja/api) の公式サンプルと再利用可能なクライアントです。自分のアプリケーションのテストで、一時アドレスの作成、メール受信、認証コード抽出、添付ファイルのダウンロードを行えます。

**Python 3.10 以降 · 標準ライブラリのみ · MIT ライセンス**

## セットアップ
```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

PowerShell では `$env:CLEANTEMPMAIL_API_KEY = 'YOUR_API_KEY'` を使用します。非同期サンプルを含め、追加パッケージのインストールは不要です。既定の URL は `https://cleantempmail.com/api` です。自分のサーバーを使う場合は `CLEANTEMPMAIL_BASE_URL` で変更できます。ローカル開発以外では HTTPS を使用してください。環境変数を読み取るだけで、`.env` ファイルは自動では読み込みません。[.env.example](.env.example) を参照してください。

## API キーと利用枠

- [API ページ](https://cleantempmail.com/ja/api) でキーを購入できます。固定の総リクエスト枠を一度だけ購入する方式で、自動更新や追加チャージはありません。最新の価格はサイトで確認してください。
- 環境変数がない場合は `ct-test` を使用します。全員で利用枠を共有する制限付きのテストキーで、すでに使い切られている場合があります。本番環境用ではなく、API が無料・無制限という意味ではありません。
- キーは `X-API-Key` ヘッダーで送信します。Git、URL、ログなどに保存しないでください。クライアントはリダイレクトを拒否します。
- 認証された保護対象のリクエストは毎回 1 回分を消費します。空の受信箱の確認、生成、本文取得、添付取得、削除、キー付き統計も対象です。処理前に枠を消費するため、失敗や再試行でも消費する場合があります。
- `get_usage()` は枠を消費しません。`get_domains()` は公開 API で、キーを送信しません。このクライアントの統計メソッドはキーを送るため、利用枠を消費します。
- `remaining_total` は総残量、`remaining_today` は当日の残量です。limit が `0`、remaining が `-1` の項目は枠の制限なしですが、頻度・同時実行数の制限はあります。`Retry-After` に従ってください。

## 使用例
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

待機はすぐに受信箱を確認し、すでに届いているメールも対象にします。既存 ID を除くには `seen_ids={...}`、条件を指定するには `predicate=lambda message: ...` を渡します。結果は要約です。期限内に届かなければ `None` を返し、回復できない API エラーは例外になります。`summary=1` は短いプレビュー付きの最新 100 件まで、通常の `get_emails(address)` は完全なメールの最新 500 件までを返します。永続的なアーカイブではありません。

## サンプル一覧
| Python | |
| --- | --- |
| [demo.py](demo.py) | 最小デモ。待機する場合は `--wait` |
| [01_generate_email.py](01_generate_email.py) | ランダムなアドレスを作成 |
| [02_custom_email.py](02_custom_email.py) | 独自のプレフィックスと有効なドメイン |
| [03_receive_email.py](03_receive_email.py) | 受信箱の完全なメールを取得 |
| [04_auto_polling.py](04_auto_polling.py) | 期限付きで 10 秒間隔の確認 |
| [05_delete_email.py](05_delete_email.py) | `--yes` を付けて 1 件削除 |
| [06_clear_inbox.py](06_clear_inbox.py) | `--yes` を付けて受信箱を空にする |
| [07_statistics.py](07_statistics.py) | 統計の取得：5 リクエスト |
| [08_async_client.py](08_async_client.py) | `asyncio.to_thread` で 3 アドレスを作成 |
| [09_verification_code.py](09_verification_code.py) | コード抽出。`--keyword` で絞り込み |
| [10_multiple_addresses.py](10_multiple_addresses.py) | 複数アドレスの作成と確認 |
| [11_key_usage.py](11_key_usage.py) | 利用枠を消費せず残量を確認 |
| [12_download_attachment.py](12_download_attachment.py) | 指定したパスに保存。上書きなし |
| [13_list_domains.py](13_list_domains.py) | 公開ドメインのページ取得。`--query` で絞り込み |

## エラーと安全な利用

`APIError` には `status`、`message`、`usage`、`retry_after`、`quota_exhausted` があります。`TransportError` は接続障害やタイムアウトを表します。失敗を空の受信箱として表示しません。HTTP タイムアウトの既定値は 15 秒です。

400 は入力を修正、401 はキーを確認、403 は非公開受信箱のため中止、404 は期限切れなどの ID を更新、409 は有効なドメインを選び直します。429 は枠の消費と一時的な頻度制限を区別してください。5xx は一時的な障害の可能性があります。通常のリクエストは自動で再送しません。ポーリングのみ段階的に待ち、`Retry-After` を守ります。3 回連続の失敗や再試行の時間が足りない場合は例外になります。再試行も枠を消費する場合があります。

独自アドレスの生成は JSON POST を使います。指定ドメインが無効なら 409 を返し、別アドレスには自動変更しません。GPTMail の非公開ドメインにはアクセスできません。添付の応答は JSON ではなくバイト列で、エラーはテキストの場合があります。削除スクリプトには `--yes` が必要です。コード抽出は推測による処理です。HTML はローカルで文字列として解析し、外部画像を読み込みません。

全エンドポイントと JSON フィールドは[英語のリファレンス](README.md#http-api-reference)と[API ドキュメント](https://cleantempmail.com/ja/api)で確認できます。[QUICK_START.md](QUICK_START.md) と [CONTRIBUTING.md](CONTRIBUTING.md) も参照してください。

## 検証
```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

テストはローカルの模擬 API と架空のメールを使います。GitHub Actions は本番キーなしで Python 3.10–3.14 を確認します。
