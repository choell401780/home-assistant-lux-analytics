# Installationsanleitung – Lux Analytics

## Voraussetzungen

- Home Assistant 2023.1.0 oder neuer
- [HACS](https://hacs.xyz) installiert und eingerichtet
- `recorder`-Integration aktiv (Standardmäßig in HA)

---

## Installation über HACS (einzige unterstützte Methode)

Lux Analytics wird ausschließlich über HACS installiert.
SSH, Samba-Freigaben oder manuelles Kopieren von Dateien sind **nicht erforderlich**.

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

### Schritt 3: Integration einrichten

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Nach **Lux Analytics** suchen und auswählen
3. Konfigurationsassistenten folgen:
   - Sensoren automatisch erkennen lassen **oder** manuell auswählen
   - Helligkeitsschwelle für helle Stunden festlegen (Standard: 1000 lx)
   - Aktualisierungsintervall wählen (Standard: 5 Minuten)
4. **Bestätigen** → Integration ist aktiv

---

## Dashboard einrichten (optional)

### Methode A: Als eigenes Dashboard

1. Datei `dashboards/lux_analytics_dashboard.yaml` aus dem HACS-Download-Verzeichnis
   in das HA-Konfigurationsverzeichnis kopieren — **oder** aus dem GitHub-Repository
   herunterladen und per Datei-Editor in HA hochladen.

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

3. HA neu starten oder Lovelace über **Entwicklertools** neu laden.

### Methode B: Karten in bestehendes Dashboard einfügen

Einzelne Karten aus der Dashboard-YAML-Datei per UI-Editor in ein bestehendes Dashboard kopieren.

---

## Fehlerbehebung

### Integration erscheint nicht unter "Integration hinzufügen"

- Sicherstellen, dass HA nach der HACS-Installation neu gestartet wurde
- HACS-Protokoll prüfen: **HACS** → **Protokolle**
- HA-Protokoll prüfen: **Einstellungen** → **System** → **Protokolle**

### Keine Sensoren werden erkannt

- Prüfen, ob Helligkeitssensoren in HA vorhanden sind:
  **Entwicklertools** → **Zustände** → nach `illuminance` filtern
- Im Integrations-Konfigurationsmenü Sensor manuell hinzufügen:
  **Einstellungen** → **Geräte & Dienste** → **Lux Analytics** → **Konfigurieren**

### Statistiken zeigen "Unbekannt"

- Der Recorder muss Verlaufsdaten für den Sensor haben
- Nach Erstinstallation mindestens einige Stunden warten
- Recorder-Konfiguration prüfen (`recorder:` in configuration.yaml oder Standard-Setup)
