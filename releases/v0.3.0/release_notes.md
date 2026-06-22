# Release Notes – v0.3.0

**Veröffentlicht:** 2026-06-22

## HACS-Readiness & Plug-and-Play Dashboard

---

## Highlights

### Dashboard funktioniert sofort nach Installation

Nach dem Update auf v0.3.0 muss das Dashboard **nie mehr manuell bearbeitet** werden.

Die Integration erzeugt jetzt vorhersagbare Entity-IDs:

| Sensor-Key       | Entity-ID (kein Label)                       |
|------------------|----------------------------------------------|
| Aktuelle Helligkeit | `sensor.lux_analytics_aktuelle_helligkeit` |
| Tagesminimum     | `sensor.lux_analytics_tagesminimum`          |
| Tagesmaximum     | `sensor.lux_analytics_tagesmaximum`          |
| … (alle 19 Sensoren) | … predictable slugs                      |

Mit Label "Garten":

| Entity-ID |
|-----------|
| `sensor.lux_analytics_garten_aktuelle_helligkeit` |
| `sensor.lux_analytics_garten_tagesminimum` |

Das mitgelieferte Dashboard `lux_analytics_dashboard.yaml` funktioniert für den ersten
(ungelabelten) Sensor sofort ohne Änderungen.

---

## HACS-Readiness Fixes

### manifest.json bereinigt
Leere Arrays `"requirements": []` und `"dependencies": []` entfernt.
Diese verursachten eine Warnung beim HACS-Validator — jetzt sauber.

### Release-Workflow robuster
- Verifiziert dass `VERSION`-Datei und Git-Tag übereinstimmen
- Fallback-Release-Notes wenn keine Datei vorhanden
- Korrekte Auflösung des `body_path` Parameters

---

## Architekturänderung: Ein Sensor pro Config Entry

### Vorher (v0.2.0)
- Eine Config Entry konnte mehrere Sensoren verwalten
- Sensor-Entity-IDs enthielten die variable Source-Entity-ID
- Dashboard musste manuell angepasst werden

### Jetzt (v0.3.0)
- **Eine Config Entry = ein Source-Sensor**
- Entity-IDs sind vorhersagbar und stabil
- Für mehrere Sensoren: mehrere Integration-Instanzen (HA-Standardprinzip)
- Jede Instanz erhält optional ein Label für die Entity-IDs

### Vorteile des neuen Ansatzes
- Plug-and-Play Dashboard
- Unabhängiges Reload/Reconfigure pro Sensor
- Verschiedene Polling-Intervalle pro Sensor möglich
- Klares 1:1 Verhältnis: eine Instanz, ein Gerät, ein Dashboard-View
- Config Entry hat unique_id → keine doppelten Einträge möglich

---

## Config Flow Verbesserungen

- Sensor-Dropdown mit Freitexteingabe als Fallback
- Numerische Slider für Schwellwert (0–200.000 lx) und Intervall (60–3.600 s)
- Beschreibung zeigt Beispiel der resultierenden Entity-ID
- Options Flow zeigt Hinweis dass Source-Sensor nicht änderbar ist

---

## Migration von v0.2.0

1. Integration entfernen: **Einstellungen → Geräte & Dienste → Lux Analytics → Löschen**
2. Neu hinzufügen: **Integration hinzufügen → Lux Analytics**
3. Einen Sensor auswählen
4. Bei Bedarf ein Label vergeben (leer lassen für Standard-Dashboard)
5. Für weitere Sensoren: Schritt 2–4 wiederholen

---

## Installationsanleitung

Ausschließlich über HACS. Kein SSH, kein Samba, kein manuelles Kopieren.

Siehe [docs/installation.md](../../docs/installation.md)
