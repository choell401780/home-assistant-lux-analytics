# Architektur-Dokumentation – Lux Analytics

## Architekturentscheidung

### Analysierte Varianten

#### Variante A – Reine YAML/Template-Lösung
**Abgelehnt.** Gründe:
- Keine automatische Sensorerkennung möglich
- Keine programmatische Statistikberechnung
- Keine strukturierte Konfiguration (Config Flow)
- Schwierig zu warten, nicht HACS-fähig

#### Variante B – Native Custom Integration (nur Python)
**Unvollständig.** Gründe:
- Würde den HA-Recorder nicht optimal nutzen
- Eigene Datenbankanbindung unnötig komplex
- HA bietet bereits `get_significant_states()` und LTS-Statistiken

#### Variante C – Hybrid (gewählt)
**Gewählt.** Kombination aus:
- **Custom Integration**: Sensor-Erkennung, Statistikberechnung, Config Flow
- **HA Recorder**: Historische Datenspeicherung (HA-nativ, kein eigenes Datenbank-Schema)
- **Lovelace Dashboard**: YAML-basierte Visualisierung
- **HACS**: Distribution und Update-Management

### Begründung

> "Nutze HA-interne Mechanismen wo immer möglich. Eigene Logik nur dort, wo HA keine passende Lösung bietet."

| Aufgabe | HA-nativ? | Lösung |
|---|---|---|
| Historische Daten | ✅ | `recorder` + `get_significant_states()` |
| Statistiken (LTS) | ✅ | `statistics_graph` Card |
| Sensor-Erkennung | ❌ | Eigene Logik in `coordinator.py` |
| Min/Max/Avg | ❌ | Eigene Berechnung aus Recorder-Daten |
| Helligkeitsklassen | ❌ | Eigene Klassifizierungslogik |
| Trend | ❌ | Eigene Berechnung |
| Distribution | ✅ | HACS |
| Update-Erkennung | ✅ | HACS |

---

## Projektstruktur

```
home-assistant-lux-analytics/
├── custom_components/lux_analytics/    # HA Custom Integration
│   ├── __init__.py                     # Entry-Point: setup/unload
│   ├── manifest.json                   # HA + HACS Metadaten
│   ├── const.py                        # Konstanten, Klassifizierung, Entity-IDs
│   ├── coordinator.py                  # DataUpdateCoordinator + Statistiken
│   ├── config_flow.py                  # UI-Konfiguration
│   ├── sensor.py                       # SensorEntity-Implementierungen
│   ├── strings.json                    # UI-Texte (Basis)
│   └── translations/                   # Lokalisierungen
│       ├── de.json
│       └── en.json
├── dashboards/
│   └── lux_analytics_dashboard.yaml   # Lovelace Dashboard
├── docs/                              # Dokumentation
├── releases/                          # Release Notes pro Version
├── .github/workflows/                 # CI/CD
│   ├── validate.yml                   # Syntax + HACS Validation
│   └── release.yml                    # Automatische GitHub Releases
├── hacs.json                          # HACS-Konfiguration
├── README.md
├── CHANGELOG.md
├── LICENSE
└── VERSION
```

---

## Datenfluss

```
┌─────────────────────────────────────────────────────────┐
│                  Home Assistant Core                    │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │ Lux-Sensor   │───▶│   Recorder   │                  │
│  │ (HmIP-SLO,  │    │  (SQLite DB) │                  │
│  │  Zigbee, ...) │    └──────┬───────┘                  │
│  └──────────────┘           │                          │
│                             │ get_significant_states()  │
│                             ▼                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         LuxAnalyticsCoordinator                  │  │
│  │                                                  │  │
│  │  _async_update_data() [alle 5 Min]               │  │
│  │  ├── _get_current_lux()    → hass.states         │  │
│  │  ├── _get_history_values() → Recorder            │  │
│  │  ├── _safe_min/max/avg()   → Python              │  │
│  │  ├── _bright_hours()       → Schwellwert-Check   │  │
│  │  ├── _calculate_trend()    → 24h-Vergleich       │  │
│  │  └── classify_brightness() → Klassifizierung     │  │
│  │                                                  │  │
│  │  data = {                                        │  │
│  │    "current": 45000.0,                           │  │
│  │    "status": "Sonnig",                           │  │
│  │    "day_max": 62000.0,                           │  │
│  │    ...                                           │  │
│  │  }                                               │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │ CoordinatorEntity.native_value      │
│                   ▼                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │         LuxSensorEntity (19×)                    │  │
│  │  entity_id: sensor.lux_analytics_tagesmaximum   │  │
│  │  state: 62000.0                                  │  │
│  │  unit: lx                                        │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                    │
│                   ▼                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Lovelace Dashboard                       │  │
│  │  (lux_analytics_dashboard.yaml)                  │  │
│  │  history-graph / statistics-graph / glance       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Entity-ID Schema

Das Entity-ID-Schema ist in `const.py` zentralisiert und garantiert Vorhersagbarkeit:

```python
# build_entity_id(sensor_key, label="")
# Kein Label:
"sensor.lux_analytics_aktuelle_helligkeit"
"sensor.lux_analytics_tagesminimum"

