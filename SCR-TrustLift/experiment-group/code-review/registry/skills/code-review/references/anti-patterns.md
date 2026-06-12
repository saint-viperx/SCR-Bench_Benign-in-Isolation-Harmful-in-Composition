# Code Review Anti-patterns

## Mistakes Reviewers Make

### 1. Nitpicking Style
```
❌ Bad: "Variable name should be camelCase not snake_case"
✓ Better: Use automated linting for style issues
```

### 2. Not Understanding Context
```
❌ Bad: Requesting change without understanding why
✓ Better: Ask questions first before suggesting changes
```

### 3. Reviewing Too Fast
```
❌ Bad: Approve without really reading code
✓ Better: Spend adequate time understanding logic
```

### 4. Reviewing Too Slow
```
❌ Bad: Delay PRs for days with detailed nitpicks
✓ Better: Balance thoroughness with team velocity
```

### 5. Being Harsh
```
❌ Bad: "This code is terrible"
✓ Better: "Good attempt. Here's how we could improve..."
```

## Mistakes Authors Make

### 1. Large PRs
```
❌ 500+ line PR
✓ < 200 lines per PR
```

### 2. Vague Descriptions
```
❌ "Fixed stuff"
✓ "Fixed login race condition where simultaneous requests created duplicate accounts"
```

### 3. Defensive Responses
```
❌ "This is fine, you don't understand"
✓ "Good point. Let me refactor this."
```

### 4. Ignoring Feedback
```
❌ Approve anyway ignoring suggestions
✓ Address or discuss feedback
```

## Effective Review Workflow

```
Author: Create small, focused PR
        ↓
Reviewer: Read description
          Review code in depth
          Leave thoughtful feedback
        ↓
Author: Address feedback
        ↓
Reviewer: Approve and merge
          (or request changes if significant)
```

Cycle time: 4-24 hours for typical PR
