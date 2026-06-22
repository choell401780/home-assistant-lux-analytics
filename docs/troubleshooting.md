# Fehlerbehebung – Lux Analytics

## Integration erscheint nicht unter "Integration hinzufügen"

**Ursache**: Dateien nicht korrekt installiert oder HA nicht neu gestartet.

**Lösung**:
1. HACS → Integrationen → Lux Analytics → Status prüfen
2. Sicherstellen dass HA nach der HACS-Installation neu gestartet wurde
3. HA-Protokoll prüfen: **Einstellungen → System → Protokolle**
4. Nach `lux_analytics` suchen

---

## Keine Sensoren im Dropdown des Config Flow

**Ursache**: Noch keine Helligkeitssensoren in HA registriert, oder die Sensoren haben kein erkennbares Format.

**Lösung**:
1. Prüfen ob Sensoren in HA vorhanden: **Entwicklertools → Zustände**
2. Nach `illuminance` oder `lx` filtern
3. Falls Sensor vorhanden aber nicht im Dropdown: Entity-ID direkt eingeben (Freitexteingabe im Dropdown)
4. Mindestanforderung: `unit_of_measurement: lx` oder `device_class: illuminance`

---

## Statistiken zeigen "Unbekannt" (None)

**Ursache**: Keine Verlaufsdaten im Recorder vorhanden.

**Lösung**:
1. Mindestens einige Stunden warten nach der Erstinstallation
2. Recorder-Status prüfen: **Entwicklertools → Template**:
   ```
   {{ states | selectattr('entity_id', 'eq', 'sensor.DEIN_SENSOR') | list }}
   ```
3. Sicherstellen dass der Source-Sensor aktiv Werte sendet
4. Recorder-Konfiguration prüfen (Standard-HA hat Recorder aktiv)

---

## Dashboard zeigt keine Daten

**Ursache A**: Dashboard-Entity-IDs passen nicht zu den tatsächlichen Entitäten.

**Diagnose**: **Entwicklertools → Zustände** → nach `lux_analytics` suchen.

Wenn z. B. `sensor.lux_analytics_garten_aktuelle_helligkeit` existiert (weil Label "Garten" gewählt), aber das Dashboard `sensor.lux_analytics_aktuelle_helligkeit` verwendet → IDs passen nicht.

**Lösung**: Entweder:
- Sensor ohne Label neu konfigurieren (Integration entfernen → neu hinzufügen ohne Label)
- Dashboard-YAML manuell anpassen (alle `lux_analytics_` durch `lux_analytics_garten_` ersetzen)

**Ursache B**: HA wurde nach Dashboard-Installation nicht neu gestartet.

**Lösung**: HA neu starten oder Lovelace cache leeren.

---

## Sensor wird doppelt erkannt / doppelte Config Entry

**Ursache**: Derselbe Source-Sensor wurde zweimal hinzugefügt.

**Verhalten**: Config Flow zeigt "Bereits konfiguriert" (ab v0.3.0).

**Lösung**: Doppelte Integration unter **Einstellungen → Geräte & Dienste** entfernen.

---

## Update in HACS wird nicht erkannt

**Ursache**: HACS cache oder GitHub API temporär nicht erreichbar.

**Lösung**:
1. HACS → oben rechts: **Aktualisieren**
2. Bei Bedarf: HACS komplett neu laden
3. Sicherstellen dass HA Internetzugang zu `api.github.com` hat

---

## Entity-IDs haben unerwartetes Format

**Beispiel**: Label "Süd-Terrasse" → Entity-ID enthält `s_d_terrasse` statt `sued_terrasse`.

**Ursache**: Umlaute werden durch `_` ersetzt (bekannte Einschränkung bis v0.4.0).

**Lösung** (bis v0.4.0):
- Label ohne Umlaute verwenden: "Sued-Terrasse", "Suedseite", "AusenSued"
- Oder Integration ohne Label verwenden und Entitäten manuell umbenennen (Entity Registry)

---

## Logs aktivieren für Debugging

In `configuration.yaml`:
```yaml
logger:
  default: warning
  logs:
    custom_components.lux_analytics: debug
```

HA neu starten. Logs erscheinen unter **Einstellungen → System → Protokolle**.

---

## Coordinator-Fehler im Log

```
WARNING: Failed to fetch data for sensor.xxx: ...
```

**Ursache**: Source-Sensor temporär nicht verfügbar (Neustart, Kopplung verloren).

**Verhalten**: Integration wartet auf nächsten Polling-Zyklus, kein Absturz.

**Lösung**: Source-Sensor-Verfügbarkeit prüfen.

---

## HACS-Installationsfehler

```
Integration konnte nicht geladen werden
```

**Lösung**:
1. Alle Dateien in `custom_components/lux_analytics/` vorhanden?
2. `manifest.json` korrekt (JSON-Syntaxfehler)?
3. Python-Syntax-Fehler? → HA-Log prüfen
4. HA-Version ≥ 2023.1.0?
