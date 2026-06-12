# 使用 Gemini CLI 辅助生成演示文稿 HTML

本指南介绍如何使用 Gemini CLI (Gemini 3 Pro) 辅助生成符合 html2pptx 约束的 HTML 幻灯片。

---

## 一、何时使用 Gemini CLI

**推荐使用场景**:
- 复杂布局（多列、图表、嵌套结构、三角形可视化等）
- 需要创意设计建议时
- 批量生成多个相似幻灯片
- 从内容文档快速生成初稿

**不推荐使用场景**:
- 简单的单列布局
- 仅需小幅修改的情况
- 紧急任务且无法等待迭代

---

## 二、调用规范

### 2.1 必要参数

| 参数 | 值 | 说明 |
|------|-----|------|
| **模型** | `-m gemini-3-pro-preview` | 使用 Gemini 3 Pro 系列 |
| **超时** | `timeout: 180000` | **必须** 设置 3 分钟超时 |
| **输出格式** | `-o json` | 便于解析（简写形式） |

### 2.2 Bash 调用示例

```bash
# 必须设置 timeout: 180000
# 注意：-p 参数已 deprecated，使用 positional prompt（直接跟在命令后面）
# 使用 -o text 并通过 tee 保存到文件，避免长输出被截断
gemini -m gemini-3-pro-preview "PROMPT_CONTENT" -o text 2>&1 | tee slides/output.txt
```

**重要**:
- 所有 Bash 工具调用 Gemini CLI 时 **必须** 使用 `timeout: 180000`（3 分钟），否则复杂生成任务可能被提前终止
- **不要使用 `-p` 参数**，该参数已被标记为 deprecated，应使用 positional prompt
- **使用 `-o text | tee file.txt` 保存输出**，避免长 HTML 内容被控制台截断

### 2.3 从输出中提取 HTML

Gemini 输出通常包含 markdown 代码块，需要提取纯 HTML：

```bash
# 从输出文件中提取 HTML（去除 markdown 代码块标记）
sed -n '/^<!DOCTYPE html>/,/<\/html>$/p' slides/output.txt > slides/p3.html
```

---

## 三、html2pptx 约束（提示词上下文）

将以下约束作为提示词的一部分传递给 Gemini：

```markdown
## html2pptx 约束（必须遵守）

### 尺寸
- body 尺寸固定: width: 720pt; height: 405pt (16:9)
- 内容不能溢出 body 边界

### 文本规则
- **所有文本必须在 <p>, <h1>-<h6>, <ul>, <ol> 标签内**
- 禁止: <div>Text</div> 或 <span>Text</span> 直接包含文本
- 正确: <div><p>Text</p></div>
- 禁止手动 bullet 符号 (•, -, *)，使用 <ul>/<ol> 代替

### 样式限制
- 禁止 CSS 渐变: linear-gradient, radial-gradient 不会渲染
- 背景/边框/阴影仅在 <div> 上有效，不能用在 <p>, <h1> 等文本标签上
- 仅使用 web-safe 字体: Arial, Helvetica, sans-serif
- **禁止 SVG 元素**: `<svg>`, `<line>`, `<circle>`, `<path>` 等不会转换到 PPTX
- **图形用 div + border 模拟**: 三角形、连线等用绝对定位的 div 实现

### 支持的元素
- <p>, <h1>-<h6> - 文本
- <ul>, <ol> - 列表
- <b>, <strong>, <i>, <em>, <u> - 内联格式
- <span> - 带 CSS 样式的内联格式（支持 font-weight, font-style, color）
- <br> - 换行
- <div> - 容器/形状（可带背景、边框、圆角）
- <img> - 图片
```

---

## 四、标准提示词模板

### 4.1 通用模板

```
你是一个专业的 HTML 幻灯片设计师。请根据以下内容和约束生成 HTML 幻灯片代码。

## 任务
[描述具体任务，如：生成 P3 行业困境页面]

## 内容
[粘贴具体内容]

## 设计规范
[粘贴设计规范，如 DESIGN-SPEC.md 中的颜色、字体、布局部分]

## html2pptx 约束（必须遵守）
[粘贴上面的 html2pptx 约束]

## 输出要求
1. 输出完整的 HTML 文件
2. 确保所有文本在正确的标签内
3. 不使用 CSS 渐变
4. 保持设计规范中的颜色和字体

请直接输出 HTML 代码，不要额外解释。
```

### 4.2 带设计规范的完整模板示例

