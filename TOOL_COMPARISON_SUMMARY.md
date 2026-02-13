# Tool Comparison Summary

## At a Glance

**Two excellent accessibility audit tools for Jupyter Notebooks:**

### 🏢 JupyterLab-a11y-checker (Berkeley)
*Professional, comprehensive, AI-powered*

**Key Strengths:**
- Real-time checking in JupyterLab
- AI-powered alt text generation (VLM/LLM)
- Axe-core integration (57+ rules)
- Research-backed detection
- Interactive remediation UI

**Best For:** Teams actively developing in JupyterLab who need comprehensive, professional tooling

### 🛠️ Custom a11y Audit Tool (This Repo)
*Lightweight, portable, customizable*

**Key Strengths:**
- Zero dependencies (Python stdlib only)
- No installation required
- Beautiful HTML reports
- Easy to customize
- Works offline/airgapped

**Best For:** Quick audits, batch processing, constrained environments, custom integration needs

---

## Quick Comparison

| What You Need | Recommended Tool |
|---------------|------------------|
| Real-time feedback while coding | **JupyterLab-a11y-checker** |
| No installation/dependencies | **Custom Tool** |
| AI-generated alt text | **JupyterLab-a11y-checker** |
| HTML reports for stakeholders | **Custom Tool** |
| Most comprehensive checks | **JupyterLab-a11y-checker** |
| Easy to customize/modify | **Custom Tool** |
| Works in JupyterLab IDE | **JupyterLab-a11y-checker** |
| Batch process many notebooks | **Both work well** |
| CI/CD integration | **Both work well** |
| Offline/airgapped environment | **Custom Tool** |

---

## Feature Matrix

### ✅ Both Tools Have
- Image alt text checking
- Heading hierarchy validation
- Table header detection
- WCAG compliance checking
- CLI interface
- JSON output
- Batch processing
- Cell-level issue location

### ⭐ JupyterLab-a11y-checker Only
- Real-time JupyterLab extension
- Axe-core integration
- AI/VLM/LLM integration
- Image contrast analysis
- Interactive fix UI
- Link text analysis
- Duplicate heading detection
- Table caption checking

### ⭐ Custom Tool Only
- Zero dependencies
- HTML report generation
- Severity categories (Critical/Warning/Success)
- Color-only information detection
- Code context checking
- Single-file portability

---

## Architecture

### JupyterLab-a11y-checker
```
TypeScript/JavaScript (Node.js)
├── Core package (shared logic)
├── CLI package (command-line)
└── Extension package (JupyterLab)
    └── Integrates axe-core
```

### Custom Tool
```
Pure Python (stdlib only)
└── Single file (~850 LOC)
    ├── Regex-based parsing
    └── Pattern matching
```

---

## Installation & Usage

### JupyterLab-a11y-checker

**Install:**
```bash
pip install jupyterlab-a11y-checker
# OR run directly
npx @jupyterlab-a11y-checker/cli notebook.ipynb
```

**Use:**
```bash
# CLI
npx @jupyterlab-a11y-checker/cli **/*.ipynb

# Extension (automatic in JupyterLab)
jupyter lab
```

### Custom Tool

**Install:**
```bash
# No installation needed!
```

**Use:**
```bash
# Audit
python a11y_audit.py notebook.ipynb

# HTML report
python a11y_audit.py notebook.ipynb --format html --output report.html

# Auto-fix
python a11y_audit.py notebook.ipynb --remediate
```

---

## Decision Guide

### Choose JupyterLab-a11y-checker if:
- ✅ You work primarily in JupyterLab
- ✅ You need real-time feedback while coding
- ✅ You want AI-powered alt text generation
- ✅ You need the most comprehensive checks
- ✅ You have Node.js infrastructure
- ✅ You want professionally maintained tools
- ✅ Your team values research-backed solutions

### Choose Custom Tool if:
- ✅ You need minimal dependencies
- ✅ You work in constrained environments
- ✅ You want quick, simple audits
- ✅ You need HTML reports for stakeholders
- ✅ You want easy customization
- ✅ You work offline/airgapped
- ✅ You prefer lightweight solutions
- ✅ You need to understand the code

