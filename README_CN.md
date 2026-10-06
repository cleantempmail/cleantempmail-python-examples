# CleanTempMail API — Python 示例

[English](README.md) | 简体中文 | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

[CleanTempMail API](https://cleantempmail.com/zh/api) 官方示例与可复用客户端：为自己的应用测试生成临时地址、收取邮件、提取验证码和下载附件。

**Python 3.10+ · 全部使用标准库 · MIT 许可证**

## 开始使用

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

PowerShell 设置方式：`$env:CLEANTEMPMAIL_API_KEY = 'YOUR_API_KEY'`。
包括异步示例在内，都不需要安装第三方依赖。默认地址是 `https://cleantempmail.com/api`；自部署服务可用 `CLEANTEMPMAIL_BASE_URL` 修改，本地开发以外请使用 HTTPS。见 [.env.example](.env.example)：脚本读取环境变量，**不会自动加载 `.env` 文件**。

## Key、付费和额度

- 在[API 页面](https://cleantempmail.com/zh/api)购买 Key。购买的是一次性固定总请求额度，没有自动续费，也不能充值；套餐和价格以网站当前信息为准。
- 未设置环境变量时，示例使用 `ct-test`。这是**所有人共享的限额测试 Key**，可能已经用完，不能用于生产，也不代表 API 完全免费或无限调用。
- Key 只放在 `X-API-Key` 请求头。不要写进代码、Git、URL、日志或截图。客户端拒绝重定向，避免把 Key 转发给其他网站。
- 每次通过 Key 鉴权的受保护请求消耗 **1 次额度**：生成地址、查询空收件箱、读取邮件、下载附件、删除、清空，以及带 Key 的统计查询均计费。额度在执行接口前扣除，因此失败或重试也可能扣费。
- `POST /api/api-key/usage` 查询余额不扣额度；`GET /api/domains` 是公开接口，客户端不在该请求中发送 Key。统计接口也支持匿名访问，但本客户端的统计方法携带 Key，所以会扣额度。
- `remaining_total` 是总余额，`remaining_today` 是当日余额。对应的 limit 为 `0`、remaining 为 `-1` 时表示该维度不限额，仍受频率和并发限制。
- 频率限制与余额不同，服务器可调整，可能同时按 Key 和来源 IP 限制；收到 `Retry-After` 应等待，不要认为付费 Key 没有限流。

## 最小示例

```python
from cleantempmail import CleanTempMailClient

client = CleanTempMailClient.from_env()
print(client.get_usage())                   # 不扣额度
address = client.generate_email()           # 扣 1 次
print(address)                              # 向这个地址发送测试邮件
message = client.wait_for_email(address, timeout=120, interval=10)
if message:
    full = client.get_email(message["id"])   # 再扣 1 次
    print(full["subject"], full["content"])
print(client.last_usage)                    # 最近一次计费 JSON 响应的额度快照
```

等待方法先立即查询，再按间隔轮询；默认包含已经到达的邮件，避免开始等待前到达的邮件被漏掉。可传 `seen_ids={...}` 忽略旧邮件，用 `predicate=lambda message: ...` 按主题或发件人筛选。返回的是**摘要**，完整正文用 `get_email(id)` 获取。正常超时未收到邮件返回 `None`，不可恢复的接口失败会抛出异常。

轮询使用 `summary=1`，返回最近最多 100 封邮件的简短预览；普通 `get_emails(address)` 返回最近最多 500 封完整邮件。邮件会按服务保留策略过期，不能作为永久归档。

## 可运行的示例

| 文件 | 用途 / 命令 |
| --- | --- |
| [demo.py](demo.py) | 最小演示；需要等待邮件时加 `--wait`，默认不轮询、不删除 |
| [01_generate_email.py](01_generate_email.py) | 随机生成一个地址 |
| [02_custom_email.py](02_custom_email.py) | `python3 02_custom_email.py --prefix qa.user`；从有效域名中选择 |
| [03_receive_email.py](03_receive_email.py) | `python3 03_receive_email.py 'ADDRESS'`；查询完整邮件 |
| [04_auto_polling.py](04_auto_polling.py) | `python3 04_auto_polling.py 'ADDRESS' --timeout 120 --interval 10` |
| [05_delete_email.py](05_delete_email.py) | `python3 05_delete_email.py 'MESSAGE_ID' --yes`；永久删除一封 |
| [06_clear_inbox.py](06_clear_inbox.py) | `python3 06_clear_inbox.py 'ADDRESS' --yes`；永久清空 |
| [07_statistics.py](07_statistics.py) | 概览、小时分布、主题/域名/发件人排名，共 5 次请求 |
| [08_async_client.py](08_async_client.py) | 用标准库 `asyncio.to_thread` 并发生成 3 个地址 |
| [09_verification_code.py](09_verification_code.py) | `python3 09_verification_code.py 'ADDRESS' --keyword verification` |
| [10_multiple_addresses.py](10_multiple_addresses.py) | `python3 10_multiple_addresses.py --count 3`；创建并分别查询 |
| [11_key_usage.py](11_key_usage.py) | 查询 Key 状态、每日额度和总余额 |
| [12_download_attachment.py](12_download_attachment.py) | `python3 12_download_attachment.py 'MESSAGE_ID' 'ATTACHMENT_ID' ./receipt.pdf` |
| [13_list_domains.py](13_list_domains.py) | 分页列出当前公开有效域名，可加 `--query` |
| [example_client.py](example_client.py) | 可复用客户端示例 |

删除脚本必须加 `--yes`，否则不发送请求。附件使用明确指定的保存路径，不使用邮件提供的文件名，也不覆盖已有文件。验证码提取是启发式规则，需要按自己的邮件格式校准；HTML 仅本地解析成文字，不加载远程图片等资源。

## 接口对应关系

所有路径相对于 `https://cleantempmail.com/api`。JSON 接口成功返回 `success: true` 与 `data`，失败返回 `success: false` 与 `error`，受保护响应可能附带 `usage`。列表在 `data.emails`，数量在 `data.count`。邮件使用 `id`、`email_address`、`from_address`、`subject`、`content`、`html_content`、`has_html`、Unix 秒时间戳 `timestamp` 和可选的附件元数据。

| 方法 | 路径 | 客户端方法 |
| --- | --- | --- |
| GET | `/domains?q=...&limit=1000&offset=0` | `get_domains()`，返回域名和分页信息 |
| GET / POST | `/generate-email` | `generate_email(prefix=None, domain=None)` |
| GET | `/emails?email=...` | `get_emails(address, summary=False)` |
| GET | `/email/{id}` | `get_email(id)` |
| GET | `/email/{id}/attachment/{attachmentID}` | `download_attachment(id, attachment_id)`，返回 bytes |
| DELETE | `/email/{id}` | `delete_email(id)` |
| DELETE | `/emails/clear?email=...` | `clear_inbox(address)`，返回删除数量 |
| POST | `/api-key/usage` | `get_usage()`，不扣额度 |
| GET | `/stats` | `get_statistics()` |
| GET | `/statistics/24h` | `get_24h_distribution()` |
| GET | `/statistics/top-subjects` | `get_top_subjects(limit=10)` |
| GET | `/statistics/top-domains` | `get_top_domains(limit=10)` |
| GET | `/statistics/top-senders` | `get_top_senders(limit=10)` |

自定义地址使用 JSON POST：`{"prefix":"qa.user","domain":"ACTIVE_DOMAIN"}`。域名可能失效，请先查询有效列表，不要固定使用旧域名。指定域名不可用时返回 **409**，不会自动换成另一个域名。GPTMail 私有域名不可通过此 API 访问。也可在本地用合法前缀和有效公开域名拼接地址，省去生成请求，但这不会预留或私有化收件箱。

附件响应是文件字节，不是 JSON；失败可能返回纯文本。附件 ID 来自完整邮件的 `attachments[].id`。不要自动访问邮件中的链接或执行附件。

## 错误与轮询

客户端提供 `APIError`、`TransportError`，前者包含 `status`、`message`、`usage`、`retry_after` 和 `quota_exhausted`。失败不会被伪装成空收件箱，命令行脚本会以非零状态退出。

- 400：修正请求，不原样重试。
- 401：Key 缺失、无效或停用，检查凭据。
- 403：私有或禁止访问的收件箱，不继续重试。
- 404：邮件或附件不存在、过期，刷新 ID。
- 409：指定域名不可用，重新选择有效域名。
- 429：区分余额耗尽与临时限流。余额耗尽立即停止；临时限流按 `Retry-After` 退避。
- 5xx / 网络超时：可以有限重试，但每次重试也可能扣费。

`CleanTempMailClient(key, timeout=15)` 设置 HTTP 超时。普通请求只调用一次，不自动重放生成或删除操作。轮询对临时 429/500/502/503/504 和网络故障退避，连续失败 3 次或没有足够时间重试时抛出异常；单次请求超时受总等待期限约束。HTTP 重定向不会被跟随。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

测试使用本地模拟 API 和虚构邮件，无需生产 Key。GitHub Actions 检查 Python 3.10–3.14。贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

[网站](https://cleantempmail.com) · [当前 API 文档和价格](https://cleantempmail.com/zh/api) · [问题反馈](https://github.com/cleantempmail/cleantempmail-python-examples/issues) · [MIT 许可证](LICENSE)