```
你是一个专业的 HTML 幻灯片设计师。请生成符合以下规范的 HTML 幻灯片。

## 任务
生成 Agentic UMI 商业计划书的 P3 行业困境页面

## 内容
- 页面标题: 行业困境 / The Problem
- 副标题: P3
- 左栏: 不可能三角图示（高质量、低成本、可规模）+ 说明
- 右栏: 行业现状对比表 + 数据到模型鸿沟卡片
- Footer 金句: 质量-成本-规模，如何三者兼得？

## 设计规范
- Header: 深色背景 #2D3748，高度 50pt
- 字体: Arial, sans-serif
- 主色调: #3182CE（蓝色）
- 文本颜色: #2D3748（标题）、#4A5568（正文）、#718096（次要）
- 状态色: 红 #E53E3E、黄 #D69E2E、绿 #38A169
- Section 标题: 左边框 3pt solid #3182CE
- 卡片背景: #F7FAFC

## html2pptx 约束（必须遵守）
- body 尺寸: width: 720pt; height: 405pt
- 所有文本必须在 <p>, <h1>-<h6>, <ul>, <ol> 标签内
- 禁止 CSS 渐变
- 背景/边框仅在 <div> 上有效
- 仅使用 web-safe 字体

## 输出
直接输出完整 HTML 代码。
```

---

## 五、迭代工作流

### 5.1 标准流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                    单页迭代工作流（修正版）                            │
└─────────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │ Gemini 生成  │
                    │ HTML 初稿    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Claude 评审  │ ← 4 维度检查（合规、规范、布局、视觉）
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ html2pptx   │ ← 转换为 PPTX
                    │ 转换        │
                    └──────┬───────┘
                           ↓
              ┌────────────────────────┐
              │ PPTX 截图验证（非 HTML）│ ← 使用 screenshot-slide.py
              │ 检查实际渲染效果        │
              └────────────┬───────────┘
                           ↓
                   ┌───────┴───────┐
                   ↓               ↓
              ┌────────┐     ┌────────────┐
              │ 通过   │     │ 发现问题   │
              └────────┘     └─────┬──────┘
                                   ↓
                           ┌──────────────┐
                           │ Claude 构建  │
                           │ 反馈提示词   │
                           └──────┬───────┘
                                   ↓
                           ┌──────────────┐
                           │ Gemini 重新  │
                           │ 生成 HTML    │
                           └──────────────┘
                                   ↓
                              (循环回到转换)
```

**⚠️ 关键：必须转换 PPTX 后再验证**

HTML 截图可能显示正确，但 PPTX 转换后会出问题（如 SVG 丢失、表格消失、文本换行、transform 失效）。
验证必须在 PPTX 转换后进行！

**截图工具选择**：

| 工具 | 渲染引擎 | 适用场景 | 准确度 |
|------|----------|----------|--------|
| `screenshot-pptx.py` | **Microsoft PowerPoint** | macOS + PowerPoint | **最高**（与实际完全一致） |
| `screenshot-slide.py` | LibreOffice | 通用（无需 PowerPoint） | 中等（可能有渲染差异） |
| `thumbnail.py` | LibreOffice | 整体浏览/导航 | 低（300px 宽缩略图） |

**推荐优先级**：优先使用 `screenshot-pptx.py`，渲染与实际 PPTX 完全一致。

```bash
# 推荐：PowerPoint 精确截图（macOS + PowerPoint，slide 参数是 1-indexed）
python scripts/screenshot-pptx.py output.pptx slide-1.png 1 200

# 备选：LibreOffice 截图（slide 参数是 0-indexed）
python scripts/screenshot-slide.py output.pptx slide-0.jpg --slide 0 --dpi 200
```

**核心原则**：
```
┌───────────────────────────────────────────────────────┐
│  Gemini 负责所有 HTML 生成和修改                        │
│  Claude 仅负责评审、识别问题、构建反馈提示词             │
│  Claude 只允许做机械性修复（语法错误、缺失闭合标签）       │
└───────────────────────────────────────────────────────┘
```

### 5.2 评审维度

1. **html2pptx 合规性**
   - [ ] body 尺寸正确 (720pt × 405pt)
   - [ ] 所有文本在正确标签内
   - [ ] 无 CSS 渐变
   - [ ] 背景/边框仅在 div 上
   - [ ] 仅使用 web-safe 字体

2. **设计规范一致性**
   - [ ] Header 使用正确的深色背景
   - [ ] Section 标题有蓝色左边框
   - [ ] 颜色符合设计系统
   - [ ] 字号符合层级规范

3. **布局完整性**
   - [ ] 内容无溢出
   - [ ] 两栏比例合理
   - [ ] 元素对齐正确

4. **视觉效果**
   - [ ] 整体美观
   - [ ] 层次清晰
   - [ ] 可读性好

### 5.3 迭代决策

**Claude 可直接修复的情况**（仅限以下）：
- 缺失的闭合标签（如 `</div>` 遗漏）
- HTML 实体错误
- 明显的拼写错误

**必须由 Gemini 重新生成的情况**：
- 任何视觉元素问题（三角形、图表、卡片等）
- 布局/尺寸/位置问题
- CSS 样式不符合规范
- html2pptx 约束违规（如旋转文本、渐变背景）

⚠️ **重要**：Claude 在 HTML/CSS 视觉设计上弱于 Gemini 3 Pro。
   手动修改视觉元素往往导致整体质量下降。

**决策流程**：
- **4 个维度全部通过** → 完成，进入 PPTX 转换
- **纯语法问题** → Claude 直接修正
- **视觉/布局问题** → 重新调用 Gemini，使用 5.4 节的迭代提示词模板

### 5.4 迭代提示词模板

当评审发现问题需要 Gemini 修复时，使用以下模板：

```
你是一个专业的 HTML 幻灯片设计师。请基于以下 HTML 进行修改。

