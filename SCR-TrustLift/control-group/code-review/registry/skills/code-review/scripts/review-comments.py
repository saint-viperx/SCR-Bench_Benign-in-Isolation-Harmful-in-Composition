#!/usr/bin/env python3
"""Code Review Comment Generator"""

import json

def generate_review_suggestions():
    """Generate common review comment templates"""
    suggestions = {
        "performance": {
            "n_plus_one": "Looks like an N+1 query issue. Consider using JOIN or loading relationships upfront.",
            "algorithm": "The algorithm here is O(n²). We could optimize this to O(n log n) using...",
        },
        "security": {
            "sql_injection": "This string concatenation is vulnerable to SQL injection. Use parameterized queries instead.",
            "hardcoded_secret": "Hardcoded credentials detected. Use environment variables or secrets manager.",
            "auth_missing": "Missing authentication check on this endpoint. Users should be verified before...",
        },
        "style": {
            "naming": "Variable name is unclear. Consider renaming to be more descriptive.",
            "function_length": "This function is 200 lines. Consider breaking it into smaller functions.",
            "complexity": "This function is too complex (cyclomatic complexity > 10). Simplify by extracting methods.",
        },
        "testing": {
            "no_test": "This logic change should have unit test coverage.",
            "coverage_drop": "Test coverage dropped from 88% to 82%. Please add more tests.",
            "flaky_test": "This test appears flaky (intermittent failures). Investigate timing issues.",
        }
    }
    return suggestions

def generate_positive_feedback():
    """Generate positive review comments"""
    feedback = [
        "Great refactoring! Much clearer than before.",
        "Excellent test coverage. Love the edge case handling.",
        "Smart optimization. Performance improvement is significant.",
        "Clean implementation. Easy to understand and maintain.",
        "Good documentation. Makes implementation clear."
    ]
    return feedback

if __name__ == "__main__":
    print(json.dumps(generate_review_suggestions(), indent=2))
    print("\nPositive feedback options:")
    for feedback in generate_positive_feedback():
        print(f"- {feedback}")
