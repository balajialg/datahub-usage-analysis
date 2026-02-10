# Jupyter Notebook Accessibility Auditor

## Overview

The Jupyter Notebook Accessibility Auditor is a comprehensive tool designed to ensure your Jupyter Notebooks meet **Web Content Accessibility Guidelines (WCAG) 2.1/2.2 Level AA** standards. This tool helps make your notebooks accessible to all users, including those using assistive technologies.

## Features

### 🔍 **Accessibility Audit Capabilities**

The auditor systematically checks for common WCAG compliance issues:

1. **Image Accessibility (WCAG 1.1.1 Non-text Content)**
   - Missing alt text on images
   - Empty alt attributes
   - Proper image descriptions

2. **Semantic Structure (WCAG 1.3.1 Info and Relationships)**
   - Proper heading hierarchy (H1 → H2 → H3, etc.)
   - Missing headings in content sections
   - Document structure

3. **Navigation (WCAG 2.4.4 Link Purpose, 2.4.6 Headings and Labels)**
   - Descriptive link text
   - Bare URLs without context
   - Proper headings for navigation

4. **Color Contrast (WCAG 1.4.3 Contrast Minimum)**
   - Inline color usage detection
   - Contrast ratio warnings

5. **Table Structure (WCAG 1.3.1)**
   - Proper table headers
   - Table accessibility

6. **Code Documentation (WCAG 3.1.5 Reading Level - AAA)**
   - Code comments for complex logic

### ✨ **Automated Remediation**

The tool can automatically fix many common issues:
- Add placeholder alt text to images
- Add H1 document titles
- Wrap bare URLs in proper markdown links
- Generate accessible notebook versions

### 📊 **Report Formats**

Generate detailed reports in multiple formats:
- **Text**: Plain text for terminal output
- **Markdown**: Formatted reports with emojis and structure
- **JSON**: Machine-readable format for integration

## Installation

### Prerequisites

- Python 3.6 or higher
- Jupyter Notebook (optional, for viewing notebooks)

### Quick Start

No installation required! The tool is a standalone Python script.

```bash
# Make the script executable (optional)
chmod +x a11y_audit.py
```

## Usage

### Command Overview

The tool has three main commands:

1. **`audit`** - Run accessibility audit only
2. **`remediate`** - Fix accessibility issues
3. **`full`** - Run audit + remediation in one step

### 1. Running an Audit

Check your notebook for accessibility issues:

```bash
# Basic audit (output to terminal)
python3 a11y_audit.py audit Demo.ipynb

# Save audit report to file
python3 a11y_audit.py audit Demo.ipynb --output audit_report.txt

# Generate Markdown report
python3 a11y_audit.py audit Demo.ipynb --format markdown --output audit_report.md

# Generate JSON report
python3 a11y_audit.py audit Demo.ipynb --format json --output audit_report.json
```

### 2. Remediating Issues

Automatically fix accessibility issues:

```bash
# Create a fixed version of your notebook
python3 a11y_audit.py remediate Demo.ipynb --output Demo_accessible.ipynb
```

### 3. Full Audit + Remediation

Run both audit and remediation in one step:

```bash
# Default: creates Demo_fixed.ipynb and Demo_audit_report.md
python3 a11y_audit.py full Demo.ipynb

# Custom output paths
python3 a11y_audit.py full Demo.ipynb \
  --output-notebook Demo_accessible.ipynb \
  --output-report accessibility_report.md \
  --format markdown
```

## Understanding the Report

### Report Structure

Reports are organized into three severity levels:

#### 🔴 **Critical Issues** (Must Fix)
These are WCAG Level A failures that **must** be fixed:
- Missing alt text on images
- Broken accessibility features

#### ⚠️ **Warnings** (Should Fix)
These are WCAG Level AA recommendations:
- Missing headings
- Non-descriptive link text
- Heading hierarchy issues

#### ✅ **Successful Checks**
Items that passed accessibility checks:
- Images with proper alt text
- Proper heading structure
- Descriptive links

### Sample Report

```markdown
# Jupyter Notebook Accessibility Audit Report

**Notebook:** Demo.ipynb
**Date:** 2026-02-10 22:28:38
**WCAG Standard:** 2.1 Level AA

## Summary

- 🔴 **Critical Issues:** 1
- ⚠️ **Warnings:** 9
- ✅ **Successful Checks:** 10

## 🔴 Critical Issues (Must Fix)

### 1. Missing Alt Text

- **Cell:** 2
- **Description:** Image missing alt text: attachment:image.jpg
- **WCAG Standard:** WCAG 2.1 Level A - 1.1.1 Non-text Content
- **Remediation:** Add descriptive alt text for the image
```

## Accessibility Best Practices

### Writing Alt Text

**Good alt text is:**
- Descriptive and specific
- Concise (aim for < 125 characters)
- Contextually relevant

**Examples:**

