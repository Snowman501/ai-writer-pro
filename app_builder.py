"""
ShatterScan Core Diagnostic Platform — Production Build Factory
Imports a6_level_1 from ase_a6_questions.py and writes:
  a6_electrical_v1.html   (single-file app)
  A6_Master_Study_Pack.zip (distribution archive)

All HTML/CSS/JS sections are plain string constants — zero f-string
brace-escaping needed.  The question JSON is spliced in via concatenation.
"""

import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ase_a6_questions import a6_level_1

OUTPUT_HTML = "a6_electrical_v1.html"
OUTPUT_ZIP  = "A6_Master_Study_Pack.zip"


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    q_json = json.dumps(a6_level_1, ensure_ascii=False, indent=2)
    html   = assemble(q_json)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(OUTPUT_HTML)

    print(f"[BUILD OK]  {OUTPUT_HTML}  ({os.path.getsize(OUTPUT_HTML):,} B)")
    print(f"[PACKED ]   {OUTPUT_ZIP}   ({os.path.getsize(OUTPUT_ZIP):,} B)")
    print(f"[QUESTIONS] {len(a6_level_1)} entries loaded")


def assemble(q_json: str) -> str:
    return (
        _HTML_HEAD
        + _BODY_LOGIN
        + _BODY_APP
        + _MODAL_HTML
        + "<script>\n"
        + "const A6_DATA = " + q_json + ";\n"
        + _JS_CORE
        + "</script>\n"
        + "</body></html>\n"
    )


