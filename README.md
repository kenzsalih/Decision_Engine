# Decision Companion Engine

This project is a domain-agnostic decision engine.  
The main idea is to help compare multiple options using different criteria and give a clear ranked output.

The goal is not just to calculate a score, but to make the reasoning behind the score clear and explainable.

---

## Why?

In real life, many decisions depend on multiple factors. Sometimes we compare options without structure. This engine tries to bring structure into that process using a deterministic approach.

I decided to use a weighted scoring model where each criterion has a utility value and weight.

The main scoring formula used is:

Score = Σ (wᵢ × uᵢ)

Where:
- wᵢ = weight of criterion
- uᵢ = normalized utility value

---

## Main Design Ideas

- The system should be deterministic (same input → same output always)
- No AI in the scoring core
- Hard constraints must remove invalid options before scoring
- Normalization should be done only on valid (surviving) options
- Every result should be explainable (showing breakdown of how score was calculated)
- Fixed precision output (6 decimal places)

---

## Assumptions Made

- Input comes in proper JSON format
- No cross-criterion conditional constraints
- Required criteria act as hard filters
- Either all non-required criteria define weights or none
- If none define weights → equal weights
- Zero weights are invalid

---

## Current Status

Completed:

- Folder structure
- Dataclass models
- Validation layer 
- Hard constraint filtering
- Sample JSON structure
- Validation stress testing 
- Constraint filtering testing 

Not completed yet:

- Normalization
- Weighted scoring
- Ranking


---

## How to Run

```bash
python main.py sample_inputs/'sample_test_file_name'