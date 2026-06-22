# Statistiken – Lux Analytics

## Überblick

Lux Analytics berechnet für jeden überwachten Sensor 19 Statistik-Entitäten.
Die Grundlage sind historische Daten aus dem HA-Recorder.

---

## Entitäten im Detail

### Echtzeitwerte

| Entität | Beschreibung | Update |
|---|---|---|
| `aktuelle_helligkeit` | Direkter Wert des Source-Sensors in lx | Sofort bei State-Change |
| `helligkeitsstatus` | Helligkeitsklasse als Text | Mit Coordinator-Update |
| `helligkeitstrend` | Steigend / Fallend / Stabil | Mit Coordinator-Update |
| `sonnenindex` | 0–100 % (0 lx = 0 %, 100.000 lx = 100 %) | Mit Coordinator-Update |

### Tagesstatistiken

Zeitraum: Tagesbeginn 00:00 Uhr bis aktueller Moment.

| Entität | Beschreibung |
|---|---|
| `tagesminimum` | Niedrigster Lux-Wert heute |
| `tagesmaximum` | Höchster Lux-Wert heute |
| `tagesdurchschnitt` | Arithmetisches Mittel heute |
| `helle_stunden_heute` | Stunden über Helligkeitsschwelle |

### Wochenstatistiken

Zeitraum: Montag 00:00 Uhr bis aktueller Moment.

| Entität | Beschreibung |
|---|---|
| `wochenminimum` | Niedrigster Lux-Wert diese Woche |
| `wochenmaximum` | Höchster Lux-Wert diese Woche |
| `wochendurchschnitt` | Arithmetisches Mittel diese Woche |
| `helle_stunden_woche` | Stunden über Schwelle diese Woche |

### Monatsstatistiken

Zeitraum: Monatserster 00:00 Uhr bis aktueller Moment.

| Entität | Beschreibung |
|---|---|
| `monatsminimum` | Niedrigster Lux-Wert diesen Monat |
| `monatsmaximum` | Höchster Lux-Wert diesen Monat |
| `monatsdurchschnitt` | Arithmetisches Mittel diesen Monat |
| `helle_stunden_monat` | Stunden über Schwelle diesen Monat |

### Gleitende Durchschnitte

| Entität | Zeitraum |
|---|---|
| `durchschnitt_24h` | Letzte 24 Stunden (rollend) |
| `durchschnitt_7_tage` | Letzte 7 Tage (rollend) |
| `durchschnitt_30_tage` | Letzte 30 Tage (rollend) |

---

## Helligkeitsklassifizierung

| Klasse | Minimum | Maximum | Typische Situation |
|---|---|---|---|
| Nacht | 0 lx | 1 lx | Mondlicht, Sternen |
| Dämmerung | 1 lx | 100 lx | Sonnenauf-/-untergang |
| Früher Morgen | 100 lx | 1.000 lx | Bedeckt, Morgengrauen |
| Morgen | 1.000 lx | 10.000 lx | Trüber Tag |
| Tag | 10.000 lx | 30.000 lx | Bewölkter Tag |
| Sonnig | 30.000 lx | 50.000 lx | Teils sonnig |
| Pralle Sonne | 50.000 lx | 70.000 lx | Direktes Sonnenlicht |
| Extreme Sonne | 70.000 lx | ∞ | Hochsommer, Mittag |

---

## Helligkeitsschwelle (helle Stunden)

Die Schwelle ist konfigurierbar (Standard: 1.000 lx).

**Empfehlungen:**

| Verwendungszweck | Empfehlung |
|---|---|
| Innenräume | 300–500 lx |
| Pflanzen (UV-Bedarf) | 2.000–5.000 lx |
| Allgemeine Helligkeit (außen) | 1.000–3.000 lx |
| Sonnenstunden (PV) | 10.000–25.000 lx |
| Beschattungssteuerung | 30.000–50.000 lx |

---

## Sonnenindex

```
Sonnenindex = min(round((lux / 100.000) × 100, 1), 100.0)
```

| Sonnenindex | Lux-Bereich |
|---|---|
| 0–1 % | 0–1.000 lx |
| 10 % | ~10.000 lx |
| 30 % | ~30.000 lx |
| 50 % | ~50.000 lx |
| 100 % | ≥ 100.000 lx |

---

## Trend-Berechnung

```python
avg_24h = Arithmetisches Mittel der letzten 24h
delta = aktueller_wert - avg_24h

if delta > avg_24h × 0.15:  → "Steigend"
if delta < avg_24h × -0.15: → "Fallend"
else:                        → "Stabil"
```

Toleranzbereich: ±15 % des 24h-Durchschnitts.
Mindestanzahl Messwerte für Trend: 10 (sonst "Stabil").

---

## Datengenauigkeit

| Aspekt | Genauigkeit |
|---|---|
| Min/Max/Avg | Exakt (alle State-Changes im Recorder) |
| Helle Stunden | ±Polling-Intervall/60 Stunden |
| Trend | Qualitativ (±15 % Toleranz) |
| Sonnenindex | Auf 0,1 % gerundet |

---

## Automationen mit Statistiken

Alle Sensoren können in HA-Automationen verwendet werden:

```yaml
# Beispiel: Beschattung bei starker Sonne
automation:
  - alias: "Markise ausfahren"
    trigger:
      - platform: numeric_state
        entity_id: sensor.lux_analytics_aktuelle_helligkeit
        above: 30000
        for: "00:10:00"
    action:
      - service: cover.close_cover
        target:
          entity_id: cover.markise

# Beispiel: Benachrichtigung bei sonnigem Tag
automation:
  - alias: "Sonniger Tag Hinweis"
    trigger:
      - platform: state
        entity_id: sensor.lux_analytics_helligkeitsstatus
        to: "Sonnig"
    action:
      - service: notify.notify
        data:
          message: >
            Sonniger Tag! Aktuell {{ states('sensor.lux_analytics_aktuelle_helligkeit') }} lx.
            Tagesdurchschnitt: {{ states('sensor.lux_analytics_tagesdurchschnitt') }} lx.
```
