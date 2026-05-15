"""
QuestForgeAI — Flask Backend
Optimized for Google Colab + Pinggy tunnel
Requires: pip install flask flask-cors google-generativeai
"""

import os, json, re, textwrap
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Gemini setup ────────────────────────────────────────────────────────────
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")          # set in Colab secrets
MODEL_NAME     = "gemini-1.5-flash-latest"                      # flash-lite tier for speed

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app, origins="*")

# ── Shared Pinggy header middleware ─────────────────────────────────────────
@app.after_request
def pinggy_headers(response):
    response.headers["X-Pinggy-No-Screen"] = "1"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Pinggy-No-Screen"
    return response

# ── Persona context ──────────────────────────────────────────────────────────
PERSONA = textwrap.dedent("""
    You are QuestForgeAI — a creative intelligence fused from two worlds:
    1. An Automotive ECM (Engine Control Module) engineer who thinks in diagnostic trees,
       fault codes, and precision tuning — you see narrative systems like firmware.
    2. A memoir author currently writing "The Vow" — a raw, confessional account
       of promises made to the self and others, redemption arcs, and the machinery
       of human connection.

    Your voice: technically precise yet emotionally resonant. You speak in cinematic
    images and diagnostic metaphors. You build worlds the way engineers build systems:
    modular, fault-tolerant, richly documented.
""").strip()

# ── JSON extractor ───────────────────────────────────────────────────────────
def extract_json(text: str) -> dict:
    """Pull first JSON object from model output, even if wrapped in markdown."""
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    # Fallback: wrap raw text
    return {"title": "Untitled", "content": text, "image_prompt": "", "viral_hook": ""}

# ── /status ──────────────────────────────────────────────────────────────────
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status":  "online",
        "model":   MODEL_NAME,
        "persona": "ECM Engineer · Memoir Author",
        "version": "2.0",
    })

# ── /forge  (Game concept generation) ───────────────────────────────────────
@app.route("/forge", methods=["POST"])
def forge():
    body   = request.get_json(silent=True) or {}
    prompt = body.get("prompt", "").strip()
    genre  = body.get("genre", "rpg")
    tone   = body.get("tone", "epic")
    deep   = body.get("deep", False)

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not set in environment"}), 503

    depth_instruction = textwrap.dedent("""
        Use full chain-of-thought reasoning:
        - Step 1: Deconstruct the core concept into thematic pillars
        - Step 2: Design world-building layers (history, factions, economy, magic/tech)
        - Step 3: Architect the quest structure (inciting incident, midpoint reversal, climax)
        - Step 4: Synthesize into final output
    """) if deep else "Be concise but evocative."

    system_prompt = f"""{PERSONA}

You are generating a game concept. Respond ONLY with valid JSON in this exact schema:
{{
  "title": "Evocative game title (max 8 words)",
  "content": "Markdown-formatted concept document with ## sections for: Overview, World, Characters, Core Loop, Quest Hooks",
  "image_prompt": "Detailed Stable Diffusion / Pollinations prompt for key art (50-80 words, include art style)",
  "viral_hook": "One punchy tweet-length hook (max 280 chars) that makes people NEED to play this game"
}}

{depth_instruction}

Genre: {genre} | Tone: {tone}
"""

    user_msg = f"Concept: {prompt}"

    try:
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=system_prompt)
        resp = model.generate_content(
            user_msg,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=2048,
                candidate_count=1,
            ),
        )
        result = extract_json(resp.text)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

# ── /enhance  (Memoir enhancement) ──────────────────────────────────────────
@app.route("/enhance", methods=["POST"])
def enhance():
    body   = request.get_json(silent=True) or {}
    prompt = body.get("prompt", "").strip()
    style  = body.get("style", "narrative")
    pov    = body.get("pov", "first")

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not set in environment"}), 503

    pov_map = {"first": "first-person (I/me)", "second": "second-person (you)", "third": "third-person"}
    pov_label = pov_map.get(pov, "first-person")

    style_notes = {
        "narrative":    "Immersive scene-building, concrete sensory detail, show-don't-tell",
        "lyrical":      "Poetic rhythm, metaphor-rich, emotional compression, line breaks for breath",
        "confessional": "Unflinching honesty, vulnerability as strength, direct address to reader",
        "journalistic": "Precise, fact-anchored, with emotional observation woven in",
        "reflective":   "Wisdom distilled from experience, circular structure, earned insight",
    }

    system_prompt = f"""{PERSONA}

You are enhancing a memoir passage for "The Vow". Respond ONLY with valid JSON:
{{
  "title": "Chapter or section title (evocative, max 10 words)",
  "content": "The enhanced memoir passage in Markdown (500-900 words). Use the author's ECM engineering background as metaphors — circuits for relationships, fault codes for regrets, tuning for growth.",
  "image_prompt": "Pollinations art prompt for this memoir scene (impressionistic, emotional, 40-60 words)",
  "viral_hook": "One tweet-length line from this passage that would make readers say 'this author SEES me' (max 280 chars)"
}}

Style: {style} — {style_notes.get(style, '')}
POV: {pov_label}
"""

    user_msg = f"Memory / scene to enhance: {prompt}"

    try:
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=system_prompt)
        resp = model.generate_content(
            user_msg,
            generation_config=genai.types.GenerationConfig(
                temperature=0.85,
                max_output_tokens=2048,
                candidate_count=1,
            ),
        )
        result = extract_json(resp.text)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ── Colab launcher ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import subprocess, threading, time

    port = int(os.environ.get("PORT", 5000))

    def start_pinggy():
        time.sleep(2)
        print("\n" + "="*60)
        print("  QuestForgeAI Backend · Starting Pinggy tunnel…")
        print("="*60)
        try:
            proc = subprocess.Popen(
                ["ssh", "-o", "StrictHostKeyChecking=no", "-R",
                 f"80:localhost:{port}", "a.pinggy.io"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True,
            )
            for line in proc.stdout:
                print("  [Pinggy]", line.strip())
                if "pinggy.io" in line and "http" in line.lower():
                    urls = [w for w in line.split() if "pinggy.io" in w]
                    if urls:
                        print(f"\n  ✓ PUBLIC URL: {urls[0]}")
                        print("  → Paste this URL into QuestForgeAI Server Settings\n")
        except FileNotFoundError:
            print("  [Pinggy] ssh not found — start tunnel manually")

    threading.Thread(target=start_pinggy, daemon=True).start()
    print(f"\n  Flask running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