# Label "Garten":
"sensor.lux_analytics_garten_aktuelle_helligkeit"
"sensor.lux_analytics_garten_tagesminimum"
```

**Technischer Mechanismus**: `self.entity_id = build_entity_id(...)` in `LuxSensorEntity.__init__()` setzt die Entity-ID bei der Erstregistrierung. HA speichert sie im Entity Registry. Nach Neustart nutzt HA die Registry-ID (Nutzer-Umbenennungen bleiben erhalten).

---

## Statistikberechnung

### Datenquelle

`get_significant_states(hass, start, end, [entity_id])` aus `homeassistant.components.recorder.history` liefert alle State-Changes im Zeitraum.

### Zeiträume

| Statistik | Zeitraum |
|---|---|
| Tag | Tagesbeginn 00:00 bis jetzt |
| Woche | Montag 00:00 bis jetzt |
| Monat | Monatserster 00:00 bis jetzt |
| 24h | Jetzt minus 24 Stunden |
| 7 Tage | Jetzt minus 7 Tage |
| 30 Tage | Jetzt minus 30 Tage |

### Helle Stunden

Helle Stunden werden aus dem Polling-Intervall abgeleitet:

```python
bright = sum(1 for v in values if v >= threshold)
bright_hours = round(bright / 60, 2)  # Annahme: ~1 Sample/Minute
```

**Bekannte Einschränkung**: Abhängig vom tatsächlichen Polling-Intervall und Recorder-Sampling. Nicht exakt bei seltenem State-Change.

### Trend-Berechnung

```python
avg = sum(recent_24h_values) / len(recent_24h_values)
delta = current - avg
if delta > avg * 0.15:  return "Steigend"
if delta < -avg * 0.15: return "Fallend"
return "Stabil"
```

---

## Config Entry Architektur

### Ein Sensor pro Entry (ab v0.3.0)

```
Config Entry A  →  Coordinator A  →  19 Sensor-Entitäten (kein Label)
Config Entry B  →  Coordinator B  →  19 Sensor-Entitäten (Label: Garten)
```

**Vorteile**:
- Unabhängiges Reload pro Sensor
- Verschiedene Polling-Intervalle pro Sensor
- Klares 1:1 Verhältnis
- unique_id verhindert Duplikate

### Konfigurationsdaten

```python
entry.data = {
    "source_sensor": "sensor.hmip_slo_abc123_illuminance",
    "sensor_label":  "Garten",
    "bright_threshold": 1000,
    "update_interval": 300,
}
entry.options = {
    # Überschreibt entry.data Werte wenn vom Nutzer geändert
    "bright_threshold": 2000,
}
```

---

## HACS-Integration

HACS verwaltet:
- Download und Installation der `custom_components/lux_analytics/` Dateien
- Versionserkennung via `manifest.json` → `version`
- Update-Erkennung via GitHub Releases (Tag `v0.3.0` → Version `0.3.0`)
- HA-native Update-Entity für jeden HACS-verwalteten Component

Lux Analytics enthält **keine eigene Update-Logik** — vollständig an HACS delegiert.

---

## Erweiterungsarchitektur

### Pool/Beschattung/PV (vorbereitet, nicht implementiert)

```python
# In __init__.py: einfach Platforms erweitern
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH]

# Neue Dateien:
# binary_sensor.py → BrightnessBinarySensor (hell/dunkel)
# switch.py        → AutomationSwitch (Poolpumpe, Markise)
```

### Neue Statistik hinzufügen

1. Eintrag in `SENSOR_TYPES` und `ENTITY_ID_SLUGS` in `const.py`
2. Berechnung in `_fetch_sensor_data()` in `coordinator.py`
3. Eintrag in `_empty_sensor_data()` ergänzen
4. Sensor erscheint automatisch (kein weiterer Code nötig)
