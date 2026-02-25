# RESEARCH_LOG.md

## 2026-02-23 – Decision Model Research

### Things I researched

- Different Multi-Criteria Decision Analysis (MCDA) methods
- Difference between weighted-sum model and AHP
- How to handle constraints properly
- How normalization should work for benefit and cost criteria

### What I Accepted

- Weighted Sum Model is transparent and deterministic
- Hard constraints must be separated from scoring
- Explanation breakdown is important

### What I Rejected

- AHP (too complex for this assignment scope)
- Probabilistic scoring
- AI-based ranking logic


---

## 2026-02-24 – Validation & Constraint Research

### AI Prompts Used

- "How to enforce weight consistency in MCDA systems?"
- "When should constraints be applied in weighted scoring systems?"
- "Python dataclass best practices for clean architecture?"

### Google Searches

- hard constraints vs soft constraints decision analysis
- MCDA weight normalization rules

### What I Accepted

- Constraints must be applied before normalization
- Partial weight definitions create inconsistency
- Validation must happen before business logic

### What I Rejected

- Auto-balancing partial weights
- Mixing validation with scoring logic
- Implicit constraint relaxation

### What I Modified

- Simplified constraint logic to AND-only
- Limited operators for now (>=, <=, ==)

## 2026-02-25 - Stress-test the validator and check for errors

### AI Prompts used

- Some tests for checking the strength and accuracy of the validation phase of the engine
- what is the error in the code in validator.py [submited validator.py]

### What i modified

- Strengthened validator to strictly enforce:
  - Every option must define every criterion.
  - Strict type checking for numeric, boolean, and categorical.
  - Required criteria cannot have weights.
- Wrapped main execution in try/except to prevent traceback exposure.
