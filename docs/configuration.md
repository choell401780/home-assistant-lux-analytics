# Konfigurationsanleitung – Lux Analytics

## Ersteinrichtung via Config Flow

### Schritt 1: Integration hinzufügen

**Einstellungen → Geräte & Dienste → Integration hinzufügen → Lux Analytics**

### Schritt 2: Sensor auswählen

Im Dropdown erscheinen alle automatisch erkannten Helligkeitssensoren.

**Erkennungskriterien:**
- `device_class: illuminance`
- `unit_of_measurement: lx` oder `lux`
- Entity-ID enthält: `lux`, `illuminance`, `brightness`, `light`, `helligkeit`, `slo`

Falls dein Sensor nicht erscheint: Entity-ID direkt eingeben (Freitexteingabe).

### Schritt 3: Bezeichnung (optional)

Die Bezeichnung bestimmt das Prefix der Entity-IDs.

| Bezeichnung | Prefix | Beispiel Entity-ID |
|---|---|---|
| *(leer)* | `lux_analytics` | `sensor.lux_analytics_aktuelle_helligkeit` |
| `Garten` | `lux_analytics_garten` | `sensor.lux_analytics_garten_aktuelle_helligkeit` |
| `Sued Pool` | `lux_analytics_sued_pool` | `sensor.lux_analytics_sued_pool_aktuelle_helligkeit` |

**Empfehlung:**
- Ersten Sensor: Bezeichnung leer lassen → Dashboard funktioniert sofort
- Weitere Sensoren: aussagekräftige ASCII-Bezeichnung wählen (keine Umlaute bis v0.4.0)

### Schritt 4: Helligkeitsschwelle

Standard: **1.000 lx**

Legt fest, ab wann eine Stunde als "helle Stunde" gezählt wird.

| Zweck | Empfehlung |
|---|---|
| Allgemeine Helligkeit | 500–1.000 lx |
| Pflanzenlicht | 2.000–5.000 lx |
| Sonnenstunden (PV) | 10.000–25.000 lx |
| Beschattungsauslöser | 30.000–50.000 lx |

### Schritt 5: Aktualisierungsintervall

Standard: **300 Sekunden (5 Minuten)**

Wie oft die Statistiken neu berechnet werden.

| Intervall | Empfehlung |
|---|---|
| 60 s | Sehr präzise, höhere CPU-Last |
| 300 s | Standard-Empfehlung |
| 600 s | Ressourcenschonend |

---

## Nachträgliche Konfiguration (Options Flow)

**Einstellungen → Geräte & Dienste → Lux Analytics → Konfigurieren**

Änderbar:
- Helligkeitsschwelle
- Aktualisierungsintervall

Nicht änderbar (Integration entfernen und neu hinzufügen):
- Source-Sensor
- Bezeichnung/Label

---

## Mehrere Sensoren

Pro Sensor eine separate Integration-Instanz:

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Lux Analytics**
2. Zweiten Sensor und eine Bezeichnung wählen
3. Separate Statistik-Sensoren werden erstellt

Der erste Sensor (ohne Bezeichnung) funktioniert mit dem Standard-Dashboard.
Für weitere Sensoren das Dashboard duplizieren und Entity-IDs anpassen.

---

## Automationen mit Lux Analytics

```yaml
# Helligkeitsabhängige Beschattung
automation:
  - alias: "Beschattung bei Sonne"
    trigger:
      platform: numeric_state
      entity_id: sensor.lux_analytics_aktuelle_helligkeit
      above: 30000
      for: "00:05:00"
    action:
      service: cover.close_cover
      target:
        entity_id: cover.markise

# Tagesstatistik-Benachrichtigung
automation:
  - alias: "Tagesbericht Helligkeit"
    trigger:
      platform: time
      at: "21:00:00"
    action:
      service: notify.notify
      data:
        title: "Tagesbericht Lux"
        message: >
          Max: {{ states('sensor.lux_analytics_tagesmaximum') }} lx |
          Ø: {{ states('sensor.lux_analytics_tagesdurchschnitt') }} lx |
          Helle Stunden: {{ states('sensor.lux_analytics_helle_stunden_heute') }} h
```
