# Jupyter Notebook Accessibility (a11y) Audit Tool

## Overview

This tool provides comprehensive accessibility auditing for Jupyter Notebooks following **WCAG 2.1/2.2 standards**. It helps ensure your notebooks are accessible to all users, including those using assistive technologies like screen readers.

## Features

### 1. Comprehensive Accessibility Audit
- **Image Alt Text**: Checks all images (Markdown and HTML) for descriptive alt text
- **Heading Structure**: Validates proper heading hierarchy (H1, H2, H3, etc.)
- **Table Accessibility**: Ensures tables have proper headers and semantic structure
- **Color Usage**: Identifies content that relies solely on color perception
- **Reading Order**: Verifies logical content flow
- **Code Context**: Checks that code cells have explanatory markdown

### 2. Detailed Reporting
Reports are categorized into three levels:
- **Critical** (Must Fix): WCAG Level A violations that must be addressed
- **Warning** (Should Fix): WCAG Level AA/AAA issues that improve accessibility
- **Success**: Confirms what's working correctly

### 3. Multiple Report Formats
- **Text**: Clean, readable text format for terminal/email
- **JSON**: Structured data for integration with other tools
- **HTML**: Beautiful, styled report that's itself accessible

### 4. Automatic Remediation
The tool can automatically fix common issues:
- Add placeholder alt text to images
- Add main title (H1) if missing
- Add table header separators
- Generate accessible version of your notebook

## Installation

No additional dependencies required! Uses Python standard library only.

```bash
# The tool is ready to use
python a11y_audit.py --help
```

## Usage

### Basic Audit

```bash
# Audit a notebook and display report in terminal
python a11y_audit.py notebooks/your-notebook.ipynb
```

### Save Report to File

```bash
# Save as text file
python a11y_audit.py notebooks/your-notebook.ipynb --output report.txt

# Save as HTML (recommended for sharing)
python a11y_audit.py notebooks/your-notebook.ipynb --format html --output report.html

# Save as JSON (for automation)
python a11y_audit.py notebooks/your-notebook.ipynb --format json --output report.json
```

### Automatic Remediation

```bash
# Fix issues automatically
python a11y_audit.py notebooks/your-notebook.ipynb --remediate

# This creates: notebooks/your-notebook_accessible.ipynb

# Specify custom output path
python a11y_audit.py notebooks/your-notebook.ipynb --remediate --remediated-output fixed.ipynb
```

### Combined Workflow

```bash
# Audit, generate HTML report, and create remediated version
python a11y_audit.py notebooks/my-notebook.ipynb \
    --format html \
    --output audit-report.html \
    --remediate
```

## Understanding the Report

### Critical Issues
These are WCAG Level A violations that **must** be fixed:

- **MISSING_ALT_TEXT**: Images without alternative text descriptions
- **MISSING_ALT_ATTRIBUTE**: HTML images missing the alt attribute
- **EMPTY_ALT_TEXT**: Images with empty alt text

**Impact**: Screen reader users cannot understand image content.

### Warnings
These are WCAG Level AA/AAA issues that **should** be fixed:

- **MISSING_TITLE**: Notebook without main H1 heading
- **HEADING_HIERARCHY**: Skipped heading levels (e.g., H1 → H3)
- **TABLE_NO_HEADER**: Tables without header rows
- **TABLE_SCOPE**: Missing scope attributes on table headers
- **CODE_CONTEXT**: Code cells without explanatory markdown
- **COLOR_ONLY**: Content relying solely on color perception

**Impact**: Reduces usability for all users, especially those with disabilities.

### Success Indicators
These confirm what's working well:

- **IMAGE_ALT_TEXT**: Images with proper alt text
- **HAS_TITLE**: Notebook has main title
- **TABLE_HEADER**: Tables with proper headers
- **HAS_MARKDOWN**: Explanatory markdown cells present

## WCAG Guidelines Reference

### WCAG 2.1 Level A (Critical)
- **1.1.1 Non-text Content**: All images must have text alternatives
- **1.3.1 Info and Relationships**: Semantic structure (headings, tables)
- **2.4.2 Page Titled**: Every page/document needs a title
- **1.4.1 Use of Color**: Don't use color as the only visual means

