# Entwicklerdokumentation – Lux Analytics

## Architektur

### Variante C – Hybrid-Ansatz (gewählt)

```
lux_analytics/
├── __init__.py          Einstiegspunkt, async_setup_entry / async_unload_entry
├── manifest.json        HACS/HA Metadaten
├── const.py             Konstanten, Helligkeitsklassen, Sensor-Typen
├── coordinator.py       DataUpdateCoordinator – Statistiken & GitHub-Check
├── config_flow.py       UI-Konfiguration (Config- und Options-Flow)
├── sensor.py            SensorEntity-Klassen
├── strings.json         UI-Texte (Deutsch, Basis)
└── translations/
    ├── de.json          Deutsche Übersetzung
    └── en.json          Englische Übersetzung
```

### Datenfluss

```
HA Recorder (Verlaufsdaten)
        │
        ▼
LuxAnalyticsCoordinator._async_update_data()
        │
        ├── _get_current_lux()          → Aktueller Wert aus hass.states
        ├── _get_history_values()       → get_significant_states() aus Recorder
        ├── _safe_min/max/avg()         → Statistische Berechnung
        ├── _bright_hours()             → Schwellwert-basierte Zählung
        ├── _calculate_trend()          → Vergleich mit 24h-Durchschnitt
        └── _maybe_check_github_version() → aiohttp → GitHub API
                │
                ▼
        coordinator.data[entity_id] = {statistic_dict}
                │
                ▼
        LuxSensorEntity.native_value     → HA Sensor State
        UpdateAvailableSensor            → Version & Release Notes
```

---

## Erweiterung: Neue Statistik hinzufügen

### 1. Konstante hinzufügen (`const.py`)

```python
SENSOR_TYPES = {
    # ... bestehende Typen
    "my_new_stat": {
        "name": "Meine neue Statistik",
        "icon": "mdi:chart-bell-curve",
        "unit": "lx"
    },
}
```

### 2. Berechnung implementieren (`coordinator.py`)

In `_fetch_sensor_data()`:

```python
return {
    # ... bestehende Werte
    "my_new_stat": self._calculate_my_stat(some_values),
}
```

### 3. Sensor wird automatisch erstellt

Die `sensor.py` iteriert über alle `SENSOR_TYPES` – kein weiterer Code nötig.

---

## Erweiterung: Pool/PV/Beschattung (vorbereitet)

Die Architektur unterstützt künftige Plattformen:

```python
# In __init__.py ergänzen:
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH]
```

Neue Dateien:
- `binary_sensor.py` – z. B. "Poolpumpe aktiv"
- `switch.py` – z. B. "Beschattung aktiv"
- `services.yaml` – Dienste für Automationen

---

## Lokale Entwicklung

### Voraussetzungen

```bash
python3 -m venv venv
source venv/bin/activate
pip install homeassistant
```

### Tests ausführen

```bash
# Syntax-Check
python3 -m py_compile custom_components/lux_analytics/*.py

# HA-Integrations-Validierung
python3 -m homeassistant --script check_config
```

### Release erstellen

1. `VERSION` Datei aktualisieren
2. `manifest.json` → `"version"` aktualisieren
3. `CHANGELOG.md` ergänzen
4. Git Tag erstellen: `git tag v0.X.0`
5. GitHub Release aus Tag erstellen

---

## HACS-Konformität

Anforderungen erfüllt:
- [x] `hacs.json` vorhanden
- [x] `custom_components/<domain>/manifest.json` vorhanden
- [x] `config_flow: true` in manifest.json
- [x] Semantische Versionierung
- [x] GitHub Releases für automatische Updates
- [x] README.md vorhanden
- [x] MIT Lizenz

---

## Versionierungsschema

```
v MAJOR . MINOR . PATCH

v0.1.0 – Erstveröffentlichung
v0.2.0 – Neue Funktionen
v0.3.0 – Weitere Funktionen
v1.0.0 – Stabile Produktionsversion
```

Breaking Changes erhöhen MAJOR.
Neue Features erhöhen MINOR.
Bugfixes erhöhen PATCH.
