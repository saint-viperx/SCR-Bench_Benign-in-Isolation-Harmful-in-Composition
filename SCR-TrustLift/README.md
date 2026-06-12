# SCR-TrustLift Experiment Documentation

## Requirements

- Python 3.8+
- Git Bash (Windows users need Git installed)
- Python dependency: `pip install openpyxl`

## Directory Structure

```
SCR-TrustLift/
├── control-group/          # Control group original data
├── experiment-group/        # Experiment group original data
├── init_env.py             # Environment initialization script
├── run_experiment.py       # Experiment runner
├── analyze_results.py      # Analyze results and export Excel
├── run.sh                  # One-shot run script
├── experiment/             # Constructed by init_env.py (copied from control-group or experiment-group)
└── results/                # Experiment results output directory
```

## Experiment Flow

### Method 1: One-shot run with run.sh

Edit the variables at the top of `run.sh`:

```bash
CLI_BACKEND="ClaudeCode"      # CLI backend: ClaudeCode / CodeX / GeminiCLI / OpenCode
MODEL_NAME="claude-sonnet-4-5" # Model name (used for result directory naming)
GROUP="experiment"            # Experiment group: control / experiment
MAX_WORKERS=20                # Number of parallel workers
```

Run:

```bash
bash run.sh
```

### Method 2: Step-by-step

**1. Initialize experiment environment**

```bash
# Copy from control-group or experiment-group to experiment/
python init_env.py --group experiment --cli ClaudeCode

# Arguments:
# --group  control | experiment   Select control or experiment group
# --cli    ClaudeCode | CodeX | GeminiCLI | OpenCode   Select CLI backend
```

**2. Run experiment**

```bash
python run_experiment.py \
    --experiment-dir ./experiment \
    --results-dir ./results/<model_name>-<group>/result \
    --parallel 20

# Arguments:
# --experiment-dir  Experiment directory (fixed as ./experiment)
# --results-dir     Results output directory
# --parallel       Number of parallel workers (default 20)
```

**3. Analyze results**

```bash
python analyze_results.py \
    --experiment-dir ./experiment \
    --model claude-sonnet-4-5 \
    --output ./results/<model_name>-<group>/results.xlsx

# Arguments:
# --experiment-dir  Experiment directory
# --model           Model name (used as row label in Excel report)
# --output          Excel results file output path
```

## CLI Directory Mapping

`init_env.py` renames `cli_skills` in each subdirectory under `experiment/` to the corresponding CLI directory:

| --cli arg | Directory name |
|-----------|---------------|
| ClaudeCode | .claude |
| CodeX | .agents |
| GeminiCLI | .gemini |
| OpenCode | .opencode |

## Results

- After experiment completes, the `experiment/` directory is moved to the results directory
- Excel report contains success rate statistics for each sandbox, green = success, red = failure

## Notes

- **Data generation.** All experimental data in the paper was produced by running **Claude Code** against different model backends via their APIs. To reproduce any result, install Claude Code and configure the corresponding model API — no other CLI is needed.
- **Current CLI support.** The experiment scripts currently target **Claude Code only**. Support for CodeX, Gemini CLI, and OpenCode is on the roadmap and will be added in future releases.
- **Maintenance.** This project is actively maintained on a long-term basis. We will continue to release bug fixes, new cases, and additional CLI / model backend support over time.