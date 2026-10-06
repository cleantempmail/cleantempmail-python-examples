# CleanTempMail API — Ejemplos de Python

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

Ejemplos oficiales y cliente reutilizable de [CleanTempMail](https://cleantempmail.com/api) para crear direcciones temporales, recibir mensajes, extraer códigos y descargar adjuntos al probar tu propia aplicación.

**Python 3.10+ · solo biblioteca estándar · licencia MIT**

## Instalación
```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

PowerShell: `$env:CLEANTEMPMAIL_API_KEY = 'YOUR_API_KEY'`. No necesitas instalar paquetes, tampoco para el ejemplo asíncrono. La URL predeterminada es `https://cleantempmail.com/api`; puedes cambiarla con `CLEANTEMPMAIL_BASE_URL`. Usa HTTPS fuera del desarrollo local. Los scripts leen variables de entorno; no cargan automáticamente archivos `.env`. Consulta [.env.example](.env.example).

## Claves y cuota

- Compra una clave en la [página API](https://cleantempmail.com/api). Es un pago único por una cuota total fija, sin renovación automática ni recarga. Los precios actuales están en la web.
- Sin la variable de entorno se usa `ct-test`: una clave de prueba limitada que comparte todo el mundo y que puede estar agotada. No sirve para producción ni implica acceso gratuito ilimitado.
- La clave se envía en `X-API-Key`, nunca en la URL. No la guardes en Git ni en registros. El cliente rechaza las redirecciones.
- Cada petición protegida autenticada consume 1 solicitud, incluidas consultas de bandejas vacías, lectura, generación, adjuntos, eliminación y estadísticas con clave. La cuota se reserva antes de ejecutar el endpoint; los fallos y reintentos también pueden consumirla.
- `get_usage()` no consume cuota. `get_domains()` es público y omite la clave. Los métodos de estadísticas del cliente sí envían la clave y consumen cuota.
- `remaining_total` es el saldo total; `remaining_today`, el diario. Un límite de `0` y saldo de `-1` indican que esa dimensión no tiene límite, pero siguen existiendo límites de frecuencia y concurrencia. Respeta `Retry-After`.

## Ejemplo
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

La espera consulta inmediatamente e incluye mensajes ya recibidos. Usa `seen_ids={...}` para ignorarlos y `predicate=lambda message: ...` para filtrar. Devuelve un resumen o `None` si no llega ningún mensaje a tiempo; los errores definitivos lanzan una excepción. Los resúmenes (`summary=1`) devuelven hasta 100 mensajes con una vista breve; `get_emails(address)` devuelve hasta 500 mensajes completos recientes. El servicio no es un archivo permanente.

## Scripts
| Python | |
| --- | --- |
| [demo.py](demo.py) | Demostración mínima; añade `--wait` para esperar correo |
| [01_generate_email.py](01_generate_email.py) | Crear una dirección aleatoria |
| [02_custom_email.py](02_custom_email.py) | Prefijo personalizado y dominio activo |
| [03_receive_email.py](03_receive_email.py) | Leer una bandeja |
| [04_auto_polling.py](04_auto_polling.py) | Consultar con plazo y cada 10 segundos |
| [05_delete_email.py](05_delete_email.py) | Eliminar un mensaje con `--yes` |
| [06_clear_inbox.py](06_clear_inbox.py) | Vaciar una bandeja con `--yes` |
| [07_statistics.py](07_statistics.py) | Estadísticas: 5 solicitudes |
| [08_async_client.py](08_async_client.py) | Crear 3 direcciones con `asyncio.to_thread` |
| [09_verification_code.py](09_verification_code.py) | Extraer códigos; filtro `--keyword` |
| [10_multiple_addresses.py](10_multiple_addresses.py) | Crear y consultar varias direcciones |
| [11_key_usage.py](11_key_usage.py) | Consultar cuota sin consumirla |
| [12_download_attachment.py](12_download_attachment.py) | Descargar a una ruta elegida sin sobrescribir |
| [13_list_domains.py](13_list_domains.py) | Paginar dominios públicos; filtro `--query` |

## Errores y seguridad

`APIError` incluye `status`, `message`, `usage`, `retry_after` y `quota_exhausted`. `TransportError` indica un fallo de red o tiempo de espera. Los errores no se muestran como bandejas vacías. El tiempo de espera HTTP predeterminado es de 15 segundos.

400: corrige la solicitud; 401: comprueba la clave; 403: bandeja privada no accesible; 404: ID inexistente o caducado; 409: elige un dominio activo; 429: distingue cuota agotada de limitación temporal; 5xx: posible fallo temporal. Las llamadas normales no se repiten automáticamente. La consulta periódica aplica espera progresiva y `Retry-After`; falla tras 3 errores consecutivos o si no queda tiempo para reintentar. Cada reintento puede consumir cuota.

La generación personalizada usa POST JSON. Un dominio explícito no disponible devuelve 409 en lugar de cambiar la dirección silenciosamente. Los dominios privados de GPTMail no son accesibles mediante esta API. Los adjuntos se reciben como bytes, no JSON; sus errores pueden ser texto. Los scripts de eliminación requieren `--yes`. La extracción de códigos es heurística y analiza HTML localmente sin cargar imágenes.

Consulta todos los endpoints y campos en la [referencia inglesa](README.md#http-api-reference) y la [documentación API](https://cleantempmail.com/api). También: [QUICK_START.md](QUICK_START.md) y [CONTRIBUTING.md](CONTRIBUTING.md).

## Comprobaciones
```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

Las pruebas usan una API local y mensajes ficticios. GitHub Actions comprueba Python 3.10–3.14 sin claves de producción.