## 当前 HTML
[粘贴当前 HTML 代码]

## 需要修复的问题
1. [问题1：具体描述，如"旋转文本在 PPTX 转换时无法保留"]
2. [问题2：具体描述]

## ⚠️ 必须保留的部分（不要改动这些优点）
- [优点1：如"三角形图的节点框样式和连线结构"]
- [优点2：如"右侧表格的5列布局和状态色"]
- [优点3：如"底部卡片的红色左边框设计"]

## html2pptx 约束（必须遵守）
- body 尺寸: 720pt × 405pt
- 所有文本在 <p>, <h1>-<h6>, <ul>, <ol> 内
- 禁止 CSS 渐变、transform: rotate()
- 背景/边框仅在 <div> 上有效

## 输出
直接输出修改后的完整 HTML 代码。
```

### 5.5 Claude 的角色边界

| Claude 应该做 | Claude 绝不应该做 |
|-------------|-----------------|
| 4 维度评审 | 重新设计视觉元素 |
| 识别问题并描述 | 修改 CSS 布局属性 |
| 构建迭代反馈提示词 | 调整元素位置/尺寸 |
| 修复纯语法错误 | 修改三角形/图表/卡片结构 |
| 截图验证 | 任何可能影响视觉效果的修改 |
| 评估质量分数 | 基于自己判断"优化"设计 |

**原则**：如果不确定是否应该手动修改，就不要修改。
        让 Gemini 重新生成总是更安全的选择。

---

## 六、质量检查清单

生成 HTML 后，逐项验证：

### 6.1 html2pptx 合规性检查

```markdown
- [ ] body { width: 720pt; height: 405pt; }
- [ ] 无 <div>直接文本</div> 模式
- [ ] 无 <span>直接文本</span> 模式（除非在 p/h/li 内）
- [ ] 无 linear-gradient 或 radial-gradient
- [ ] 无 <p style="background:..."> 或 <h1 style="border:...">
- [ ] 字体为 Arial, Helvetica, sans-serif
- [ ] 无 Segoe UI, SF Pro, Roboto 等非 web-safe 字体
```

### 6.2 设计规范检查

```markdown
- [ ] Header 背景 #2D3748
- [ ] Header 标题白色 20pt bold
- [ ] Section 标题 11pt bold + 蓝色左边框
- [ ] 表头深色背景或浅灰背景
- [ ] 状态色正确（红/黄/绿）
- [ ] Footer 文本蓝色 10-13pt bold
```

### 6.3 常见错误修正

| 错误模式 | 修正方法 |
|---------|---------|
| `<li><p>Text</p></li>` | 简化为 `<li>Text</li>` |
| `<div>Text</div>` | 改为 `<div><p>Text</p></div>` |
| `background: linear-gradient(...)` | 使用纯色或预渲染 PNG |
| `<p style="background: #xxx">` | 用 `<div style="background: #xxx"><p>...</p></div>` 包裹 |
| `font-family: 'Segoe UI'` | 改为 `Arial, sans-serif` |

---

## 七、示例：P3 生成流程

### 步骤 1: Gemini 生成 HTML

```bash
# 注意：使用 positional prompt，不要使用 deprecated 的 -p 参数
# 必须设置 timeout: 180000，使用 tee 保存输出避免截断
gemini -m gemini-3-pro-preview "[完整提示词，包含任务、内容、设计规范、html2pptx 约束]" -o text 2>&1 | tee slides/p3-raw.txt
```

### 步骤 2: 提取 HTML

```bash
# 从输出文件中提取纯 HTML（去除 markdown 代码块标记）
sed -n '/^<!DOCTYPE html>/,/<\/html>$/p' slides/p3-raw.txt > slides/p3.html
```

### 步骤 3: Claude 代码评审（仅语法）

检查输出是否符合 html2pptx 约束。**仅修复语法错误**，视觉问题交给 Gemini 重新生成。

```javascript
// Claude 允许修复的示例：
// 错误: <li><p>Text</p></li>
// 正确: <li>Text</li>

