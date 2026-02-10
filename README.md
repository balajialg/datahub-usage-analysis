# datahub-usage-analysis
Code for Berkeley's DataHub JupyterHub installation analysis.

Data is stored in a shared GDrive folder.

## Jupyter Notebook Accessibility (a11y) Audit Tool

This repository now includes a comprehensive accessibility audit tool for Jupyter Notebooks that ensures compliance with WCAG 2.1/2.2 standards.

### Quick Start

```bash
# Audit a notebook
python a11y_audit.py notebooks/your-notebook.ipynb

# Generate HTML report
python a11y_audit.py notebooks/your-notebook.ipynb --format html --output report.html

# Auto-fix accessibility issues
python a11y_audit.py notebooks/your-notebook.ipynb --remediate
```

### Features

- **Comprehensive WCAG 2.1/2.2 Compliance Checks**: Images, headings, tables, color usage, and more
- **Detailed Reports**: Available in text, JSON, and HTML formats with Critical/Warning/Success categories
- **Automatic Remediation**: Fixes common issues like missing alt text, improper heading structure, and table headers
- **Professional & Educational**: Technical terminology with clear explanations for non-experts

### Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 3 steps
- **[A11Y_AUDIT_README.md](A11Y_AUDIT_README.md)** - Complete documentation
- **[notebooks/a11y-audit-example.ipynb](notebooks/a11y-audit-example.ipynb)** - Interactive tutorial
- **[example-audit-report.html](example-audit-report.html)** - Sample HTML report
