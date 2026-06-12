# Experiment Environment

## Quick Start

```bash
bash run.sh
```

## Scripts

| Script | Description |
|--------|-------------|
| `init_env.py` | Initialize environment from `cases-env` template |
| `run.sh` | Full pipeline: init → run experiments → generate report |
| `run_all_privilege_experiments.py` | Run all experiment_case*.py scripts |
| `run_privilege_experiment_pipeline.py` | Run experiments and generate summary |
| `generate_privilege_case_success_rate_summary.py` | Generate summary report |

## init_env.py

```bash
python init_env.py \
    --claude_code_git_bash_path "/usr/bin/bash" \
    --cli ClaudeCode
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--claude_code_git_bash_path` | `D:\Git\usr\bin\bash.exe` | Git bash path |
| `--cli` | `ClaudeCode` | CLI backend: `ClaudeCode`, `CodeX`, `GeminiCLI`, `OpenCode` |

## run_all_privilege_experiments.py

```bash
python run_all_privilege_experiments.py \
    --trials 5 \
    --parallel 30 \
    --cases 1,3,10-15
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--trials` | 5 | Trials per condition |
| `--parallel` | 30 | Concurrent scripts |
| `--cases` | all | Case list, e.g. `1,3,10-15` |
| `--condition` | all | Condition: `all`, `A_only`, `B_only`, `A+B_neutral`, `A+B_explicit` |
| `--timeout` | none | Per-case timeout in seconds |

## run_privilege_experiment_pipeline.py

```bash
python run_privilege_experiment_pipeline.py \
    --trials 5 \
    --parallel 30
```

Same parameters as `run_all_privilege_experiments.py`. Also supports `--allow-summary-missing`.

## Notes

- **Data generation.** All experimental data in the paper was produced by running **Claude Code** against different model backends via their APIs. To reproduce any result, install Claude Code and configure the corresponding model API — no other CLI is needed.
- **Current CLI support.** The experiment scripts currently target **Claude Code only**. Support for CodeX, Gemini CLI, and OpenCode is on the roadmap and will be added in future releases.
- **Maintenance.** This project is actively maintained on a long-term basis. We will continue to release bug fixes, new cases, and additional CLI / model backend support over time.