# Release Notes – v0.4.0

**Veröffentlicht:** 2026-06-22

## Custom Lovelace Card – Vollständiges Plug-and-Play

---

## Das ist neu

### Lux Analytics Card – erscheint automatisch in "Karte hinzufügen"

Nach dem Update auf v0.4.0 erscheint **Lux Analytics** im Lovelace Kartenpicker:

**Einstellungen → Dashboards → Bearbeiten → Karte hinzufügen → Lux Analytics**

Kein YAML. Kein Datei-Import. Keine Entity-IDs eintragen.

---

### Was die Card zeigt

| Element | Beschreibung |
|---|---|
| **Lux-Wert (groß)** | Aktueller Messwert, k-Notation ab 10.000 lx |
| **Status-Badge** | Farbige Helligkeitsklasse (Nacht → Extreme Sonne) |
| **Trend-Pfeil** | ↑ Steigend / ↓ Fallend / → Stabil |
| **Sonnenindex-Balken** | 0–100 %, Farbe von Blau (tief) bis Rot (hoch) |
| **Tages-Grid** | Min / Max / Ø des heutigen Tages |
| **Rollierende Ø** | 24h / 7 Tage / 30 Tage Durchschnitt |
| **Helle Stunden** | Heute und diese Woche |
| **Periode** | Wochen- und Monatsdurchschnitt |

---

### Mehrere Sensoren

Wenn mehrere Lux Analytics Instanzen konfiguriert sind (z. B. Garten, Terrasse, Pool),
erscheint beim Bearbeiten der Card ein Dropdown zur Auswahl der gewünschten Instanz.

---

### Umlaut-Support für Labels

Labels mit Umlauten werden jetzt korrekt in Entity-IDs umgewandelt:

| Label | Entity-ID Prefix |
|---|---|
| `Süd-Pool` | `sensor.lux_analytics_sued_pool_` |
| `Terrasse Süd` | `sensor.lux_analytics_terrasse_sued_` |
| `Gärtnerei` | `sensor.lux_analytics_gaertnerei_` |

---

## Migration von v0.3.0

**Keine Breaking Changes.** Alle bestehenden Entity-IDs bleiben unverändert.

1. HACS: **Aktualisieren** auf v0.4.0
2. Home Assistant neu starten
3. Nach dem Neustart erscheint die Card automatisch im Kartenpicker
4. Alte YAML-Dashboard-Datei kann weiterhin verwendet werden

**Hinweis:** Bei Labeln mit Umlauten die Instanz einmal entfernen und neu anlegen,
damit die korrekten Entity-IDs erzeugt werden. Bei ASCII-Labels (Garten, Pool, etc.)
ist keine Aktion erforderlich.

---

## Technische Details

- JavaScript Card in Shadow DOM – kein CSS-Konflikt mit HA-Themes
- Lovelace-Ressource wird automatisch beim ersten HA-Start registriert
- Funktioniert mit Light-Mode, Dark-Mode und allen HA-Themes
- Keine externen JavaScript-Abhängigkeiten
- Kompatibel mit Home Assistant 2023.1.0+
