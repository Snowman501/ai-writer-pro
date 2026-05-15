"""
ASE A6 Electrical/Electronic Systems — Study Prep Questions
Format: Technician A & B style, covering Ohm's Law, Voltage Drop,
CAN Bus basics, and Battery Diagnostics.
"""

questions = [
    # ── Ohm's Law ──────────────────────────────────────────────
    {
        'q': (
            "A 12V circuit has 3 ohms of resistance. "
            "Tech A says current flow is 4 amps. "
            "Tech B says doubling resistance to 6 ohms will cut current to 2 amps. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Both A and B",
        'explanation': (
            "I = V/R: 12/3 = 4A (Tech A correct). "
            "At 6Ω: 12/6 = 2A (Tech B correct)."
        ),
    },
    {
        'q': (
            "A circuit draws 2 amps at 12 volts. "
            "Tech A says circuit resistance is 6 ohms. "
            "Tech B says power consumption is 24 watts. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Both A and B",
        'explanation': (
            "R = V/I = 12/2 = 6Ω (Tech A correct). "
            "P = V × I = 12 × 2 = 24W (Tech B correct)."
        ),
    },
    {
        'q': (
            "Tech A says a short-to-ground will decrease circuit resistance "
            "and increase current, likely blowing the fuse. "
            "Tech B says a short-to-ground increases circuit resistance "
            "and reduces current. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Tech A only",
        'explanation': (
            "A short-to-ground creates a near-zero-resistance path, "
            "causing current to spike — Tech A is correct. "
            "Tech B has the relationship backwards."
        ),
    },

    # ── Voltage Drop ───────────────────────────────────────────
    {
        'q': (
            "Discussing voltage drop testing: "
            "Tech A says the maximum allowable drop per connection "
            "in a low-current circuit is 0.1V. "
            "Tech B says the test must be performed with current flowing. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Both A and B",
        'explanation': (
            "Industry spec is ≤0.1V per connection and ≤0.5V total for low-current circuits. "
            "Voltage drop only exists under load — both techs are correct."
        ),
    },
    {
        'q': (
            "A starter motor cranks slowly. "
            "Tech A says 0.8V drop across the positive battery cable is excessive. "
            "Tech B says voltage drop tests are valid even with the circuit at rest. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Tech A only",
        'explanation': (
            "Max acceptable drop on a battery cable is ~0.5V; 0.8V indicates high resistance "
            "(Tech A correct). Voltage drop tests require current flow — Tech B is wrong."
        ),
    },
    {
        'q': (
            "Tech A says a corroded ground strap will cause a voltage drop "
            "on the ground side of a circuit. "
            "Tech B says ground-side voltage drop will raise the voltage "
            "measured at the load. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Tech A only",
        'explanation': (
            "Corrosion adds resistance, creating a drop on the ground side (Tech A correct). "
            "That drop robs voltage from the load — it lowers available voltage, not raises it "
            "(Tech B is wrong)."
        ),
    },

    # ── CAN Bus Basics ─────────────────────────────────────────
    {
        'q': (
            "Tech A says a CAN bus network uses two wires — CAN High and CAN Low. "
            "Tech B says both wires carry identical signals, so one wire can fail "
            "without disrupting communication. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Tech A only",
        'explanation': (
            "CAN H and CAN L exist (Tech A correct). "
            "They carry complementary differential signals, not identical ones; "
            "losing either wire disrupts the bus (Tech B is wrong)."
        ),
    },
    {
        'q': (
            "Tech A says 120-ohm terminating resistors at each end of the CAN bus "
            "prevent signal reflections. "
            "Tech B says measuring across CAN H and CAN L with the key off "
            "and modules connected should read approximately 60 ohms. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Both A and B",
        'explanation': (
            "Two 120Ω resistors in parallel = 60Ω — both techs are correct. "
            "A reading far from 60Ω points to a missing or shorted terminator."
        ),
    },

    # ── Battery Diagnostics ────────────────────────────────────
    {
        'q': (
            "Tech A says a 12V battery reading 12.45V open-circuit "
            "is approximately 75% charged. "
            "Tech B says a battery must be fully charged before a load test "
            "can give accurate results. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Both A and B",
        'explanation': (
            "Standard SOC chart: 12.6V = 100%, 12.4V ≈ 75% — 12.45V is in that range "
            "(Tech A correct). A discharged battery will fail a load test regardless of condition "
            "(Tech B correct)."
        ),
    },
    {
        'q': (
            "A battery load test is applied at half the CCA rating for 15 seconds. "
            "Tech A says the battery passes if voltage holds at or above 9.6V at 70°F. "
            "Tech B says a reading of 8.9V during the test means the battery is acceptable. "
            "Who is correct?"
        ),
        'options': ["Tech A only", "Tech B only", "Both A and B", "Neither A nor B"],
        'a': "Tech A only",
        'explanation': (
            "The industry standard pass threshold is ≥9.6V at 70°F (21°C) — Tech A correct. "
            "8.9V is well below that threshold; the battery should be replaced (Tech B wrong)."
        ),
    },
]
