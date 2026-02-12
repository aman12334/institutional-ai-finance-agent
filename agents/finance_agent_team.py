import time
import re

from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

from core.analytics import build_analysis_summary


db = SqliteDb(db_file="agents.db")


# -----------------------------------
# Agent Team Builder
# -----------------------------------
def build_agent_team():

    bull = Agent(
        name="Bullish Analyst",
        role="Present upside thesis using only structured analytics.",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Use institutional tone.",
            "Highlight potential recovery drivers.",
            "Use only provided analytics.",
            "Do NOT invent numbers.",
        ],
        db=db,
        markdown=True,
    )

    bear = Agent(
        name="Bearish Analyst",
        role="Present downside risks and structural concerns.",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Emphasize volatility, drawdown, and downside persistence.",
            "Use only provided analytics.",
            "Do NOT invent numbers.",
        ],
        db=db,
        markdown=True,
    )

    risk = Agent(
        name="Chief Risk Officer",
        role="Evaluate institutional risk posture.",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Focus on volatility percentile and drawdown severity.",
            "Clearly separate facts from interpretation.",
            "Do NOT invent numbers.",
        ],
        db=db,
        markdown=True,
    )

    chair = Agent(
        name="Investment Committee Chair",
        role="Produce final institutional memo aligned to regime discipline.",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Review analyst perspectives.",
            "Weight conclusions according to regime severity.",
            "If DEFENSIVE, downside must dominate narrative.",
            "If CAUTION, balanced tone.",
            "If CONSTRUCTIVE, opportunity-focused tone.",
            "Never contradict regime classification.",
            "Do NOT invent numbers.",
        ],
        db=db,
        markdown=True,
    )

    return Team(
        name="Institutional Investment Committee",
        model=OpenAIChat(id="gpt-4o"),
        members=[bull, bear, risk, chair],
        markdown=True,
    )


# -----------------------------------
# Validation Layer
# -----------------------------------
def validate_narrative(narrative: str, summary: dict):

    validation = {
        "fabricated_numbers_detected": False,
        "regime_conflict": False,
        "allocation_conflict": False,
        "validation_notes": [],
    }

    numeric_values = re.findall(r"\d+\.?\d*", narrative)

    allowed_numbers = [
        str(summary.get("annualized_volatility")),
        str(summary.get("max_drawdown_pct")),
        str(summary.get("volatility_percentile")),
        str(summary.get("downtrend_days")),
        str(summary.get("recovery_probability_pct")),
    ]

    for num in numeric_values:
        if num not in allowed_numbers:
            validation["fabricated_numbers_detected"] = True
            validation["validation_notes"].append(
                f"Potential fabricated number detected: {num}"
            )

    regime = summary.get("regime")

    if regime == "DEFENSIVE":
        if "increase exposure" in narrative.lower():
            validation["allocation_conflict"] = True
            validation["validation_notes"].append(
                "Exposure increase suggested in DEFENSIVE regime."
            )

        if "strong upside" in narrative.lower():
            validation["regime_conflict"] = True
            validation["validation_notes"].append(
                "Optimistic tone conflicts with DEFENSIVE regime."
            )

    return validation


# -----------------------------------
# Consistency Scoring
# -----------------------------------
def compute_consistency_score(validation: dict):

    score = 100

    if validation["fabricated_numbers_detected"]:
        score -= 40

    if validation["regime_conflict"]:
        score -= 30

    if validation["allocation_conflict"]:
        score -= 30

    return max(score, 0)


# -----------------------------------
# Regime Override Layer (Hard Guardrail)
# -----------------------------------
def enforce_regime_override(narrative: str, summary: dict):

    regime = summary.get("regime")

    if regime == "DEFENSIVE":
        narrative += "\n\nFinal Deterministic Override: Capital preservation remains the dominant priority under the current DEFENSIVE regime. Increased exposure is not recommended."

    if regime == "CAUTION":
        narrative += "\n\nFinal Deterministic Override: Position sizing should remain moderate and closely monitored under CAUTION regime."

    if regime == "CONSTRUCTIVE":
        narrative += "\n\nFinal Deterministic Override: Opportunity bias acceptable within disciplined risk limits."

    return narrative


# -----------------------------------
# Main Orchestration
# -----------------------------------
def run_financial_intelligence(ticker: str):

    start_time = time.time()

    analysis_summary = build_analysis_summary(ticker)

    team = build_agent_team()

    prompt = f"""
Institutional Financial Intelligence Debate

Structured Analytics:
{analysis_summary}

Debate Order:
1. Bullish Analyst
2. Bearish Analyst
3. Chief Risk Officer
4. Investment Committee Chair

Rules:
- Use only provided analytics.
- Never contradict regime classification.
- Do NOT fabricate numerical data.
"""

    response = team.run(prompt)

    narrative = response.content if hasattr(response, "content") else str(response)

    # Regime-weighted enforcement
    narrative = enforce_regime_override(narrative, analysis_summary)

    # Validation
    validation = validate_narrative(narrative, analysis_summary)
    consistency_score = compute_consistency_score(validation)

    runtime_seconds = round(time.time() - start_time, 2)

    observability = {
        "ticker": ticker,
        "regime": analysis_summary.get("regime"),
        "risk_score": analysis_summary.get("risk_score"),
        "runtime_seconds": runtime_seconds,
        "narrative_length_chars": len(narrative),
    }

    return {
        "analysis_summary": analysis_summary,
        "agent_narrative": narrative,
        "validation": validation,
        "consistency_score": consistency_score,
        "observability": observability,
        "reasoning_log": [
            "Step 1: Deterministic analytics computed.",
            f"Step 2: Regime classified as {analysis_summary.get('regime')}.",
            "Step 3: Multi-agent debate executed.",
            "Step 4: Regime-weighted synthesis enforced.",
            "Step 5: Post-generation validation performed.",
            "Step 6: Observability metrics logged.",
        ],
    }
