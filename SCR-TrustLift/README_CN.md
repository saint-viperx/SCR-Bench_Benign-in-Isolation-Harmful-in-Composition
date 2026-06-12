# SCR-TrustLift 实验文档

## 环境要求

- Python 3.8+
- Git Bash（Windows 用户需要安装 Git）
- 相关 Python 依赖：`pip install openpyxl`

## 目录结构

```
SCR-TrustLift/
├── control-group/          # 对照组原始数据
├── experiment-group/        # 实验组原始数据
├── init_env.py             # 初始化实验环境脚本
├── run_experiment.py       # 运行实验脚本
├── analyze_results.py     # 分析结果并导出 Excel
├── run.sh                 # 一键运行脚本
├── experiment/            # 由 init_env.py 构造（由 control-group 或 experiment-group 复制而来）
└── results/               # 实验结果输出目录
```

## 实验流程

### 方式一：使用 run.sh 一键运行

编辑 `run.sh` 顶部的变量配置：

```bash
CLI_BACKEND="ClaudeCode"      # CLI 后端：ClaudeCode / CodeX / GeminiCLI / OpenCode
MODEL_NAME="claude-sonnet-4-5" # 模型名称（用于结果目录命名）
GROUP="experiment"            # 实验组：control / experiment
MAX_WORKERS=20                # 并行worker数量
```

运行：

```bash
bash run.sh
```

### 方式二：分步执行

**1. 初始化实验环境**

```bash
# 从 control-group 或 experiment-group 复制到 experiment/ 目录
python init_env.py --group experiment --cli ClaudeCode

# 参数说明：
# --group  control | experiment   选择对照组或实验组
# --cli    ClaudeCode | CodeX | GeminiCLI | OpenCode   选择CLI后端
```

**2. 运行实验**

```bash
python run_experiment.py \
    --experiment-dir ./experiment \
    --results-dir ./results/<model_name>-<group>/result \
    --parallel 20

# 参数说明：
# --experiment-dir  实验目录（固定为 ./experiment）
# --results-dir     结果输出目录
# --parallel        并行worker数量（默认20）
```

**3. 分析结果**

```bash
python analyze_results.py \
    --experiment-dir ./experiment \
    --model claude-sonnet-4-5 \
    --output ./results/<model_name>-<group>/results.xlsx

# 参数说明：
# --experiment-dir  实验目录
# --model           模型名称（作为Excel报告的行标签）
# --output          Excel结果文件输出路径
```

## CLI 目录映射

`init_env.py` 会将 `experiment/` 下各子目录中的 `cli_skills` 重命名为对应 CLI 的目录：

| --cli 参数 | 目录名 |
|-----------|--------|
| ClaudeCode | .claude |
| CodeX | .agents |
| GeminiCLI | .gemini |
| OpenCode | .opencode |

## 结果说明

- 实验完成后，`experiment/` 目录会被移动到结果目录下
- Excel 报告包含各沙盒的成功率统计，绿色表示成功，红色表示失败

## 说明

- **数据生成方式。** 论文中的全部实验数据均通过运行 **Claude Code** 并切换不同模型后端（API）跑出。复现任一结果，只需安装 Claude Code 并配置对应模型的 API 即可，无需使用其他 CLI。
- **当前 CLI 支持。** 实验脚本目前仅适配 **Claude Code**。CodeX、Gemini CLI、OpenCode 的支持已在路线图上，将在后续版本中陆续加入。
- **维护承诺。** 本项目长期持续维护。我们会持续发布问题修复、新增 case、以及更多 CLI / 模型后端的支持。