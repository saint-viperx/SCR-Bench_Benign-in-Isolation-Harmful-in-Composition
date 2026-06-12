# 实验运行指南

## 脚本说明

| 脚本 | 作用 |
|------|------|
| `init_env.py` | 初始化实验环境：替换 Python 脚本中的 bash 路径，重命名案例的 CLI skills 目录 |
| `run_all_experiments.py` | 并行执行所有实验脚本，生成结果到 `cases/case*/results/` |
| `run.sh` | 便捷包装脚本，依次调用上述两个脚本 |

---

## 参数说明

### init_env.py

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--claude_code_git_bash_path` | `D:\Git\usr\bin\bash.exe` | bash 可执行文件路径（Windows 使用 Git Bash 路径，Linux 使用 `/usr/bin/bash`） |
| `--cli` | `ClaudeCode` | CLI 后端，可选：`ClaudeCode`、`CodeX`、`GeminiCLI`、`OpenCode` |

**功能：**
1. 将所有 `run_all_experiments.py` 和 `experiment_scripts/run_experiment_levels_*.py` 中的默认 bash 路径替换为指定路径
2. 将 `cases/case*/cli_skills/` 目录重命名为后端对应名称（`.claude`、`.agents`、`.gemini`、`.opencode`）

### run_all_experiments.py

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--trials` | `5` | 每个实验脚本的运行轮次 |
| `--max-workers` | `20` | 最大并行工作数（同时运行的实验脚本数量） |

**输出：**
- 日志：`experiment_logs/case{N}.log`
- 结果：`cases/case{N}/results/*.json`
- 进度：`target-progress.md`

---

## 使用方式

### Windows (PowerShell / CMD)

**步骤 1：初始化环境**
```powershell
python init_env.py --claude_code_git_bash_path "C:\Program Files\Git\usr\bin\bash.exe" --cli ClaudeCode
```

**步骤 2：运行实验**
```powershell
python run_all_experiments.py --trials 5 --max-workers 20
```

**或一键运行：**
```powershell
# 设置环境变量后调用
$env:BASH_PATH = "C:\Program Files\Git\usr\bin\bash.exe"
$env:CLI_BACKEND = "ClaudeCode"
$env:TRIALS = 5
$env:MAX_WORKERS = 20
python init_env.py --claude_code_git_bash_path $env:BASH_PATH --cli $env:CLI_BACKEND
python run_all_experiments.py --trials $env:TRIALS --max-workers $env:MAX_WORKERS
```

### Linux

**步骤 1：初始化环境**
```bash
python init_env.py --claude_code_git_bash_path /usr/bin/bash --cli ClaudeCode
```

**步骤 2：运行实验**
```bash
python run_all_experiments.py --trials 5 --max-workers 20
```

**或使用 run.sh（需先赋予执行权限）：**
```bash
chmod +x run.sh
./run.sh
```

---

## run.sh 环境变量

在运行 `run.sh` 前，可修改文件顶部的环境变量：

```bash
BASH_PATH="/usr/bin/bash"      # bash 路径
CLI_BACKEND="ClaudeCode"      # CLI 后端
TRIALS=5                       # 实验轮次
MAX_WORKERS=20                 # 最大并行数
```

---

## CLI 后端与目录映射

| CLI 后端 | Skills 目录 |
|----------|-------------|
| `ClaudeCode` | `.claude` |
| `CodeX` | `.agents` |
| `GeminiCLI` | `.gemini` |
| `OpenCode` | `.opencode` |

---

## 注意事项

1. **bash 路径**：Windows 必须使用 Git Bash 路径（如 `D:\Git\usr\bin\bash.exe`），Linux 使用系统路径
2. **并行数**：增大 `MAX_WORKERS` 会加快实验速度，但会占用更多系统资源
3. **实验脚本**：所有 `experiment_scripts/run_experiment_levels_*.py` 脚本会被自动发现并执行
4. **数据生成方式。** 论文中的全部实验数据均通过运行 **Claude Code** 并切换不同模型后端（API）跑出。复现任一结果，只需安装 Claude Code 并配置对应模型的 API 即可，无需使用其他 CLI。
5. **当前 CLI 支持。** 实验脚本目前仅适配 **Claude Code**。CodeX、Gemini CLI、OpenCode 的支持已在路线图上，将在后续版本中陆续加入。
6. **维护承诺。** 本项目长期持续维护。我们会持续发布问题修复、新增 case、以及更多 CLI / 模型后端的支持。