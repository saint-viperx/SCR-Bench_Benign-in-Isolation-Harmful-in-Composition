# Code Review Best Practices

## Purpose of Code Reviews
- Catch bugs and security issues early
- Share knowledge across team
- Maintain code quality standards
- Improve code readability and maintainability
- Foster collaboration and learning

## What to Review

### Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Are there potential bugs or race conditions?
- Are error cases handled properly?

### Performance
- Will this code scale?
- Are there unnecessary loops or operations?
- Are algorithms optimal?
- Are resources (memory, CPU) used efficiently?

### Security
- Are inputs validated?
- Is sensitive data protected?
- Are SQL injection risks mitigated?
- Are authentication/authorization correct?
- Are dependencies up-to-date?

### Maintainability
- Is the code readable and understandable?
- Are variable and function names descriptive?
- Is documentation adequate?
- Is the code DRY (Don't Repeat Yourself)?
- Are design patterns applied appropriately?

### Testing
- Is test coverage adequate?
- Do tests cover edge cases?
- Are tests maintainable and clear?
- Is mocking used appropriately?

## Code Review Checklist

### Before Submitting
- [ ] Code follows project style guide
- [ ] No hardcoded values or credentials
- [ ] Tests are written and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No debug code or console.log statements
- [ ] Performance impact assessed

### During Review
- [ ] Code is readable and well-structured
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Security best practices followed
- [ ] No breaking changes without discussion
- [ ] Performance is acceptable
- [ ] Tests adequately cover functionality

## Communication Guidelines

### Constructive Feedback
✓ "This could be more efficient using a Set instead of an array"
✗ "Your code is inefficient"

✓ "Consider extracting this into a separate function for readability"
✗ "This is too long"

✓ "Have you considered this edge case?"
✗ "You didn't handle this case"

### Approve When
- [ ] All feedback been addressed
- [ ] Code quality meets standards
- [ ] Tests are adequate
- [ ] Documentation is complete
- [ ] No outstanding concerns

### Request Changes When
- [ ] Security issues found
- [ ] Major bugs identified
- [ ] Architecture concerns
- [ ] Test coverage inadequate
- [ ] Documentation missing

## Review Example

### Code Submission
```python
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price'] * item['quantity']
    return total
```

### Review Comment
```
Great implementation! A few suggestions:

1. Prefer += operator: `total += item['price'] * item['quantity']`
2. Consider using sum() with a generator expression for more Pythonic code:
   ```python
   return sum(item['price'] * item['quantity'] for item in items)
   ```
3. Add docstring and type hints:
   ```python
   from typing import List, Dict
   
   def calculate_total(items: List[Dict]) -> float:
       """Calculate total price from items list."""
       return sum(item['price'] * item['quantity'] for item in items)
   ```
4. Add error handling for missing keys

This is a good optimization!
```

## Common Issues Found in Code Reviews

### Style & Formatting
- Inconsistent indentation
- Line too long (>100 chars)
- Missing whitespace for readability
- Unused imports
- Unused variables

### Functionality
- Off-by-one errors
- Missing null/error checks
- Incomplete error handling
- Logic errors

### Security
- SQL injection risks
- XSS vulnerabilities
- Hardcoded secrets
- Insecure deserialization

### Performance
- N+1 queries
- Inefficient algorithms
- Memory leaks
- Unnecessary deep copies

### Maintainability
- Magic numbers
- Unclear variable names
- Missing documentation
- Code duplication
- Complex nested logic

## Review Time Guidelines
- Small changes (< 100 lines): 10-15 minutes
- Medium changes (100-500 lines): 20-30 minutes
- Large changes (> 500 lines): 60+ minutes

**Pro tip**: Keep PR sizes small (<400 lines) for faster, more thorough reviews

## Tools for Code Review
- GitHub/GitLab/Bitbucket Reviews
- Gerrit for detailed review
- Reviewboard for documentation
- Crucible for distributed teams
- CodeStream IDE integration
