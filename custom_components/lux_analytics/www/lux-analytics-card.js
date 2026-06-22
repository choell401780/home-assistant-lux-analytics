/**
 * Lux Analytics Card – Home Assistant Custom Lovelace Card
 * Auto-discovers lux_analytics entities, no YAML configuration needed.
 *
 * https://github.com/choell401780/home-assistant-lux-analytics
 */

const CARD_VERSION = "0.4.0";

const ENTITY_SLUGS = {
  current:           "aktuelle_helligkeit",
  status:            "helligkeitsstatus",
  trend:             "helligkeitstrend",
  sun_index:         "sonnenindex",
  day_min:           "tagesminimum",
  day_max:           "tagesmaximum",
  day_avg:           "tagesdurchschnitt",
  week_min:          "wochenminimum",
  week_max:          "wochenmaximum",
  week_avg:          "wochendurchschnitt",
  month_avg:         "monatsdurchschnitt",
  bright_hours_day:  "helle_stunden_heute",
  bright_hours_week: "helle_stunden_woche",
  avg_24h:           "durchschnitt_24h",
  avg_7d:            "durchschnitt_7_tage",
  avg_30d:           "durchschnitt_30_tage",
};

const STATUS_COLORS = {
  "Nacht":         { bg: "#1a1a2e", text: "#aaa" },
  "Dämmerung":     { bg: "#16213e", text: "#ccc" },
  "Früher Morgen": { bg: "#8b5e3c", text: "#fff" },
  "Morgen":        { bg: "#d4874e", text: "#fff" },
  "Tag":           { bg: "#87ceeb", text: "#1a1a2e" },
  "Sonnig":        { bg: "#f5c518", text: "#1a1a2e" },
  "Pralle Sonne":  { bg: "#ff8c00", text: "#fff" },
  "Extreme Sonne": { bg: "#e63000", text: "#fff" },
};

const TREND_CONFIG = {
  "Steigend": { icon: "↑", color: "#4caf50" },
  "Fallend":  { icon: "↓", color: "#f44336" },
  "Stabil":   { icon: "→", color: "#9e9e9e" },
};

function fmt(val, unit = "", decimals = 0) {
  if (!val || val === "unknown" || val === "unavailable" || val === "None") return "—";
  const n = parseFloat(val);
  if (isNaN(n)) return "—";
  if (unit === "lx" && n >= 10000) return `${(n / 1000).toFixed(1)}k lx`;
  if (unit === "lx") return `${n.toFixed(0)} lx`;
  return n.toFixed(decimals) + (unit ? ` ${unit}` : "");
}

// ─────────────────────────────────────────────────────────────
//  Card Editor (shown in "Edit card" dialog)
// ─────────────────────────────────────────────────────────────
class LuxAnalyticsCardEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = config || {};
    this._render();
  }

  _getInstances() {
    if (!this._hass) return [];
    const seen = new Set();
    Object.keys(this._hass.states).forEach((id) => {
      if (id.endsWith("_aktuelle_helligkeit")) {
        const core = id.replace("sensor.lux_analytics_", "").replace("_aktuelle_helligkeit", "");
        seen.add(core === id.replace("sensor.", "") ? "" : core);
      } else if (id === "sensor.lux_analytics_aktuelle_helligkeit") {
        seen.add("");
      }
    });
    return [...seen];
  }

  _render() {
    const instances = this._getInstances();
    const current = this._config?.label ?? "";

    const opts = instances.length
      ? instances.map(
          (l) =>
            `<option value="${l}" ${l === current ? "selected" : ""}>${l === "" ? "Standard (kein Label)" : l[0].toUpperCase() + l.slice(1)}</option>`
        ).join("")
      : `<option value="">— Keine Instanz gefunden —</option>`;

    this.innerHTML = `
      <style>
        .editor { padding: 16px; font-family: var(--paper-font-body1_-_font-family, inherit); }
        label { display: block; margin-bottom: 4px; font-size: 0.85em; color: var(--secondary-text-color); }
        select {
          width: 100%; padding: 8px 10px; border-radius: 6px;
          border: 1px solid var(--divider-color, #ccc);
          background: var(--card-background-color, #fff);
          color: var(--primary-text-color, #000);
          font-size: 0.95em; cursor: pointer;
        }
        .hint { margin-top: 10px; font-size: 0.78em; color: var(--secondary-text-color); line-height: 1.4; }
      </style>
      <div class="editor">
        <label>Lux Analytics Instanz</label>
        <select id="sel">${opts}</select>
        <div class="hint">
          Wenn nur eine Instanz vorhanden ist, wird sie automatisch verwendet.<br>
          Für mehrere Instanzen hier die gewünschte auswählen.
        </div>
      </div>`;

    this.querySelector("#sel")?.addEventListener("change", (e) => {
      this.dispatchEvent(
        new CustomEvent("config-changed", {
          detail: { config: { ...this._config, label: e.target.value } },
          bubbles: true,
          composed: true,
        })
      );
    });
  }
}
customElements.define("lux-analytics-card-editor", LuxAnalyticsCardEditor);

