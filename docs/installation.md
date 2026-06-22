# Installationsanleitung – Lux Analytics

## Voraussetzungen

- Home Assistant 2023.1.0 oder neuer
- [HACS](https://hacs.xyz) installiert und eingerichtet
- `recorder`-Integration aktiv (Standardmäßig in HA)

---

## Installation (vollständig über HACS)

Lux Analytics wird ausschließlich über HACS installiert.
SSH, Samba, Dateieditor oder manuelles Kopieren von Dateien sind **nicht erforderlich**.

### Schritt 1: Repository in HACS hinzufügen

1. Seitenleiste: **HACS** öffnen
2. **Integrationen** auswählen
3. Oben rechts: drei Punkte (⋮) → **Benutzerdefinierte Repositories**
4. URL eingeben:
   ```
   https://github.com/choell401780/home-assistant-lux-analytics
   ```
5. Kategorie: **Integration** auswählen
6. **Hinzufügen** klicken

### Schritt 2: Integration installieren

1. Im HACS-Bereich **Integrationen** nach **Lux Analytics** suchen
2. Karte anklicken → **Herunterladen** → Version bestätigen
3. Home Assistant neu starten

### Schritt 3: Sensor einrichten

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. Nach **Lux Analytics** suchen und auswählen
3. Helligkeitssensor aus Dropdown wählen
4. Optional: Name vergeben (z. B. Garten, Pool, Terrasse)
5. **Bestätigen** – fertig

---

## Dashboard einrichten (kein YAML nötig)

Nach der Installation erscheint **Lux Analytics** automatisch im Lovelace-Kartenpicker.

### Karte hinzufügen

1. Ein Dashboard öffnen und in den **Bearbeitungsmodus** wechseln
2. **Karte hinzufügen** klicken
3. Im Suchfeld **Lux Analytics** eingeben
4. **Lux Analytics** Card auswählen → **Hinzufügen**

Die Card zeigt sofort alle Daten des konfigurierten Sensors – ohne YAML, ohne Entity-IDs.

### Mehrere Sensoren

Wenn mehrere Lux Analytics Instanzen konfiguriert sind, erscheint beim Bearbeiten
der Card ein Dropdown zur Auswahl der gewünschten Instanz.

---

## Fehlerbehebung

### Integration erscheint nicht unter "Integration hinzufügen"

- Sicherstellen, dass HA nach der HACS-Installation **neu gestartet** wurde
- HACS-Protokoll prüfen: **HACS → Protokolle**
- HA-Protokoll prüfen: **Einstellungen → System → Protokolle**

### Card erscheint nicht im Kartenpicker

- HA einmal neu starten (Lovelace-Ressource wird beim ersten Start registriert)
- Sicherstellen, dass Lovelace im **Storage-Modus** läuft (nicht YAML-Modus)
- Im YAML-Modus: Ressource manuell in `configuration.yaml` eintragen:
  ```yaml
  lovelace:
    resources:
      - url: /lux-analytics/lux-analytics-card.js
        type: module
  ```

### Keine Sensoren werden erkannt

- Prüfen, ob Helligkeitssensoren in HA vorhanden sind:
  **Entwicklertools → Zustände** → nach `illuminance` filtern
- Im Integrations-Konfigurationsmenü Sensor manuell eingeben:
  **Einstellungen → Geräte & Dienste → Lux Analytics → Konfigurieren**

### Statistiken zeigen "—" oder "Unbekannt"

- Nach Erstinstallation mindestens einige Stunden warten (Recorder benötigt Verlaufsdaten)
- Recorder-Konfiguration prüfen (läuft standardmäßig in HA)
