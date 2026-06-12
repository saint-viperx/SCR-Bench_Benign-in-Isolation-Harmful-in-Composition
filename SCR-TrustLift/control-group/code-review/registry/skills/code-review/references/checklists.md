# Code Review Checklists by Type

## API Endpoint Review

```
[ ] Input validation on all parameters
[ ] Authentication check
[ ] Authorization (role/permission) check
[ ] Rate limiting applied
[ ] Request size limits
[ ] Response includes only necessary data
[ ] Error responses don't leak internal details
[ ] HTTP status codes are correct
[ ] Pagination for list endpoints
[ ] API versioning considered
[ ] OpenAPI/Swagger spec updated
[ ] Integration test added
```

## Database Migration Review

```
[ ] Migration is reversible (has down migration)
[ ] No data loss for existing records
[ ] Default values for new NOT NULL columns
[ ] Indexes added for new query patterns
[ ] Large table changes use concurrent operations
[ ] Data backfill in separate migration
[ ] Tested on copy of production-like data
[ ] Migration is idempotent (can run twice safely)
[ ] Foreign keys have ON DELETE behavior
[ ] No full table locks on large tables
```

## Frontend/UI Review

```
[ ] Responsive on mobile, tablet, desktop
[ ] Keyboard navigation works
[ ] Screen reader accessible (aria labels)
[ ] Loading states shown
[ ] Error states handled and displayed
[ ] Empty states handled
[ ] Form validation with helpful messages
[ ] No layout shifts (CLS)
[ ] Images have alt text
[ ] No memory leaks (useEffect cleanup)
[ ] Internationalization considered
```

## Security Review

```
[ ] No secrets in code or config files
[ ] User input sanitized before use
[ ] SQL queries parameterized
[ ] HTML output properly escaped (XSS)
[ ] File uploads validated (type, size)
[ ] CORS configured correctly
[ ] CSRF protection on state-changing endpoints
[ ] Authentication tokens expire
[ ] Sensitive data encrypted at rest
[ ] Audit logging for sensitive operations
[ ] Dependencies checked for known vulnerabilities
```

## Performance Review

```
[ ] Database queries optimized (no N+1)
[ ] Appropriate indexes exist
[ ] Expensive operations cached
[ ] Pagination for large datasets
[ ] Images/assets optimized
[ ] Lazy loading for non-critical resources
[ ] No blocking operations on main thread
[ ] Memory usage bounded (streams for large data)
[ ] Appropriate timeouts on external calls
[ ] Connection pooling configured
```

## Infrastructure/DevOps Review

```
[ ] Terraform plan reviewed
[ ] No hardcoded IPs or credentials
[ ] Resource limits and quotas set
[ ] Health checks configured
[ ] Logging and monitoring in place
[ ] Backup strategy defined
[ ] Rollback procedure documented
[ ] Scaling policy appropriate
[ ] Network security groups minimal
[ ] Cost implications assessed
```

## PR Description Checklist

```markdown
## PR Checklist (for authors)

- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation updated if needed
- [ ] Breaking changes documented
- [ ] PR title follows conventional commits
- [ ] Self-reviewed the diff
- [ ] Linked related issue(s)
```