// ─────────────────────────────────────────────────────────────
//  Main Card
// ─────────────────────────────────────────────────────────────
class LuxAnalyticsCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
  }

  static getConfigElement() {
    return document.createElement("lux-analytics-card-editor");
  }

  static getStubConfig(hass) {
    const found = Object.keys(hass?.states || {}).find(
      (id) =>
        id.startsWith("sensor.lux_analytics_") &&
        id.endsWith("_aktuelle_helligkeit")
    );
    if (found) {
      const mid = found
        .replace("sensor.lux_analytics_", "")
        .replace("_aktuelle_helligkeit", "");
      return { label: mid === found.replace("sensor.", "") ? "" : mid };
    }
    return { label: "" };
  }

  setConfig(config) {
    this._config = config || {};
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  _label() {
    return (this._config.label || "").trim();
  }

  _eid(key) {
    const slug = ENTITY_SLUGS[key] || key;
    const lbl = this._label();
    const prefix = lbl ? `sensor.lux_analytics_${lbl}_` : "sensor.lux_analytics_";
    return prefix + slug;
  }

  _state(key) {
    return this._hass?.states[this._eid(key)]?.state;
  }

  _render() {
    if (!this._hass) return;

    const lbl = this._label();
    const title = lbl ? `Lux Analytics – ${lbl[0].toUpperCase() + lbl.slice(1)}` : "Lux Analytics";

    const current    = this._state("current");
    const status     = this._state("status") || "Unbekannt";
    const trend      = this._state("trend")  || "Stabil";
    const sunIdx     = this._state("sun_index");
    const dayMin     = this._state("day_min");
    const dayMax     = this._state("day_max");
    const dayAvg     = this._state("day_avg");
    const weekAvg    = this._state("week_avg");
    const monthAvg   = this._state("month_avg");
    const brightDay  = this._state("bright_hours_day");
    const brightWeek = this._state("bright_hours_week");
    const avg24h     = this._state("avg_24h");
    const avg7d      = this._state("avg_7d");
    const avg30d     = this._state("avg_30d");

    const statusColor = STATUS_COLORS[status] || { bg: "#9e9e9e", text: "#fff" };
    const trendCfg    = TREND_CONFIG[trend]   || TREND_CONFIG["Stabil"];
    const sunPct      = Math.min(100, Math.max(0, parseFloat(sunIdx) || 0));

    // Gradient colour for sun bar
    const barColor = sunPct > 75 ? "#e63000" : sunPct > 50 ? "#ff8c00" : sunPct > 25 ? "#f5c518" : "#87ceeb";

    // Main lux display (compact)
    const luxVal = (() => {
      if (!current || current === "unknown" || current === "unavailable") return "—";
      const n = parseFloat(current);
      if (isNaN(n)) return "—";
      if (n >= 100000) return `${(n / 1000).toFixed(0)}k`;
      if (n >= 10000)  return `${(n / 1000).toFixed(1)}k`;
      return n.toFixed(0);
    })();

    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        ha-card {
          padding: 16px 18px 14px;
          overflow: hidden;
          position: relative;
        }

        /* ── Header ── */
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 14px;
        }
        .title {
          font-size: 1em;
          font-weight: 600;
          color: var(--primary-text-color);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 65%;
        }
        .badge {
          padding: 3px 10px;
          border-radius: 20px;
          font-size: 0.75em;
          font-weight: 600;
          letter-spacing: 0.3px;
          background: ${statusColor.bg};
          color: ${statusColor.text};
          white-space: nowrap;
          box-shadow: 0 1px 3px rgba(0,0,0,.25);
        }

        /* ── Lux hero ── */
        .hero {
          display: flex;
          align-items: baseline;
          gap: 5px;
          margin-bottom: 4px;
        }
        .lux-num {
          font-size: 2.8em;
          font-weight: 700;
          color: var(--primary-text-color);
          line-height: 1;
        }
        .lux-unit {
          font-size: 1.1em;
          color: var(--secondary-text-color);
          margin-bottom: 2px;
        }
        .trend {
          font-size: 1.5em;
          color: ${trendCfg.color};
          margin-left: 4px;
          line-height: 1;
        }

        /* ── Sun index bar ── */
        .bar-row {
          display: flex;
          align-items: center;
          gap: 8px;
          margin: 10px 0 4px;
        }
        .bar-track {
          flex: 1;
          height: 7px;
          background: var(--divider-color, #e0e0e0);
          border-radius: 4px;
          overflow: hidden;
        }
        .bar-fill {
          height: 100%;
          width: ${sunPct}%;
          background: linear-gradient(90deg, #87ceeb, ${barColor});
          border-radius: 4px;
          transition: width 0.6s ease;
        }
        .bar-label {
          font-size: 0.75em;
          color: var(--secondary-text-color);
          white-space: nowrap;
        }

        /* ── Divider ── */
        hr { border: none; border-top: 1px solid var(--divider-color, #e0e0e0); margin: 12px 0; }

        /* ── Day stats grid ── */
        .stat-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 6px;
        }
        .stat-box {
          background: var(--secondary-background-color, rgba(128,128,128,.07));
          border-radius: 8px;
          padding: 8px 6px;
          text-align: center;
        }
        .stat-lbl {
          font-size: 0.67em;
          color: var(--secondary-text-color);
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: 3px;
        }
        .stat-val {
          font-size: 0.88em;
          font-weight: 600;
          color: var(--primary-text-color);
        }

        /* ── Averages ── */
        .avgs {
          display: grid;
          grid-template-columns: 1fr 1fr 1fr;
          gap: 0;
          font-size: 0.8em;
        }
        .avg-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 4px 2px;
        }
        .avg-item .a-lbl { color: var(--secondary-text-color); font-size: 0.85em; }
        .avg-item .a-val { color: var(--primary-text-color); font-weight: 600; margin-top: 1px; }

        /* ── Bright hours ── */
        .bright-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 10px;
          font-size: 0.82em;
        }
        .bright-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 2px;
        }
        .bright-item .b-lbl { color: var(--secondary-text-color); font-size: 0.85em; }
        .bright-item .b-val { color: #f5c518; font-weight: 700; }

        /* ── Weekly/Monthly ── */
        .period-row {
          display: flex;
          justify-content: space-between;
          font-size: 0.8em;
          margin-top: 6px;
          color: var(--secondary-text-color);
        }
        .period-item { display: flex; gap: 4px; }
        .period-item b { color: var(--primary-text-color); }
      </style>

      <ha-card>
        <div class="header">
          <div class="title">${title}</div>
          <div class="badge">${status}</div>
        </div>

        <div class="hero">
          <div class="lux-num">${luxVal}</div>
          <div class="lux-unit">lx</div>
          <div class="trend">${trendCfg.icon}</div>
        </div>

        <div class="bar-row">
          <div class="bar-track"><div class="bar-fill"></div></div>
          <div class="bar-label">Sonnenindex ${sunPct.toFixed(0)} %</div>
        </div>

        <hr>

        <div class="stat-grid">
          <div class="stat-box"><div class="stat-lbl">Min heute</div><div class="stat-val">${fmt(dayMin, "lx")}</div></div>
          <div class="stat-box"><div class="stat-lbl">Max heute</div><div class="stat-val">${fmt(dayMax, "lx")}</div></div>
          <div class="stat-box"><div class="stat-lbl">Ø heute</div><div class="stat-val">${fmt(dayAvg, "lx")}</div></div>
        </div>

        <hr>

        <div class="avgs">
          <div class="avg-item"><div class="a-lbl">Ø 24h</div><div class="a-val">${fmt(avg24h, "lx")}</div></div>
          <div class="avg-item"><div class="a-lbl">Ø 7 Tage</div><div class="a-val">${fmt(avg7d, "lx")}</div></div>
          <div class="avg-item"><div class="a-lbl">Ø 30 Tage</div><div class="a-val">${fmt(avg30d, "lx")}</div></div>
        </div>

        <div class="bright-row">
          <div class="bright-item">
            <div class="b-lbl">☀ Helle Stunden heute</div>
            <div class="b-val">${fmt(brightDay, "h", 1)}</div>
          </div>
          <div class="bright-item">
            <div class="b-lbl">☀ diese Woche</div>
            <div class="b-val">${fmt(brightWeek, "h", 1)}</div>
          </div>
        </div>

        <div class="period-row">
          <div class="period-item">Woche Ø: <b>${fmt(weekAvg, "lx")}</b></div>
          <div class="period-item">Monat Ø: <b>${fmt(monthAvg, "lx")}</b></div>
        </div>
      </ha-card>`;
  }

  getCardSize() {
    return 5;
  }
}

customElements.define("lux-analytics-card", LuxAnalyticsCard);

// Register in HA card picker ("Add card" dialog)
window.customCards = window.customCards || [];
const _existing = window.customCards.find((c) => c.type === "lux-analytics-card");
if (!_existing) {
  window.customCards.push({
    type: "lux-analytics-card",
    name: "Lux Analytics",
    description: "Helligkeitssensor – Lux, Status, Trend, Statistiken, Helle Stunden",
    preview: true,
    documentationURL:
      "https://github.com/choell401780/home-assistant-lux-analytics",
  });
}

console.info(
  `%c LUX ANALYTICS CARD %c v${CARD_VERSION} `,
  "background:#1a1a2e;color:#f5c518;padding:2px 6px;border-radius:3px 0 0 3px;font-weight:bold",
  "background:#f5c518;color:#1a1a2e;padding:2px 6px;border-radius:0 3px 3px 0;font-weight:bold"
);
