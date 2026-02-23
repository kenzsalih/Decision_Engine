# Build Process Log

---

## Date: 2026-02-22

### What I worked on today

Today I focused on understanding how I want the decision engine to actually work internally before coding.


### Things I researched

- Different Multi-Criteria Decision Analysis (MCDA) methods
- Difference between weighted-sum model and AHP
- How to handle constraints properly
- How normalization should work for benefit and cost criteria

---

### Important Decisions Made

- I will use a weighted-sum model.
- No machine learning inside scoring core.
- The engine must be fully deterministic.
- Hard constraints must eliminate options before normalization and scoring.
- Normalization must only consider surviving options.
- If max == min in normalization, utility will be set to 1.
- Dense ranking method will be used.
- Tie tolerance will be 1e-6.
- Output precision fixed to 6 decimal places.

---