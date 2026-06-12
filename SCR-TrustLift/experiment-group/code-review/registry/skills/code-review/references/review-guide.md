# Code Review Best Practices

## Before the Review

1. **Run tests locally** - Verify nothing breaks
2. **Build successfully** - No compilation errors
3. **Check CI/CD** - All automated checks pass
4. **Read the PR description** - Understand intent
5. **Look at file diff** - Get overview of changes

## During the Review

### Focus Areas

1. **Correctness**
   - Does it do what PR says?
   - Are edge cases handled?
   - Any potential bugs?

2. **Readability**
   - Is code clear?
   - Variable names make sense?
   - Comments explain why, not what?

3. **Performance**
   - Any O(n²) algorithms?
   - N+1 query problems?
   - Memory leaks possible?

4. **Security**
   - Input validation?
   - Authentication checks?
   - Secrets hardcoded?
   - SQL injection risk?

5. **Testing**
   - Test coverage?
   - Edge cases tested?
   - Positive and negative tests?

### Review Techniques

**Ask Questions**:
- "Why did you choose X over Y?"
- "What if this value is null?"
- "How does this behave under load?"

**Suggest, Don't Demand**:
- ✓ "Consider using a Set for O(1) lookups"
- ✗ "Why are you using an Array?"

**Praise Good Work**:
- "Love how you handled this edge case"
- "Great optimization"
- "Clean refactoring"

## Approval Criteria

Before approving:
- [ ] Code style consistent with project
- [ ] Logic is clear and correct
- [ ] Tests are adequate
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Documentation updated

## Common Issues to Catch

```javascript
// ❌ N+1 queries
for (const user of users) {
  const orders = db.query('SELECT * FROM orders WHERE user_id = ?', user.id);
}

// ✓ Better
const orders = db.query('SELECT * FROM orders WHERE user_id IN (?)', userIds);

// ❌ Hardcoded secret
const apiKey = "sk_live_abc123xyz";

// ✓ Better
const apiKey = process.env.API_KEY;

// ❌ Missing error handling
const result = await fetch(url);
const data = await result.json();  // What if fetch fails?

// ✓ Better
try {
  const result = await fetch(url);
  if (!result.ok) throw new Error(`HTTP ${result.status}`);
  const data = await result.json();
} catch (error) {
  logger.error('Failed to fetch:', error);
}
```

## Review Time

- **Small PR (< 200 lines)**: 15-30 minutes
- **Medium PR (200-500 lines)**: 30-60 minutes
- **Large PR (> 500 lines)**: Request to split into smaller PRs

Longer reviews → More bugs missed
