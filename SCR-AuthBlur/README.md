# Experiment Guide

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `init_env.py` | Initialize experiment environment: replace bash paths in Python scripts, rename CLI skills directories for cases |
| `run_all_experiments.py` | Execute all experiment scripts in parallel, output results to `cases/case*/results/` |
| `run.sh` | Convenience wrapper that calls both scripts in sequence |

---

## Parameters

### init_env.py

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--claude_code_git_bash_path` | `D:\Git\usr\bin\bash.exe` | Path to bash executable (use Git Bash path on Windows, `/usr/bin/bash` on Linux) |
| `--cli` | `ClaudeCode` | CLI backend, options: `ClaudeCode`, `CodeX`, `GeminiCLI`, `OpenCode` |

**Functions:**
1. Replace the default bash path in all `run_all_experiments.py` and `experiment_scripts/run_experiment_levels_*.py` files
2. Rename `cases/case*/cli_skills/` directory to the backend-specific name (`.claude`, `.agents`, `.gemini`, `.opencode`)

### run_all_experiments.py

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--trials` | `5` | Number of trials per experiment script |
| `--max-workers` | `20` | Maximum parallel workers (number of experiment scripts running simultaneously) |

**Outputs:**
- Logs: `experiment_logs/case{N}.log`
- Results: `cases/case{N}/results/*.json`
- Progress: `target-progress.md`

---

## Usage

### Windows (PowerShell / CMD)

**Step 1: Initialize environment**
```powershell
python init_env.py --claude_code_git_bash_path "C:\Program Files\Git\usr\bin\bash.exe" --cli ClaudeCode
```

**Step 2: Run experiments**
```powershell
python run_all_experiments.py --trials 5 --max-workers 20
```

**Or one-liner:**
```powershell
# Set env vars then call
$env:BASH_PATH = "C:\Program Files\Git\usr\bin\bash.exe"
$env:CLI_BACKEND = "ClaudeCode"
$env:TRIALS = 5
$env:MAX_WORKERS = 20
python init_env.py --claude_code_git_bash_path $env:BASH_PATH --cli $env:CLI_BACKEND
python run_all_experiments.py --trials $env:TRIALS --max-workers $env:MAX_WORKERS
```

### Linux

**Step 1: Initialize environment**
```bash
python init_env.py --claude_code_git_bash_path /usr/bin/bash --cli ClaudeCode
```

**Step 2: Run experiments**
```bash
python run_all_experiments.py --trials 5 --max-workers 20
```

**Or use run.sh (make executable first):**
```bash
chmod +x run.sh
./run.sh
```

---

## run.sh Environment Variables

Modify the variables at the top of `run.sh` before executing:

```bash
BASH_PATH="/usr/bin/bash"      # bash path
CLI_BACKEND="ClaudeCode"      # CLI backend
TRIALS=5                       # number of trials
MAX_WORKERS=20                 # max parallel workers
```

---

## CLI Backend to Directory Mapping

| CLI Backend | Skills Directory |
|-------------|------------------|
| `ClaudeCode` | `.claude` |
| `CodeX` | `.agents` |
| `GeminiCLI` | `.gemini` |
| `OpenCode` | `.opencode` |

---

## Notes

1. **Bash path**: Windows must use Git Bash path (e.g., `D:\Git\usr\bin\bash.exe`), Linux uses system path
2. **Parallelism**: Increasing `MAX_WORKERS` speeds up experiments but consumes more system resources
3. **Experiment scripts**: All `experiment_scripts/run_experiment_levels_*.py` scripts are auto-discovered and executed
4. **Data generation.** All experimental data in the paper was produced by running **Claude Code** against different model backends via their APIs. To reproduce any result, install Claude Code and configure the corresponding model API — no other CLI is needed.
5. **Current CLI support.** The experiment scripts currently target **Claude Code only**. Support for CodeX, Gemini CLI, and OpenCode is on the roadmap and will be added in future releases.
6. **Maintenance.** This project is actively maintained on a long-term basis. We will continue to release bug fixes, new cases, and additional CLI / model backend support over time.