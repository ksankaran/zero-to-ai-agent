# Save as: exercise_1_19_7_solution.py
"""
Exercise 1 Solution: Security Audit Script

A comprehensive security audit tool that scans your codebase
for common security issues in AI agent deployments.

Run: python exercise_1_19_7_solution.py /path/to/project
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List
from enum import Enum
from datetime import datetime


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Finding:
    severity: Severity
    category: str
    description: str
    file: str
    line: int | None
    recommendation: str


class SecurityAuditor:
    """Audit codebase for security issues."""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings: List[Finding] = []
    
    def audit(self) -> List[Finding]:
        """Run all audit checks."""
        self.findings = []
        
        print(f"🔍 Auditing: {self.project_path}")
        print("=" * 50)
        
        self._check_hardcoded_secrets()
        self._check_gitignore()
        self._check_input_validation()
        self._check_error_handling()
        self._check_logging()
        self._check_dependencies()
        self._check_dockerfile()
        
        return self.findings
    
    def _check_hardcoded_secrets(self):
        """Look for hardcoded API keys and secrets."""
        print("Checking for hardcoded secrets...")
        
        secret_patterns = [
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API key"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
        ]
        
        for py_file in self.project_path.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                content = py_file.read_text()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Skip comments
                    if line.strip().startswith('#'):
                        continue
                    
                    for pattern, description in secret_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.findings.append(Finding(
                                severity=Severity.CRITICAL,
                                category="Hardcoded Secrets",
                                description=f"Possible {description} found",
                                file=str(py_file),
                                line=i,
                                recommendation="Move to environment variable"
                            ))
            except Exception:
                pass  # Skip files that can't be read
    
    def _check_gitignore(self):
        """Check if .gitignore properly excludes sensitive files."""
        print("Checking .gitignore...")
        
        gitignore_path = self.project_path / ".gitignore"
        
        if not gitignore_path.exists():
            self.findings.append(Finding(
                severity=Severity.HIGH,
                category="Git Security",
                description="No .gitignore file found",
                file=".gitignore",
                line=None,
                recommendation="Create .gitignore with .env and other sensitive files"
            ))
            return
        
        content = gitignore_path.read_text()
        required_patterns = [".env", "*.pem", "*.key", "__pycache__"]
        
        for pattern in required_patterns:
            if pattern not in content:
                self.findings.append(Finding(
                    severity=Severity.MEDIUM,
                    category="Git Security",
                    description=f"'{pattern}' not in .gitignore",
                    file=".gitignore",
                    line=None,
                    recommendation=f"Add '{pattern}' to .gitignore"
                ))
    
    def _check_input_validation(self):
        """Check for input validation in API endpoints."""
        print("Checking input validation...")
        
        for py_file in self.project_path.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                content = py_file.read_text()
                
                # Check for FastAPI endpoints without Pydantic models
                if "@app.post" in content or "@app.get" in content:
                    if "BaseModel" not in content:
                        self.findings.append(Finding(
                            severity=Severity.MEDIUM,
                            category="Input Validation",
                            description="API endpoints may lack Pydantic validation",
                            file=str(py_file),
                            line=None,
                            recommendation="Use Pydantic models for request validation"
                        ))
            except Exception:
                pass
    
    def _check_error_handling(self):
        """Check for information leakage in error handling."""
        print("Checking error handling...")
        
        for py_file in self.project_path.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                content = py_file.read_text()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for stack trace exposure
                    if "traceback.format_exc()" in line and "return" in content[content.find(line):content.find(line)+200]:
                        self.findings.append(Finding(
                            severity=Severity.HIGH,
                            category="Information Leakage",
                            description="Stack trace may be exposed to users",
                            file=str(py_file),
                            line=i,
                            recommendation="Log stack traces, return generic error messages"
                        ))
                    
                    # Check for detailed error returns
                    if re.search(r'detail\s*=\s*str\(e\)', line):
                        self.findings.append(Finding(
                            severity=Severity.MEDIUM,
                            category="Information Leakage",
                            description="Exception details may be exposed",
                            file=str(py_file),
                            line=i,
                            recommendation="Return generic error messages to users"
                        ))
            except Exception:
                pass
    
    def _check_logging(self):
        """Check for sensitive data in logging."""
        print("Checking logging practices...")
        
        for py_file in self.project_path.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                content = py_file.read_text()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for logging API keys
                    if re.search(r'log.*api.?key', line, re.IGNORECASE):
                        self.findings.append(Finding(
                            severity=Severity.HIGH,
                            category="Logging Security",
                            description="API key may be logged",
                            file=str(py_file),
                            line=i,
                            recommendation="Never log API keys or secrets"
                        ))
            except Exception:
                pass
    
    def _check_dependencies(self):
        """Check for dependency security."""
        print("Checking dependencies...")
        
        requirements = self.project_path / "requirements.txt"
        
        if not requirements.exists():
            self.findings.append(Finding(
                severity=Severity.LOW,
                category="Dependencies",
                description="No requirements.txt found",
                file="requirements.txt",
                line=None,
                recommendation="Create requirements.txt with pinned versions"
            ))
            return
        
        content = requirements.read_text()
        
        # Check for unpinned versions
        for line in content.split('\n'):
            if line and not line.startswith('#'):
                if '==' not in line and '>=' not in line:
                    self.findings.append(Finding(
                        severity=Severity.LOW,
                        category="Dependencies",
                        description=f"Unpinned dependency: {line}",
                        file="requirements.txt",
                        line=None,
                        recommendation="Pin all dependency versions"
                    ))
    
    def _check_dockerfile(self):
        """Check Dockerfile for security issues."""
        print("Checking Dockerfile...")
        
        dockerfile = self.project_path / "Dockerfile"
        
        if not dockerfile.exists():
            return
        
        content = dockerfile.read_text()
        
        # Check for root user
        if "USER" not in content:
            self.findings.append(Finding(
                severity=Severity.MEDIUM,
                category="Container Security",
                description="Container runs as root user",
                file="Dockerfile",
                line=None,
                recommendation="Add a non-root USER instruction"
            ))
        
        # Check for latest tag
        if "FROM" in content and ":latest" in content:
            self.findings.append(Finding(
                severity=Severity.LOW,
                category="Container Security",
                description="Using :latest tag",
                file="Dockerfile",
                line=None,
                recommendation="Pin to specific image version"
            ))
    
    def generate_report(self) -> str:
        """Generate a markdown security report."""
        report = ["# Security Audit Report\n"]
        report.append(f"**Project:** {self.project_path}\n")
        report.append(f"**Date:** {datetime.now().isoformat()}\n")
        report.append(f"**Total Findings:** {len(self.findings)}\n")
        
        # Summary by severity
        report.append("\n## Summary\n")
        for severity in Severity:
            count = sum(1 for f in self.findings if f.severity == severity)
            if count > 0:
                report.append(f"- **{severity.value}:** {count}\n")
        
        # Findings by category
        report.append("\n## Findings\n")
        
        categories = set(f.category for f in self.findings)
        for category in sorted(categories):
            report.append(f"\n### {category}\n")
            
            for finding in self.findings:
                if finding.category == category:
                    icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "⚪"}
                    report.append(f"\n{icon[finding.severity.value]} **{finding.severity.value}**: {finding.description}\n")
                    report.append(f"- **File:** {finding.file}")
                    if finding.line:
                        report.append(f" (line {finding.line})")
                    report.append(f"\n- **Recommendation:** {finding.recommendation}\n")
        
        # Remediation plan
        report.append("\n## Remediation Plan\n")
        report.append("| Priority | Finding | Action | Status |\n")
        report.append("|----------|---------|--------|--------|\n")
        
        for i, finding in enumerate(sorted(self.findings, key=lambda f: list(Severity).index(f.severity)), 1):
            desc = finding.description[:40] + "..." if len(finding.description) > 40 else finding.description
            rec = finding.recommendation[:40] + "..." if len(finding.recommendation) > 40 else finding.recommendation
            report.append(f"| {i} | {desc} | {rec} | ⬜ TODO |\n")
        
        return "".join(report)


# Run the audit
if __name__ == "__main__":
    import sys
    
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    auditor = SecurityAuditor(path)
    findings = auditor.audit()
    
    print("\n" + "=" * 50)
    
    report = auditor.generate_report()
    print(report)
    
    # Save report
    with open("security_audit_report.md", "w") as f:
        f.write(report)
    
    print(f"\n✅ Report saved to security_audit_report.md")
    print(f"📊 Found {len(findings)} potential issues")
    
    # Exit with error if critical issues found
    critical_count = sum(1 for f in findings if f.severity == Severity.CRITICAL)
    if critical_count > 0:
        print(f"\n⚠️  {critical_count} CRITICAL issues require immediate attention!")
        sys.exit(1)
