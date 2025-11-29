# CleanTempMail API - Ejemplos de Python

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | Español

Ejemplos oficiales de Python para [CleanTempMail](https://cleantempmail.com) - un servicio gratuito de correo electrónico temporal con API potente.

## 🚀 Características

- **Generar correos temporales** instantáneamente
- **Recibir correos** en tiempo real
- **Acceder a los 500 correos recientes** por dirección
- **API de estadísticas** para análisis
- **Gratis** - completamente gratis con límites generosos

## 📦 Instalación

¡No se requieren dependencias externas! Todos los ejemplos usan solo la biblioteca estándar de Python.

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
```

## 🔑 Clave API

Obtén tu clave API gratuita en [CleanTempMail API](https://cleantempmail.com/api)

Para pruebas, usa: `ct-test`

## 🎯 Inicio Rápido

```python
import requests

API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# Generar correo
response = requests.get(
    f"{BASE_URL}/generate-email",
    headers={"X-API-Key": API_KEY}
)
email = response.json()["data"]["email"]
print(f"✅ Generado: {email}")
```

## 📚 Ejemplos

| Archivo | Descripción |
|---------|-------------|
| [`demo.py`](demo.py) | 🎬 Demostración completa de todas las funciones |
| [`01_generate_email.py`](01_generate_email.py) | Generar correo temporal aleatorio |
| [`02_custom_email.py`](02_custom_email.py) | Crear correo con prefijo personalizado |
| [`03_receive_email.py`](03_receive_email.py) | Recibir y leer correos entrantes |
| [`04_auto_polling.py`](04_auto_polling.py) | Sondeo automático de nuevos correos |
| [`09_verification_code.py`](09_verification_code.py) | Extraer códigos de verificación |
| [`cleantempmail.py`](cleantempmail.py) | Clase de cliente Python reutilizable |
| [`example_client.py`](example_client.py) | Cómo usar la clase de cliente |

## 🔧 Casos de Uso

- **Pruebas** - Probar flujos de verificación de correo
- **Automatización** - Automatizar procesos de registro
- **Privacidad** - Proteger tu correo real
- **Desarrollo** - Probar funciones de correo sin SMTP
- **QA** - Verificar entrega de correos

## 🌐 Enlaces

- 🌍 Sitio web: [cleantempmail.com](https://cleantempmail.com)
- 📚 Documentación API: [cleantempmail.com/api](https://cleantempmail.com/api)
- 💬 Issues: [GitHub Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues)

---

Hecho con ❤️ por [CleanTempMail](https://cleantempmail.com)
