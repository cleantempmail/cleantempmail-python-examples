# CleanTempMail API - Python 示例

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README.md) | 简体中文

[CleanTempMail](https://cleantempmail.com) 官方 Python 示例 - 免费临时邮箱服务，强大的 API 接口。

## 🚀 特性

- **即时生成**临时邮箱
- **实时接收**邮件
- 每个地址可获取**最近 500 封邮件**
- **统计 API** 用于数据分析
- **完全免费** - 慷慨的速率限制

## 📦 安装

无需外部依赖！所有示例仅使用 Python 标准库。

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
```

异步示例（可选）：
```bash
pip install -r requirements.txt
```

## 🔑 API 密钥

在 [CleanTempMail API](https://cleantempmail.com/api) 获取免费 API 密钥

测试密钥：`ct-test`

## 📚 示例

### 基础示例

| 文件 | 说明 |
|------|------|
| [`01_generate_email.py`](01_generate_email.py) | 生成随机临时邮箱 |
| [`02_custom_email.py`](02_custom_email.py) | 创建自定义前缀邮箱 |
| [`03_receive_email.py`](03_receive_email.py) | 接收和阅读邮件 |
| [`04_auto_polling.py`](04_auto_polling.py) | 自动轮询新邮件 |
| [`05_delete_email.py`](05_delete_email.py) | 删除指定邮件 |
| [`06_clear_inbox.py`](06_clear_inbox.py) | 清空收件箱 |

### 高级示例

| 文件 | 说明 |
|------|------|
| [`07_statistics.py`](07_statistics.py) | 获取系统统计 |
| [`08_async_client.py`](08_async_client.py) | 异步 API 客户端 |
| [`09_verification_code.py`](09_verification_code.py) | 提取验证码 |
| [`10_multiple_addresses.py`](10_multiple_addresses.py) | 管理多个邮箱 |

### 工具类

| 文件 | 说明 |
|------|------|
| [`cleantempmail.py`](cleantempmail.py) | 可复用的 Python 客户端类 |
| [`example_client.py`](example_client.py) | 客户端类使用示例 |

## 🎯 快速开始

```python
import requests

# 配置
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# 生成邮箱
response = requests.get(
    f"{BASE_URL}/generate-email",
    headers={"X-API-Key": API_KEY}
)
email = response.json()["data"]["email"]
print(f"✅ 已生成: {email}")

# 等待邮件
import time
time.sleep(10)

# 获取邮件
response = requests.get(
    f"{BASE_URL}/emails",
    params={"email": email},
    headers={"X-API-Key": API_KEY}
)
emails = response.json()["data"]["emails"]
print(f"📧 收到 {len(emails)} 封邮件")
```

## 📖 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/generate-email` | GET/POST | 生成临时邮箱 |
| `/api/emails` | GET | 获取邮件列表 |
| `/api/email/{id}` | GET | 获取单封邮件 |
| `/api/email/{id}` | DELETE | 删除邮件 |
| `/api/emails/clear` | DELETE | 清空所有邮件 |
| `/api/stats` | GET | 系统统计 |
| `/api/statistics/24h` | GET | 24小时分布 |
| `/api/statistics/top-subjects` | GET | 热门主题 |
| `/api/statistics/top-domains` | GET | 热门域名 |
| `/api/statistics/top-senders` | GET | 热门发件人 |

## 🔧 使用场景

- **测试** - 测试邮箱验证流程
- **自动化** - 自动化注册流程
- **隐私** - 保护真实邮箱
- **开发** - 无需 SMTP 测试邮件功能
- **QA** - 验证邮件送达

## 📝 许可证

MIT 许可证 - 可自由用于您的项目！

## 🌐 链接

- 🌍 网站：[cleantempmail.com](https://cleantempmail.com)
- 📚 API 文档：[cleantempmail.com/api](https://cleantempmail.com/api)
- 💬 问题反馈：[GitHub Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues)

## ⭐ 给个星星！

如果觉得有用，请给仓库加星！

---

用 ❤️ 制作 by [CleanTempMail](https://cleantempmail.com)