### WCAG 2.1 Level AA (Important)
- **1.4.3 Contrast (Minimum)**: 4.5:1 contrast ratio for normal text
- **1.4.5 Images of Text**: Avoid text in images when possible
- **2.4.6 Headings and Labels**: Descriptive headings and labels

### WCAG 2.1 Level AAA (Enhancement)
- **3.1.5 Reading Level**: Content understandable at appropriate level

## Best Practices

### Images
```markdown
# Good ✓
![Bar chart showing student enrollment increasing from 2020-2023](enrollment-chart.png)

# Bad ✗
![](enrollment-chart.png)
![ ](enrollment-chart.png)
```

### Headings
```markdown
# Good ✓
# Main Title
## Section 1
### Subsection 1.1
## Section 2

# Bad ✗
# Main Title
### Subsection (skipped H2)
```

### Tables
```markdown
# Good ✓
| Name | Score |
|------|-------|
| Alice| 95    |
| Bob  | 87    |

# Bad ✗
| Alice| 95    |
| Bob  | 87    |
```

### Code Context
```markdown
# Good ✓
## Data Loading
We load the dataset from CSV and clean missing values.

import pandas as pd
df = pd.read_csv('data.csv')

# Bad ✗
import pandas as pd
df = pd.read_csv('data.csv')

import numpy as np
arr = np.array([1,2,3])
```

## Programmatic Usage

You can also use the tool in your Python scripts:

```python
from a11y_audit import AccessibilityAuditor, AccessibilityRemediator

# Audit a notebook
auditor = AccessibilityAuditor('my-notebook.ipynb')
issues = auditor.audit()

# Generate reports
text_report = auditor.generate_report('text')
html_report = auditor.generate_report('html')
auditor.save_report('report.html', 'html')

# Remediate issues
remediator = AccessibilityRemediator('my-notebook.ipynb')
changes = remediator.remediate(auto_fix=True)
output_path = remediator.save_remediated('fixed-notebook.ipynb')

print(f"Made {len(changes['changes'])} changes")
print(f"Saved to: {output_path}")
```

## Accessibility Terminology

- **ARIA**: Accessible Rich Internet Applications - standards for making web content accessible
- **Alt Text**: Alternative text description for images, read by screen readers
- **Contrast Ratio**: Measure of difference between text and background colors (e.g., 4.5:1)
- **Semantic Structure**: Using HTML/Markdown elements for their intended meaning (e.g., headings for titles)
- **Screen Reader**: Assistive technology that reads content aloud for visually impaired users
- **WCAG**: Web Content Accessibility Guidelines - international standards for web accessibility

## Why Accessibility Matters

1. **Legal Compliance**: Many organizations are legally required to provide accessible content
2. **Inclusive Education**: Ensures all students can learn, regardless of ability
3. **Better for Everyone**: Accessible design improves usability for all users
4. **SEO Benefits**: Well-structured content ranks better in search engines
5. **Ethics**: Everyone deserves equal access to information and education

## Limitations

- **Color Contrast**: Currently detects color references but doesn't analyze actual contrast ratios in images/plots
- **Language**: Assumes English content for some checks
- **Context**: Cannot understand semantic meaning - may flag decorative images that don't need alt text
- **Generated Content**: Cannot check accessibility of dynamically generated visualizations in output cells

## Future Enhancements

Planned features:
- AI-powered alt text generation using image analysis
- Color contrast analysis for matplotlib/seaborn plots
- Link text accessibility checking
- Math equation accessibility (MathJax/LaTeX)
- Language detection and multilingual support
- Integration with Jupyter Lab/Notebook as extension

## Contributing

To improve this tool:
1. Test with diverse notebooks
2. Report issues and edge cases
3. Suggest additional WCAG checks
4. Share best practices

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM - Web Accessibility In Mind](https://webaim.org/)
- [A11Y Project](https://www.a11yproject.com/)
- [Jupyter Accessibility](https://jupyter-accessibility.readthedocs.io/)

## Support

For questions or issues with this tool, please open an issue in the repository.

---

**Remember**: Accessibility is not a one-time checklist but an ongoing commitment to inclusive design. This tool helps identify issues, but human judgment is essential for truly accessible content.
