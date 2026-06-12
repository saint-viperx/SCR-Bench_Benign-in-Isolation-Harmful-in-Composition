# Skill Structure Specification

This document defines the standard structure, naming conventions, and validation rules for Claude Code skills.

## Directory Structure

```
skills/
└── skill-name/
    ├── SKILL.md                      # Main skill file (REQUIRED)
    ├── references/                   # Supporting documentation (OPTIONAL)
    │   ├── api-reference.md
    │   └── best-practices.md
    ├── examples/                     # Usage examples (OPTIONAL)
    │   ├── basic-usage.md
    │   └── advanced-patterns.md
    └── assets/                       # Templates, checklists (OPTIONAL)
        ├── template.md
        └── checklist.md
```

## SKILL.md Structure

### YAML Frontmatter (REQUIRED)

```yaml
---
name: skill-name
description: Brief one-line description (max 1024 chars)
author: Author Name <email@example.com> (OPTIONAL)
version: 1.0.0 (OPTIONAL)
tags: [tag1, tag2, tag3] (OPTIONAL)
context: main (OPTIONAL, default: main)
---
```

**Field Definitions:**

- **name** (REQUIRED): Kebab-case identifier matching directory name
- **description** (REQUIRED): Concise description shown in skill list
- **author** (OPTIONAL): Skill author information
- **version** (OPTIONAL): Semantic version number
- **tags** (OPTIONAL): Array of tags for categorization
- **context** (OPTIONAL): Execution context (main|fork, default: main)

**Context Values:**
- `main`: Skill executes in main conversation (default)
- `fork`: Skill executes in isolated context (experimental, avoid if possible)

### Content Structure (REQUIRED)

Skills should follow this standard structure:

```markdown
# Skill Name

Brief overview paragraph explaining the skill's purpose.

## When to Use This Skill

Clear, specific criteria for when this skill should be invoked.

- Condition 1
- Condition 2
- Condition 3

## When NOT to Use This Skill

Clear criteria for when NOT to use this skill (avoid scope creep).

- Exclusion 1
- Exclusion 2

## Workflow

Step-by-step process the skill follows:

### Step 1: [Action Name]

Description of this step.

**Tools:** [List of Claude tools used]

**Output:** What this step produces

### Step 2: [Action Name]

...

## Quality Gates (OPTIONAL)

Validation checkpoints at key phases:

- [ ] Checkpoint 1
- [ ] Checkpoint 2

## Examples (OPTIONAL)

### Example 1: [Scenario Name]

```
Input: [User request]
Output: [Expected result]
```

## Notes (OPTIONAL)

- Important consideration 1
- Important consideration 2
```

## Naming Conventions

### File Naming

- **Skills directory**: `skills/skill-name/` (kebab-case)
- **SKILL.md**: Always uppercase `SKILL.md`
- **Supporting files**: `kebab-case.md`
- **No spaces in filenames**: Use hyphens

### Skill Names

- **Format**: `kebab-case` (lowercase, hyphens for separators)
- **Examples**:
  - ✅ `skill-editor`
  - ✅ `test-driven-development`
  - ✅ `code-review`
  - ❌ `SkillEditor` (no PascalCase)
  - ❌ `skill_editor` (no underscores)
  - ❌ `skill editor` (no spaces)

### Namespace Conventions

For related skills, use prefixes:

- `skill-editor-*` for skill-editor sub-skills
- `superpowers:*` for superpowers plugin skills
- `scientific-skills:*` for scientific-skills plugin skills

## Validation Rules

### YAML Frontmatter Validation

```python
import yaml

def validate_frontmatter(skill_file):
    with open(skill_file, 'r') as f:
        content = f.read()

    # Extract frontmatter
    if not content.startswith('---'):
        raise ValueError("Missing YAML frontmatter")

    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError("Invalid YAML frontmatter format")

    # Parse YAML
    frontmatter = yaml.safe_load(parts[1])

    # Required fields
    if 'name' not in frontmatter:
        raise ValueError("Missing required field: name")
    if 'description' not in frontmatter:
        raise ValueError("Missing required field: description")

    # Validate name format
    name = frontmatter['name']
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        raise ValueError(f"Invalid name format: {name}")

    # Validate description length
    if len(frontmatter['description']) > 1024:
        raise ValueError("Description exceeds 1024 characters")

    return True
```

### Directory Structure Validation

- SKILL.md must exist in `skills/skill-name/SKILL.md`
- Directory name must match `name` field in YAML frontmatter
- No files at root of `skills/` directory (only subdirectories)

### Content Validation

- SKILL.md must have at least:
  - YAML frontmatter
  - Heading 1 (`# Skill Name`)
  - "When to Use This Skill" section
  - "Workflow" section
