# Home Assistant Lux Analytics

[![Version](https://img.shields.io/github/v/release/choell401780/home-assistant-lux-analytics?label=Version&color=blue)](https://github.com/choell401780/home-assistant-lux-analytics/releases/latest)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![HA min version](https://img.shields.io/badge/Home%20Assistant-2023.1.0%2B-brightgreen)](https://www.home-assistant.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/choell401780/home-assistant-lux-analytics)](https://github.com/choell401780/home-assistant-lux-analytics/issues)

**Automatische Erkennung, Analyse und Visualisierung von Helligkeitssensoren in Home Assistant.**

Lux Analytics ist eine vollständig lokale Custom Integration für Home Assistant, die Helligkeitssensoren (Lux) automatisch erkennt, historische Statistiken berechnet und ein sofort nutzbares Lovelace-Dashboard bereitstellt — ohne manuelle Konfiguration der Entity-IDs.

---

## Warum Lux Analytics?

Home Assistant zeigt Sensor-Rohdaten, bietet aber keine integrierte Lösung für:

- Tages-, Wochen- und Monatsstatistiken pro Helligkeitssensor
- Helligkeitsklassifizierung (Nacht bis Extreme Sonne)
- Sonnenstunden-Berechnung mit konfigurierbler Schwelle
- Trend-Analyse und Sonnenindex
- Fertige Dashboards ohne manuelle Entity-ID-Konfiguration

Lux Analytics schließt diese Lücke — vollständig lokal, HACS-installierbar, Plug-and-Play.

---

## Funktionsübersicht

| Funktion | Beschreibung |
|---|---|
| Automatische Sensorerkennung | Findet alle `device_class: illuminance` Sensoren |
| 8-stufige Klassifizierung | Nacht (0 lx) bis Extreme Sonne (>70.000 lx) |
| 19 Statistik-Sensoren | Min/Max/Avg pro Tag/Woche/Monat + mehr |
| Helle Stunden | Konfigurierbare Schwelle, Heute/Woche/Monat |
| Trend-Erkennung | Steigend / Fallend / Stabil (24h-Basis) |
| Sonnenindex | Normalisiert 0–100 % |
| Plug-and-Play Dashboard | Entity-IDs vorhersagbar — kein Bearbeiten nötig |
| HACS-Updates | Automatisch über HACS erkannt |
| Vollständig lokal | Keine Cloud außer HACS-Update-Check |

---

## Unterstützte Sensoren

Alle Sensoren mit `device_class: illuminance`, Unit `lx`/`lux`, oder `lux` im Entity-ID werden **automatisch erkannt**:

| Hersteller / Protokoll | Beispiel-Modell | Erkennung |
|---|---|---|
| **Homematic IP** | HmIP-SLO | Automatisch |
| Zigbee (ZHA/Z2M) | Aqara, IKEA, Philips Hue | Automatisch |
| Z-Wave | Fibaro, Aeotec | Automatisch |
| MQTT | Alle mit `lx`-Unit | Automatisch |
| ESPHome | BH1750, TSL2561 | Automatisch |
| Generic REST | Beliebig | Manuell wählbar |

### Homematic IP HmIP-SLO Beispiel

Der HmIP-SLO erzeugt in HA typischerweise Entity-IDs wie:
```
sensor.hmip_slo_<id>_illuminance
```
Diese werden von Lux Analytics automatisch erkannt (`illuminance` im Name + Unit `lx`).

---

## Helligkeitsklassifizierung

| Klasse | Bereich |
|---|---|
| Nacht | 0 – 1 lx |
| Dämmerung | 1 – 100 lx |
| Früher Morgen | 100 – 1.000 lx |
| Morgen | 1.000 – 10.000 lx |
| Tag | 10.000 – 30.000 lx |
| Sonnig | 30.000 – 50.000 lx |
| Pralle Sonne | 50.000 – 70.000 lx |
| Extreme Sonne | > 70.000 lx |

---

## Installation

### Voraussetzungen

- Home Assistant 2023.1.0 oder neuer
- [HACS](https://hacs.xyz) installiert

### Schritt 1 – Repository in HACS hinzufügen

1. **HACS** → **Integrationen** → drei Punkte (⋮) → **Benutzerdefinierte Repositories**
2. URL eingeben:
   ```
   https://github.com/choell401780/home-assistant-lux-analytics
   ```
3. Kategorie: **Integration** → **Hinzufügen**

### Schritt 2 – Integration installieren

1. HACS → Integrationen → nach **Lux Analytics** suchen
2. **Herunterladen** → Version bestätigen
3. **Home Assistant neu starten**

### Schritt 3 – Einrichten

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. **Lux Analytics** suchen und auswählen
3. Sensor aus Dropdown wählen (automatisch erkannte Sensoren werden angezeigt)
4. Optional: Bezeichnung eingeben (z. B. `Garten`)
5. **Bestätigen**

Kein SSH, kein Samba, kein Datei-Editor erforderlich.

---

## Erste Einrichtung – Details

### Sensor auswählen

Im Config Flow werden alle erkannten Helligkeitssensoren aufgelistet. Falls dein Sensor nicht erscheint, kann er manuell eingegeben werden (Freitexteingabe).

### Bezeichnung (optional)

Die Bezeichnung bestimmt die Entity-IDs:

| Bezeichnung | Entity-ID Beispiel |
|---|---|
| *(leer)* | `sensor.lux_analytics_aktuelle_helligkeit` |
| `Garten` | `sensor.lux_analytics_garten_aktuelle_helligkeit` |
| `Terrasse Pool` | `sensor.lux_analytics_terrasse_pool_aktuelle_helligkeit` |

**Empfehlung**: Ersten Sensor ohne Bezeichnung einrichten (Dashboard funktioniert sofort). Weitere Sensoren mit Bezeichnung.

### Mehrere Sensoren

Pro Sensor eine separate Integration-Instanz hinzufügen:
- **Einstellungen → Geräte & Dienste → Integration hinzufügen → Lux Analytics** (erneut)
- Zweiten Sensor und eine Bezeichnung wählen

---

## Dashboard

Das mitgelieferte Dashboard `dashboards/lux_analytics_dashboard.yaml` funktioniert **ohne Anpassungen** für den ersten (unbezeichneten) Sensor.

### Installation

1. Datei in das HA-Konfigurationsverzeichnis kopieren (per HACS-Download verfügbar)
2. In `configuration.yaml` eintragen:

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

3. HA neu starten

### Dashboard-Ansichten

| Ansicht | Inhalt |
|---|---|
| Übersicht | Aktueller Wert, Status, Trend, Sonnenindex |
| Tagesansicht | 24h-Diagramm + Min/Max/Avg/Helle Std. |
| Wochenansicht | 7-Tage-Diagramm + Statistiken |
| Monatsansicht | 30-Tage-Diagramm + Statistiken |
| Statistiken | HA-native Statistikgraphen |

---

## Erzeugte Entitäten

Pro überwachtem Sensor werden 19 Entitäten erstellt:

```
sensor.lux_analytics_aktuelle_helligkeit     # Aktueller Lux-Wert
sensor.lux_analytics_helligkeitsstatus       # Nacht / Tag / Sonnig / ...
sensor.lux_analytics_helligkeitstrend        # Steigend / Fallend / Stabil
sensor.lux_analytics_sonnenindex             # 0–100 %
sensor.lux_analytics_tagesminimum            # Min heute
sensor.lux_analytics_tagesmaximum            # Max heute
sensor.lux_analytics_tagesdurchschnitt       # Ø heute
sensor.lux_analytics_wochenminimum           # Min diese Woche
sensor.lux_analytics_wochenmaximum           # Max diese Woche
sensor.lux_analytics_wochendurchschnitt      # Ø diese Woche
sensor.lux_analytics_monatsminimum           # Min diesen Monat
sensor.lux_analytics_monatsmaximum           # Max diesen Monat
sensor.lux_analytics_monatsdurchschnitt      # Ø diesen Monat
sensor.lux_analytics_helle_stunden_heute     # Helle Stunden heute
sensor.lux_analytics_helle_stunden_woche     # Helle Stunden Woche
sensor.lux_analytics_helle_stunden_monat     # Helle Stunden Monat
sensor.lux_analytics_durchschnitt_24h        # Ø letzte 24h
sensor.lux_analytics_durchschnitt_7_tage     # Ø letzte 7 Tage
sensor.lux_analytics_durchschnitt_30_tage    # Ø letzte 30 Tage
```

---

## Updates

Updates werden automatisch über HACS erkannt und angezeigt.

**Update durchführen:**
1. HACS → Integrationen → Lux Analytics → **Aktualisieren**
2. Home Assistant neu starten

---

## Konfigurationsoptionen

| Option | Standard | Beschreibung |
|---|---|---|
| Helligkeitsschwelle | 1.000 lx | Schwelle für helle Stunden |
| Aktualisierungsintervall | 300 s | Polling-Intervall (60–3.600 s) |

Änderbar unter: **Einstellungen → Geräte & Dienste → Lux Analytics → Konfigurieren**

---

## Roadmap

Siehe [ROADMAP.md](ROADMAP.md) für geplante Versionen:

- **v0.4.0** – Konfigurierbare Helligkeitsgrenzen, Umlaut-Normalisierung
- **v0.5.0** – Heatmaps, erweiterte Diagramme
- **v0.6.0** – Pool & Beschattungs-Modul Vorbereitung
- **v1.0.0** – Produktiv-Release

---

## Bekannte Einschränkungen

| Einschränkung | Geplante Lösung |
|---|---|
| Umlaute in Labels → z. B. `ü` → `_` | v0.4.0: Umlaut-Normalisierung |
| Helligkeitsklassen nicht über UI konfigurierbar | v0.4.0 |
| Helle-Stunden-Berechnung Polling-basiert (±1 min) | v0.5.0: Zeitstempel-basiert |
| Dashboard für Sensor Nr. 2+ braucht manuelle Kopie | v0.5.0: Multi-View |

---

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/choell401780/home-assistant-lux-analytics/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/choell401780/home-assistant-lux-analytics/discussions)
- **Fehler melden**: [Bug Report](https://github.com/choell401780/home-assistant-lux-analytics/issues/new)

---

## Mitwirken

Beiträge sind willkommen! Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

---

## Lizenz

MIT – siehe [LICENSE](LICENSE)

---

## Danksagung

Inspiriert von der Home Assistant Community und dem HA Core-Team für die exzellente Custom-Integration-API.
