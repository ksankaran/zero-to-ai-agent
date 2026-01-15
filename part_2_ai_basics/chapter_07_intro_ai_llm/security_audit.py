# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: security_audit.py

"""
Security audit tool to scan projects for exposed API keys and security issues.
Essential for preventing expensive mistakes and security breaches.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json
import subprocess
from datetime import datetime


class APIKeyAuditor:
    """
    Comprehensive security auditor for API keys in your project
    """
    
    # Patterns that might indicate API keys
    KEY_PATTERNS = {
        "OpenAI": r'sk-[a-zA-Z0-9]{48}',
        "Anthropic": r'sk-ant-[a-zA-Z0-9-]+',
        "Google": r'AIza[a-zA-Z0-9_-]{35}',
        "Replicate": r'[a-f0-9]{40}',  # Less specific, more false positives
        "Generic Secret": r'(api[_-]?key|secret|token|password)[\s]*=[\s]*["\'][^"\']{20,}["\']'
    }
    
    # Files/folders to skip
    SKIP_PATHS = {
        ".git", ".env", "venv", "env", "__pycache__", 
        "node_modules", ".pytest_cache", "dist", "build"
    }
    
    # File extensions to check
    CHECK_EXTENSIONS = {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", 
        ".yml", ".md", ".txt", ".sh", ".bash", ".config"
    }
    
    def __init__(self, project_dir: str = "."):
        """Initialize the auditor with a project directory"""
        self.project_dir = Path(project_dir)
        self.violations = []
        self.warnings = []
        self.safe_files = []
    
    def audit_file(self, filepath: Path) -> List[Dict]:
        """Audit a single file for exposed keys"""
        violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check each line
                for line_num, line in enumerate(content.splitlines(), 1):
                    # Skip comments and docstrings for false positives
                    if line.strip().startswith(('#', '//', '"""', "'''")):
                        continue
                    
                    # Check for each pattern
                    for key_type, pattern in self.KEY_PATTERNS.items():
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            # Check if it's likely a real key
                            if self._is_likely_real_key(match.group(), key_type):
                                violations.append({
                                    "file": str(filepath.relative_to(self.project_dir)),
                                    "line": line_num,
                                    "type": key_type,
                                    "preview": self._mask_sensitive_data(line.strip()),
                                    "severity": "HIGH"
                                })
        
        except Exception as e:
            self.warnings.append(f"Could not scan {filepath}: {e}")
        
        return violations
    
    def _is_likely_real_key(self, text: str, key_type: str) -> bool:
        """Check if a match is likely a real API key"""
        # Common false positive indicators
        false_positive_indicators = [
            "example", "your-key", "add_your", "placeholder",
            "xxx", "...", "abc", "123", "test", "demo"
        ]
        
        text_lower = text.lower()
        
        # Check for obvious placeholders
        for indicator in false_positive_indicators:
            if indicator in text_lower:
                return False
        
        # Check for repeated characters (likely fake)
        if len(set(text)) < len(text) / 3:  # Too many repeated chars
            return False
        
        return True
    
    def _mask_sensitive_data(self, text: str) -> str:
        """Mask potential sensitive data in preview"""
        # Replace potential keys with masked versions
        for key_type, pattern in self.KEY_PATTERNS.items():
            text = re.sub(pattern, lambda m: m.group()[:10] + "***MASKED***", text)
        return text[:100] + "..." if len(text) > 100 else text
    
    def audit_project(self) -> Dict:
        """Audit the entire project for security issues"""
        print(f"🔍 Auditing project: {self.project_dir.absolute()}")
        
        files_scanned = 0
        
        # Walk through project files
        for file_path in self._get_files_to_scan():
            violations = self.audit_file(file_path)
            
            if violations:
                self.violations.extend(violations)
            else:
                self.safe_files.append(str(file_path.relative_to(self.project_dir)))
            
            files_scanned += 1
        
        # Check additional security issues
        self._check_gitignore()
        self._check_git_history()
        self._check_environment_files()
        
        # Compile results
        results = {
            "scan_time": datetime.now().isoformat(),
            "project_dir": str(self.project_dir.absolute()),
            "files_scanned": files_scanned,
            "violations": self.violations,
            "warnings": self.warnings,
            "safe_files_count": len(self.safe_files),
            "summary": self._generate_summary()
        }
        
        return results
    
    def _get_files_to_scan(self) -> List[Path]:
        """Get list of files to scan, respecting skip patterns"""
        files_to_scan = []
        
        for file_path in self.project_dir.rglob("*"):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip excluded paths
            if any(skip in file_path.parts for skip in self.SKIP_PATHS):
                continue
            
            # Only check relevant extensions
            if file_path.suffix not in self.CHECK_EXTENSIONS:
                continue
            
            files_to_scan.append(file_path)
        
        return files_to_scan
    
    def _check_gitignore(self):
        """Check if .gitignore properly excludes sensitive files"""
        gitignore_path = self.project_dir / ".gitignore"
        
        if not gitignore_path.exists():
            self.warnings.append("⚠️ No .gitignore file found!")
            return
        
        with open(gitignore_path) as f:
            gitignore_content = f.read()
        
        # Check for important exclusions
        important_exclusions = [".env", "config.json", "secrets", "*.key"]
        missing_exclusions = []
        
        for exclusion in important_exclusions:
            if exclusion not in gitignore_content:
                missing_exclusions.append(exclusion)
        
        if missing_exclusions:
            self.warnings.append(
                f"⚠️ .gitignore missing important exclusions: {', '.join(missing_exclusions)}"
            )
    
    def _check_git_history(self):
        """Check git history for accidentally committed keys"""
        try:
            # Only run if in a git repository
            if not (self.project_dir / ".git").exists():
                return
            
            # Search git history for key patterns (last 50 commits)
            result = subprocess.run(
                ["git", "log", "-50", "--grep", "sk-", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            
            if result.stdout:
                self.warnings.append(
                    "⚠️ Git history might contain API keys. Review commit history!"
                )
        except Exception:
            # Git might not be available
            pass
    
    def _check_environment_files(self):
        """Check for improperly secured environment files"""
        env_files = [".env", ".env.local", "config.json", "secrets.json"]
        
        for env_file in env_files:
            file_path = self.project_dir / env_file
            if file_path.exists():
                # Check permissions (Unix-like systems)
                try:
                    stats = file_path.stat()
                    mode = oct(stats.st_mode)[-3:]
                    if mode != "600":  # Should be readable only by owner
                        self.warnings.append(
                            f"⚠️ {env_file} has loose permissions: {mode}"
                        )
                except:
                    pass
    
    def _generate_summary(self) -> Dict:
        """Generate a summary of the audit results"""
        severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for violation in self.violations:
            severity = violation.get("severity", "MEDIUM")
            severity_counts[severity] += 1
        
        return {
            "total_violations": len(self.violations),
            "total_warnings": len(self.warnings),
            "severity_breakdown": severity_counts,
            "status": self._get_status()
        }
    
    def _get_status(self) -> str:
        """Determine overall security status"""
        if len(self.violations) == 0 and len(self.warnings) == 0:
            return "✅ SECURE"
        elif len(self.violations) == 0:
            return "⚠️ WARNINGS"
        else:
            return "❌ VULNERABLE"
    
    def generate_report(self, results: Dict, output_format: str = "console"):
        """Generate a security report in various formats"""
        
        if output_format == "console":
            self._print_console_report(results)
        elif output_format == "json":
            return json.dumps(results, indent=2)
        elif output_format == "markdown":
            return self._generate_markdown_report(results)
    
    def _print_console_report(self, results: Dict):
        """Print a formatted console report"""
        print("\n" + "=" * 60)
        print("🔒 SECURITY AUDIT REPORT")
        print("=" * 60)
        
        # Status
        print(f"\nStatus: {results['summary']['status']}")
        print(f"Files Scanned: {results['files_scanned']}")
        
        # Violations
        if results['violations']:
            print(f"\n❌ VIOLATIONS FOUND: {len(results['violations'])}")
            print("-" * 40)
            
            for violation in results['violations'][:5]:  # Show first 5
                print(f"\n📁 {violation['file']} (line {violation['line']})")
                print(f"   Type: {violation['type']}")
                print(f"   Preview: {violation['preview']}")
            
            if len(results['violations']) > 5:
                print(f"\n... and {len(results['violations']) - 5} more violations")
        
        # Warnings
        if results['warnings']:
            print(f"\n⚠️ WARNINGS: {len(results['warnings'])}")
            print("-" * 40)
            for warning in results['warnings']:
                print(f"  • {warning}")
        
        # Recommendations
        print("\n" + "=" * 60)
        print("📋 RECOMMENDATIONS")
        print("=" * 60)
        
        if results['violations']:
            print("1. ⚠️ IMMEDIATELY remove exposed keys from code")
            print("2. 🔄 Rotate any exposed API keys")
            print("3. 📝 Move keys to environment variables or .env file")
            print("4. 🚫 Add .env to .gitignore")
            print("5. 🧹 Clean git history if keys were committed")
        else:
            print("✅ No critical issues found!")
            print("Continue following security best practices:")
            print("  • Never hardcode API keys")
            print("  • Use environment variables")
            print("  • Keep .gitignore updated")
            print("  • Rotate keys periodically")
    
    def _generate_markdown_report(self, results: Dict) -> str:
        """Generate a markdown-formatted report"""
        md = f"""# Security Audit Report

**Date:** {results['scan_time']}
**Project:** {results['project_dir']}
**Status:** {results['summary']['status']}

## Summary
- Files Scanned: {results['files_scanned']}
- Violations: {results['summary']['total_violations']}
- Warnings: {results['summary']['total_warnings']}

## Violations
"""
        
        if results['violations']:
            for v in results['violations']:
                md += f"\n### {v['file']} (line {v['line']})\n"
                md += f"- **Type:** {v['type']}\n"
                md += f"- **Severity:** {v['severity']}\n"
                md += f"- **Preview:** `{v['preview']}`\n"
        else:
            md += "\nNo violations found ✅\n"
        
        return md


def quick_security_check():
    """Run a quick security check on the current directory"""
    auditor = APIKeyAuditor()
    results = auditor.audit_project()
    auditor.generate_report(results)
    
    return results['summary']['status'] == "✅ SECURE"


if __name__ == "__main__":
    print("Starting Security Audit...")
    print("-" * 60)
    
    # Run audit on current directory
    auditor = APIKeyAuditor(".")
    results = auditor.audit_project()
    
    # Generate report
    auditor.generate_report(results, "console")
    
    # Save detailed report
    with open("security_audit_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n📄 Detailed report saved to: security_audit_report.json")
