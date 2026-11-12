# TransFormateur — Code de base

Application web de conversion de fichiers entre différents formats.

## Prérequis

- Python 3.10+
- Flask (`pip install flask`)

## Démarrage

```bash
python app.py
```

L'application est accessible à l'adresse `http://localhost:5000`.

## Formats supportés

| Source | Cible |
|--------|-------|
| CSV | JSON |
| JSON | CSV |
| CSV | XML |
| XML | CSV |
| JSON | XML |
| XML | JSON |
| Markdown | HTML |

Des fichiers de données test sont disponibles dans le répertoire `dataset/` :