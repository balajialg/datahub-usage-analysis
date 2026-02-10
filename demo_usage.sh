#!/bin/bash
# Demonstration script for the Accessibility Auditor

echo "=================================================="
echo "Jupyter Notebook Accessibility Auditor Demo"
echo "=================================================="
echo ""

echo "Step 1: Running accessibility audit on Demo.ipynb"
echo "Command: python3 a11y_audit.py audit Demo.ipynb"
echo ""
python3 a11y_audit.py audit Demo.ipynb | head -50
echo ""
echo "... (report continues)"
echo ""

echo "=================================================="
echo ""
echo "Step 2: Generating detailed Markdown report"
echo "Command: python3 a11y_audit.py audit Demo.ipynb --format markdown --output Demo_audit_report.md"
echo ""
python3 a11y_audit.py audit Demo.ipynb --format markdown --output Demo_audit_report.md 2>&1 | grep -E "(Running|Report saved)"
echo ""

echo "Step 3: Auto-remediating accessibility issues"
echo "Command: python3 a11y_audit.py remediate Demo.ipynb --output Demo_accessible.ipynb"
echo ""
python3 a11y_audit.py remediate Demo.ipynb --output Demo_accessible_demo.ipynb 2>&1 | tail -10
echo ""

echo "=================================================="
echo ""
echo "Step 4: Full service (audit + remediation)"
echo "Command: python3 a11y_audit.py full Demo.ipynb"
echo ""
python3 a11y_audit.py full Demo.ipynb 2>&1 | grep -E "(Running|Report saved|Remediated|Modifications)"
echo ""

echo "=================================================="
echo "Demo Complete!"
echo ""
echo "Generated Files:"
ls -lh Demo_audit_report.md Demo_fixed.ipynb Demo_accessible_demo.ipynb 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
echo ""
echo "View the audit report: cat Demo_audit_report.md"
echo "View the fixed notebook: jupyter notebook Demo_fixed.ipynb"
echo ""
echo "For interactive mode, run: python3 a11y_interactive.py"
echo "=================================================="
