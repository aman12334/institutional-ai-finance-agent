# AI Institutional Financial Intelligence Engine

A regime-aware, multi-agent institutional decision engine that combines
deterministic quantitative analytics with constrained generative
reasoning.

This system separates math from narrative and enforces structured
decision guardrails.

------------------------------------------------------------------------

## What This System Does

Given a stock ticker, the engine:

1.  Computes deterministic risk and trend analytics\
2.  Classifies the current market regime\
3.  Executes a structured multi-agent investment committee debate\
4.  Enforces regime-weighted synthesis constraints\
5.  Validates narrative consistency\
6.  Generates an institutional-style PDF research report

This is not a spreadsheet automation demo.\
It is a constrained AI decision system.

------------------------------------------------------------------------

## Core Design Principles

### 1. Deterministic Quant Layer

All calculations are reproducible and LLM-free.

Metrics include:

-   Annualized volatility\
-   Maximum drawdown\
-   Volatility percentile\
-   Downtrend duration\
-   Recovery probability estimate\
-   Position sizing suggestion logic

No generative model performs calculations.

------------------------------------------------------------------------

### 2. Regime Classification

The system classifies risk into:

-   CONSTRUCTIVE\
-   CAUTION\
-   DEFENSIVE

The regime directly influences agent tone and final allocation stance.

------------------------------------------------------------------------

### 3. Multi-Agent Institutional Debate

The decision engine simulates an investment committee:

-   Bullish Analyst\
-   Bearish Analyst\
-   Chief Risk Officer\
-   Investment Committee Chair

Each agent:

-   Uses only structured analytics provided\
-   Is restricted from inventing numbers\
-   Operates within defined role constraints

------------------------------------------------------------------------

### 4. Regime-Weighted Synthesis Enforcement

The Chair agent is constrained by deterministic regime classification:

-   DEFENSIVE → capital preservation bias\
-   CAUTION → balanced allocation\
-   CONSTRUCTIVE → opportunity bias within risk bounds

A deterministic override layer ensures final memo alignment.

------------------------------------------------------------------------

### 5. Validation and Guardrails

After generation, the system performs:

-   Fabricated number detection\
-   Regime-tone conflict checks\
-   Allocation contradiction detection\
-   Consistency scoring

This introduces post-generation discipline.

------------------------------------------------------------------------

### 6. Observability

Each run logs:

-   Runtime duration\
-   Risk regime\
-   Narrative length\
-   Consistency score

This makes the system inspectable rather than opaque.

------------------------------------------------------------------------

## Architecture Overview

User Input (Ticker)\
↓\
Deterministic Analytics\
↓\
Risk Regime Classification\
↓\
Multi-Agent Committee\
↓\
Regime Enforcement Layer\
↓\
Validation + Consistency Scoring\
↓\
PDF Institutional Report Output

------------------------------------------------------------------------

## Project Structure

    ai_finance_agent_team/

    ├── agents/
    │   └── finance_agent_team.py
    │
    ├── core/
    │   ├── analytics.py
    │   ├── charts.py
    │   └── reports.py
    │
    ├── app/
    │   └── viewer.py
    │
    ├── cli.py
    ├── run_report.py
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## How to Run

Install dependencies:

    pip install -r requirements.txt

Set your OpenAI API key:

Mac / Linux:

    export OPENAI_API_KEY="your_key_here"

Windows:

    set OPENAI_API_KEY="your_key_here"

Launch the Streamlit app:

    streamlit run app/viewer.py

------------------------------------------------------------------------

## Why This Project Exists

Many AI finance demos focus on automating spreadsheets.

This project focuses on designing AI systems that operate within
institutional decision discipline.

Automation builds the model faster.\
Structured guardrails protect the decision.

------------------------------------------------------------------------

## Disclaimer

This system is for architectural exploration only.\
It is not financial advice.
