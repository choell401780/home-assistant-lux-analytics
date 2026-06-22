# Update-Anleitung – Lux Analytics

## Updates über HACS

Lux Analytics-Updates werden vollständig über HACS verwaltet.
**Kein manueller Eingriff ins Dateisystem erforderlich.**

### Update-Erkennung

HACS überwacht automatisch das GitHub-Repository und vergleicht:
- Die installierte Version (aus `manifest.json`)
- Die neueste verfügbare Version (aus GitHub Releases)

Wenn eine neue Version veröffentlicht wird, erscheint:
1. Ein Benachrichtigungs-Badge auf dem HACS-Symbol in der Seitenleiste
2. Eine Update-Karte unter **HACS** → **Integrationen**
3. Ein Hinweis in der Home Assistant Benachrichtigungsleiste (über die native HA Update-Integration)

### Update durchführen

1. **HACS** → **Integrationen** öffnen
2. **Lux Analytics** in der Liste der verfügbaren Updates suchen
3. **Aktualisieren** klicken
4. Änderungen bestätigen
5. Home Assistant neu starten

---

## Automatische Benachrichtigung einrichten

Um per HA-Benachrichtigung über Updates informiert zu werden:

```yaml
automation:
  - alias: "HACS Update verfügbar"
    trigger:
      - platform: state
        entity_id: sensor.hacs
        attribute: repositories
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.hacs', 'repositories') | selectattr('display_name', 'eq', 'Lux Analytics') | list | count > 0 }}
    action:
      - service: notify.notify
        data:
          title: "Lux Analytics Update"
          message: "Eine neue Version von Lux Analytics ist in HACS verfügbar."
```

---

## Warum kein eigener Update-Sensor?

Ab v0.2.0 wurde die eigene GitHub-API-Update-Prüfung **vollständig entfernt**.

**Begründung:**
- HACS übernimmt exakt diese Aufgabe nativ und zuverlässiger
- HACS liefert eine HA-native Update-Entity für jede verwaltete Integration
- Eigene GitHub-API-Abfragen erzeugen unnötigen Netzwerkverkehr
- Die HACS-Update-Anzeige ist in die Standard-HA-Oberfläche integriert
- Kein redundanter Code, weniger Wartungsaufwand

---

## Versionshistorie

Siehe [CHANGELOG.md](../CHANGELOG.md)
