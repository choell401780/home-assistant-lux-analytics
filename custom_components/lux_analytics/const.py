"""Constants for Lux Analytics."""

DOMAIN = "lux_analytics"
VERSION = "0.1.0"
GITHUB_REPO = "choell/home-assistant-lux-analytics"

CONF_SENSORS = "sensors"
CONF_AUTO_DISCOVER = "auto_discover"
CONF_BRIGHT_THRESHOLD = "bright_threshold"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_AUTO_DISCOVER = True
DEFAULT_BRIGHT_THRESHOLD = 1000
DEFAULT_UPDATE_INTERVAL = 300

ATTR_BRIGHTNESS_CLASS = "brightness_class"
ATTR_SOURCE_ENTITY = "source_entity"
ATTR_TREND = "trend"
ATTR_SUN_INDEX = "sun_index"

BRIGHTNESS_CLASSES = [
    {"name": "Nacht",        "min": 0,     "max": 1},
    {"name": "Dämmerung",    "min": 1,     "max": 100},
    {"name": "Früher Morgen","min": 100,   "max": 1000},
    {"name": "Morgen",       "min": 1000,  "max": 10000},
    {"name": "Tag",          "min": 10000, "max": 30000},
    {"name": "Sonnig",       "min": 30000, "max": 50000},
    {"name": "Pralle Sonne", "min": 50000, "max": 70000},
    {"name": "Extreme Sonne","min": 70000, "max": float("inf")},
]

SENSOR_TYPES = {
    "current":      {"name": "Aktuelle Helligkeit",        "icon": "mdi:white-balance-sunny",  "unit": "lx"},
    "status":       {"name": "Helligkeitsstatus",          "icon": "mdi:weather-sunny",        "unit": None},
    "trend":        {"name": "Helligkeitstrend",           "icon": "mdi:trending-up",          "unit": None},
    "sun_index":    {"name": "Sonnenindex",                "icon": "mdi:solar-power",          "unit": "%"},
    "day_min":      {"name": "Tagesminimum",               "icon": "mdi:arrow-down",           "unit": "lx"},
    "day_max":      {"name": "Tagesmaximum",               "icon": "mdi:arrow-up",             "unit": "lx"},
    "day_avg":      {"name": "Tagesdurchschnitt",          "icon": "mdi:calculator-variant",   "unit": "lx"},
    "week_min":     {"name": "Wochenminimum",              "icon": "mdi:arrow-down",           "unit": "lx"},
    "week_max":     {"name": "Wochenmaximum",              "icon": "mdi:arrow-up",             "unit": "lx"},
    "week_avg":     {"name": "Wochendurchschnitt",         "icon": "mdi:calculator-variant",   "unit": "lx"},
    "month_min":    {"name": "Monatsminimum",              "icon": "mdi:arrow-down",           "unit": "lx"},
    "month_max":    {"name": "Monatsmaximum",              "icon": "mdi:arrow-up",             "unit": "lx"},
    "month_avg":    {"name": "Monatsdurchschnitt",         "icon": "mdi:calculator-variant",   "unit": "lx"},
    "bright_hours_day":   {"name": "Helle Stunden Heute",  "icon": "mdi:clock-time-eight",    "unit": "h"},
    "bright_hours_week":  {"name": "Helle Stunden Woche",  "icon": "mdi:clock-time-eight",    "unit": "h"},
    "bright_hours_month": {"name": "Helle Stunden Monat",  "icon": "mdi:clock-time-eight",    "unit": "h"},
    "avg_24h":      {"name": "Durchschnitt 24h",           "icon": "mdi:chart-line",           "unit": "lx"},
    "avg_7d":       {"name": "Durchschnitt 7 Tage",        "icon": "mdi:chart-line",           "unit": "lx"},
    "avg_30d":      {"name": "Durchschnitt 30 Tage",       "icon": "mdi:chart-line",           "unit": "lx"},
}

ILLUMINANCE_DEVICE_CLASSES = ["illuminance"]
ILLUMINANCE_UNITS = ["lx", "lux"]
ILLUMINANCE_KEYWORDS = ["lux", "illuminance", "brightness", "light", "helligkeit", "hell", "slo"]