# ── HTML HEAD + CSS ───────────────────────────────────────────────────────────
_HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
  <meta name="theme-color" content="#060810" />
  <title>ShatterScan A6 — Core Diagnostic Platform</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg:      #060810;
      --surf:    #0d1020;
      --surf2:   #141828;
      --border:  #1e2840;
      --cyan:    #00d4ff;
      --amber:   #ff9800;
      --green:   #00e676;
      --red:     #ff1744;
      --text:    #c8d8f0;
      --muted:   #4a5878;
      --font:    "Courier New", "Lucida Console", monospace;
    }
    html, body {
      height: 100%; background: var(--bg); color: var(--text);
      font-family: var(--font); overflow: hidden;
    }

    /* ── Login ── */
    #login-screen {
      position: fixed; inset: 0; z-index: 999;
      background: radial-gradient(ellipse at center, #0a0d18 0%, #020408 100%);
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; padding: 24px; text-align: center;
    }
    .login-logo {
      font-size: 26px; letter-spacing: 5px; color: var(--cyan); margin-bottom: 4px;
      text-shadow: 0 0 22px rgba(0,212,255,.55);
    }
    .login-sub { font-size: 9px; letter-spacing: 3px; color: var(--muted); margin-bottom: 30px; }
    .legal-box {
      background: rgba(14,17,32,.9); border: 1px solid var(--amber);
      border-left: 4px solid var(--amber); border-radius: 4px;
      padding: 18px 20px; max-width: 560px; text-align: left; margin-bottom: 26px;
    }
    .legal-box h3 {
      font-size: 10px; letter-spacing: 2px; color: var(--amber); margin-bottom: 10px;
    }
    .legal-box p { font-size: 11px; line-height: 1.85; color: #8899bb; }
    .legal-box p + p { margin-top: 10px; }
    #accept-btn {
      background: transparent; border: 2px solid var(--cyan); color: var(--cyan);
      padding: 14px 32px; font-family: var(--font); font-size: 12px; letter-spacing: 3px;
      cursor: pointer; border-radius: 2px; transition: all .2s;
      text-shadow: 0 0 8px rgba(0,212,255,.5);
      box-shadow: 0 0 16px rgba(0,212,255,.1);
    }
    #accept-btn:hover, #accept-btn:active {
      background: rgba(0,212,255,.1); box-shadow: 0 0 28px rgba(0,212,255,.3);
    }
    .login-ver { margin-top: 18px; font-size: 9px; color: var(--muted); letter-spacing: 2px; }

    /* ── App shell ── */
    #app-screen { display: none; flex-direction: column; height: 100dvh; }

    .app-header {
      background: var(--surf); border-bottom: 1px solid var(--border);
      padding: 8px 14px; display: flex; align-items: center;
      justify-content: space-between; flex-shrink: 0;
    }
    .hdr-logo  { font-size: 11px; letter-spacing: 2px; color: var(--cyan); }
    .hdr-sub   { font-size: 9px;  letter-spacing: 1px; color: var(--muted); margin-top: 1px; }
    #obd-status { font-size: 9px; letter-spacing: 1px; color: var(--muted); }

    /* ── Gauges ── */
    .gauges-section {
      background: var(--surf); border-bottom: 1px solid var(--border);
      padding: 10px 12px; display: flex; align-items: center;
      gap: 10px; flex-shrink: 0; flex-wrap: wrap;
    }
    .dial-wrap { display: flex; flex-direction: column; align-items: center; }
    canvas {
      display: block; width: 130px; height: 130px;
      border-radius: 50%; background: #080b14;
    }
    .obd-col {
      flex: 1; min-width: 140px; display: flex; flex-direction: column; gap: 7px;
    }
    #obd-btn {
      background: transparent; border: 1px solid var(--cyan); color: var(--cyan);
      padding: 9px 12px; font-family: var(--font); font-size: 10px;
      letter-spacing: 2px; cursor: pointer; border-radius: 2px; transition: all .2s;
    }
    #obd-btn:hover, #obd-btn.active {
      background: rgba(0,212,255,.08); border-color: var(--green); color: var(--green);
    }
    #telem-log {
      background: #04060e; border: 1px solid var(--border); border-radius: 2px;
      padding: 6px 8px; font-size: 9px; color: #3a5060; line-height: 1.65;
      min-height: 62px; overflow: hidden;
    }

    /* ── Quiz ── */
    .quiz-section {
      flex: 1; overflow-y: auto; padding: 12px;
      display: flex; flex-direction: column; gap: 10px;
    }
    .quiz-header {
      display: flex; align-items: center; gap: 8px;
    }
    #q-counter  { font-size: 10px; color: var(--muted); white-space: nowrap; flex-shrink: 0; }
    .prog-track { flex: 1; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
    #q-prog-fill {
      height: 100%; width: 0%; background: var(--cyan);
      border-radius: 2px; transition: width .4s;
    }
    #tts-btn {
      flex-shrink: 0; background: transparent; border: 1px solid var(--muted);
      color: var(--muted); padding: 4px 9px; font-family: var(--font);
      font-size: 10px; cursor: pointer; border-radius: 2px; white-space: nowrap;
    }
    #tts-btn:hover, #tts-btn:active { border-color: var(--cyan); color: var(--cyan); }
    .scenario-label { font-size: 9px; letter-spacing: 2px; color: var(--amber); margin-bottom: 5px; }
    #q-text { font-size: 13px; line-height: 1.8; color: var(--text); }

    .opt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .opt-btn {
      background: var(--surf2); border: 1px solid var(--border); color: var(--text);
      padding: 11px 9px; font-family: var(--font); font-size: 11px; line-height: 1.4;
      cursor: pointer; border-radius: 3px; transition: all .15s; text-align: center;
    }
    .opt-btn:hover:not(:disabled) {
      border-color: var(--cyan); color: var(--cyan); background: rgba(0,212,255,.05);
    }
    .opt-btn.correct {
      border-color: var(--green) !important; color: var(--green) !important;
      background: rgba(0,230,118,.07) !important;
    }
    .opt-btn.wrong {
      border-color: var(--red) !important; color: var(--red) !important;
      background: rgba(255,23,68,.07) !important;
    }
    .opt-btn:disabled { cursor: default; opacity: .8; }

    /* ── Review modal ── */
    #review-modal {
      position: fixed; inset: 0; background: rgba(2,4,8,.93); z-index: 500;
      display: none; align-items: center; justify-content: center; padding: 20px;
    }
    #review-modal.open { display: flex; }
    .modal-card {
      background: var(--surf); border: 1px solid var(--border); border-radius: 4px;
      padding: 24px 20px; max-width: 480px; width: 100%;
    }
    .modal-result  { font-size: 15px; letter-spacing: 2px; margin-bottom: 8px; }
    .modal-result.pass { color: var(--green); }
    .modal-result.fail { color: var(--red); }
    #modal-answer { font-size: 11px; color: var(--amber); margin-bottom: 14px; letter-spacing: 1px; }
    .modal-exp-lbl { font-size: 9px; color: var(--muted); letter-spacing: 2px; margin-bottom: 6px; }
    #modal-expl { font-size: 12px; line-height: 1.8; color: #9aadcc; margin-bottom: 20px; }
    #modal-cont {
      width: 100%; background: transparent; border: 1px solid var(--cyan);
      color: var(--cyan); padding: 11px; font-family: var(--font);
      font-size: 11px; letter-spacing: 3px; cursor: pointer;
      border-radius: 2px; transition: all .2s;
    }
    #modal-cont:hover, #modal-cont:active { background: rgba(0,212,255,.1); }

    @media (max-width: 480px) {
      canvas { width: 108px; height: 108px; }
      .opt-grid { grid-template-columns: 1fr; }
      #q-text { font-size: 12px; }
    }
  </style>
