# FAQ – Häufig gestellte Fragen

## Installation

**F: Die Integration erscheint nicht in der Integrationsliste.**

A: Sicherstellen, dass der Ordner `custom_components/lux_analytics/` korrekt im HA-Konfigurationsverzeichnis liegt und HA nach dem Kopieren neu gestartet wurde. Logs unter **Einstellungen** → **System** → **Protokolle** prüfen.

---

**F: HACS findet das Repository nicht.**

A: Das Repository muss als "Benutzerdefiniertes Repository" mit der Kategorie "Integration" hinzugefügt werden. Anschließend im HACS-Suchfeld nach "Lux Analytics" suchen.

---

## Sensoren

**F: Meine Homematic IP HmIP-SLO-Sensoren werden nicht erkannt.**

A: Die Integration erkennt Sensoren anhand von `device_class`, Unit (`lx`) und Entity-ID-Schlüsselwörtern. Bei HmIP-SLO meist über Schlüsselwort `slo`. Falls nicht automatisch erkannt, Sensor manuell im Konfigurationsassistenten hinzufügen.

---

**F: Es werden zu viele Sensoren erkannt.**

A: `Sensoren automatisch erkennen` deaktivieren und nur die gewünschten Sensoren manuell auswählen (**Einstellungen** → **Geräte & Dienste** → **Lux Analytics** → **Konfigurieren**).

---

**F: Die Statistiken zeigen "Unbekannt".**

A: Nach der Erstinstallation benötigt die Integration Verlaufsdaten aus dem HA-Recorder. Mindestens einige Stunden warten. Der Recorder muss aktiv sein (`recorder:` in configuration.yaml oder Standard-Setup).

---

**F: Helle Stunden werden nicht korrekt berechnet.**

A: Den Schwellwert in der Integrationskonfiguration anpassen. Für Sonnenstunden empfehlen sich 10.000–25.000 lx, für allgemeine Helligkeit 500–2.000 lx.

---

## Dashboard

**F: Die Lux Analytics Card zeigt keine Daten.**

A: Sicherstellen, dass die Integration konfiguriert ist (**Einstellungen → Geräte & Dienste → Lux Analytics**) und mindestens ein Sensor ausgewählt wurde. Nach der Erstinstallation benötigt die Integration einige Stunden, um Verlaufsdaten zu berechnen – aktuelle Werte erscheinen sofort.

**F: Die Lux Analytics Card erscheint nicht im "Karte hinzufügen"-Dialog.**

A: Home Assistant einmal neu starten – die Lovelace-Ressource wird beim ersten Start automatisch registriert. Bei Lovelace im YAML-Modus muss die Ressource manuell in der `configuration.yaml` eingetragen werden (siehe [Installationsanleitung](installation.md)).

---

**F: Kann ich das Dashboard auf einem Tablet als Kiosk nutzen?**

A: Ja. [Kiosk Mode](https://github.com/NemesisRE/kiosk-mode) via HACS installieren und im Dashboard aktivieren.

---

## Updates

**F: Die Update-Prüfung funktioniert nicht.**

A: Die Integration benötigt Internetzugriff zu `api.github.com`. Prüfen ob der HA-Server Internetzugriff hat. Fehler werden als DEBUG-Logs geschrieben.

---

**F: Kann ich die Update-Prüfung deaktivieren?**

A: Aktuell nicht über die UI. Das Update-Check-Intervall beträgt 6 Stunden und läuft nur, wenn Internetzugriff besteht. Bei keiner Verbindung wird kein Fehler angezeigt.

---

## Erweiterungen

**F: Plant ihr Pool/Beschattungssteuerung?**

A: Ja – die Architektur ist bereits dafür vorbereitet. Geplant für künftige Versionen sind:
- Poolpumpensteuerung (helligkeitsabhängige Laufzeiten)
- Beschattungssteuerung
- PV-Optimierung
- Sonnenstundenberechnung

Feedback und Feature-Requests: [GitHub Issues](https://github.com/choell401780/home-assistant-lux-analytics/issues)
