# Home Assistant Lux Analytics

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/choell/home-assistant-lux-analytics/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HA min version](https://img.shields.io/badge/Home%20Assistant-2023.1.0%2B-brightgreen)](https://www.home-assistant.io)

Automatische Erkennung, Analyse und Visualisierung von Helligkeitssensoren (Lux) in Home Assistant.

---

## Funktionen

- **Automatische Sensorerkennung** – findet alle Helligkeitssensoren (device_class, unit, entity_id)
- **Helligkeitsklassifizierung** – 8 Stufen von Nacht (0 lx) bis Extreme Sonne (>70.000 lx)
- **Vollständige Statistiken** – Min, Max, Durchschnitt für Tag, Woche und Monat
- **Helle Stunden** – konfigurierbare Schwelle für helle/sonnige Stunden
- **Trend-Erkennung** – Steigend / Fallend / Stabil
- **Sonnenindex** – normalisierter Wert 0–100 %
- **Automatische Update-Erkennung** – vergleicht installierte mit aktueller GitHub-Version
- **Modernes Dashboard** – Lovelace-basiert, optimiert für Tablet und Desktop
- **HACS-kompatibel** – einfache Installation über HACS
- **Vollständig lokal** – keine Cloud-Abhängigkeit außer für Update-Prüfung

---

## Unterstützte Sensoren

| Hersteller / Protokoll | Typ                  | Erkennung         |
|------------------------|----------------------|-------------------|
| Homematic IP           | HmIP-SLO             | Automatisch       |
| Zigbee                 | Alle Lux-Sensoren    | Automatisch       |
| Z-Wave                 | Alle Lux-Sensoren    | Automatisch       |
| MQTT                   | Alle Lux-Sensoren    | Automatisch       |
| Generic                | device_class: illuminance | Automatisch  |

---

## Helligkeitsklassen

| Bereich         | Wert (lx)        |
|-----------------|------------------|
| Nacht           | 0 – 1            |
| Dämmerung       | 1 – 100          |
| Früher Morgen   | 100 – 1.000      |
| Morgen          | 1.000 – 10.000   |
| Tag             | 10.000 – 30.000  |
| Sonnig          | 30.000 – 50.000  |
| Pralle Sonne    | 50.000 – 70.000  |
| Extreme Sonne   | > 70.000         |

---

## Installation

### Via HACS (empfohlen)

1. HACS in Home Assistant öffnen
2. **Integrationen** → **Benutzerdefinierte Repositories**
3. URL eingeben: `https://github.com/choell/home-assistant-lux-analytics`
4. Kategorie: **Integration** → **Hinzufügen**
5. Integration suchen: **Lux Analytics** → **Herunterladen**
6. Home Assistant neu starten

### Manuell

1. Den Ordner `custom_components/lux_analytics/` in das Verzeichnis
   `<ha_config>/custom_components/` kopieren
2. Home Assistant neu starten

### Einrichten

1. **Einstellungen** → **Integrationen** → **Integration hinzufügen**
2. Suche nach **Lux Analytics**
3. Sensoren automatisch erkennen lassen oder manuell auswählen
4. Konfiguration bestätigen

---

## Dashboard einrichten

1. Datei `dashboards/lux_analytics_dashboard.yaml` in deine HA-Konfiguration kopieren
2. In `configuration.yaml` eintragen:

```yaml
lovelace:
  mode: yaml
  resources: []
  dashboards:
    lux-analytics:
      mode: yaml
      filename: lux_analytics_dashboard.yaml
      title: Lux Analytics
      icon: mdi:white-balance-sunny
      show_in_sidebar: true
```

3. Home Assistant neu starten oder Lovelace neu laden

---

## Erzeugte Entitäten

Für jeden überwachten Sensor werden folgende Entitäten erstellt:

| Entität                              | Beschreibung                     |
|--------------------------------------|----------------------------------|
| `sensor.*_aktuelle_helligkeit`       | Aktueller Lux-Wert               |
| `sensor.*_helligkeitsstatus`         | Helligkeitsklasse (Text)         |
| `sensor.*_helligkeitstrend`          | Steigend / Fallend / Stabil      |
| `sensor.*_sonnenindex`               | Sonnenindex 0–100 %              |
| `sensor.*_tagesminimum`              | Min heute                        |
| `sensor.*_tagesmaximum`              | Max heute                        |
| `sensor.*_tagesdurchschnitt`         | Ø heute                          |
| `sensor.*_wochenminimum`             | Min diese Woche                  |
| `sensor.*_wochenmaximum`             | Max diese Woche                  |
| `sensor.*_wochendurchschnitt`        | Ø diese Woche                    |
| `sensor.*_monatsminimum`             | Min diesen Monat                 |
| `sensor.*_monatsmaximum`             | Max diesen Monat                 |
| `sensor.*_monatsdurchschnitt`        | Ø diesen Monat                   |
| `sensor.*_helle_stunden_heute`       | Helle Stunden heute              |
| `sensor.*_helle_stunden_woche`       | Helle Stunden Woche              |
| `sensor.*_helle_stunden_monat`       | Helle Stunden Monat              |
| `sensor.*_durchschnitt_24h`          | Ø letzte 24 Stunden              |
| `sensor.*_durchschnitt_7_tage`       | Ø letzte 7 Tage                  |
| `sensor.*_durchschnitt_30_tage`      | Ø letzte 30 Tage                 |
| `sensor.lux_analytics_update`        | Update-Status und Versionsinfo   |

---

## Konfigurationsoptionen

| Option                  | Standard | Beschreibung                                  |
|-------------------------|----------|-----------------------------------------------|
| `auto_discover`         | `true`   | Sensoren automatisch erkennen                 |
| `sensors`               | `[]`     | Manuelle Sensor-Liste (bei auto=false)        |
| `bright_threshold`      | `1000`   | Schwellwert für helle Stunden (lx)            |
| `update_interval`       | `300`    | Aktualisierungsintervall in Sekunden          |

---

## Architektur

Dieses Projekt verwendet **Variante C (Hybrid)**:

- **Custom Integration** – Sensorerkennung, Statistikberechnung, GitHub-Update-Check
- **HA-native Recorder** – historische Datenspeicherung über den integrierten Recorder
- **Lovelace Dashboard** – YAML-basierte Visualisierung
- **Template-fähig** – alle Werte als HA-Sensoren für eigene Automationen nutzbar

### Erweiterungsvorbereitung

Die Architektur ist bereits vorbereitet für:
- Poolpumpensteuerung (helligkeitsabhängige Laufzeiten)
- Beschattungssteuerung
- PV-Optimierung
- Sonnenstundenberechnung
- Temperaturintegration

---

## Update-Erkennung

Die Integration prüft alle 6 Stunden die aktuelle Version auf GitHub.

Der Sensor `sensor.lux_analytics_update` zeigt:
- Installierte Version
- Neueste verfügbare Version
- Release Notes
- Update-Hinweis bei verfügbarem Update

---

## Anforderungen

- Home Assistant 2023.1.0 oder neuer
- `recorder`-Integration aktiv (Standard in HA)
- Python 3.11+ (in HA enthalten)

---

## Lizenz

MIT – siehe [LICENSE](LICENSE)

---

## Mitwirken

Issues und Pull Requests sind willkommen!
[GitHub Issues](https://github.com/choell/home-assistant-lux-analytics/issues)
