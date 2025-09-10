const API_BASE = "http://127.0.0.1:8000";

const qs = (s, el = document) => el.querySelector(s);
const qsa = (s, el = document) => Array.from(el.querySelectorAll(s));

const state = {
  formulas: [],
  prefixes: {},
  chart: null,
};

function buildPrefixSelect() {
  const sel = document.createElement("select");
  Object.entries(state.prefixes).forEach(([sym, [, label]]) => {
    const opt = document.createElement("option");
    opt.value = sym;
    opt.textContent = `${sym}${label}`;
    sel.appendChild(opt);
  });
  sel.value = ""; // (10^0)
  return sel;
}

function renderFormulaMeta(formula) {
  const meta = qs("#formula-meta");
  meta.innerHTML = `<div class="card" style="background: var(--card); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,.08)">
    <div><strong>${formula.desc}</strong></div>
    <div class="muted" style="margin-top:6px">${formula.explain}</div>
  </div>`;
}

function renderFields(formula) {
  const container = qs("#fields");
  container.innerHTML = "";

  formula.fields.forEach((f) => {
    const row = document.createElement("div");
    row.className = "form-row inline";

    const label = document.createElement("label");
    label.textContent = `${f.label}`;
    label.setAttribute("for", `fld-${f.name}`);

    const input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.id = `fld-${f.name}`;
    input.placeholder = `${f.label}...`;

    const prefixSel = buildPrefixSelect();

    const unit = document.createElement("div");
    unit.textContent = f.unit;
    unit.style.alignSelf = "center";

    row.appendChild(label);
    row.appendChild(input);
    row.appendChild(prefixSel);
    row.appendChild(unit);
    container.appendChild(row);
  });
}

async function fetchJSON(url, opts) {
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
  return res.json();
}

