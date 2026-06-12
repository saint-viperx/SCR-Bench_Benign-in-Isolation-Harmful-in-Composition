#!/bin/bash
# Pull Request Template Enforcer - Validate PR descriptions against template
# Usage: ./pr-template-enforcer.sh <pr-description-file>

set -e

PR_FILE="${1:-.github/PULL_REQUEST_TEMPLATE.md}"
DESCRIPTION_FILE="${2:-/dev/stdin}"

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
NC='\033[0m'

print_error() {
    echo -e "${COLOR_RED}✗ $1${NC}"
}

print_success() {
    echo -e "${COLOR_GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${COLOR_YELLOW}⚠ $1${NC}"
}

check_required_sections() {
    local description=$(cat "$DESCRIPTION_FILE")
    local has_issues=0
    
    # Check for description
    if ! echo "$description" | grep -qi "## Description\|## Summary"; then
        print_error "Missing 'Description' or 'Summary' section"
        has_issues=1
    else
        print_success "Description section found"
    fi
    
    # Check for type of change
    if ! echo "$description" | grep -qi "## Type of Change\|## Changes"; then
        print_warning "Missing 'Type of Change' section"
    else
        print_success "Type of Change section found"
    fi
    
    # Check for testing
    if ! echo "$description" | grep -qi "## Testing\|## How to Test"; then
        print_warning "Missing 'Testing' section"
    else
        print_success "Testing section found"
    fi
    
    return $has_issues
}

check_issue_reference() {
    local description=$(cat "$DESCRIPTION_FILE")
    
    if ! echo "$description" | grep -qiE "fixes #|closes #|resolves #"; then
        print_warning "No issue reference found (use 'Fixes #123')"
        return 1
    else
        print_success "Issue reference found"
        return 0
    fi
}

check_checklist() {
    local description=$(cat "$DESCRIPTION_FILE")
    
    if ! echo "$description" | grep -q "\- \[x\]\|\- \[ \]"; then
        print_warning "No checklist items found"
        return 1
    else
        # Count completed items
        local completed=$(echo "$description" | grep -c "\- \[x\]" || true)
        print_success "Checklist found with $completed completed items"
        return 0
    fi
}

main() {
    echo "Validating PR description..."
    echo ""
    
    check_required_sections
    echo ""
    
    check_issue_reference
    echo ""
    
    check_checklist
    echo ""
    
    print_success "PR validation complete!"
}

main
