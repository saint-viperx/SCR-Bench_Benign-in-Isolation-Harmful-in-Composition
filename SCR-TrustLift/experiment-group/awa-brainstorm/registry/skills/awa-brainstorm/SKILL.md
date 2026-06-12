---
name: awa-brainstorm
description: Brainstorm ideas, explore solutions, and evaluate options. Use this when asked to brainstorm, explore ideas, or analyze trade-offs.
---

# Brainstorm Ideas

## Bootstrap

<tool name="read_file">
 <read path=".awa/.agent/awa.core.md" required="true" error="on not found" />
 <read path=".awa/rules/*.md" required="true" />
 <read path=".awa/specs/ARCHITECTURE.md" required="if exists" />
</tool>

## User Input

```text
${input}
```

You **MUST** consider the user input before proceeding (if not empty).

## Inputs

<file type="architecture" path=".awa/specs/ARCHITECTURE.md" />
<file type="feat" path=".awa/specs/FEAT-{CODE}-{feature-name}.md" required="if relevant" />
<file type="examples" path=".awa/specs/EXAMPLE-{CODE}-{feature-name}-{nnn}.md" required="if relevant" />
<file type="requirements" path=".awa/specs/REQ-{CODE}-{feature-name}.md" required="if relevant" />
<file type="design" path=".awa/specs/DESIGN-{CODE}-{feature-name}.md" required="if relevant" />
<file type="api" path=".awa/specs/API-{CODE}-{feature-name}.md" required="if relevant" />
<file type="tasks" path=".awa/tasks/TASK-{CODE}-{feature-name}-{nnn}.md" required="if relevant" />
<file type="code" required="if relevant" />

## Action

Brainstorm ideas and explore solutions for the specified topic.

1. DIVERGE: Generate multiple distinct approaches without filtering
2. ANALYZE: Evaluate options against constraints and trade-offs
3. CONVERGE: Recommend top candidates with rationale

## Outputs

<cli>Brainstorm summary in conversation</cli>
<file path=".awa/plans/PLAN-{nnn}-{brainstorm-topic}.md" if="user requests formalization" />

## Rules

You SHALL explore multiple distinct approaches before converging.
You SHALL identify trade-offs honestly, not just pros.
You SHALL distinguish between facts and assumptions.
You SHOULD challenge assumptions and explore alternatives.
You SHALL NOT dismiss ideas prematurely during divergence.
You SHALL engage in dialogue; ask clarifying questions.
You MAY use web search for research and validation.
You MAY use todos and tools as needed.
