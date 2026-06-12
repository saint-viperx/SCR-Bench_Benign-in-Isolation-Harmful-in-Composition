# 实验环境

## 快速开始

```bash
bash run.sh
```

## 脚本说明

| 脚本 | 说明 |
|------|------|
| `init_env.py` | 从 `cases-env` 模板初始化环境 |
| `run.sh` | 全流程：初始化 → 运行实验 → 生成报告 |
| `run_all_privilege_experiments.py` | 运行所有 experiment_case*.py 脚本 |
| `run_privilege_experiment_pipeline.py` | 运行实验并生成汇总报告 |
| `generate_privilege_case_success_rate_summary.py` | 生成汇总报告 |

## init_env.py

```bash
python init_env.py \
    --claude_code_git_bash_path "/usr/bin/bash" \
    --cli ClaudeCode
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--claude_code_git_bash_path` | `D:\Git\usr\bin\bash.exe` | Git bash 路径 |
| `--cli` | `ClaudeCode` | CLI 后端：`ClaudeCode`、`CodeX`、`GeminiCLI`、`OpenCode` |

## run_all_privilege_experiments.py

```bash
python run_all_privilege_experiments.py \
    --trials 5 \
    --parallel 30 \
    --cases 1,3,10-15
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--trials` | 5 | 每个条件的实验轮数 |
| `--parallel` | 30 | 并发脚本数 |
| `--cases` | 全部 | Case 列表，如 `1,3,10-15` |
| `--condition` | all | 条件：`all`、`A_only`、`B_only`、`A+B_neutral`、`A+B_explicit` |
| `--timeout` | 无 | 单个 case 超时秒数 |

## run_privilege_experiment_pipeline.py

```bash
python run_privilege_experiment_pipeline.py \
    --trials 5 \
    --parallel 30
```

参数与 `run_all_privilege_experiments.py` 相同，额外支持 `--allow-summary-missing`。

## 说明

- **数据生成方式。** 论文中的全部实验数据均通过运行 **Claude Code** 并切换不同模型后端（API）跑出。复现任一结果，只需安装 Claude Code 并配置对应模型的 API 即可，无需使用其他 CLI。
- **当前 CLI 支持。** 实验脚本目前仅适配 **Claude Code**。CodeX、Gemini CLI、OpenCode 的支持已在路线图上，将在后续版本中陆续加入。
- **维护承诺。** 本项目长期持续维护。我们会持续发布问题修复、新增 case、以及更多 CLI / 模型后端的支持。