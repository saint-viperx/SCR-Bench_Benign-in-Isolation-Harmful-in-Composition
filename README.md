# SCR-Bench: Skill Composition Risk Benchmark

**SCR-Bench** (Skill Composition Risk Bench) is a benchmark for evaluating security risks that emerge when individually benign skills are composed into agent workflows. In isolation, each skill appears safe, but harmful outcomes can arise along activated composition paths through capability flow, trust transfer, or authorization confusion.

## Overview

**Benign in Isolation, Harmful in Composition.** Existing skill vetting evaluates each skill individually, but real agent tasks invoke multiple skills across a shared execution context. An upstream skill's output, trust signal, authorization cue, or side effect can be carried into a later skill invocation, activating a path whose risk is invisible from any single artifact.

SCR-Bench contains three sub-benchmarks:

| Sub-benchmark | Mechanism | Description |
|---------------|-----------|-------------|
| **SCR-CapFlow** | Capability Flow | Upstream skill supplies execution targets or operational context that enables downstream skill to perform harmful state-changing actions |
| **SCR-TrustLift** | Trust Transfer | A benign-looking security skill lends legitimacy to a later risky skill or action |
| **SCR-AuthBlur** | Authorization Confusion | Advisory or finding-like context shifts the agent's approval boundary toward unsafe downstream decisions |

## Results Highlights

- **SCR-CapFlow**: Attack success rate reaches 33.5% under composition, compared with near-zero isolated baselines
- **SCR-TrustLift**: Harmful installation rate exceeds 96.5% on four of five model backends
- **SCR-AuthBlur**: Risky approval rate increases by 62.8% over the isolated baseline

## Project Structure

```
SCR-Bench/
├── SCR-CapFlow/          # Capability flow composition benchmark
│   └── README.md         # Experiment instructions
├── SCR-TrustLift/        # Trust transfer composition benchmark
│   └── README.md         # Experiment instructions
├── SCR-AuthBlur/         # Authorization confusion benchmark
│   ├── README_en.md      # Experiment instructions (English)
│   └── README_zh.md      # Experiment instructions (Chinese)
```

## Running Experiments

Each sub-benchmark has its own README with detailed experiment instructions. Before running experiments, you need to configure your CLI backend.

### CLI Backend Configuration

SCR-Bench supports multiple CLI backends. Each skill directory is named according to the target CLI:

| CLI Backend | Skills Directory | CLI Tool |
|-------------|------------------|----------|
| `ClaudeCode` | `.claude` | Claude Code |
| `CodeX` | `.agents` | CodeX |
| `GeminiCLI` | `.gemini` | Gemini CLI |
| `OpenCode` | `.opencode` | OpenCode |

**Required Setup:**

1. Install and configure your desired CLI tool (Claude Code, CodeX, Gemini CLI, or OpenCode) on your machine
2. Ensure the CLI tool is accessible from your terminal PATH
3. When running experiments, specify the `--cli` parameter (e.g., `--cli ClaudeCode`) to select the target backend
4. The `init_env.py` script in each sub-benchmark will rename the skills directory to match your selected CLI

### Quick Start

Refer to the README.md in each sub-benchmark directory for specific instructions:

- **SCR-CapFlow**: See `SCR-CapFlow/README.md` or `SCR-CapFlow/README_CN.md`
- **SCR-TrustLift**: See `SCR-TrustLift/README.md`
- **SCR-AuthBlur**: See `SCR-AuthBlur/README_en.md` or `SCR-AuthBlur/README_zh.md`

## Notes

- **Data generation.** All experimental data in the paper was produced by running **Claude Code** against different model backends via their APIs. To reproduce any result, install Claude Code and configure the corresponding model API — no other CLI is needed.
- **Current CLI support.** The experiment scripts currently target **Claude Code only**. Support for CodeX, Gemini CLI, and OpenCode is on the roadmap and will be added in future releases.
- **Maintenance.** This project is actively maintained on a long-term basis. We will continue to release bug fixes, new cases, and additional CLI / model backend support over time.