</head>
<body>
"""

# ── Login screen ──────────────────────────────────────────────────────────────
_BODY_LOGIN = """\
<div id="login-screen">
  <div class="login-logo">⬡ SHATTERSCAN</div>
  <div class="login-sub">CORE DIAGNOSTIC PLATFORM — ASE A6 ELECTRICAL</div>
  <div class="legal-box">
    <h3>⚠ LOGIC BOUND STUDIOS — LEGAL LIABILITY NOTICE</h3>
    <p>This platform is provided for educational and study-preparation purposes only.
    Logic Bound Studios makes no warranty, express or implied, as to the accuracy,
    completeness, or fitness for any particular purpose of the content contained herein.
    All diagnostic scenarios are simulated and do not represent real vehicle data or
    real-time ECU telemetry.</p>
    <p>By engaging this system you acknowledge that you are solely responsible for any
    action taken based on information presented within this application. This software
    does not replace certified professional diagnostic equipment or qualified technician
    judgment. Logic Bound Studios shall not be held liable for any injury, vehicle
    damage, or financial loss arising from use or misuse of this platform.</p>
    <p>Proceed only if you agree to these terms in full and understand the simulated
    nature of all data displayed.</p>
  </div>
  <button id="accept-btn">I ACCEPT &amp; ENGAGE SYSTEM</button>
  <div class="login-ver">v1.0.0 — SHATTERSCAN CORE / ASE A6 LEVEL 1</div>
</div>
"""

# ── App screen ────────────────────────────────────────────────────────────────
_BODY_APP = """\
<div id="app-screen">
  <div class="app-header">
    <div>
      <div class="hdr-logo">⬡ SHATTERSCAN / A6-ELECTRICAL</div>
      <div class="hdr-sub">NEXT-GEN DIAGNOSTIC INTERFACE — LEVEL 1 STUDY RIG</div>
    </div>
    <div id="obd-status">DATALINK: OFFLINE</div>
  </div>

  <div class="gauges-section">
    <div class="dial-wrap">
      <canvas id="volt-canvas" width="200" height="200"></canvas>
    </div>
    <div class="dial-wrap">
      <canvas id="rpm-canvas" width="200" height="200"></canvas>
    </div>
    <div class="obd-col">
      <button id="obd-btn" onclick="toggleOBD()">⬡ CONNECT DATALINK</button>
      <div id="telem-log">-- AWAITING DATALINK --</div>
    </div>
  </div>

  <div class="quiz-section">
    <div class="quiz-header">
      <span id="q-counter">Q 1 / 10  |  Score: 0/0</span>
      <div class="prog-track"><div id="q-prog-fill"></div></div>
      <button id="tts-btn" onclick="replayTTS()">🔊 REPLAY</button>
    </div>
    <div>
      <div class="scenario-label">TECHNICIAN A &amp; B SCENARIO</div>
      <div id="q-text"></div>
    </div>
    <div class="opt-grid" id="q-options"></div>
  </div>
</div>
"""

# ── Review modal ──────────────────────────────────────────────────────────────
_MODAL_HTML = """\
<div id="review-modal">
  <div class="modal-card">
    <div id="modal-result" class="modal-result">—</div>
    <div id="modal-answer"></div>
    <div class="modal-exp-lbl">DIAGNOSTIC EXPLANATION</div>
    <div id="modal-expl"></div>
    <button id="modal-cont" onclick="closeModal()">CONTINUE →</button>
  </div>
</div>
"""

# ── JavaScript — raw string so every { } and \ is literal ────────────────────
# Unicode chars are kept as \u escapes so JS (not Python) resolves them.
_JS_CORE = r"""
/* ── state ── */
var currentIndex = 0;
var score        = 0;
var answered     = false;
var obdInterval  = null;
var voltageVal   = 12.6;
var rpmVal       = 800;

