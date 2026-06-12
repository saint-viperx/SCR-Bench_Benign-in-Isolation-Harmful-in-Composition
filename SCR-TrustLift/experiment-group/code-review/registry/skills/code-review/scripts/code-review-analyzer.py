#!/usr/bin/env python3
"""
Code Review Analyzer - Automated code review suggestions using static analysis
Usage: python3 code-review-analyzer.py <file> [--output FORMAT]
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import List, Dict, Tuple

class CodeReviewAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = ""
        self.issues = []
        self.suggestions = []
        self.load_file()
    
    def load_file(self):
        """Load and read file content"""
        try:
            with open(self.filepath, 'r') as f:
                self.content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
    
    def check_line_length(self, max_length: int = 100):
        """Check for lines exceeding max length"""
        lines = self.content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                self.issues.append({
                    'severity': 'info',
                    'line': i,
                    'issue': f'Line length {len(line)} exceeds {max_length} characters',
                    'suggestion': 'Break long lines into multiple lines for readability'
                })
    
    def check_indentation(self):
        """Check for inconsistent indentation"""
        lines = self.content.split('\n')
        indent_types = set()
        
        for i, line in enumerate(lines, 1):
            if line and line[0] in (' ', '\t'):
                if line.startswith('\t'):
                    indent_types.add('tabs')
                elif line.startswith('    '):
                    indent_types.add('spaces-4')
                elif line.startswith('  '):
                    indent_types.add('spaces-2')
        
        if len(indent_types) > 1:
            self.issues.append({
                'severity': 'warning',
                'line': 0,
                'issue': f'Inconsistent indentation detected: {indent_types}',
                'suggestion': 'Use consistent indentation throughout the file (recommend 4 spaces)'
            })
    
    def check_comments(self):
        """Check comment quality"""
        lines = self.content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for TODO comments
            if 'TODO' in line or 'FIXME' in line or 'HACK' in line:
                self.suggestions.append({
                    'severity': 'info',
                    'line': i,
                    'issue': f'Found TODO/FIXME comment: {line.strip()}',
                    'suggestion': 'Consider creating an issue for this instead of leaving comments'
                })
            
            # Check for commented code
            if line.strip().startswith('#') and any(
                keyword in line for keyword in ['=', '(', ')', 'return', 'if', 'for']
            ):
                if not any(word in line for word in ['http://', 'https://', 'email']):
                    self.suggestions.append({
                        'severity': 'info',
                        'line': i,
                        'issue': 'Commented code detected',
                        'suggestion': 'Remove commented code; use git history to retrieve old code'
                    })
    
    def check_python_specific(self):
        """Python-specific code review checks"""
        if not self.filepath.endswith('.py'):
            return
        
        lines = self.content.split('\n')
        
        # Check for print statements (should use logging)
        for i, line in enumerate(lines, 1):
            if re.match(r'^\s*print\(', line):
                self.suggestions.append({
                    'severity': 'warning',
                    'line': i,
                    'issue': 'Found print() statement',
                    'suggestion': 'Use logging module instead of print() for production code'
                })
            
            # Check for bare except
            if re.match(r'^\s*except\s*:', line):
                self.issues.append({
                    'severity': 'error',
                    'line': i,
                    'issue': 'Bare except clause found',
                    'suggestion': 'Specify exception type (e.g., except Exception or except ValueError)'
                })
            
            # Check for use of global
            if re.match(r'^\s*global\s+', line):
                self.suggestions.append({
                    'severity': 'warning',
                    'line': i,
                    'issue': 'Use of global keyword',
                    'suggestion': 'Avoid global variables; use classes or pass as parameters instead'
                })
        
        # Parse AST for more complex checks
        try:
            tree = ast.parse(self.content)
            self._check_complexity(tree)
            self._check_naming(tree)
        except SyntaxError:
            self.issues.append({
                'severity': 'error',
                'line': 0,
                'issue': 'Syntax error in file',
                'suggestion': 'Fix syntax errors before review'
            })
    
    def _check_complexity(self, tree):
        """Check function complexity"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines_of_code = node.end_lineno - node.lineno
                if lines_of_code > 50:
                    self.suggestions.append({
                        'severity': 'warning',
                        'line': node.lineno,
                        'issue': f'Function "{node.name}" is {lines_of_code} lines long',
                        'suggestion': 'Consider breaking this function into smaller functions (max ~30 lines)'
                    })
    
    def _check_naming(self, tree):
        """Check for proper naming conventions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_') and not node.name.startswith('__'):
                    continue  # Private methods are ok
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    self.suggestions.append({
                        'severity': 'info',
                        'line': node.lineno,
                        'issue': f'Function "{node.name}" doesn\'t follow snake_case naming',
                        'suggestion': 'Use snake_case for function names (e.g., my_function)'
                    })
    
    def check_security(self):
        """Check for common security issues"""
        lines = self.content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for hardcoded credentials
            if any(keyword in line for keyword in ['password', 'secret', 'token', 'key']):
                if any(char in line for char in ['=', ':', ':']):
                    if not re.search(r'\b(def|class|import|environ)\b', line):
                        self.issues.append({
                            'severity': 'error',
                            'line': i,
                            'issue': 'Possible hardcoded credential detected',
                            'suggestion': 'Use environment variables or secure vaults (AWS Secrets, HashiCorp Vault)'
                        })
            
            # Check for SQL injection risks
            if 'SELECT' in line.upper() or 'INSERT' in line.upper():
                if '+' in line or 'format(' in line or f'{' in line:
                    self.issues.append({
                        'severity': 'error',
                        'line': i,
                        'issue': 'Potential SQL injection vulnerability',
                        'suggestion': 'Use parameterized queries or ORM (SQLAlchemy, Django ORM)'
                    })
    
    def generate_report(self) -> Dict:
        """Generate comprehensive code review report"""
        self.check_line_length()
        self.check_indentation()
        self.check_comments()
        self.check_python_specific()
        self.check_security()
        
        return {
            'file': self.filepath,
            'total_issues': len(self.issues),
            'total_suggestions': len(self.suggestions),
            'errors': [issue for issue in self.issues if issue['severity'] == 'error'],
            'warnings': [issue for issue in self.issues + self.suggestions if issue['severity'] == 'warning'],
            'info': [issue for issue in self.issues + self.suggestions if issue['severity'] == 'info'],
            'all_issues': sorted(self.issues + self.suggestions, key=lambda x: x['line'])
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Code Review Analyzer')
    parser.add_argument('file', help='File to analyze')
    parser.add_argument('--output', choices=['json', 'text'], default='text')
    
    args = parser.parse_args()
    
    analyzer = CodeReviewAnalyzer(args.file)
    report = analyzer.generate_report()
    
    if args.output == 'json':
        print(json.dumps(report, indent=2))
    else:
        print(f"\n📋 Code Review Report: {report['file']}")
        print(f"{'='*60}")
        print(f"Errors: {len(report['errors'])}")
        print(f"Warnings: {len(report['warnings'])}")
        print(f"Info: {len(report['info'])}")
        print(f"{'='*60}\n")
        
        for issue in report['all_issues']:
            print(f"[{issue['severity'].upper()}] Line {issue['line']}: {issue['issue']}")
            print(f"  → {issue['suggestion']}\n")

if __name__ == '__main__':
    main()
