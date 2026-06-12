# Code Review Examples

## Example PR Description Template
```markdown
## Description
Implemented authentication system with JWT tokens and refresh token rotation.

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change

## Related Issues
Fixes #123 - User authentication needed

## How to Test
1. Run `npm install`
2. Start the server: `npm start`
3. POST to `/api/auth/login` with valid credentials
4. Verify JWT token is returned
5. Test token refresh with `/api/auth/refresh`

## Checklist
- [x] Unit tests added
- [x] Integration tests added
- [x] Documentation updated
- [x] No breaking changes
- [x] Security review completed
- [x] Performance impact assessed

## Reviewer Checklist
- [ ] Code follows project standards
- [ ] Tests are adequate
- [ ] No security issues
- [ ] Performance is acceptable
- [ ] Documentation is clear
```

## Example Code Review Comments

### Comment 1: Security Issue
```
🔒 Security Concern

The token is being stored in localStorage without HttpOnly flag. This makes it vulnerable to XSS attacks.

**Recommendation:**
- Use httpOnly cookies for token storage
- Or implement CSRF protection if using localStorage
- Reference: [OWASP Token Storage](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#localStorage)

**Suggested Change:**
```javascript
response.cookie('token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});
```

### Comment 2: Performance Issue
```
⚡ Performance Consideration

This N+1 query issue will cause performance problems with large datasets.

**Current Code:**
```javascript
for (const userId of userIds) {
  const user = await User.findById(userId);
}
```

**Better Approach:**
```javascript
const users = await User.find().where('_id').in(userIds);
```

This reduces database calls from N+1 to just 1.

### Comment 3: Code Quality
```
📚 Maintainability

This function mixes validation, transformation, and persistence logic. Consider separating concerns.

**Suggestion:**
Break into three functions:
1. `validateUserInput(data)` - validation
2. `transformUserData(data)` - transformation  
3. `saveUser(data)` - persistence

This makes testing easier and code more maintainable.
```

### Comment 4: Documentation
```
📖 Documentation Needed

Please add a docstring explaining:
- What the function does
- Parameters and their types
- Return value
- Any exceptions that could be raised

```python
def process_payment(user_id: int, amount: float) -> bool:
    """
    Process a payment for the given user.
    
    Args:
        user_id: The ID of the user making the payment
        amount: The payment amount in USD
        
    Returns:
        True if payment successful, False otherwise
        
    Raises:
        ValueError: If amount is negative or user doesn't exist
        PaymentError: If payment gateway returns error
    """
```

### Comment 5: Approval with Minor Changes
```
👍 Looks Great!

This implementation is solid. Just requested minor changes above:
1. Add type hints
2. Update docstring
3. Consider the performance suggestion for large datasets

After addressing these, I'll approve.
```