/* ── boot: login → app ── */
document.getElementById('accept-btn').addEventListener('click', function () {
  document.getElementById('login-screen').style.display = 'none';
  var app = document.getElementById('app-screen');
  app.style.display = 'flex';
  drawDial('volt-canvas', voltageVal, 0, 16,   'VOLTAGE',    'V',   '#00d4ff');
  drawDial('rpm-canvas',  rpmVal,     0, 8000, 'ENGINE RPM', 'rpm', '#ff9800');
  showQuestion(0);
});

/* ── canvas dial renderer ── */
function drawDial(canvasId, value, min, max, label, unit, accentColor) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var W = canvas.width, H = canvas.height;
  var cx = W / 2, cy = H / 2;
  var r  = Math.min(cx, cy) - 6;

  ctx.clearRect(0, 0, W, H);

  /* outer face */
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fillStyle = '#080b14';
  ctx.fill();
  ctx.strokeStyle = '#1e2840';
  ctx.lineWidth = 2;
  ctx.stroke();

  /* arc geometry: 135 deg start, 270 deg total sweep */
  var startA = Math.PI * 0.75;
  var totalA = Math.PI * 1.5;
  var pct    = Math.max(0, Math.min(1, (value - min) / (max - min)));
  var valueA = startA + totalA * pct;
  var trackR = r - 16;

  /* background track */
  ctx.beginPath();
  ctx.arc(cx, cy, trackR, startA, startA + totalA);
  ctx.strokeStyle = '#1a1e2e';
  ctx.lineWidth = 12;
  ctx.lineCap = 'round';
  ctx.stroke();

  /* value arc */
  if (pct > 0.005) {
    ctx.beginPath();
    ctx.arc(cx, cy, trackR, startA, valueA);
    ctx.strokeStyle = accentColor;
    ctx.lineWidth = 12;
    ctx.lineCap = 'round';
    ctx.stroke();
  }

  /* tick marks */
  for (var i = 0; i <= 8; i++) {
    var t      = i / 8;
    var tAngle = startA + totalA * t;
    var major  = (i % 2 === 0);
    var inner  = r - (major ? 28 : 23);
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(tAngle) * inner,    cy + Math.sin(tAngle) * inner);
    ctx.lineTo(cx + Math.cos(tAngle) * (r - 4),  cy + Math.sin(tAngle) * (r - 4));
    ctx.strokeStyle = major ? '#4a5878' : '#252d44';
    ctx.lineWidth   = major ? 2 : 1;
    ctx.lineCap = 'butt';
    ctx.stroke();
  }

  /* needle */
  ctx.beginPath();
  ctx.moveTo(cx - Math.cos(valueA) * 14, cy - Math.sin(valueA) * 14);
  ctx.lineTo(cx + Math.cos(valueA) * (trackR - 4), cy + Math.sin(valueA) * (trackR - 4));
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  ctx.stroke();

  /* hub dot */
  ctx.beginPath();
  ctx.arc(cx, cy, 5, 0, Math.PI * 2);
  ctx.fillStyle = accentColor;
  ctx.fill();

  /* value readout */
  ctx.fillStyle = '#ddeeff';
  ctx.font = 'bold 15px "Courier New", monospace';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  var valStr = (unit === 'V') ? value.toFixed(2) : String(Math.round(value));
  ctx.fillText(valStr + ' ' + unit, cx, cy + 26);

  /* label */
  ctx.font = '9px "Courier New", monospace';
  ctx.fillStyle = '#4a5878';
  ctx.fillText(label, cx, cy + 40);

  /* min / max corner labels */
  ctx.font = '8px "Courier New", monospace';
  ctx.fillStyle = '#2e3a54';
  var edge = r + 4;
  ctx.fillText(String(min), cx + Math.cos(startA) * edge, cy + Math.sin(startA) * edge);
  ctx.fillText(String(max), cx + Math.cos(startA + totalA) * edge,
                             cy + Math.sin(startA + totalA) * edge);
}

