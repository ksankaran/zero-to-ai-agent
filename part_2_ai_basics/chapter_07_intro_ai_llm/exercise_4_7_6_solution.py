# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: exercise_4_7_6_solution.py

"""
Exercise 4 Solution: API Key Audit Tool
Comprehensive tool to scan projects for exposed API keys and generate security reports.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime
import hashlib


class ComprehensiveAPIAuditor:
    """
    Advanced API key audit tool that:
    - Scans projects for exposed API keys
    - Checks Git history for accidentally committed keys
    - Validates that all keys in use are properly secured
    - Generates detailed security reports
    """
    
    # Enhanced patterns for different API key types
    KEY_PATTERNS = {
        "OpenAI": {
            "pattern": r'sk-[a-zA-Z0-9]{48}',
            "description": "OpenAI API Key",
            "severity": "CRITICAL"
        },
        "Anthropic": {
            "pattern": r'sk-ant-api[0-9]{2}-[a-zA-Z0-9-]+',
            "description": "Anthropic API Key",
            "severity": "CRITICAL"
        },
        "Google/Gemini": {
            "pattern": r'AIza[a-zA-Z0-9_-]{35}',
            "description": "Google AI API Key",
            "severity": "CRITICAL"
        },
        "Replicate": {
            "pattern": r'r8_[a-zA-Z0-9]{37}',
            "description": "Replicate API Token",
            "severity": "HIGH"
        },
        "GitHub": {
            "pattern": r'ghp_[a-zA-Z0-9]{36}',
            "description": "GitHub Personal Access Token",
            "severity": "HIGH"
        },
        "AWS": {
            "pattern": r'AKIA[A-Z0-9]{16}',
            "description": "AWS Access Key",
            "severity": "CRITICAL"
        },
        "Generic API Key": {
            "pattern": r'(api[_-]?key|apikey|api_token|access[_-]?token)[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
            "description": "Generic API Key Pattern",
            "severity": "MEDIUM"
        },
        "Generic Secret": {
            "pattern": r'(secret|password|passwd|pwd)[\s]*[:=][\s]*["\']([^"\']{8,})["\']',
            "description": "Generic Secret Pattern",
            "severity": "MEDIUM"
        }
    }
    
    # Files and directories to skip
    SKIP_PATTERNS = {
        # Directories
        ".git", ".env", "venv", "env", "__pycache__", "node_modules",
        ".pytest_cache", "dist", "build", ".vscode", ".idea",
        # Files
        "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.dylib",
        "*.exe", "*.bin", "*.jpg", "*.png", "*.gif", "*.pdf"
    }
    
    # Files that should be in .gitignore
    SENSITIVE_FILES = [
        ".env", ".env.local", ".env.production", ".env.development",
        "config.json", "secrets.json", "credentials.json",
        "*.key", "*.pem", "*.p12", "*.pfx"
    ]
    
    def __init__(self, project_dir: str = "."):
        """Initialize the auditor"""
        self.project_dir = Path(project_dir).resolve()
        self.findings = []
        self.warnings = []
        self.recommendations = []
        self.scan_summary = {}
    
    def audit_complete(self) -> Dict:
        """
        Run a complete security audit
        
        Returns:
            Comprehensive audit report
        """
        print("🔍 Starting Comprehensive Security Audit...")
        print(f"📁 Project: {self.project_dir}")
        print("-" * 60)
        
        # Reset findings
        self.findings = []
        self.warnings = []
        self.recommendations = []
        
        # Run all audit checks
        self._scan_source_files()
        self._check_gitignore()
        self._scan_git_history()
        self._check_environment_files()
        self._validate_active_keys()
        self._check_dependencies()
        
        # Generate report
        report = self._generate_report()
        
        return report
    
    def _scan_source_files(self):
        """Scan all source files for exposed keys"""
        print("\n📝 Scanning source files...")
        
        files_scanned = 0
        files_with_issues = 0
        
        for file_path in self._get_files_to_scan():
            violations = self._scan_file(file_path)
            
            if violations:
                files_with_issues += 1
                self.findings.extend(violations)
            
            files_scanned += 1
        
        self.scan_summary["files_scanned"] = files_scanned
        self.scan_summary["files_with_issues"] = files_with_issues
        
        print(f"  Scanned {files_scanned} files")
        if files_with_issues > 0:
            print(f"  ⚠️ Found issues in {files_with_issues} files")
    
    def _get_files_to_scan(self) -> List[Path]:
        """Get list of files to scan"""
        files_to_scan = []
        
        for file_path in self.project_dir.rglob("*"):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip based on patterns
            should_skip = False
            for pattern in self.SKIP_PATTERNS:
                if pattern.startswith("*"):
                    if file_path.suffix == pattern[1:]:
                        should_skip = True
                        break
                elif pattern in file_path.parts:
                    should_skip = True
                    break
            
            if not should_skip:
                files_to_scan.append(file_path)
        
        return files_to_scan
    
    def _scan_file(self, file_path: Path) -> List[Dict]:
        """Scan a single file for exposed keys"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                for line_num, line in enumerate(content.splitlines(), 1):
                    # Skip obvious comments
                    stripped = line.strip()
                    if stripped.startswith(('#', '//', '/*', '*', '"""', "'''")):
                        continue
                    
                    # Check each pattern
                    for key_type, info in self.KEY_PATTERNS.items():
                        pattern = info["pattern"]
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        
                        for match in matches:
                            # Validate if it's likely a real key
                            if self._is_likely_real_key(match.group()):
                                violations.append({
                                    "type": "exposed_key",
                                    "file": str(file_path.relative_to(self.project_dir)),
                                    "line": line_num,
                                    "key_type": key_type,
                                    "description": info["description"],
                                    "severity": info["severity"],
                                    "preview": self._mask_line(line)
                                })
        
        except Exception as e:
            self.warnings.append(f"Could not scan {file_path}: {e}")
        
        return violations
    
    def _is_likely_real_key(self, text: str) -> bool:
        """Check if a match is likely a real API key"""
        # Common placeholders to ignore
        placeholders = [
            "your-key", "your_key", "add_your", "example",
            "xxx", "...", "placeholder", "test", "demo",
            "sample", "dummy", "fake", "mock"
        ]
        
        text_lower = text.lower()
        
        for placeholder in placeholders:
            if placeholder in text_lower:
                return False
        
        # Check for repeated characters
        if len(text) > 10:
            unique_chars = len(set(text))
            if unique_chars < len(text) / 4:  # Too repetitive
                return False
        
        return True
    
    def _mask_line(self, line: str) -> str:
        """Mask sensitive data in a line"""
        # Replace potential keys with masked versions
        for key_type, info in self.KEY_PATTERNS.items():
            pattern = info["pattern"]
            line = re.sub(
                pattern,
                lambda m: m.group()[:10] + "***MASKED***" if len(m.group()) > 10 else "***",
                line,
                flags=re.IGNORECASE
            )
        
        # Truncate long lines
        if len(line) > 80:
            line = line[:77] + "..."
        
        return line
    
    def _check_gitignore(self):
        """Check if .gitignore properly excludes sensitive files"""
        print("\n🚫 Checking .gitignore...")
        
        gitignore_path = self.project_dir / ".gitignore"
        
        if not gitignore_path.exists():
            self.findings.append({
                "type": "missing_gitignore",
                "severity": "HIGH",
                "description": "No .gitignore file found"
            })
            self.recommendations.append(
                "Create a .gitignore file to exclude sensitive files"
            )
            return
        
        with open(gitignore_path) as f:
            gitignore_content = f.read()
        
        # Check for important exclusions
        missing = []
        for sensitive_file in self.SENSITIVE_FILES:
            if sensitive_file not in gitignore_content:
                missing.append(sensitive_file)
        
        if missing:
            self.warnings.append(
                f".gitignore missing important exclusions: {', '.join(missing)}"
            )
            self.recommendations.append(
                f"Add these to .gitignore: {', '.join(missing)}"
            )
    
    def _scan_git_history(self):
        """Scan git history for accidentally committed keys"""
        print("\n🕒 Scanning git history...")
        
        if not (self.project_dir / ".git").exists():
            print("  No git repository found")
            return
        
        try:
            # Check recent commits for key patterns
            for key_type, info in self.KEY_PATTERNS.items():
                pattern = info["pattern"][:20]  # Use partial pattern for speed
                
                result = subprocess.run(
                    ["git", "log", "-S", pattern, "--oneline", "-n", "10"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_dir,
                    timeout=5
                )
                
                if result.stdout:
                    self.findings.append({
                        "type": "git_history",
                        "severity": "HIGH",
                        "description": f"Possible {key_type} in git history",
                        "commits": result.stdout.strip().split('\n')[:3]
                    })
            
            print("  Git history scanned")
            
        except subprocess.TimeoutExpired:
            self.warnings.append("Git history scan timed out")
        except Exception as e:
            self.warnings.append(f"Could not scan git history: {e}")
    
    def _check_environment_files(self):
        """Check security of environment files"""
        print("\n🔒 Checking environment files...")
        
        env_files = [".env", ".env.local", ".env.production", "config.json"]
        
        for env_file in env_files:
            file_path = self.project_dir / env_file
            
            if file_path.exists():
                # Check if it's in git
                try:
                    result = subprocess.run(
                        ["git", "ls-files", env_file],
                        capture_output=True,
                        text=True,
                        cwd=self.project_dir
                    )
                    
                    if result.stdout.strip():
                        self.findings.append({
                            "type": "tracked_env_file",
                            "severity": "CRITICAL",
                            "description": f"{env_file} is tracked in git!",
                            "file": env_file
                        })
                
                except:
                    pass
                
                # Check file permissions (Unix-like systems)
                try:
                    stats = file_path.stat()
                    mode = oct(stats.st_mode)[-3:]
                    
                    if mode not in ["600", "644"]:
                        self.warnings.append(
                            f"{env_file} has loose permissions: {mode}"
                        )
                
                except:
                    pass
    
    def _validate_active_keys(self):
        """Validate that active keys are properly secured"""
        print("\n✓ Validating active keys...")
        
        # Check environment variables
        env_vars_to_check = [
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", 
            "GOOGLE_API_KEY", "AWS_ACCESS_KEY_ID"
        ]
        
        for var in env_vars_to_check:
            value = os.environ.get(var)
            if value:
                # Check if it looks like a placeholder
                if any(p in value.lower() for p in ["your", "add", "placeholder"]):
                    self.warnings.append(
                        f"{var} appears to be a placeholder"
                    )
    
    def _check_dependencies(self):
        """Check for security issues in dependencies"""
        print("\n📦 Checking dependencies...")
        
        # Check for requirements.txt
        req_file = self.project_dir / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                deps = f.read()
                
                # Check for insecure practices
                if "git+" in deps and "@" in deps:
                    self.warnings.append(
                        "requirements.txt contains git dependencies with possible tokens"
                    )
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive security report"""
        # Calculate severity counts
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for finding in self.findings:
            severity = finding.get("severity", "MEDIUM")
            severity_counts[severity] += 1
        
        # Determine overall status
        if severity_counts["CRITICAL"] > 0:
            status = "❌ CRITICAL ISSUES FOUND"
        elif severity_counts["HIGH"] > 0:
            status = "⚠️ HIGH RISK ISSUES FOUND"
        elif len(self.findings) > 0:
            status = "⚠️ ISSUES FOUND"
        elif len(self.warnings) > 0:
            status = "⚠️ WARNINGS"
        else:
            status = "✅ SECURE"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_dir),
            "status": status,
            "summary": {
                "total_findings": len(self.findings),
                "total_warnings": len(self.warnings),
                "severity_breakdown": severity_counts,
                **self.scan_summary
            },
            "findings": self.findings,
            "warnings": self.warnings,
            "recommendations": self.recommendations
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print formatted report to console"""
        print("\n" + "=" * 70)
        print("🔒 SECURITY AUDIT REPORT")
        print("=" * 70)
        
        print(f"\nStatus: {report['status']}")
        print(f"Project: {report['project']}")
        print(f"Time: {report['timestamp']}")
        
        # Summary
        print("\n📊 Summary:")
        print(f"  Files Scanned: {report['summary'].get('files_scanned', 0)}")
        print(f"  Total Findings: {report['summary']['total_findings']}")
        print(f"  Total Warnings: {report['summary']['total_warnings']}")
        
        # Severity breakdown
        print("\n🎯 Severity Breakdown:")
        for severity, count in report['summary']['severity_breakdown'].items():
            if count > 0:
                print(f"  {severity}: {count}")
        
        # Critical findings
        critical = [f for f in report['findings'] if f.get('severity') == 'CRITICAL']
        if critical:
            print("\n🚨 CRITICAL FINDINGS:")
            for finding in critical[:3]:
                print(f"\n  • {finding.get('description', 'Unknown issue')}")
                if 'file' in finding:
                    print(f"    File: {finding['file']}")
                if 'line' in finding:
                    print(f"    Line: {finding['line']}")
                if 'preview' in finding:
                    print(f"    Preview: {finding['preview']}")
        
        # Recommendations
        if report['recommendations']:
            print("\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "=" * 70)
    
    def save_report(self, report: Dict, format: str = "json"):
        """Save report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            filename = f"security_audit_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(report, f, indent=2)
        
        elif format == "markdown":
            filename = f"security_audit_{timestamp}.md"
            with open(filename, "w") as f:
                f.write(self._generate_markdown_report(report))
        
        print(f"📄 Report saved to: {filename}")
        return filename
    
    def _generate_markdown_report(self, report: Dict) -> str:
        """Generate markdown formatted report"""
        md = f"""# Security Audit Report

**Date:** {report['timestamp']}  
**Project:** {report['project']}  
**Status:** {report['status']}

## Summary

- Files Scanned: {report['summary'].get('files_scanned', 0)}
- Total Findings: {report['summary']['total_findings']}
- Total Warnings: {report['summary']['total_warnings']}

## Severity Breakdown

"""
        
        for severity, count in report['summary']['severity_breakdown'].items():
            if count > 0:
                md += f"- **{severity}:** {count}\n"
        
        if report['findings']:
            md += "\n## Findings\n\n"
            for finding in report['findings']:
                md += f"### {finding.get('description', 'Issue')}\n"
                md += f"- **Severity:** {finding.get('severity', 'Unknown')}\n"
                if 'file' in finding:
                    md += f"- **File:** `{finding['file']}`\n"
                if 'line' in finding:
                    md += f"- **Line:** {finding['line']}\n"
                md += "\n"
        
        if report['recommendations']:
            md += "\n## Recommendations\n\n"
            for rec in report['recommendations']:
                md += f"- {rec}\n"
        
        return md


# Main execution
if __name__ == "__main__":
    print("🔐 Comprehensive API Key Security Audit Tool")
    print("=" * 70)
    
    # Create auditor
    auditor = ComprehensiveAPIAuditor(".")
    
    # Run complete audit
    report = auditor.audit_complete()
    
    # Print report
    auditor.print_report(report)
    
    # Save reports
    auditor.save_report(report, "json")
    auditor.save_report(report, "markdown")
    
    # Exit with appropriate code
    if report['status'].startswith("❌"):
        exit(1)  # Critical issues
    elif report['status'].startswith("⚠️"):
        exit(0)  # Warnings but not critical
    else:
        exit(0)  # All good