async function loadBoot() {
  const [formulas, prefixes] = await Promise.all([
    fetchJSON(`${API_BASE}/formulas`),
    fetchJSON(`${API_BASE}/prefixes`),
  ]);
  state.formulas = formulas;
  state.prefixes = prefixes;

  const sel = qs("#formula");
  sel.innerHTML = "";
  const blank = document.createElement("option");
  blank.value = "";
  blank.textContent = "Elige una fórmula…";
  sel.appendChild(blank);
  state.formulas.forEach((f) => {
    const opt = document.createElement("option");
    opt.value = f.id;
    opt.textContent = f.title;
    sel.appendChild(opt);
  });

  sel.addEventListener("change", () => {
    const formula = state.formulas.find((f) => f.id === sel.value);
    if (!formula) { qs("#fields").innerHTML = ""; qs("#formula-meta").innerHTML = ""; return; }
    renderFormulaMeta(formula);
    renderFields(formula);
    qs("#result").textContent = "";
  });

  qs("#btn-calc").addEventListener("click", async () => {
    const id = sel.value;
    if (!id) return;
    const formula = state.formulas.find((f) => f.id === id);
    const rows = qsa("#fields .form-row");
    const values = {};

    rows.forEach((row, idx) => {
      const f = formula.fields[idx];
      const input = row.querySelector("input");
      const pref = row.querySelector("select").value;
      const factor = state.prefixes[pref]?.[0] ?? 1;
      const raw = input.value.trim();
      if (raw === "") throw new Error(`Falta el valor de '${f.name}'.`);
      const num = parseFloat(raw);
      if (Number.isNaN(num)) throw new Error(`Valor inválido en '${f.name}'.`);
      values[f.name] = num * factor;
    });

    try {
      const res = await fetchJSON(`${API_BASE}/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ formula_id: id, values }),
      });
      qs("#result").textContent = `Resultado: ${res.display}`;
      qs("#result").style.color = "var(--ok)";
    } catch (e) {
      qs("#result").textContent = `Error: ${e.message}`;
      qs("#result").style.color = "#ef4444";
    }
  });

  qs("#btn-clear").addEventListener("click", () => {
    qsa("#fields input").forEach((i) => (i.value = ""));
    qsa("#fields select").forEach((s) => (s.value = ""));
    qs("#result").textContent = "";
    if (state.chart) { state.chart.destroy(); state.chart = null; }
  });

  qs("#btn-plot").addEventListener("click", () => {
    const id = sel.value;
    if (!id) return;
    const formula = state.formulas.find((f) => f.id === id);
    if (!formula) return;

    const ctx = document.getElementById("chart");
    if (state.chart) { state.chart.destroy(); state.chart = null; }

    // Curvas pedagógicas simples por fórmula (sin llamar a API)
    if (id === "shannon") {
      const BRow = qsa("#fields .form-row")[0];
      const B = parseFloat(BRow.querySelector("input").value || "1");
      const pref = BRow.querySelector("select").value; const factor = state.prefixes[pref]?.[0] ?? 1;
      const Bsi = (Number.isNaN(B) ? 1 : B) * factor;
      const snrDb = Array.from({ length: 41 }, (_, i) => -10 + i);
      const snrLin = snrDb.map((x) => Math.pow(10, x / 10));
      const C = snrLin.map((s) => Bsi * Math.log2(1 + s));
      state.chart = new Chart(ctx, {
        type: "line",
        data: { labels: snrDb, datasets: [{ label: "Capacidad (bits/s)", data: C, borderColor: "#60a5fa" }] },
        options: { scales: { x: { title: { display: true, text: "SNR (dB)" } }, y: { title: { display: true, text: "Capacidad (bits/s)" } } } },
      });
    } else if (id === "noise_power") {
      const TRow = qsa("#fields .form-row")[0];
      const T = parseFloat(TRow.querySelector("input").value || "290");
      const Tpref = TRow.querySelector("select").value; const Tfac = state.prefixes[Tpref]?.[0] ?? 1;
      const Tsi = (Number.isNaN(T) ? 290 : T) * Tfac;
      const B = Array.from({ length: 50 }, (_, i) => (i + 1) * 1e3);
      const N = B.map((b) => 1.38e-23 * Tsi * b);
      state.chart = new Chart(ctx, {
        type: "line",
        data: { labels: B, datasets: [{ label: "N (W)", data: N, borderColor: "#a78bfa" }] },
        options: { scales: { x: { title: { display: true, text: "B (Hz)" } }, y: { title: { display: true, text: "Potencia de ruido (W)" } } } },
      });
    } else if (id === "noise_voltage") {
      const RRow = qsa("#fields .form-row")[0];
      const R = parseFloat(RRow.querySelector("input").value || "50");
      const Rpref = RRow.querySelector("select").value; const Rfac = state.prefixes[Rpref]?.[0] ?? 1;
      const TRow = qsa("#fields .form-row")[1];
      const T = parseFloat(TRow.querySelector("input").value || "290");
      const Tpref = TRow.querySelector("select").value; const Tfac = state.prefixes[Tpref]?.[0] ?? 1;
      const BRow = qsa("#fields .form-row")[2];
      const B = parseFloat(BRow.querySelector("input").value || "1e6");
      const Bpref = BRow.querySelector("select").value; const Bfac = state.prefixes[Bpref]?.[0] ?? 1;
      const Rsi = (Number.isNaN(R) ? 50 : R) * Rfac;
      const Tsi = (Number.isNaN(T) ? 290 : T) * Tfac;
      const Bsi = (Number.isNaN(B) ? 1e6 : B) * Bfac;
      const Trange = Array.from({ length: 50 }, (_, i) => 200 + i * 10);
      const Vn = Trange.map((t) => Math.sqrt(4 * 1.38e-23 * Rsi * t * Bsi));
      state.chart = new Chart(ctx, {
        type: "line",
        data: { labels: Trange, datasets: [{ label: "Vn (V)", data: Vn, borderColor: "#34d399" }] },
        options: { scales: { x: { title: { display: true, text: "T (K)" } }, y: { title: { display: true, text: "Voltaje de ruido (V)" } } } },
      });
    } else if (id === "noise_factor") {
      const Frange = Array.from({ length: 50 }, (_, i) => 1 + i * 0.1);
      const NF = Frange.map((F) => 10 * Math.log10(F));
      state.chart = new Chart(ctx, {
        type: "line",
        data: { labels: Frange, datasets: [{ label: "NF (dB)", data: NF, borderColor: "#f59e0b" }] },
        options: { scales: { x: { title: { display: true, text: "F (adim)" } }, y: { title: { display: true, text: "Índice de ruido (dB)" } } } },
      });
    } else if (id === "noise_figure") {
      const Frange = Array.from({ length: 50 }, (_, i) => 1 + i * 0.1);
      const NF = Frange.map((F) => 10 * Math.log10(F));
      state.chart = new Chart(ctx, {
        type: "line",
        data: { labels: Frange, datasets: [{ label: "NF (dB)", data: NF, borderColor: "#ef4444" }] },
        options: { scales: { x: { title: { display: true, text: "F (adim)" } }, y: { title: { display: true, text: "Índice de ruido (dB)" } } } },
      });
    } else if (id === "bandwidth") {
      const Fmax = Array.from({ length: 50 }, (_, i) => (i + 1) * 1e6);
      const Fmin = 1e6;
      const B = Fmax.map((f) => f - Fmin);
      state.chart = new Chart(ctx, {
        type: "line",
        data: { labels: Fmax, datasets: [{ label: "B (Hz)", data: B, borderColor: "#60a5fa" }] },
        options: { scales: { x: { title: { display: true, text: "Fmax (Hz)" } }, y: { title: { display: true, text: "Ancho de banda (Hz)" } } } },
      });
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  loadBoot().catch((e) => {
    qs("#result").textContent = `No se pudo cargar la API: ${e.message}. ¿Iniciaste el servidor?`;
  });
});


