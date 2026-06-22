# Dashboard-Anleitung – Lux Analytics

## Überblick

Das Lux Analytics Dashboard ist eine YAML-basierte Lovelace-Ansicht mit vier Bereichen:

| Ansicht        | Inhalt                                                |
|----------------|-------------------------------------------------------|
| Übersicht      | Aktueller Wert, Status, Trend, Sonnenindex            |
| Tagesansicht   | 24h-Diagramm, Tages-Min/Max/Avg, Helle Stunden       |
| Wochenansicht  | 7-Tage-Diagramm, Wochen-Min/Max/Avg, Helle Stunden   |
| Monatsansicht  | 30-Tage-Diagramm, Monats-Min/Max/Avg, Helle Stunden  |
| Statistiken    | HA-native Statistikgraphen (Monat/Woche)              |

---

## Installation

### Methode 1: Eigenes Dashboard (empfohlen)

1. Datei `lux_analytics_dashboard.yaml` in das HA-Konfigurationsverzeichnis kopieren
2. In `configuration.yaml`:

```yaml
lovelace:
  mode: yaml
  dashboards:
    lux-analytics:
      mode: yaml
      filename: lux_analytics_dashboard.yaml
      title: Lux Analytics
      icon: mdi:white-balance-sunny
      show_in_sidebar: true
```

### Methode 2: In bestehendes Dashboard integrieren

Einzelne Karten aus `lux_analytics_dashboard.yaml` in ein bestehendes Dashboard kopieren.

---

## Entity-IDs anpassen

Das Dashboard verwendet Platzhalter-IDs. Diese müssen durch die tatsächlich von der Integration erzeugten Entity-IDs ersetzt werden.

**Ermittlung der echten IDs:**
1. **Entwicklertools** → **Zustände**
2. Nach `lux_analytics` filtern
3. Die echten Entity-IDs kopieren

---

## Visualisierungsoptionen

### history-graph (Standard)

Verwendet HA's eingebauten History-Graphen. Keine zusätzliche Installation nötig.

### statistics-graph (empfohlen für Langzeitdaten)

Nutzt Long-Term Statistics des Recorders. Zeigt Min/Max/Avg pro Zeitraum.

### Erweiterte Visualisierung (optional mit ApexCharts)

Für Heatmaps und Histogramme kann [ApexCharts Card](https://github.com/RomRider/apexcharts-card) (via HACS) verwendet werden.

Beispiel-Konfiguration für ein Lux-Diagramm mit ApexCharts:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Helligkeit letzte 24 Stunden
graph_span: 24h
series:
  - entity: sensor.DEIN_SENSOR_aktuelle_helligkeit
    name: Lux
    type: line
    stroke_width: 2
    color: "#f39c12"
    fill_raw: last
```

---

## Responsives Design

Das Dashboard ist für folgende Geräte optimiert:

| Gerät    | Empfohlene Breite | HA-Layout   |
|----------|-------------------|-------------|
| Desktop  | > 1200 px         | Sidebar     |
| Tablet   | 768 – 1200 px     | Kiosk-Modus |
| Mobil    | < 768 px          | HA-Standard |

Für Tablet-Kiosk-Modus: [Kiosk Mode](https://github.com/NemesisRE/kiosk-mode) via HACS.
