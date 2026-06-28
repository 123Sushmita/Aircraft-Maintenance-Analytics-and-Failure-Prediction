let c1, c2, c3;

const PALETTE = {
  go: "#5FE085",
  caution: "#F2B84B",
  warn: "#EF5350",
  data: "#5BC8F2",
  violet: "#9D8CF2"
};

function fmtMoney(n) {
  return Number(n || 0).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function statusBadge(status) {
  const s = (status || "").toLowerCase();
  const cls = s === "complete" ? "badge-complete" : s === "failed" ? "badge-failed" : "badge-pending";
  return `<span class="badge ${cls}">${escapeHtml(status || "unknown")}</span>`;
}

const DEFAULT_SUGGESTIONS = [
  "What's the total cost across the fleet?",
  "Which aircraft has the most maintenance jobs?",
  "How many jobs have failed?",
  "What maintenance type costs the most?"
];

function renderSuggestions(list) {
  const el = document.getElementById("suggestions");
  if (!el || !list) return;
  el.innerHTML = list.map(s =>
    `<button class="chip" onclick="askSuggestion(this)">${escapeHtml(s)}</button>`
  ).join("");
}

function askSuggestion(btn) {
  document.getElementById("q").value = btn.textContent;
  ask();
}

async function loadDashboard() {

  const d = await fetch("/api/dashboard").then(r => r.json());

  // KPI
  document.getElementById("kpi").innerHTML = `
    <div class="metric"><div class="metric-label">Total Jobs</div><div class="metric-value">${d.kpi.total_jobs}</div></div>
    <div class="metric"><div class="metric-label">Total Cost</div><div class="metric-value data">$${fmtMoney(d.kpi.total_cost)}</div></div>
    <div class="metric"><div class="metric-label">Avg Cost</div><div class="metric-value">$${fmtMoney(d.kpi.avg_cost)}</div></div>
    <div class="metric"><div class="metric-label">Max Cost</div><div class="metric-value">$${fmtMoney(d.kpi.max_cost)}</div></div>
    <div class="metric"><div class="metric-label">Min Cost</div><div class="metric-value">$${fmtMoney(d.kpi.min_cost)}</div></div>
  `;

  // KRI — LED color reflects actual severity, not decoration
  const failedJobs = Number(d.kri.failed_jobs || 0);
  const highRisk = Number(d.kri.high_risk_jobs || 0);
  const failedLed = failedJobs > 0 ? "led-warn" : "led-go";
  const riskLed = highRisk > 0 ? "led-caution" : "led-go";

  document.getElementById("kri").innerHTML = `
    <div class="metric"><div class="metric-label"><span class="led ${failedLed}"></span>Failed Jobs</div><div class="metric-value">${failedJobs}</div></div>
    <div class="metric"><div class="metric-label"><span class="led ${riskLed}"></span>High Risk</div><div class="metric-value">${highRisk}</div></div>
  `;

  // DESTROY OLD CHARTS (IMPORTANT FIX)
  if (c1) c1.destroy();
  if (c2) c2.destroy();
  if (c3) c3.destroy();

  const ctx1 = document.getElementById("c1").getContext("2d");
  const ctx2 = document.getElementById("c2").getContext("2d");
  const ctx3 = document.getElementById("c3").getContext("2d");

  const legendColor = "#8B97A3";

  // -------------------- CHART 1 --------------------
  c1 = new Chart(ctx1, {
    type: "bar",
    data: {
      labels: d.aircraft.map(x => x.aircraft_id),
      datasets: [{
        label: "Jobs",
        data: d.aircraft.map(x => Number(x.c)),
        backgroundColor: PALETTE.data,
        borderRadius: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: legendColor } } },
      scales: {
        x: { ticks: { color: legendColor }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: legendColor }, grid: { color: "rgba(255,255,255,0.05)" } }
      }
    }
  });

  // -------------------- CHART 2 --------------------
  c2 = new Chart(ctx2, {
    type: "pie",
    data: {
      labels: d.maintenance.map(x => x.maintenance_type),
      datasets: [{
        data: d.maintenance.map(x => Number(x.c)),
        backgroundColor: [PALETTE.go, PALETTE.caution, PALETTE.warn, PALETTE.data, PALETTE.violet]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: legendColor } } }
    }
  });

  // -------------------- CHART 3 --------------------
  c3 = new Chart(ctx3, {
    type: "doughnut",
    data: {
      labels: d.status.map(x => x.status),
      datasets: [{
        data: d.status.map(x => Number(x.c)),
        backgroundColor: [PALETTE.go, PALETTE.caution, PALETTE.warn]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: legendColor } } }
    }
  });

  // DROPDOWN
  const a = await fetch("/api/aircraft").then(r => r.json());

  document.getElementById("aircraft").innerHTML =
    `<option value="">-- select aircraft --</option>` +
    a.map(x => `<option value="${x.aircraft_id}">${x.aircraft_id}</option>`).join("");
}

// ---------------- HISTORY ----------------
async function loadHistory(id) {
  if (!id) {
    document.getElementById("history").innerHTML = "";
    return;
  }

  const d = await fetch(`/api/aircraft/${id}`).then(r => r.json());

  let html = `
    <tr>
      <th>ID</th><th>TYPE</th><th>COST</th><th>STATUS</th><th>DATE</th>
    </tr>`;

  if (d.length === 0) {
    html += `<tr><td colspan="5">No maintenance logs found for ${escapeHtml(id)}</td></tr>`;
  }

  d.forEach(r => {
    html += `<tr>
      <td>${escapeHtml(r.log_id)}</td>
      <td>${escapeHtml(r.maintenance_type)}</td>
      <td>$${fmtMoney(r.cost_usd)}</td>
      <td>${statusBadge(r.status)}</td>
      <td>${escapeHtml(r.log_date)}</td>
    </tr>`;
  });

  document.getElementById("history").innerHTML = html;
}

// ---------------- CHAT ----------------
async function ask() {
  const input = document.getElementById("q");
  const q = input.value.trim();
  if (!q) return;

  const chat = document.getElementById("chat");
  const button = document.querySelector("button[onclick='ask()']");

  chat.innerHTML += `<div class="msg-user"><div class="bubble">${escapeHtml(q)}</div></div>`;
  input.value = "";
  if (button) button.disabled = true;

  const thinkingId = "thinking-" + Date.now();
  chat.innerHTML += `<div id="${thinkingId}" class="msg-ai"><div class="bubble"><i>Reading the data...</i></div></div>`;
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ q })
    });

    if (!res.ok) throw new Error("Server returned " + res.status);

    const d = await res.json();
    const el = document.getElementById(thinkingId);
    if (el) el.querySelector(".bubble").innerHTML = escapeHtml(d.message);
    renderSuggestions(d.suggestions);
  } catch (err) {
    const el = document.getElementById(thinkingId);
    if (el) el.querySelector(".bubble").innerHTML = "Sorry, something went wrong reaching the chat service.";
    console.error(err);
  } finally {
    if (button) button.disabled = false;
    chat.scrollTop = chat.scrollHeight;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderSuggestions(DEFAULT_SUGGESTIONS);

  const input = document.getElementById("q");
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") ask();
    });
  }
});

// INIT
loadDashboard();
