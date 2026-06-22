# Release Notes – v0.1.0

**Veröffentlicht:** 2026-06-22

## Erstveröffentlichung – Home Assistant Lux Analytics

Dies ist die erste offizielle Version von **Home Assistant Lux Analytics**.

---

## Neue Funktionen

### Automatische Sensorerkennung
- Erkennt alle Helligkeitssensoren anhand von `device_class: illuminance`, Einheit `lx`/`lux` und Entity-ID-Schlüsselwörtern
- Unterstützt: Homematic IP HmIP-SLO, Zigbee, Z-Wave, MQTT und generische Lux-Sensoren
- Manuelle Sensor-Auswahl alternativ möglich

### Helligkeitsklassifizierung
- 8 Stufen: Nacht, Dämmerung, Früher Morgen, Morgen, Tag, Sonnig, Pralle Sonne, Extreme Sonne
- Konfigurierbare Schwellwerte (in zukünftiger Version über UI)

### Statistik-Sensoren (pro überwachtem Sensor)
- Tages-Min/Max/Durchschnitt
- Wochen-Min/Max/Durchschnitt
- Monats-Min/Max/Durchschnitt
- Helle Stunden: Heute / Woche / Monat
- Durchschnitt: letzte 24h / 7 Tage / 30 Tage
- Trend: Steigend / Fallend / Stabil
- Sonnenindex: 0–100 %

### Lovelace Dashboard
- Übersichtskarte mit Trend und Sonnenindex
- 24h / 7-Tage / 30-Tage Verlaufsdiagramme
- Statistikvergleich Tages/Wochen/Monatsansicht
- Update-Hinweis bei verfügbarer neuer Version

### Automatische Update-Erkennung
- Prüft alle 6 Stunden die neueste GitHub-Version
- Sensor `lux_analytics_update` zeigt Status, Versionen und Release Notes
- Vorbereitet für HACS-Ein-Klick-Updates

### Konfiguration
- Config Flow: Einrichtung komplett über die HA-UI
- Options Flow: Nachträgliche Anpassung ohne Neuinstallation
- Einstellbar: Sensoren, Helligkeitsschwelle, Aktualisierungsintervall

### HACS-Unterstützung
- `hacs.json` und konforme Projektstruktur
- Semantische Versionierung
- GitHub-Release-Struktur für automatische HACS-Updates

---

## Technische Details

- Mindestanforderung: Home Assistant 2023.1.0
- Keine externen Python-Abhängigkeiten (aiohttp ist in HA enthalten)
- DataUpdateCoordinator für effizientes Polling
- HA-native Recorder-Integration für historische Daten
- Deutsche und englische Übersetzungen

---

## Erweiterungsvorbereitung

Die Architektur ist bereits vorbereitet für:
- Poolpumpensteuerung
- Beschattungssteuerung
- PV-Optimierung
- Sonnenstundenberechnung
- Temperaturintegration

---

## Installation

Siehe [Installationsanleitung](../../docs/installation.md)

---

## Bekannte Einschränkungen

- Helligkeitsklassen-Schwellwerte noch nicht über UI konfigurierbar (geplant für v0.2.0)
- Helle-Stunden-Berechnung basiert auf Polling-Häufigkeit (nicht exakter Zeitstempel)
- Dashboard Entity-IDs müssen manuell auf tatsächliche IDs angepasst werden
