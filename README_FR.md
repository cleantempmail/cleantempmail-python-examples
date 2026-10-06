# CleanTempMail API — Exemples Python

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

Exemples officiels et client réutilisable pour [CleanTempMail](https://cleantempmail.com/api) : créer des adresses temporaires, recevoir des messages, extraire des codes et télécharger des pièces jointes pour tester votre propre application.

**Python 3.10+ · bibliothèque standard uniquement · licence MIT**

## Installation
```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

PowerShell : `$env:CLEANTEMPMAIL_API_KEY = 'YOUR_API_KEY'`. Aucune installation par pip, même pour l'exemple asynchrone. L'URL par défaut est `https://cleantempmail.com/api` ; `CLEANTEMPMAIL_BASE_URL` permet de la modifier. Utilisez HTTPS hors développement local. Les scripts lisent les variables d'environnement et ne chargent pas automatiquement [.env.example](.env.example) ni un fichier `.env`.

## Clés et quotas

- Achetez une clé sur la [page API](https://cleantempmail.com/api). Le quota total est payé une fois, sans renouvellement automatique ni recharge. Consultez le site pour les tarifs actuels.
- Sans variable d'environnement, les exemples utilisent `ct-test`, une clé de démonstration limitée et partagée par tous. Son quota peut être épuisé. Elle ne convient pas à la production ; l'API n'est pas un service gratuit illimité.
- Les clés sont envoyées uniquement dans l'en-tête `X-API-Key`. Ne les mettez pas dans Git, les URL ou les journaux. Le client refuse les redirections.
- Chaque requête protégée authentifiée coûte 1 requête : génération, boîte vide, lecture, pièce jointe, suppression et statistiques avec une clé. Le quota est décompté avant l'exécution ; un échec ou une nouvelle tentative peut aussi être facturé.
- `get_usage()` ne consomme pas de quota. `get_domains()` est public et n'envoie pas la clé. Les méthodes de statistiques de ce client utilisent la clé et consomment le quota.
- `remaining_total` indique le solde total, `remaining_today` le solde quotidien. Une limite de `0` et un solde de `-1` signifient sans limite pour ce quota, mais les limites de fréquence et de concurrence restent applicables. Respectez `Retry-After`.

## Exemple
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

L'attente vérifie immédiatement la boîte et inclut les messages déjà reçus. Utilisez `seen_ids={...}` pour les ignorer et `predicate=lambda message: ...` pour filtrer. Elle renvoie un résumé ou `None` si aucun message n'arrive à temps ; les erreurs définitives déclenchent une exception. Les résumés (`summary=1`) contiennent jusqu'à 100 messages avec un aperçu ; `get_emails(address)` renvoie jusqu'à 500 messages complets récents. Le stockage n'est pas une archive permanente.

## Scripts
| Python | |
| --- | --- |
| [demo.py](demo.py) | Démonstration minimale ; ajouter `--wait` pour surveiller |
| [01_generate_email.py](01_generate_email.py) | Créer une adresse aléatoire |
| [02_custom_email.py](02_custom_email.py) | Préfixe personnalisé et domaine actif |
| [03_receive_email.py](03_receive_email.py) | Lire une boîte |
| [04_auto_polling.py](04_auto_polling.py) | Surveiller avec délai et intervalle de 10 secondes |
| [05_delete_email.py](05_delete_email.py) | Supprimer un message avec `--yes` |
| [06_clear_inbox.py](06_clear_inbox.py) | Vider une boîte avec `--yes` |
| [07_statistics.py](07_statistics.py) | Statistiques : 5 requêtes |
| [08_async_client.py](08_async_client.py) | 3 générations avec `asyncio.to_thread` |
| [09_verification_code.py](09_verification_code.py) | Extraire des codes ; filtre `--keyword` |
| [10_multiple_addresses.py](10_multiple_addresses.py) | Créer et consulter plusieurs adresses |
| [11_key_usage.py](11_key_usage.py) | Consulter le quota sans le consommer |
| [12_download_attachment.py](12_download_attachment.py) | Télécharger vers un chemin choisi, sans écraser |
| [13_list_domains.py](13_list_domains.py) | Parcourir les domaines publics ; filtre `--query` |

## Erreurs et sécurité

`APIError` expose `status`, `message`, `usage`, `retry_after` et `quota_exhausted`. `TransportError` signale un problème réseau ou un délai dépassé. Un échec n'est jamais présenté comme une boîte vide. Le délai HTTP par défaut est de 15 secondes.

400 : corriger la requête ; 401 : vérifier la clé ; 403 : boîte privée interdite ; 404 : identifiant absent ou expiré ; 409 : choisir un domaine actif ; 429 : distinguer quota épuisé et limitation temporaire ; 5xx : panne temporaire possible. Les appels ordinaires ne sont pas relancés automatiquement. La surveillance applique un recul et `Retry-After`, puis s'arrête après 3 échecs consécutifs ou si le délai ne permet plus une tentative. Chaque nouvelle tentative peut consommer du quota.

La génération personnalisée utilise un POST JSON. Un domaine explicitement indisponible retourne 409, sans remplacement silencieux. Les domaines privés GPTMail sont inaccessibles par cette API. Les pièces jointes sont des octets, pas du JSON ; leurs erreurs peuvent être du texte. Les scripts de suppression exigent `--yes`. L'extraction de codes est heuristique et analyse le HTML localement sans charger d'images.

Les chemins et champs JSON complets sont décrits dans la [référence anglaise](README.md#http-api-reference) et la [documentation API](https://cleantempmail.com/api). Voir aussi [QUICK_START.md](QUICK_START.md) et [CONTRIBUTING.md](CONTRIBUTING.md).

## Vérification
```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

Les tests utilisent des messages fictifs et une API locale. GitHub Actions vérifie Python 3.10–3.14 sans clé de production.
