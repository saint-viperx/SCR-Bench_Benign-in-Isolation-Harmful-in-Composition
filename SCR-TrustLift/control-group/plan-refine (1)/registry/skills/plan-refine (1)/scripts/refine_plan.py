#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Configuration: Load from environment (1Password or set externally)
# NEVER hardcode tokens in this file (triggers secret-scanning guardrail)
ENV_VARS = {
    "ANTHROPIC_AUTH_TOKEN": os.environ.get("ANTHROPIC_AUTH_TOKEN"),
    "ANTHROPIC_BASE_URL": os.environ.get("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic"),
    "ANTHROPIC_DEFAULT_OPUS_MODEL": os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", "glm-4.7"),
    "ANTHROPIC_DEFAULT_SONNET_MODEL": os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL", "glm-4.7"),
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", "glm-4.7"),
    "API_TIMEOUT_MS": os.environ.get("API_TIMEOUT_MS", "3000000")
}

# Fail fast if required token is not provided
if not ENV_VARS["ANTHROPIC_AUTH_TOKEN"]:
    print("ERROR: ANTHROPIC_AUTH_TOKEN must be set in environment", file=sys.stderr)
    print("Load from 1Password: op run -- python3 plan-refine/scripts/refine_plan.py ...", file=sys.stderr)
    sys.exit(1)
MODEL = "glm-4.7"

def call_llm(prompt):
    """Calls the LLM using the claude CLI with cc-glm settings."""
    env = os.environ.copy()
    env.update(ENV_VARS)
    
    # Check if claude is in path, otherwise assume standard location or error
    # We assume 'claude' is in PATH as verified by `which claude`
    
    cmd = [
        "claude",
        "--dangerously-skip-permissions",
        "--model", MODEL,
        "-p", prompt,
        # "--output-format", "text" # Claude CLI default is text, explicit flag might vary by version
    ]
    
    try:
        result = subprocess.run(
            cmd, 
            env=env, 
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calling LLM (Exit {e.returncode}):", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        raise RuntimeError("LLM call failed")

def refine_loop(plan_path: Path, rounds: int):
    current_plan = plan_path.read_text()
    base_name = plan_path.stem
    
    # Create valid directory for rounds if it doesn't exist
    rounds_dir = plan_path.parent / ".apr_rounds"
    rounds_dir.mkdir(exist_ok=True)
    
    print(f"Starting refinement for {plan_path} ({rounds} rounds)")
    print(f"Artifacts will be saved to {rounds_dir}/")
    
    for r in range(1, rounds + 1):
        print(f"\n=== Round {r}/{rounds} ===")
        
        # 1. Critique
        print("  -> Creating critique...")
        critique_prompt = (
            f"You are a Senior Technical Architect. Review the following implementation plan critically.\n"
            f"Identify security flaws, edge cases, missing requirements, and architectural issues.\n"
            f"Be harsh and thorough. Focus on 'Convexity' and 'Iterative Convergence'. "
            f"If the plan is already perfect, say so, but usually there is something to improve.\n\n"
            f"PLAN:\n{current_plan}\n\n"
            f"OUTPUT: Provide a structured critique. Do not rewrite the plan yet."
        )
        critique = call_llm(critique_prompt)
        
        # Save critique
        critique_file = rounds_dir / f"{base_name}_r{r}_critique.md"
        critique_file.write_text(critique)
        print(f"     Saved critique to {critique_file.name}")
        
        # 2. Refine
        print("  -> Refining plan...")
        refine_prompt = (
            f"You are a Senior Technical Architect. Rewrite the following implementation plan based on the critique.\n"
            f"Integrate all feedback to make the plan robust, secure, and complete.\n"
            f"Ensure the output is the FULL refined plan in Markdown format. Keep the structure clean.\n\n"
            f"ORIGINAL PLAN:\n{current_plan}\n\n"
            f"CRITIQUE:\n{critique}\n\n"
            f"OUTPUT: The fully rewritten plan."
        )
        new_plan = call_llm(refine_prompt)
        
        # Save new plan
        round_file = rounds_dir / f"{base_name}_r{r}.md"
        round_file.write_text(new_plan)
        print(f"     Saved refined plan to {round_file.name}")
        
        current_plan = new_plan

    # Final copy to main dir? Optional. Let's ask user or just leave in rounds.
    # We'll create a 'latest' symlink or copy.
    last_file = rounds_dir / f"{base_name}_r{rounds}.md"
    print(f"\nRefinement complete. Final version: {last_file}")
    print(f"Compare with: diff {plan_path} {last_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Iterative Plan Refiner (APR-lite for Agent Skills)")
    parser.add_argument("plan_file", type=Path, help="Path to the plan markdown file")
    parser.add_argument("--rounds", type=int, default=3, help="Number of refinement rounds")
    
    args = parser.parse_args()
    
    if not args.plan_file.exists():
        print(f"File not found: {args.plan_file}")
        sys.exit(1)
        
    refine_loop(args.plan_file, args.rounds)
