# Unterstützte Versionen

## Home Assistant Kompatibilität

| Lux Analytics | Home Assistant | Status    |
|---------------|----------------|-----------|
| 0.3.x         | 2023.1.0+      | ✅ Aktiv  |
| 0.2.x         | 2023.1.0+      | ❌ EOL    |
| 0.1.x         | 2023.1.0+      | ❌ EOL    |

## Unterstützte Sensor-Protokolle

| Protokoll    | Status   | Erkennung        |
|--------------|----------|------------------|
| Homematic IP | ✅       | Automatisch      |
| Zigbee       | ✅       | Automatisch      |
| Z-Wave       | ✅       | Automatisch      |
| MQTT         | ✅       | Automatisch      |
| ESPHome      | ✅       | Automatisch      |
| Matter       | ✅       | Automatisch (lx) |
| Generic REST | ✅       | Manuell          |

## Getestete Sensoren

| Modell        | Hersteller    | Status   |
|---------------|---------------|----------|
| HmIP-SLO      | Homematic IP  | ✅       |
| TRÅDFRI       | IKEA          | ✅*      |
| Aqara MCCGQ   | Aqara         | ✅*      |
| Generic lx    | —             | ✅       |

*Gemäß Community-Rückmeldungen – nicht direkt getestet.

## Python Kompatibilität

| Python | Status |
|--------|--------|
| 3.12   | ✅     |
| 3.11   | ✅     |
| 3.10   | ⚠️ Ungetestet |
