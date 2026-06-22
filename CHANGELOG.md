# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

---

## [0.1.0] – 2026-06-22

### Neu
- Automatische Erkennung aller Helligkeitssensoren (device_class, unit, entity_id)
- Unterstützung für Homematic IP HmIP-SLO, Zigbee, Z-Wave und MQTT Sensoren
- Custom Integration mit Config Flow (UI-Einrichtung)
- Options Flow für nachträgliche Konfigurationsänderung
- Helligkeitsklassifizierung (8 Stufen: Nacht bis Extreme Sonne)
- Statistik-Sensoren: Tages-, Wochen- und Monats-Min/Max/Avg
- Helle Stunden: Heute, Woche, Monat
- Durchschnittssensoren: 24h, 7 Tage, 30 Tage
- Trend-Erkennung (Steigend / Fallend / Stabil)
- Sonnenindex (0–100 %)
- Automatische GitHub-Versionsprüfung (alle 6 Stunden)
- Update-Sensor mit Anzeige in der HA-Oberfläche
- Lovelace Dashboard (Übersicht, Tages-, Wochen-, Monatsansicht, Statistiken)
- HACS-konforme Projektstruktur
- Deutsche und englische Übersetzungen
- Vollständige Dokumentation (Installation, Konfiguration, Dashboard, FAQ, Entwicklung)

### Architektur
- Entscheidung für Variante C (Hybrid): Custom Integration + HA-native Statistics + Dashboard
- DataUpdateCoordinator für effizientes Polling
- Erweiterungsvorbereitung für Pool-, PV- und Beschattungsautomation

### Technisch
- Mindestanforderung: Home Assistant 2023.1.0
- Keine externen Python-Abhängigkeiten außer aiohttp (bereits in HA enthalten)
- HACS-ready: hacs.json, manifest.json, semantische Versionierung

---

## [Unveröffentlicht]

*Änderungen in Entwicklung werden hier gesammelt.*
