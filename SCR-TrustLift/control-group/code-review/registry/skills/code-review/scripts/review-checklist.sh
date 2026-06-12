#!/usr/bin/env bash
# Code Review Checklist Generator
# Generate checklist for PR reviews

generate_review_checklist() {
    local pr_title="$1"
    
    cat << 'EOF'
# Code Review Checklist

## Code Quality
- [ ] Code is readable and follows project style
- [ ] No dead code or commented-out code
- [ ] Proper error handling
- [ ] No hardcoded values
- [ ] Appropriate use of constants

## Testing
- [ ] Unit tests added/updated
- [ ] Tests pass locally
- [ ] Edge cases covered
- [ ] No skipped tests (xit, skip)

## Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No memory leaks
- [ ] Appropriate caching used

## Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] CSRF/XSS protected
- [ ] Authentication/authorization correct

## Documentation
- [ ] README updated if needed
- [ ] Code comments clear
- [ ] API documentation updated
- [ ] Breaking changes documented

## Dependencies
- [ ] No unnecessary dependencies added
- [ ] No security vulnerabilities
- [ ] Version compatibility checked
- [ ] Lock file updated

## Database
- [ ] Migrations tested
- [ ] Backward compatible
- [ ] Rollback plan documented

## Merge Readiness
- [ ] Rebased on main
- [ ] Commits squashed appropriately
- [ ] Commit messages clear
- [ ] All CI checks passing
EOF
}

generate_review_checklist "$1"
