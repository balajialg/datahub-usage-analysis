# datahub-usage-analysis
Code for Berkeley's DataHub JupyterHub installation anaylsis.

Data is stored in a shared GDrive folder.

## 🌐 Accessibility Features

This repository includes a comprehensive **Jupyter Notebook Accessibility Auditor** that ensures notebooks meet WCAG 2.1/2.2 standards.

### Quick Start

```bash
# Interactive mode (recommended)
python3 a11y_interactive.py

# Command-line mode
python3 a11y_audit.py audit Demo.ipynb
```

**Documentation:**
- [Getting Started Guide](GETTING_STARTED.md) - Quick start and examples
- [Full Documentation](A11Y_AUDIT_README.md) - Comprehensive reference

**Features:**
- ✅ Automated accessibility audits (WCAG 2.1/2.2 Level AA)
- ✅ Auto-fix common issues (alt text, headings, links)
- ✅ Detailed reports (Text, Markdown, JSON formats)
- ✅ Interactive and command-line interfaces