- No broken internal links (references to files that don't exist)

## Integration with sync-config.py

Skills are synced from `claude-config/skills/` → `~/.claude/skills/`:

```bash
# Validate before syncing
./validate-skills.sh

# Sync to system
./sync-config.py push

# Verify
claude /skill-name
```

## Best Practices

1. **Keep skills focused**: One clear purpose per skill
2. **Use quality gates**: Add checkpoints for complex workflows
3. **Provide examples**: Show realistic use cases
4. **Document exclusions**: Clarify when NOT to use the skill
5. **Reference supporting docs**: Link to external resources in references/
6. **Test thoroughly**: Invoke skill in Claude session before committing
7. **Follow conventions**: Use standard sections and naming patterns

## Common Patterns

### Multi-Phase Workflow Skills

```markdown
## Workflow

### Phase 1: Analysis
- Analyze codebase
- Identify patterns

### Phase 2: Implementation
- Make changes
- Run tests

### Phase 3: Verification
- Validate results
- Document changes
```

### Skills with Subtasks

```markdown
## Subtasks

This skill delegates to specialized sub-skills:

- `skill-editor-request-refiner`: Refine user request
- `skill-editor-executor`: Execute changes
```

### Skills with External Tools

```markdown
## Required Tools

This skill requires:
- sync-config.py (for configuration management)
- git (for version control)
- Python 3.8+ (for validation scripts)
```

## Anti-Patterns

❌ **Avoid:**

- Skills with vague "When to Use" criteria
- Skills that duplicate existing functionality
- Skills without clear workflow steps
- Skills with hardcoded file paths
- Skills that mix multiple unrelated concerns
- Massive monolithic skills (break into sub-skills)
- Skills without examples

✅ **Instead:**

- Specific, measurable criteria
- Check existing skills first, extend if needed
- Clear step-by-step workflows
- Use relative paths or configuration
- One purpose per skill
- Compose smaller, focused skills
- Provide realistic examples

## Orchestrator Skill Requirements

Orchestrator skills coordinate other skills or agents to accomplish complex, multi-phase work. They have additional requirements beyond standard skills.

### Detection Criteria

A skill qualifies as an orchestrator when it scores 4+ on the detection algorithm (see `orchestrator-best-practices.md` for the complete scoring system). Key signals include: delegates to other skills via Task tool, has named phases/stages, manages session state, and has quality gates between phases.

### REQUIRED Sections (for new orchestrator skills)

These sections MUST be present. Evaluated by Phase 2 best-practices-reviewer.

1. **Delegation Mandate**: Explicit "you ARE / you are NOT" section defining orchestrator vs. specialist boundaries
2. **State Anchoring**: Response prefix format, state file read before each phase, re-anchor after interaction
3. **Tool Selection Table**: Explicit table mapping situations to tools (Task vs. Read) with self-check
4. **Error Handling (Structured)**: Named patterns (retry, circuit breaker, saga, graceful degradation)
5. **Timeout Configuration**: Per-phase timeout table with exceeded-action for each
6. **Session Management**: Session directory, state file, interrupt handling

### RECOMMENDED Sections (for orchestrator skills)

These sections SHOULD be present when applicable. Evaluated by Phase 2 knowledge-engineer. Missing RECOMMENDED sections are noted but do not fail quality gates.

7. **Handoff Schema**: Structured YAML handoff between phases with validation
8. **Pre-Flight Validation**: Check skill dependencies before workflow starts
9. **Mode Selection / Complexity Detection**: Three-tier detection with user override
10. **Handoff Frontmatter**: YAML frontmatter declaring handoff capabilities

### OPTIONAL Sections

11. **Quality Gate Override Protocol**: Severity-based override with logging (single-implementation pattern)

### Forward-Looking Note

These requirements apply to NEW orchestrator skills created via skill-editor and serve as RECOMMENDED guidance for existing orchestrators. They are not retroactive mandates.

### References

- Pattern templates and detection checklists: `orchestrator-best-practices.md`
- Evaluation framework: `orchestrator-checklist.md`

## Version Control

Skills should be version controlled with:

1. **Semantic versioning** in YAML frontmatter
2. **Git commits** following conventional commit format:
   ```
   feat(skill-name): Add new feature
   fix(skill-name): Fix bug in workflow
   docs(skill-name): Update documentation
   ```

3. **Planning journal entries** for significant changes:
   ```bash
   ./sync-config.py plan --title "Add skill-editor workflow"
   ```

## Migration Guide

When refactoring existing skills:

1. Read existing SKILL.md
2. Identify sections that match specification
3. Add missing required sections
4. Validate YAML frontmatter
5. Test skill invocation
6. Create planning entry
7. Commit changes

## References

- [Anthropic Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [YAML Specification](https://yaml.org/spec/)
- [Semantic Versioning](https://semver.org/)