/* ── OBD-II simulation ── */
function toggleOBD() {
  var btn    = document.getElementById('obd-btn');
  var status = document.getElementById('obd-status');
  var log    = document.getElementById('telem-log');

  if (obdInterval) {
    clearInterval(obdInterval);
    obdInterval = null;
    btn.textContent = '⬡ CONNECT DATALINK';
    btn.classList.remove('active');
    status.textContent = 'DATALINK: OFFLINE';
    status.style.color = '';
    voltageVal = 12.6; rpmVal = 800;
    drawDial('volt-canvas', voltageVal, 0, 16,   'VOLTAGE',    'V',   '#00d4ff');
    drawDial('rpm-canvas',  rpmVal,     0, 8000, 'ENGINE RPM', 'rpm', '#ff9800');
    log.innerHTML = '-- DATALINK CLOSED --';
    return;
  }

  btn.textContent = '■ DISCONNECT';
  btn.classList.add('active');
  status.textContent = 'DATALINK: LIVE ●';
  status.style.color = '#00e676';
  log.innerHTML = '';

  obdInterval = setInterval(function () {
    voltageVal += (Math.random() - 0.48) * 0.34;
    voltageVal  = Math.max(11.5, Math.min(14.8, voltageVal));
    rpmVal     += (Math.random() - 0.5)  * 260;
    rpmVal      = Math.max(680, Math.min(5400, rpmVal));

    drawDial('volt-canvas', voltageVal, 0, 16,   'VOLTAGE',    'V',   '#00d4ff');
    drawDial('rpm-canvas',  rpmVal,     0, 8000, 'ENGINE RPM', 'rpm', '#ff9800');

    var ts   = new Date().toLocaleTimeString();
    var line = document.createElement('div');
    line.textContent = '[' + ts + ']  VBAT:' + voltageVal.toFixed(2) +
                       'V   RPM:' + Math.round(rpmVal);
    log.insertBefore(line, log.firstChild);
    if (log.children.length > 7) log.removeChild(log.lastChild);
  }, 750);
}

/* ── text-to-speech ── */
function speakQuestion(q) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  var letters  = ['A', 'B', 'C', 'D'];
  var optText  = q.options.map(function (o, i) {
    return letters[i] + ': ' + o;
  }).join('. ');
  var utter    = new SpeechSynthesisUtterance(q.q + '. Options: ' + optText);
  utter.rate   = 0.88;
  utter.pitch  = 1.0;
  window.speechSynthesis.speak(utter);
}

/* ── quiz engine ── */
function showQuestion(idx) {
  answered = false;
  var q   = A6_DATA[idx];
  var pct = Math.round((idx / A6_DATA.length) * 100);

  document.getElementById('q-prog-fill').style.width = pct + '%';
  document.getElementById('q-counter').textContent =
    'Q ' + (idx + 1) + ' / ' + A6_DATA.length + '  |  Score: ' + score + '/' + idx;
  document.getElementById('q-text').textContent = q.q;

  var grid = document.getElementById('q-options');
  grid.innerHTML = '';
  q.options.forEach(function (opt) {
    var btn       = document.createElement('button');
    btn.className = 'opt-btn';
    btn.textContent = opt;
    /* IIFE captures btn + opt so the closure is correct inside the loop */
    btn.addEventListener('click', (function (b, o) {
      return function () { if (!answered) selectAnswer(b, o, q); };
    }(btn, opt)));
    grid.appendChild(btn);
  });

  speakQuestion(q);
}

function selectAnswer(btn, chosen, q) {
  answered        = true;
  window.speechSynthesis.cancel();
  var correct     = (chosen === q.a);
  if (correct) score++;

  document.querySelectorAll('.opt-btn').forEach(function (b) {
    if (b.textContent === q.a) {
      b.classList.add('correct');
    } else if (b === btn && !correct) {
      b.classList.add('wrong');
    }
    b.disabled = true;
  });

  setTimeout(function () { showModal(correct, q); }, 550);
}

function showModal(correct, q) {
  var res = document.getElementById('modal-result');
  res.textContent = correct ? '✓ CORRECT' : '✗ INCORRECT';
  res.className   = 'modal-result ' + (correct ? 'pass' : 'fail');
  document.getElementById('modal-answer').textContent =
    'Correct answer: ' + q.a;
  document.getElementById('modal-expl').textContent = q.explanation;
  document.getElementById('review-modal').classList.add('open');
}

function closeModal() {
  document.getElementById('review-modal').classList.remove('open');
  currentIndex = (currentIndex + 1) % A6_DATA.length;
  if (currentIndex === 0) score = 0;   /* wrap-around resets score */
  showQuestion(currentIndex);
}

function replayTTS() {
  speakQuestion(A6_DATA[currentIndex]);
}
"""

if __name__ == "__main__":
    main()
