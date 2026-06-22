# Konfigurationsanleitung – Lux Analytics

## Ersteinrichtung

Nach der Installation erscheint die Integration in **Einstellungen** → **Geräte & Dienste**.

### Schritt 1: Sensoren auswählen

**Option A: Automatische Erkennung (Standard)**

Die Integration erkennt automatisch alle Sensoren mit:
- `device_class: illuminance`
- Einheit `lx` oder `lux`
- Entity-IDs mit Schlüsselwörtern wie `lux`, `illuminance`, `hell`, `slo`

**Option B: Manuelle Auswahl**

`Sensoren automatisch erkennen` deaktivieren und Sensoren aus der Liste auswählen.

### Schritt 2: Helligkeitsschwelle

Standardwert: **1000 lx**

Dieser Wert bestimmt, ab wann eine Stunde als "helle Stunde" gezählt wird.
Empfehlungen:
- Innen: 300–500 lx
- Außen: 1000–5000 lx
- Sonnenstunden: 10000–25000 lx

### Schritt 3: Aktualisierungsintervall

Standardwert: **300 Sekunden (5 Minuten)**

Wie oft die Statistiken neu berechnet werden. Niedrigere Werte erhöhen die CPU-Last.

---

## Nachträgliche Konfiguration

1. **Einstellungen** → **Geräte & Dienste** → **Lux Analytics** → **Konfigurieren**
2. Sensoren anpassen, Schwellwert oder Intervall ändern
3. **Speichern**

Die Integration wird automatisch neu geladen.

---

## Helligkeitsklassen anpassen

In `custom_components/lux_analytics/const.py` die `BRIGHTNESS_CLASSES`-Liste anpassen:

```python
BRIGHTNESS_CLASSES = [
    {"name": "Nacht",        "min": 0,     "max": 1},
    {"name": "Dämmerung",    "min": 1,     "max": 100},
    # ... weitere Klassen
]
```

*(In einer zukünftigen Version werden diese Werte über die UI konfigurierbar sein.)*

---

## Mehrere Sensor-Gruppen

Mehrere Instanzen der Integration können hinzugefügt werden, z. B.:
- Eine für Außensensoren
- Eine für Innensensoren

Jede Instanz erhält einen eigenen Satz Statistik-Sensoren.

---

## Automationen

Alle erzeugten Sensoren können in HA-Automationen verwendet werden:

```yaml
automation:
  - alias: "Beschattung bei starker Sonne"
    trigger:
      - platform: numeric_state
        entity_id: sensor.sensor_name_aktuelle_helligkeit
        above: 30000
    action:
      - service: cover.close_cover
        target:
          entity_id: cover.markise
```
