# Contributing to Home Assistant Lux Analytics

Vielen Dank für dein Interesse an Lux Analytics! Beiträge sind herzlich willkommen.

---

## Vor dem ersten Beitrag

Bitte lies dir zunächst durch:
- [README.md](README.md) – Projektübersicht
- [docs/architecture.md](docs/architecture.md) – Technische Architektur
- [docs/development.md](docs/development.md) – Entwicklungsumgebung einrichten

---

## Beitragsarten

### Bug Reports
Bitte nutze den [Issue Tracker](https://github.com/choell401780/home-assistant-lux-analytics/issues) und verwende die **Bug Report** Vorlage.

Pflichtangaben:
- Home Assistant Version
- Lux Analytics Version
- Sensor-Typ und -Hersteller
- Fehlerbeschreibung
- Logs (HA Protokolle mit Debug-Level)
- Schritte zur Reproduktion

### Feature Requests
Erstelle ein Issue mit dem Label `enhancement`. Beschreibe:
- Was du dir wünschst
- Warum es nützlich wäre
- Mögliche Implementierungsideen

### Pull Requests
1. Fork des Repositories erstellen
2. Feature-Branch erstellen: `git checkout -b feature/mein-feature`
3. Änderungen implementieren
4. Tests und Syntax-Prüfung durchführen
5. Commit mit aussagekräftiger Nachricht
6. Pull Request öffnen

---

## Entwicklungsstandards

### Python
- Kompatibel mit Python 3.12+
- Alle Dateien müssen `py_compile` bestehen
- Keine externen Abhängigkeiten außer HA-internen (kein `requirements`)
- Typisierung mit Type Hints

### Commits
Format: `type(scope): beschreibung`

Typen: `feat`, `fix`, `refactor`, `docs`, `chore`

Beispiele:
```
feat(sensor): add solar radiation sensor support
fix(coordinator): handle unavailable state gracefully
docs(installation): update HACS instructions
```

### Versionierung
Semantisches Versioning: `MAJOR.MINOR.PATCH`

- `PATCH`: Bugfixes
- `MINOR`: Neue Features (rückwärtskompatibel)
- `MAJOR`: Breaking Changes

### Vor jedem Commit
```bash
# Syntax prüfen
python3 -m py_compile custom_components/lux_analytics/*.py

# JSON prüfen
python3 -c "import json; [json.load(open(f)) for f in ['custom_components/lux_analytics/manifest.json', 'hacs.json']]"

# Versionskonsistenz prüfen
FILE_VER=$(cat VERSION | tr -d '[:space:]')
MANIFEST_VER=$(python3 -c "import json; print(json.load(open('custom_components/lux_analytics/manifest.json'))['version'])")
[ "$FILE_VER" = "$MANIFEST_VER" ] && echo "OK" || echo "MISMATCH"
```

---

## Release-Prozess

Nur Maintainer erstellen Releases. Siehe [docs/release-process.md](docs/release-process.md).

---

## Verhaltenskodex

Dieses Projekt folgt dem [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Fragen?

[GitHub Discussions](https://github.com/choell401780/home-assistant-lux-analytics/discussions) oder [Issues](https://github.com/choell401780/home-assistant-lux-analytics/issues).
