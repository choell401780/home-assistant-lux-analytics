# Release Notes – v0.2.0

**Veröffentlicht:** 2026-06-22

## HACS-Architekturanpassung – vollständige HACS-Kompatibilität

Diese Version stellt vollständige HACS-Konformität her und entfernt redundante
Update-Logik zugunsten der nativen HACS-Update-Verwaltung.

---

## Entfernte Funktionen

### Eigene GitHub-Update-Prüfung
Die bisherige `_maybe_check_github_version()`-Logik im Coordinator und der
`UpdateAvailableSensor` wurden vollständig entfernt.

**Warum?** HACS übernimmt exakt diese Aufgabe:
- Vergleich installierte Version vs. GitHub Release
- Native HA Update-Entity für jede HACS-verwaltete Integration
- Anzeige in der Standard-HA-Oberfläche
- Ein-Klick-Update ohne eigene Logik

Eigene GitHub-API-Abfragen wären redundant, würden unnötigen Netzwerkverkehr
erzeugen und einen eigenen Fehlerpfad einführen.

---

## Neue Funktionen

### HACS-Validierung in CI
GitHub Actions führt jetzt `hacs/action` aus und validiert automatisch die
HACS-Konformität bei jedem Push und Pull Request.

### info.md
Kurze Beschreibung für den HACS-Store wird jetzt über `info.md` bereitgestellt.

---

## HACS-Konformitätsprüfung

| Anforderung                              | Status |
|------------------------------------------|--------|
| `custom_components/<domain>/` an Root    | ✅     |
| `manifest.json` vollständig              | ✅     |
| `config_flow: true`                      | ✅     |
| `hacs.json` vorhanden                    | ✅     |
| `README.md` / `info.md` vorhanden        | ✅     |
| Semantische Versionierung                | ✅     |
| GitHub Release mit Tag                   | ✅     |
| HACS-Validierung in CI                   | ✅ neu |
| Keine eigene redundante Update-Logik     | ✅ neu |

---

## Migration

Kein manueller Eingriff erforderlich. HACS aktualisiert automatisch.

Nach dem Update und HA-Neustart wird der bisherige `sensor.lux_analytics_update`
von HA als verwaiste Entität markiert und kann über die UI entfernt werden.

---

## Installationsweg

Ausschließlich über HACS – keine SSH, kein Samba, kein manuelles Dateikopieren.

Siehe [Installationsanleitung](../../docs/installation.md)
