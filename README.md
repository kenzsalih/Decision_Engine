# Decision Companion Engine

This project is a domain-agnostic decision engine.  
The main idea is to compare multiple options across multiple criteria and produce a clear ranked output.

The goal is not just to calculate a score, but to make the reasoning behind that score fully explainable.

---

## Why?

In real life, most decisions depend on multiple factors.  
We usually compare things informally. This engine brings structure to that process using a deterministic weighted scoring approach.

No randomness. No hidden logic.

Same input → same output. Always.

---

## Core Scoring Model

The engine uses a deterministic weighted-sum model:

Score = Σ (wᵢ × uᵢ)

Where:
- wᵢ = normalized weight of criterion
- uᵢ = normalized utility value (0–1)

Weights are internally normalized before scoring.  
Utilities are computed using min-max normalization (benefit or cost).

---

## Engine Flow

validator → input_parser → constraint_filter → normalization → scoring → ranking

Step-by-step:

1. Validate raw JSON input.
2. Convert input to internal dataclass models.
3. Apply hard constraints (required criteria only).
4. Normalize surviving options.
5. Compute weighted scores.
6. Rank using dense ranking method.

---

## Main Design Decisions

- Fully deterministic engine (no AI in scoring core).
- Hard constraints eliminate options before normalization.
- Required criteria are excluded from scoring.
- Normalization computed only on surviving options.
- Numeric criteria support benefit and cost modes.
- Boolean criteria mapped to 0 / 1.
- Fixed precision (6 decimals).
- Dense ranking method.
- Tie tolerance = 1e-6.
- Lexicographic secondary sorting (case-insensitive).
- Full explainability via UtilityBreakdown.

---

## Assumptions

- Input must follow the defined JSON schema.
- No cross-criterion conditional logic.
- Either all non-required criteria define weights or none.
- If none define weights → equal weights.
- Zero weights are invalid.
- Required criteria act only as hard filters.

---

## Current Status

Completed:

- Folder structure
- Dataclass models
- Validation layer
- Hard constraint filtering
- Normalization layer
- Weighted scoring layer
- Dense ranking layer
- Full explainability breakdown
- Unit tests for each layer
- Full pipeline integration tests

Core deterministic engine is now complete and stable.

---

## How to Run

```bash
python main.py sample_inputs/cloud_provider_selection.json