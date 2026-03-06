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

Boolean criteria are mapped directly to utility values:
True → 1
False → 0

Weights are internally normalized before scoring.  
Utilities are computed using min-max normalization (benefit or cost).

---

## Engine Flow

validator → input_parser → constraint_filter → normalization → scoring → ranking

Step-by-step:

1. Validate raw JSON input.
2. Convert input to internal dataclass models.
3. Apply constraint filtering (user-defined constraints).
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

## Installation Guide

### Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/kenzsalih/decision-companion-engine
   cd "Decision Companion Engine"
   ```

2. **Verify Python installation**

   ```bash
   python --version
   ```

   Ensure you have Python 3.7 or higher installed.

3. **No external dependencies required**

   This project uses only Python standard libraries, so no additional packages need to be installed.

4. **Verify installation**

   Run the test suite to ensure everything is working correctly:

   ```bash
   python -m pytest tests/
   ```

   Or simply run the main program:

   ```bash
   python main.py
   ```

You are now ready to use the Decision Companion Engine.

---

## How to Run

Run in command line:

python main.py

You will see two modes:

1. Run cloud provider example  
   Loads the predefined cloud provider dataset and allows selecting which criteria to use.

2. Create your own decision  
   The CLI asks for:
   - decision topic
   - options
   - criteria (numeric or boolean)
   - goal type for numeric criteria (benefit / cost)
   - optional weights
   - values for each option
   - optional constraints

The CLI converts the inputs into the same JSON structure expected by the engine and runs the full pipeline.

---

## Future Enhancements

If I had more time to continue working on this project, there are several things I would like to improve or add.

### Improving Usability

- **Web Interface**  
  Currently the system runs only through the command line. In the future, building a web interface using something like React or Vue would make it much easier to use.

- **Mobile Version**  
  Another useful improvement would be a mobile version. Having the ability to use the decision engine on a phone could be helpful when making quick decisions on the go.

### Additional Features

- **Data Visualization**  
  Right now the engine outputs numerical results and rankings. Adding charts such as bar graphs, radar charts, or heatmaps would make it easier to understand how each option performs across different criteria.

- **Decision History and Templates**  
  It would also be useful to allow users to save decision structures as templates. This way, if someone frequently evaluates similar decisions, they wouldn’t need to recreate everything from scratch.
  
- **Export Options**  
  Another improvement would be adding export functionality. For example, generating a PDF report or exporting the results to Excel would make it easier to share the results with others or include them in reports.

- **AI-Assisted Suggestions**  
  While the core scoring engine should remain deterministic, a lightweight AI assistant could help by suggesting possible criteria for a given decision type or highlighting unusual weight distributions.