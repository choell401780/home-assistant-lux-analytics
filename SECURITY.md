# Security Policy

## Unterstützte Versionen

Sicherheitsupdates werden für die aktuelle Hauptversion bereitgestellt.

| Version | Unterstützt        |
|---------|--------------------|
| 0.3.x   | ✅ Ja              |
| 0.2.x   | ❌ Nein            |
| 0.1.x   | ❌ Nein            |

## Sicherheitslücken melden

**Bitte keine Sicherheitslücken als öffentliches Issue melden.**

Sicherheitslücken bitte per E-Mail an:
**christian.hendrik.hoell@googlemail.com**

Bitte folgende Informationen mitteilen:
- Art der Sicherheitslücke
- Betroffene Versionen
- Schritte zur Reproduktion
- Mögliche Auswirkungen
- Vorschlag zur Behebung (optional)

## Sicherheitsüberlegungen

Lux Analytics:
- Läuft vollständig lokal innerhalb des Home Assistant Netzwerks
- Verwendet keine Cloud-Dienste (außer optionaler GitHub-Update-Check durch HACS)
- Verarbeitet nur Sensor-Daten aus dem lokalen HA-Recorder
- Speichert keine Anmeldedaten
- Benötigt keine Port-Weiterleitungen oder externe Erreichbarkeit
