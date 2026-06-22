"""Constants for Lux Analytics."""

from __future__ import annotations

import re

DOMAIN = "lux_analytics"
VERSION = "0.4.0"

CONF_SOURCE_SENSOR = "source_sensor"
CONF_SENSOR_LABEL = "sensor_label"
CONF_BRIGHT_THRESHOLD = "bright_threshold"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_BRIGHT_THRESHOLD = 1000
DEFAULT_UPDATE_INTERVAL = 300

ATTR_BRIGHTNESS_CLASS = "brightness_class"
ATTR_SOURCE_ENTITY = "source_entity"
ATTR_TREND = "trend"
ATTR_SUN_INDEX = "sun_index"

BRIGHTNESS_CLASSES = [
    {"name": "Nacht",         "min": 0,     "max": 1},
    {"name": "Dämmerung",     "min": 1,     "max": 100},
    {"name": "Früher Morgen", "min": 100,   "max": 1000},
    {"name": "Morgen",        "min": 1000,  "max": 10000},
    {"name": "Tag",           "min": 10000, "max": 30000},
    {"name": "Sonnig",        "min": 30000, "max": 50000},
    {"name": "Pralle Sonne",  "min": 50000, "max": 70000},
    {"name": "Extreme Sonne", "min": 70000, "max": float("inf")},
]

SENSOR_TYPES = {
    "current":            {"name": "Aktuelle Helligkeit",   "icon": "mdi:white-balance-sunny", "unit": "lx"},
    "status":             {"name": "Helligkeitsstatus",     "icon": "mdi:weather-sunny",       "unit": None},
    "trend":              {"name": "Helligkeitstrend",      "icon": "mdi:trending-up",         "unit": None},
    "sun_index":          {"name": "Sonnenindex",           "icon": "mdi:solar-power",         "unit": "%"},
    "day_min":            {"name": "Tagesminimum",          "icon": "mdi:arrow-down",          "unit": "lx"},
    "day_max":            {"name": "Tagesmaximum",          "icon": "mdi:arrow-up",            "unit": "lx"},
    "day_avg":            {"name": "Tagesdurchschnitt",     "icon": "mdi:calculator-variant",  "unit": "lx"},
    "week_min":           {"name": "Wochenminimum",         "icon": "mdi:arrow-down",          "unit": "lx"},
    "week_max":           {"name": "Wochenmaximum",         "icon": "mdi:arrow-up",            "unit": "lx"},
    "week_avg":           {"name": "Wochendurchschnitt",    "icon": "mdi:calculator-variant",  "unit": "lx"},
    "month_min":          {"name": "Monatsminimum",         "icon": "mdi:arrow-down",          "unit": "lx"},
    "month_max":          {"name": "Monatsmaximum",         "icon": "mdi:arrow-up",            "unit": "lx"},
    "month_avg":          {"name": "Monatsdurchschnitt",    "icon": "mdi:calculator-variant",  "unit": "lx"},
    "bright_hours_day":   {"name": "Helle Stunden Heute",  "icon": "mdi:clock-time-eight",    "unit": "h"},
    "bright_hours_week":  {"name": "Helle Stunden Woche",  "icon": "mdi:clock-time-eight",    "unit": "h"},
    "bright_hours_month": {"name": "Helle Stunden Monat",  "icon": "mdi:clock-time-eight",    "unit": "h"},
    "avg_24h":            {"name": "Durchschnitt 24h",      "icon": "mdi:chart-line",          "unit": "lx"},
    "avg_7d":             {"name": "Durchschnitt 7 Tage",   "icon": "mdi:chart-line",          "unit": "lx"},
    "avg_30d":            {"name": "Durchschnitt 30 Tage",  "icon": "mdi:chart-line",          "unit": "lx"},
}

# Maps sensor_key → predictable German entity_id slug
ENTITY_ID_SLUGS: dict[str, str] = {
    "current":            "aktuelle_helligkeit",
    "status":             "helligkeitsstatus",
    "trend":              "helligkeitstrend",
    "sun_index":          "sonnenindex",
    "day_min":            "tagesminimum",
    "day_max":            "tagesmaximum",
    "day_avg":            "tagesdurchschnitt",
    "week_min":           "wochenminimum",
    "week_max":           "wochenmaximum",
    "week_avg":           "wochendurchschnitt",
    "month_min":          "monatsminimum",
    "month_max":          "monatsmaximum",
    "month_avg":          "monatsdurchschnitt",
    "bright_hours_day":   "helle_stunden_heute",
    "bright_hours_week":  "helle_stunden_woche",
    "bright_hours_month": "helle_stunden_monat",
    "avg_24h":            "durchschnitt_24h",
    "avg_7d":             "durchschnitt_7_tage",
    "avg_30d":            "durchschnitt_30_tage",
}

ILLUMINANCE_DEVICE_CLASSES = ["illuminance"]
ILLUMINANCE_UNITS = ["lx", "lux"]
ILLUMINANCE_KEYWORDS = ["lux", "illuminance", "brightness", "light", "helligkeit", "hell", "slo"]


def _normalize_label(label: str) -> str:
    """Convert a user label to a safe ASCII slug (handles German umlauts)."""
    label = label.strip().lower()
    label = (
        label.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
        .replace("Ä", "ae")
        .replace("Ö", "oe")
        .replace("Ü", "ue")
    )
    return re.sub(r"[^a-z0-9]+", "_", label).strip("_")


def build_entity_id(sensor_key: str, label: str = "") -> str:
    """Return a predictable sensor entity_id for a given key and optional label.

    No label          → sensor.lux_analytics_aktuelle_helligkeit
    label="Garten"    → sensor.lux_analytics_garten_aktuelle_helligkeit
    label="Süd Pool"  → sensor.lux_analytics_sued_pool_aktuelle_helligkeit
    """
    slug = ENTITY_ID_SLUGS.get(sensor_key, sensor_key)
    if label:
        safe_label = _normalize_label(label)
        if safe_label:
            return f"sensor.{DOMAIN}_{safe_label}_{slug}"
    return f"sensor.{DOMAIN}_{slug}"
