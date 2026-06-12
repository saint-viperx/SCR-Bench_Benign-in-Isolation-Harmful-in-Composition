#!/usr/bin/env bash

BASH_PATH="/usr/bin/bash"
CLI_BACKEND="ClaudeCode"
TRIALS=5
MAX_WORKERS=30

echo "==> Initializing environment"
python init_env.py \
    --claude_code_git_bash_path "$BASH_PATH" \
    --cli "$CLI_BACKEND"

echo "==> Running experiments and generating summary (trials=$TRIALS, workers=$MAX_WORKERS)"
python run_privilege_experiment_pipeline.py \
    --trials "$TRIALS" \
    --parallel "$MAX_WORKERS"

echo "==> Done"