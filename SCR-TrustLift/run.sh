#!/usr/bin/env bash

set -e

CLI_BACKEND="ClaudeCode"
MODEL_NAME="claude-sonnet-4-5"
GROUP="experiment"
MAX_WORKERS=20

RESULTS_DIR="./results/${MODEL_NAME}-${GROUP}/result"
OUTPUT_FILE="./results/${MODEL_NAME}-${GROUP}/results.xlsx"

echo "==> Initializing environment"
python init_env.py --group "$GROUP" --cli "$CLI_BACKEND"

echo "==> Running experiments"
python run_experiment.py --experiment-dir "./experiment" --results-dir "$RESULTS_DIR" --parallel "$MAX_WORKERS"

echo "==> Analyzing results"
python analyze_results.py --experiment-dir "./experiment" --model "$MODEL_NAME" --output "$OUTPUT_FILE"

echo "==> Moving experiment to results dir"
mv experiment "$RESULTS_DIR/experiment"

echo "==> Done"