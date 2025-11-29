# CleanTempMail API - Exemples Python

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README.md) | [简体中文](README_CN.md) | Français | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

Exemples Python officiels pour [CleanTempMail](https://cleantempmail.com) - un service d'email temporaire gratuit avec une API puissante.

## 🚀 Fonctionnalités

- **Générer des emails temporaires** instantanément
- **Recevoir des emails** en temps réel
- **Accéder aux 500 derniers emails** par adresse
- **API de statistiques** pour l'analyse
- **Gratuit** - complètement gratuit avec des limites généreuses

## 📦 Installation

Aucune dépendance externe requise ! Tous les exemples utilisent uniquement la bibliothèque standard Python.

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
```

## 🔑 Clé API

Obtenez votre clé API gratuite sur [CleanTempMail API](https://cleantempmail.com/api)

Pour les tests, utilisez : `ct-test`

## 🎯 Démarrage Rapide

```python
import requests

API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# Générer un email
response = requests.get(
    f"{BASE_URL}/generate-email",
    headers={"X-API-Key": API_KEY}
)
email = response.json()["data"]["email"]
print(f"✅ Généré : {email}")
```

## 📚 Exemples

| Fichier | Description |
|---------|-------------|
| [`demo.py`](demo.py) | 🎬 Démo complète de toutes les fonctionnalités |
| [`01_generate_email.py`](01_generate_email.py) | Générer un email temporaire aléatoire |
| [`02_custom_email.py`](02_custom_email.py) | Créer un email avec préfixe personnalisé |
| [`03_receive_email.py`](03_receive_email.py) | Recevoir et lire les emails entrants |
| [`04_auto_polling.py`](04_auto_polling.py) | Interrogation automatique des nouveaux emails |
| [`09_verification_code.py`](09_verification_code.py) | Extraire les codes de vérification |
| [`cleantempmail.py`](cleantempmail.py) | Classe client Python réutilisable |
| [`example_client.py`](example_client.py) | Comment utiliser la classe client |

## 🔧 Cas d'Usage

- **Tests** - Tester les flux de vérification email
- **Automatisation** - Automatiser les processus d'inscription
- **Confidentialité** - Protéger votre vrai email
- **Développement** - Tester les fonctionnalités email sans SMTP
- **QA** - Vérifier la livraison des emails

## 🌐 Liens

- 🌍 Site web : [cleantempmail.com](https://cleantempmail.com)
- 📚 Documentation API : [cleantempmail.com/api](https://cleantempmail.com/api)
- 💬 Issues : [GitHub Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues)

---

Fait avec ❤️ par [CleanTempMail](https://cleantempmail.com)
