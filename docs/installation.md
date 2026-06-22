# Installationsanleitung – Lux Analytics

## Voraussetzungen

- Home Assistant 2023.1.0 oder neuer
- `recorder`-Integration aktiv (Standardmäßig in HA)
- HACS (empfohlen) oder manueller Zugriff auf die HA-Konfigurationsdateien

---

## Installation via HACS (empfohlen)

### Schritt 1: Repository hinzufügen

1. HACS in der Seitenleiste öffnen
2. **Integrationen** auswählen
3. Oben rechts auf die drei Punkte (⋮) klicken → **Benutzerdefinierte Repositories**
4. URL eingeben: `https://github.com/choell/home-assistant-lux-analytics`
5. Kategorie: **Integration** auswählen
6. **Hinzufügen** klicken

### Schritt 2: Integration installieren

1. Im HACS-Bereich **Integrationen** nach **Lux Analytics** suchen
2. **Herunterladen** klicken
3. Home Assistant neu starten

### Schritt 3: Integration einrichten

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Nach **Lux Analytics** suchen
3. Konfigurationsassistenten folgen (siehe [Konfigurationsanleitung](configuration.md))

---

## Manuelle Installation

### Schritt 1: Dateien kopieren

Den Ordner `custom_components/lux_analytics/` aus diesem Repository in:

```
<your_ha_config>/custom_components/lux_analytics/
```

Die Verzeichnisstruktur muss so aussehen:

```
custom_components/
└── lux_analytics/
    ├── __init__.py
    ├── manifest.json
    ├── config_flow.py
    ├── coordinator.py
    ├── sensor.py
    ├── const.py
    ├── strings.json
    └── translations/
        ├── de.json
        └── en.json
```

### Schritt 2: Home Assistant neu starten

```bash
ha core restart
```

oder über die HA-Oberfläche: **Einstellungen** → **System** → **Neu starten**

### Schritt 3: Integration einrichten

Wie oben beschrieben.

---

## Dashboard installieren

1. `dashboards/lux_analytics_dashboard.yaml` in das HA-Konfigurationsverzeichnis kopieren
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

3. HA neu starten oder Lovelace über **Entwicklertools** neu laden

---

## Fehlerbehebung

### Integration wird nicht gefunden

- Sicherstellen, dass alle Dateien korrekt kopiert wurden
- HA-Logs prüfen: **Einstellungen** → **System** → **Protokolle**

### Keine Sensoren erkannt

- Prüfen ob Helligkeitssensoren vorhanden sind: **Entwicklertools** → **Zustände** → nach `device_class: illuminance` suchen
- Manuell einen Sensor in der Integrations-Konfiguration hinzufügen

### Statistiken zeigen "Unbekannt"

- Die Integration benötigt Verlaufsdaten aus dem Recorder
- Nach der Erstinstallation einige Stunden warten, bis Daten gesammelt wurden