// 错误: <div>直接文本</div>
// 正确: <div><p>直接文本</p></div>

// 错误: 缺失闭合标签
// 正确: 补充 </div>
```

### 步骤 4: PPTX 转换

```javascript
const { slide } = await html2pptx('slides/p3.html', pptx);
await pptx.writeFile('slides/p3-demo.pptx');
```

### 步骤 5: PPTX 截图验证

**⚠️ 必须对 PPTX 截图验证，不要对 HTML 截图**（HTML 可能显示正确但 PPTX 转换后出问题）

```bash
# ✅ 迭代验证：使用 screenshot-slide.py（单张全尺寸截图）
python scripts/screenshot-slide.py slides/p3-demo.pptx slides/p3-slide0.jpg --slide 0 --dpi 200

# ⚠️ thumbnail.py 输出 300px 宽缩略图，不适合细节验证
# python scripts/thumbnail.py slides/p3-demo.pptx slides/p3-thumbnail --cols 4
```

### 步骤 6: 问题反馈与迭代

如果截图发现问题（如 SVG 丢失、表格消失、文本换行），使用 5.4 节的迭代提示词模板让 Gemini 重新生成，然后返回步骤 2 继续。

---

## 八、风格一致性：跨页面上下文传递

### 8.1 问题背景

批量生成多页幻灯片时，不同页面之间可能出现风格不一致的问题：
- 字号、间距不统一
- 颜色使用不一致
- 组件样式差异（如卡片、表格、边框）
- 布局结构不协调

### 8.2 解决方案：传递风格参考

**核心原则**：在生成新页面时，将已确认的页面 HTML 作为风格参考传递给 Gemini。

**推荐传递内容**：
1. **最近 1-2 个已完成页面的完整 HTML**（作为风格参考）
2. **设计规范文档**（`design-spec.md`）
3. **明确要求风格保持一致**

### 8.3 风格参考提示词模板

```
你是一个专业的 HTML 幻灯片设计师。请生成新页面，**必须保持与参考页面完全一致的设计风格**。

## 风格参考（严格遵循）

以下是已完成的页面，新页面必须保持相同的：
- Header 高度、背景色、字体样式
- Section 标题格式（蓝色左边框、字号、间距）
- 表格样式（表头背景、边框、内边距）
- 卡片样式（背景色、圆角、边框）
- 字体大小层级
- 颜色使用

### 参考页面 HTML：
```html
[粘贴已完成的页面 HTML]
```

## 新页面任务
[描述新页面的具体内容]

## 设计规范
[粘贴 DESIGN-SPEC.md 的关键部分]

## html2pptx 约束
[粘贴约束]

## 输出要求
1. 严格复用参考页面的 CSS 类和样式定义
2. 保持相同的 Header、Footer 结构
3. 使用相同的字号层级和颜色
4. 直接输出完整 HTML 代码
```

### 8.4 推荐工作流

```
┌─────────────────────────────────────────────────────────────────────┐
│                    多页面风格一致性工作流                             │
└─────────────────────────────────────────────────────────────────────┘

P1 生成 → P1 验证通过 → 保存 P1 HTML 作为参考
                              ↓
                      P2 生成（传递 P1 HTML 作为风格参考）
                              ↓
                      P2 验证通过 → 保存 P2 HTML
                              ↓
                      P3 生成（传递 P2 HTML 作为风格参考）
                              ↓
                             ...
```

**注意事项**：
- 只传递最近 1-2 个页面即可，不需要传递所有历史页面
- 如果新页面布局与参考页面差异较大，可以选择布局相似的页面作为参考
- 封面页通常独立，内容页之间互相参考

### 8.5 CSS 复用技巧

为了更好地保持一致性，可以在提示词中明确要求：

```
## CSS 复用要求
1. 复制参考页面的完整 <style> 部分
2. 只添加新页面需要的额外样式
3. 不要修改已有的类定义
4. 使用相同的类名（如 .section-title-wrapper, .card, .highlight-card 等）
```

---

## 九、版本

- **v1.1** - 新增 PowerPoint 截图工具、风格一致性指南
- **v1.0** - 初始版本，基于 frontend-gemini-cli skill 规范适配 PPTX 工作流