### Use Both if:
- ✅ You develop in JupyterLab (use Extension)
- ✅ AND need HTML reports (use Custom Tool)
- ✅ AND run CI/CD (use either)

---

## Real-World Scenarios

### Scenario 1: Course Material Creation
**Use Case:** Professor creating notebooks for class

**Recommendation:** **JupyterLab-a11y-checker**
- Real-time feedback while creating content
- AI helps generate alt text quickly
- Comprehensive checking ensures quality

### Scenario 2: Legacy Content Audit
**Use Case:** Auditing 100+ existing notebooks

**Recommendation:** **Custom Tool**
- No installation overhead
- Batch process all at once
- Generate HTML reports for administration

### Scenario 3: GitHub Repository
**Use Case:** Open source project with notebooks

**Recommendation:** **JupyterLab-a11y-checker CLI**
- Easy GitHub Actions integration
- Professional tooling
- LLM-friendly JSON output

### Scenario 4: Corporate Environment
**Use Case:** Restricted network, no npm access

**Recommendation:** **Custom Tool**
- Works offline
- No external dependencies
- Can be vetted and approved easily

### Scenario 5: Data Science Team
**Use Case:** Team collaborating in JupyterLab

**Recommendation:** **JupyterLab-a11y-checker**
- Extension provides real-time guidance
- Consistent checking across team
- Interactive fixes speed up workflow

---

## Standards Coverage

### Both Tools Cover:
- WCAG 1.1.1 - Non-text Content
- WCAG 1.3.1 - Info and Relationships  
- WCAG 2.4.2 - Page Titled
- WCAG 2.4.6 - Headings and Labels

### JupyterLab-a11y-checker Also:
- WCAG 1.4.3 - Contrast (via image analysis)
- WCAG 2.4.4 - Link Purpose
- 57+ additional rules via axe-core

### Custom Tool Also:
- WCAG 1.4.1 - Use of Color
- WCAG 3.1.5 - Reading Level

---

## Performance

| Metric | JupyterLab-a11y-checker | Custom Tool |
|--------|------------------------|-------------|
| Analysis Speed | Thorough | Fast |
| Memory Usage | Higher | Lower |
| Accuracy | Very High | Good |
| False Positives | Low | Moderate |
| Startup Time | Moderate | Fast |

---

## Community & Support

### JupyterLab-a11y-checker
- Maintained by Berkeley DSEP infrastructure team
- Research-backed (arXiv paper)
- Active development
- Growing community
- Professional support available

### Custom Tool
- Individual/small team maintenance
- Open source
- Simple, understandable codebase
- Easy to contribute to
- Designed for learning and customization

---

## Cost

### Both Tools:
- ✅ Free and open source
- ✅ No licensing fees
- ✅ No subscription costs

### Additional Costs:
- **JupyterLab-a11y-checker**: Optional LLM/VLM API costs for AI features
- **Custom Tool**: None

---

## The Bottom Line

**There's no "wrong" choice** - both tools are excellent and serve different needs:

- **JupyterLab-a11y-checker** = More comprehensive, professional, feature-rich
- **Custom Tool** = Simpler, more portable, easier to understand

Many users will benefit from having **both available**:
- Use JupyterLab-a11y-checker for development
- Use Custom Tool for reporting and batch operations

---

## Learn More

- **Detailed Comparison:** [COMPARISON.md](COMPARISON.md)
- **Side-by-Side Tables:** [QUICK_COMPARISON.md](QUICK_COMPARISON.md)
- **Custom Tool Docs:** [A11Y_AUDIT_README.md](A11Y_AUDIT_README.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **JupyterLab-a11y-checker:** https://github.com/berkeley-dsep-infra/jupyterlab-a11y-checker

---

**Questions? Issues?** Open an issue in this repository or the JupyterLab-a11y-checker repository.

**Want to contribute?** Both projects welcome contributions!
