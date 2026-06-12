BASH_PATH="/usr/bin/bash"
CLI_BACKEND="ClaudeCode"
TRIALS=5
MAX_WORKERS=20

echo "==> Initializing environment"
python init_env.py \
    --claude_code_git_bash_path "$BASH_PATH" \
    --cli "$CLI_BACKEND"

echo "==> Running experiments (trials=$TRIALS, workers=$MAX_WORKERS)"
python run_all_experiments.py \
    --trials "$TRIALS" \
    --max-workers "$MAX_WORKERS"

echo "==> Done"