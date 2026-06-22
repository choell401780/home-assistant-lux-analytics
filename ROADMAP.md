# Roadmap – Home Assistant Lux Analytics

## Aktuell: v0.3.0 ✅

- HACS-konforme Projektstruktur
- Automatische Sensorerkennung
- Plug-and-Play Dashboard (vorhersagbare Entity-IDs)
- Ein-Sensor-Architektur pro Config Entry
- Vollständige Statistiken (Min/Max/Avg, helle Stunden, Trend, Sonnenindex)

---

## Geplant

### v0.4.0 – Konfiguration & UX
**Geplant: Q3 2026**

- Konfigurierbare Helligkeitsklassen-Schwellwerte über Options-Flow
- Umlaut-Normalisierung in Labels (ü→ue, ä→ae, ö→oe, ß→ss)
- Bessere Fehlerbehandlung bei nicht vorhandenem Sensor
- Automatische Sensor-Reaktivierung nach Neustart
- Dashboard: zweite View für gelabelte Sensoren

### v0.5.0 – Erweiterte Visualisierung
**Geplant: Q4 2026**

- ApexCharts-Unterstützung (optionaler HACS-Frontend-Dependenz)
- Lux-Heatmap (Stunde × Wochentag)
- Sonnenstunden-Balkendiagramm (Monatssicht)
- Lux-Histogramm (Häufigkeitsverteilung)
- Sensor-Vergleichsview für mehrere Instanzen

### v0.6.0 – Pool & Beschattungs-Modul
**Geplant: Q1 2027**

Vorbereitung für Automationsmodule (keine aktiven Automationen, nur Grundlage):

- Sonnenstunden-Kalkulation (kWh-Äquivalent)
- Schwellwert-Binary-Sensor (hell/dunkel)
- Helligkeitsabhängige Zeitfenster-Berechnung
- Vorbereitung Beschattungssteuerung
- Vorbereitung Poolpumpenlogik

### v0.7.0 – PV-Integration
**Geplant: Q2 2027**

- Korrelation Lux ↔ PV-Ertrag
- Sonnenpotenzial-Index
- Vorhersage-Grundlage (gleitende Durchschnitte)
- Temperaturkorrelation (optional)

### v1.0.0 – Produktiv-Release
**Geplant: Q3 2027**

- Vollständige Testabdeckung
- Performance-Optimierung für große Historien
- Vollständige API-Dokumentation
- HACS Default Repository Einreichung
- Multilingual: FR, NL, PL
- Barrierefreiheit im Dashboard

---

## Designprinzipien für alle Versionen

- **Lokal first**: Keine Cloud-Abhängigkeit für Kernfunktionen
- **HA-nativ**: HA-interne APIs bevorzugen (Recorder, Statistics, Templates)
- **HACS-konform**: Jede Version HACS-installierbar
- **Plug-and-Play**: Keine manuelle Dateibearbeitung nach Installation
- **Herstellerunabhängig**: Alle `device_class: illuminance` Sensoren
- **Erweiterbar**: Architektur vorbereitet für Pool/PV/Beschattung

---

## Ideen-Backlog (nicht versioniert)

- Matter-native Unterstützung
- HA-native Dashboard-Strategy (automatisch generiertes Dashboard)
- REST-API für externe Tools
- Exportfunktion (CSV/JSON)
- Nachtmodus-Helfer (Lux < Schwellwert → Nacht)
- Benutzeroberfläche für Sensor-Kalibrierung

---

Feedback und Feature-Requests: [GitHub Issues](https://github.com/choell401780/home-assistant-lux-analytics/issues)
