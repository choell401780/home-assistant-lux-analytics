# Update-Anleitung – Lux Analytics

## Automatische Update-Erkennung

Lux Analytics prüft alle 6 Stunden, ob auf GitHub eine neue Version verfügbar ist.

### Update-Status prüfen

Der Sensor `sensor.lux_analytics_update` zeigt:
- `Aktuell` – die neueste Version ist installiert
- `Update verfügbar` – eine neue Version wurde auf GitHub veröffentlicht

Attribute des Sensors:
- `installed_version` – aktuell installierte Version
- `latest_version` – neueste verfügbare Version auf GitHub
- `release_notes` – Änderungsprotokoll der neuen Version
- `update_available` – `true` / `false`

---

## Update über HACS (empfohlen)

1. HACS öffnen → **Integrationen**
2. **Lux Analytics** suchen
3. **Aktualisieren** klicken
4. Home Assistant neu starten

---

## Manuelles Update

1. Neuste Version von GitHub herunterladen
2. Ordner `custom_components/lux_analytics/` ersetzen
3. Home Assistant neu starten

---

## Benachrichtigung bei Updates einrichten

Automation für automatische Benachrichtigung:

```yaml
automation:
  - alias: "Lux Analytics Update verfügbar"
    trigger:
      - platform: state
        entity_id: sensor.lux_analytics_update
        to: "Update verfügbar"
    action:
      - service: notify.notify
        data:
          title: "Lux Analytics Update"
          message: >
            Version {{ state_attr('sensor.lux_analytics_update', 'latest_version') }}
            ist verfügbar. Installiert: {{ state_attr('sensor.lux_analytics_update', 'installed_version') }}
```

---

## Versionsverlauf

Siehe [CHANGELOG.md](../CHANGELOG.md)
