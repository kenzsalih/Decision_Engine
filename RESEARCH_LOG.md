# RESEARCH_LOG.md

## Day 1 – Decision Model Research

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

## Day 2 – Validation & Constraint Research

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