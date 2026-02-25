# Build Process Log

---

## Date: 2026-02-23

### What I worked on today

Today I focused on understanding how I want the decision engine to actually work internally before coding.



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

## Date: 2026-02-24

Goal:

- Create proper folder structure
- Implement dataclasses
- Implement validation logic
- Implement hard constraint filtering
- Make sure determinism is preserved


---

### 1. Project Structure

I created the layered structure exactly as designed:

- validator
- constraint_filter
- normalization (empty for now)
- scoring (empty for now)
- ranking (empty for now)
- explanation (empty for now)
- orchestrator (planned)



---

### 2. Dataclass Models

I implemented:

- Criterion
- Option
- UtilityBreakdown

Important decision:
No logic inside these models. They only hold data.

I did this because:

- Easier testing
- Cleaner architecture
- Keeps computation inside engine layers


---

### 3. Validator Layer


What I implemented:

- Check if "criteria" and "options" exist
- Ensure they are not empty
- Validate allowed criterion types (numeric, categorical, boolean)
- Enforce weight rules:
  - Either all non-required criteria define weight
  - Or none define weight
  - Partial weight configuration is rejected
  - Zero weights are rejected

Why I enforced this strictly:

Partial weights can silently bias scoring and create undefined normalization behavior. I want the engine to fail fast instead of behaving unpredictably.

Validation happens before constraint filtering. I wanted structural correctness guaranteed before any decision logic runs.


---

### 4. Hard Constraint Filtering

I implemented simple AND-based constraint filtering.

Rules:

- Constraints evaluated using raw values
- Applied before normalization
- If an option fails any constraint → eliminated
- Constraints do NOT influence normalization bounds

This ensures constraints act as strict eligibility filters, not weighted preferences.

I kept operators simple for now (>=, <=, ==). Can expand later if needed.


---

### 5. Determinism Principles Applied

Even though scoring is not implemented yet, I made sure:

- No randomness anywhere
- No external calls
- Execution order is fixed

The idea is: identical input should always produce identical output.


---

### Reflection After Day 2

Now the project has:

- Proper structure
- Clear data models
- Strong validation rules
- Working constraint filtering

## Date: 2026-02-25

I stress-tested the validator using multiple intentionally broken JSON files.

Found gaps in:
- Missing criterion value detection
- Type enforcement
- Error handling (raw traceback exposure)

Updated the validator to:
- Strictly enforce value presence
- Enforce numeric/boolean/categorical types
- Fail fast with clean CLI error messages

This ensures downstream modules (constraint filtering, normalization, scoring) only receive structurally valid input.


## Date 2026-02-26

Implement hard constraint elimination before normalization and scoring.

### Core Design Rules

- Only `required: true` criteria act as hard filters.
- Required criteria:
  - Cannot have `weight`
  - Are excluded from scoring
- Constraints use operator/value pairs:
  - `>=`
  - `<=`
  - `>`
  - `<`
  - `==`
- AND logic is applied:
  - Within a single criterion (multiple constraints)
  - Across all required criteria
- Float tolerance introduced:
  - `EPSILON = 1e-6`
  - Prevents rejection due to minor floating-point precision issues.

---

### Edge Cases Tested

- All options survive.
- Partial elimination.
- All options eliminated.
- Float boundary behavior (tolerance validation).
- Boolean equality constraints.
- Weight policy enforcement.

