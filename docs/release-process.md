# Release-Prozess – Lux Analytics

## Übersicht

Releases werden durch Git-Tags ausgelöst. GitHub Actions erstellt automatisch:
- ZIP-Archiv mit Integration + Dashboard
- GitHub Release mit Release Notes
- HACS erkennt die neue Version automatisch

---

## Versionierungsschema

Semantisches Versioning: `MAJOR.MINOR.PATCH`

| Typ | Wann | Beispiel |
|---|---|---|
| PATCH | Bugfix, keine neuen Features | 0.3.0 → 0.3.1 |
| MINOR | Neues Feature, rückwärtskompatibel | 0.3.0 → 0.4.0 |
| MAJOR | Breaking Change, Migration nötig | 0.x.x → 1.0.0 |

---

## Release Checkliste

### 1. Version erhöhen

```bash
# VERSION Datei
echo "0.4.0" > VERSION

# manifest.json
# "version": "0.4.0"
```

### 2. CHANGELOG aktualisieren

```markdown
## [0.4.0] – YYYY-MM-DD

### Neu
- ...

### Geändert
- ...

### Behoben
- ...
```

### 3. Release Notes erstellen

```bash
mkdir -p releases/v0.4.0
# releases/v0.4.0/release_notes.md erstellen
```

### 4. Alles committen und pushen

```bash
git add -A
git commit -m "feat: v0.4.0 – ..."
git push origin main
```

### 5. Tag setzen und pushen

```bash
git tag v0.4.0
git push origin v0.4.0
```

### 6. GitHub Actions übernimmt automatisch

- Verifiziert VERSION vs. Tag
- Erstellt ZIP-Archiv
- Erstellt GitHub Release mit Release Notes
- HACS erkennt neue Version

---

## GitHub Actions

### validate.yml – läuft bei jedem Push

```
Python Syntax Check → JSON Validation → Version Consistency → HACS Validation
```

### release.yml – läuft bei Tag-Push `v*.*.*`

```
Checkout → Version verify → ZIP erstellen → Release Notes auflösen → GitHub Release
```

---

## HACS Update-Mechanismus

1. Tag `v0.4.0` wird gepusht
2. GitHub Actions erstellt Release `v0.4.0`
3. HACS liest GitHub Releases API
4. HACS vergleicht `manifest.json`-Version mit neuestem Release
5. HA zeigt Update-Benachrichtigung für alle Nutzer
6. Nutzer klickt "Aktualisieren" in HACS

---

## Hotfix-Prozess

```bash
# Aus aktuellem main branchen (kein separater Release-Branch nötig)
git checkout main
# Fix implementieren
git add -A
git commit -m "fix: ..."
echo "0.3.1" > VERSION
# manifest.json, CHANGELOG aktualisieren
git commit -m "chore: v0.3.1"
git tag v0.3.1
git push origin main v0.3.1
```