```markdown
# ❌ Bad
![](chart.png)
![image](chart.png)

# ✅ Good
![Bar chart showing 45% increase in student enrollment from 2020-2024](chart.png)
```

### Heading Hierarchy

**Proper hierarchy:**
```markdown
# H1 - Document Title
## H2 - Main Section
### H3 - Subsection
#### H4 - Sub-subsection
```

**❌ Avoid skipping levels:**
```markdown
# H1
### H3  ← Skip from H1 to H3 (bad)
```

### Link Text

**Good link text describes the destination:**

```markdown
# ❌ Bad
Click [here](https://example.com)
Visit [this link](https://example.com)

# ✅ Good
Read the [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/)
Download the [2024 Annual Report (PDF)](https://example.com/report.pdf)
```

### Table Accessibility

**Always use headers in tables:**

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

## Technical Details

### WCAG Standards Covered

- **WCAG 2.1 Level A** (minimum requirements)
  - 1.1.1 Non-text Content
  - 1.3.1 Info and Relationships
  - 2.4.4 Link Purpose (In Context)

- **WCAG 2.1 Level AA** (recommended)
  - 1.4.3 Contrast (Minimum)
  - 2.4.6 Headings and Labels

- **WCAG 2.1 Level AAA** (enhanced)
  - 3.1.5 Reading Level

### Automated Remediation Details

The tool makes these automated fixes:

1. **Images without alt text**
   - Adds placeholder: `![Descriptive image - please update alt text](url)`
   - User should update with actual description

2. **Missing H1 heading**
   - Adds: `# Notebook Title` at the start
   - User should customize the title

3. **Bare URLs**
   - Wraps: `[Link to URL](URL)`
   - User should improve link text

### Limitations

The tool **cannot** automatically detect:
- **Color contrast ratios** (requires visual analysis)
- **Image content** for generating accurate alt text
- **Logical reading order** in complex layouts
- **Context-specific** accessibility issues

## Integration with Workflows

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run accessibility audit before commit
python3 a11y_audit.py audit *.ipynb --format text
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Accessibility Audit
  run: |
    python3 a11y_audit.py audit *.ipynb --format json --output audit.json
    # Fail if critical issues found
    if [ $? -ne 0 ]; then
      echo "Critical accessibility issues found!"
      exit 1
    fi
```

### Jupyter Lab/Notebook Extension

For interactive auditing, consider installing:
```bash
pip install jupyterlab-a11y-checker
```

## Troubleshooting

### Common Issues

**Q: The tool reports false positives**
A: Some decorative images may intentionally have empty alt text. Review each issue in context.

**Q: My custom markdown isn't detected**
A: The tool uses regex patterns for common markdown. Complex HTML may need manual review.

**Q: How do I fix color contrast issues?**
A: Use online tools like [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to verify your colors meet WCAG standards.

## Resources

### WCAG Guidelines
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [How to Meet WCAG](https://www.w3.org/WAI/WCAG21/quickref/)

### Alt Text Resources
- [WebAIM: Alternative Text](https://webaim.org/techniques/alttext/)
- [W3C Alt Decision Tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)

### Color Contrast Tools
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colour Contrast Analyser](https://www.tpgi.com/color-contrast-checker/)

### Jupyter Accessibility
- [Jupyter Accessibility Efforts](https://jupyter-accessibility.readthedocs.io/)
- [JupyterLab Accessibility](https://jupyterlab.readthedocs.io/en/stable/user/accessibility.html)

## Support and Contributing

### Reporting Issues

If you find bugs or have suggestions:
1. Check existing issues in the repository
2. Provide a sample notebook (if possible)
3. Describe expected vs. actual behavior

### Contributing

Contributions are welcome! Areas for improvement:
- Additional WCAG checks
- Better alt text generation (AI integration)
- More output formats
- Interactive remediation mode

## License

This tool is provided under the same license as the repository.

## Acknowledgments

Built following WCAG 2.1/2.2 standards and best practices from:
- W3C Web Accessibility Initiative (WAI)
- WebAIM
- Jupyter Accessibility Working Group

---

## Quick Reference Card

### Commands
```bash
# Audit only
python3 a11y_audit.py audit notebook.ipynb

# Fix issues
python3 a11y_audit.py remediate notebook.ipynb --output fixed.ipynb

# Audit + Fix
python3 a11y_audit.py full notebook.ipynb
```

### Key Accessibility Principles
1. **Perceivable**: Alt text, captions, color contrast
2. **Operable**: Keyboard navigation, descriptive links
3. **Understandable**: Clear structure, consistent navigation
4. **Robust**: Valid markup, semantic structure

### Before Publishing Checklist
- [ ] All images have descriptive alt text
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Links have descriptive text (not "click here")
- [ ] Tables have header rows
- [ ] Color contrast meets WCAG AA (4.5:1 minimum)
- [ ] Code has explanatory comments
- [ ] Ran accessibility audit with 0 critical issues
