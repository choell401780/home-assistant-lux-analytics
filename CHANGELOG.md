# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

---

## [0.4.0] – 2026-06-22

### Custom Lovelace Card – Plug-and-Play ohne YAML

#### Neue Lovelace Card (lux-analytics-card)
- **Automatische Installation**: Card wird als Lovelace-Ressource beim ersten HA-Start registriert
- **"Karte hinzufügen"**: Card erscheint im UI-Kartenpicker ohne jede YAML-Konfiguration
- **Auto-Discovery**: Card findet lux_analytics-Instanzen selbstständig
- **GUI-Editor**: Bei mehreren Instanzen Dropdown-Auswahl im Card-Konfigurationsdialog
- **Shadow DOM**: Vollständige Style-Isolation, kein CSS-Konflikt mit HA-Themes
- **HA-Theming**: Nutzt HA CSS-Variablen – funktioniert mit Light/Dark Mode automatisch

#### Card-Inhalt (alle Werte live)
- Aktueller Lux-Wert (Hero-Display, kompakt formatiert: k-Notation ab 10.000 lx)
- Helligkeitsstatus als Farbige Badge (8 Klassen, kontrastgerecht)
- Trend-Pfeil (↑/↓/→) in kontrastierender Farbe
- Sonnenindex-Balken mit Farbgradient (blau→orange→rot)
- Tages-Min/Max/Durchschnitt als 3-spaltige Stat-Grid
- Rollierende Durchschnitte (24h / 7 Tage / 30 Tage)
- Helle Stunden heute und diese Woche
- Wochen- und Monatsdurchschnitt als Footer

#### Technische Umsetzung
- `custom_components/lux_analytics/www/lux-analytics-card.js` – Self-contained JS Card
- `async_setup()` in `__init__.py` registriert statischen Pfad `/lux-analytics/`
- Lovelace-Ressource wird beim Event `homeassistant_started` automatisch eingetragen
- Fallback: bei YAML-Lovelace-Modus wird Registrierung übersprungen (kein Fehler)
- `window.customCards` Eintrag für HA-Kartenpicker mit Vorschau-Flag

#### Umlaut-Normalisierung (Labels)
- `build_entity_id()` konvertiert Umlaute: ä→ae, ö→oe, ü→ue, ß→ss
- Label "Süd-Pool" erzeugt jetzt `sensor.lux_analytics_sued_pool_aktuelle_helligkeit`
- Keine manuellen ASCII-Umbenennungen mehr nötig

---

## [0.3.0] – 2026-06-22

### HACS-Readiness & Plug-and-Play Dashboard

#### HACS-Korrekturen
- `manifest.json`: Leere Arrays `requirements` und `dependencies` entfernt (HACS-Validation-Warnung behoben)
- `release.yml`: Robuster Release-Workflow — VERSION-File vs. Tag-Prüfung, Fallback-Release-Notes, korrektes Body-Path-Handling
- Vollständige HACS-Readiness-Prüfung dokumentiert und alle Punkte adressiert

#### Architektur: Ein Sensor pro Config Entry
- `config_flow.py`: Umgebaut auf **einen Source-Sensor** pro Config Entry + optionalem Label
- Config Entry erhält `unique_id` = `lux_analytics_{source_sensor}` → verhindert doppelte Einträge
- Entry-Titel: "Lux Analytics – {Label}" oder "Lux Analytics ({sensor_name})"
- `CONF_SOURCE_SENSOR` und `CONF_SENSOR_LABEL` ersetzen altes `CONF_AUTO_DISCOVER` + `CONF_SENSORS`
- `coordinator.py`: Vereinfacht auf single-source — `source_entity_id` statt `sensor_ids` Liste
- `discover_illuminance_sensors()` als eigenständige Modul-Funktion (wiederverwendbar)

#### Plug-and-Play Dashboard
- `sensor.py`: `self.entity_id` wird direkt gesetzt → **vorhersagbare Entity-IDs**
- Schema ohne Label: `sensor.lux_analytics_aktuelle_helligkeit` (Dashboard funktioniert sofort)
- Schema mit Label "garten": `sensor.lux_analytics_garten_aktuelle_helligkeit`
- `build_entity_id()` Hilfsfunktion in `const.py` zentralisiert die ID-Logik
- `ENTITY_ID_SLUGS` Mapping: sensor_key → deutschen Slug
- Dashboard-YAML muss **nicht mehr bearbeitet werden** nach der Installation

#### Config Flow Verbesserungen
- Sensor-Dropdown mit `custom_value=True` → manuelle Eingabe wenn Sensor nicht erkannt
- `NumberSelector` für Schwellwert und Intervall (statt freies Textfeld)
- Options Flow zeigt Hinweis, dass Source-Sensor nicht änderbar ist
- Beschreibung im Config Flow zeigt Beispiel-Entity-ID

#### Translations
- `strings.json`, `de.json`, `en.json`: Neue Felder `source_sensor` und `sensor_label`
- `abort.already_configured` Nachricht für doppelte Sensor-Einträge

### Migration von v0.2.0
Da v0.2.0 mehrere Sensoren pro Entry erlaubte, muss nach dem Update die Integration
neu eingerichtet werden: Integration entfernen → neu hinzufügen → einen Sensor wählen.
Pro zusätzlichem Sensor eine weitere Integration-Instanz hinzufügen.

---

## [0.2.0] – 2026-06-22

### Architektur
- **Entfernt**: Eigene GitHub-API-Update-Prüfung – vollständig durch HACS ersetzt
- **Entfernt**: `UpdateAvailableSensor` – HACS liefert native Update-Entität
- **Entfernt**: `GITHUB_REPO`-Konstante und `GITHUB_RELEASES_URL` (nicht mehr benötigt)
- **Entfernt**: `aiohttp`-Import aus Coordinator (keine externen HTTP-Calls mehr)
- **Entfernt**: Nicht verwendeter `statistics_during_period`-Import
- **Entfernt**: Nicht verwendeter `UpdateFailed`-Import

### Neu
- `info.md` für HACS-Store-Anzeige
- HACS-Validierungs-Job in GitHub Actions CI (`hacs/action`)

### Geändert
- Dashboard: Update-Sensor-Karte entfernt (Update-Hinweise kommen von HACS)
- Dokumentation: Installation und Update-Anleitung auf HACS-only umgeschrieben
- Coordinator: vereinfacht und bereinigt (keine GitHub-Netzwerk-Calls)

### Migration von v0.1.0
Kein manueller Eingriff nötig. HACS installiert die neue Version automatisch.
Der `sensor.lux_analytics_update`-Sensor wird nach dem Update und HA-Neustart
automatisch entfernt.

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
