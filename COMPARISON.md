# Comparison: JupyterLab-a11y-checker vs. Custom a11y Audit Tool

## Executive Summary

This document provides a comprehensive comparison between two Jupyter Notebook accessibility audit tools:

1. **JupyterLab-a11y-checker** - Berkeley DSEP infrastructure project with both a JupyterLab extension and CLI tool
2. **Custom a11y Audit Tool** (this repository) - A standalone Python-based CLI tool for WCAG compliance auditing

Both tools aim to ensure Jupyter Notebooks meet accessibility standards, but they differ significantly in architecture, features, implementation, and use cases.

---

## Architecture & Implementation

### JupyterLab-a11y-checker

**Tech Stack:**
- TypeScript/JavaScript (Node.js)
- Monorepo structure with 3 packages:
  - `@berkeley-dsep-infra/a11y-checker-core` - Shared logic
  - `@berkeley-dsep-infra/a11y-checker-cli` - Command-line tool
  - `@berkeley-dsep-infra/a11y-checker-extension` - JupyterLab extension
- Integrates **axe-core** (industry-standard accessibility engine from Deque)
- Vision-Language Model (VLM) and LLM integration for AI assistance

**Installation:**
```bash
pip install jupyterlab-a11y-checker
# OR
npx @jupyterlab-a11y-checker/cli notebook.ipynb
```

**Architecture Benefits:**
- Real-time checking within JupyterLab interface
- Axe-core integration provides deep DOM-level analysis
- Shared core logic between extension and CLI
- Professional packaging and distribution

### Custom a11y Audit Tool (This Repository)

**Tech Stack:**
- Pure Python (stdlib only: `json`, `re`, `pathlib`)
- Single-file implementation (~850 LOC)
- Regex-based parsing of Markdown and HTML
- No external dependencies

**Installation:**
```bash
# No installation needed - just run the script
python a11y_audit.py notebook.ipynb
```

**Architecture Benefits:**
- Zero dependencies - works everywhere Python runs
- Simple, readable code base
- Easy to customize and extend
- Lightweight and portable
- Can be dropped into any project

---

## Feature Comparison

### Detection Capabilities

| Feature | JupyterLab-a11y-checker | Custom a11y Audit Tool |
|---------|------------------------|------------------------|
| **Images** |
| Missing alt text | ✅ | ✅ |
| Empty alt text | ✅ | ✅ |
| HTML img tags | ✅ | ✅ |
| AI-generated alt text | ✅ (VLM integration) | ⚠️ (Placeholder only) |
| **Headings** |
| Missing H1 | ✅ | ✅ |
| Multiple H1s | ✅ | ❌ |
| Duplicate headings | ✅ | ❌ |
| Heading hierarchy | ✅ | ✅ |
| Empty headings | ✅ | ❌ |
| **Tables** |
| Missing headers | ✅ | ✅ |
| Missing captions | ✅ | ❌ |
| Missing scope attribute | ✅ | ⚠️ (Detection only) |
| **Color** |
| Contrast ratio analysis | ✅ (Image analysis) | ⚠️ (Pattern detection) |
| Color-only information | ❌ | ✅ |
| **Links** |
| Non-descriptive link text | ✅ | ❌ |
| **Code Context** |
| Consecutive code cells | ❌ | ✅ |
| **Other** |
| Axe-core integration | ✅ (Extension only) | ❌ |

### Remediation Capabilities

| Feature | JupyterLab-a11y-checker | Custom a11y Audit Tool |
|---------|------------------------|------------------------|
| Automatic fixes | ✅ (Interactive UI) | ✅ (CLI-based) |
| Image alt text | ✅ (AI-powered) | ✅ (Placeholder) |
| Table headers | ✅ | ✅ |
| Heading issues | ✅ | ⚠️ (Add title only) |
| Interactive UI | ✅ (JupyterLab) | ❌ |
| Batch processing | ✅ | ✅ |
| Preview before save | ✅ | ❌ |

### Reporting

| Feature | JupyterLab-a11y-checker | Custom a11y Audit Tool |
|---------|------------------------|------------------------|
| Text report | ✅ | ✅ |
| JSON report | ✅ (LLM-optimized) | ✅ |
| HTML report | ❌ | ✅ |
| Real-time feedback | ✅ (Extension) | ❌ |
| Cell-level location | ✅ | ✅ |
| WCAG references | ✅ | ✅ |
| Remediation guidance | ✅ | ✅ |
| Severity categories | ❌ | ✅ (Critical/Warning/Success) |

---

## Standards Alignment

### JupyterLab-a11y-checker

**Standards Coverage:**
- Based on research: "Notably Inaccessible — Data Driven Understanding of Data Science Notebook (In)Accessibility" (arXiv 2023)
- Prioritizes empirically-identified issues in Jupyter Notebooks
- WCAG 2.1 AA guidelines
- Axe-core covers 57+ accessibility rules

**Covered Guidelines:**
- WCAG 1.1.1 (Non-text Content)
- WCAG 1.3.1 (Info and Relationships)
- WCAG 1.4.3 (Contrast - Minimum)
- WCAG 2.4.2 (Page Titled)
- WCAG 2.4.4 (Link Purpose)
- WCAG 2.4.6 (Headings and Labels)

### Custom a11y Audit Tool

**Standards Coverage:**
- WCAG 2.1/2.2 compliance focus
- Addresses most common notebook issues
- Level A (Critical) vs AA/AAA (Warning) distinction

**Covered Guidelines:**
- WCAG 1.1.1 (Non-text Content)
- WCAG 1.3.1 (Info and Relationships)
- WCAG 1.4.1 (Use of Color)
- WCAG 2.4.2 (Page Titled)
- WCAG 3.1.5 (Reading Level)

---

## Use Cases

### When to Use JupyterLab-a11y-checker

**Best For:**
1. **Active development in JupyterLab**
   - Real-time feedback as you create content
   - Interactive fixing with guided UI
   - Immediate validation

2. **Comprehensive accessibility coverage**
   - Need DOM-level analysis via axe-core
   - Require color contrast analysis on images
   - Want AI-powered alt text generation

3. **CI/CD integration**
   - GitHub Actions workflow
   - Automated checks on every push
   - LLM-optimized JSON output

4. **Team/organizational use**
   - Professional packaging (npm/pip)
   - Regular updates and maintenance
   - Community support from Berkeley

5. **Advanced features**
   - VLM/LLM integration for AI assistance
   - Detailed link text analysis
   - Caption and scope attribute checking

**Example Workflow:**
```bash
# In CI/CD
npx @jupyterlab-a11y-checker/cli **/*.ipynb

# Local development
jupyter lab  # Extension provides real-time checks
```

### When to Use Custom a11y Audit Tool

**Best For:**
1. **Simple, standalone audits**
   - One-off accessibility checks
   - No installation overhead
   - Quick validation of notebooks

2. **Resource-constrained environments**
   - No npm/node.js available
   - Minimal dependencies preferred
   - Limited disk space

3. **Custom integration**
   - Need to modify audit logic
   - Integrate into existing Python workflows
   - Add organization-specific checks

4. **Batch processing**
   - Audit many notebooks at once
   - Generate HTML reports for stakeholders
   - Remediate multiple files automatically

5. **Learning and education**
   - Simple, readable codebase
   - Easy to understand implementation
   - Good teaching example

6. **Offline/airgapped environments**
   - No external API calls required
   - No npm registry access needed
   - Pure Python standard library

**Example Workflow:**
```bash
# Audit all notebooks
for nb in notebooks/*.ipynb; do
    python a11y_audit.py "$nb" --output "reports/$(basename "$nb" .ipynb).txt"
done

# Generate stakeholder report
python a11y_audit.py important.ipynb --format html --output report.html

# Batch remediation
python a11y_audit.py notebook.ipynb --remediate
```

---

## Strengths & Weaknesses

### JupyterLab-a11y-checker

**Strengths:**
- ✅ **Professional development**: Maintained by Berkeley team with accessibility expertise
- ✅ **Comprehensive coverage**: Axe-core + custom rules = extensive checking
- ✅ **Real-time feedback**: Extension provides immediate guidance
- ✅ **AI integration**: VLM/LLM for intelligent alt text generation
- ✅ **Research-based**: Rules derived from empirical notebook accessibility study
- ✅ **Interactive remediation**: Guided UI for fixing issues
- ✅ **CI/CD ready**: GitHub Actions integration out of the box

**Weaknesses:**
- ❌ **Dependencies**: Requires Node.js ecosystem
- ❌ **Complexity**: Monorepo setup, TypeScript, multiple packages
- ❌ **Extension-only features**: Some features (axe-core) only work in extension
- ❌ **Learning curve**: More complex to modify or extend
- ❌ **Installation overhead**: Requires npm/pip installation

### Custom a11y Audit Tool

**Strengths:**
- ✅ **Zero dependencies**: Pure Python stdlib
- ✅ **Simple architecture**: Single file, ~850 LOC, easy to understand
- ✅ **Portable**: Works anywhere Python runs
- ✅ **Customizable**: Easy to modify for specific needs
- ✅ **Multiple report formats**: Text, JSON, and HTML
- ✅ **Severity categories**: Clear Critical/Warning/Success distinction
- ✅ **HTML reports**: Beautiful, shareable reports
- ✅ **Fast deployment**: No installation, just run the script

**Weaknesses:**
- ❌ **Limited detection**: No DOM-level analysis, regex-based only
- ❌ **No real-time checking**: CLI-only, no JupyterLab integration
- ❌ **Basic remediation**: Placeholder text only, no AI generation
- ❌ **Manual image analysis**: No color contrast computation
- ❌ **Feature gaps**: Missing some advanced checks (duplicate headings, link text, captions)
- ❌ **Single maintainer**: Not backed by an organization

---

## Technical Deep Dive

### Detection Methods

**JupyterLab-a11y-checker:**
```typescript
// Uses parsed cell structure + axe-core
const cells = rawIpynbToGeneralCells(jsonContent);
const issues = await analyzeCellsAccessibilityCLI(cells, imageProcessor);

// Image processing with VLM
const imageProcessor = new NodeImageProcessor();
// Analyzes actual image files for contrast, content, etc.
```

**Custom a11y Audit Tool:**
```python
# Regex-based pattern matching
image_patterns = [
    r'!\[(.*?)\]\(.*?\)',  # Markdown
    r'<img\s+[^>]*src=["\'].*?["\'][^>]*>',  # HTML
]

# Iterates through notebook JSON
for cell in cells:
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell.get('source', []))
        # Apply regex patterns
```

### Output Comparison

**JupyterLab-a11y-checker output:**
```
Analyzing /path/to/notebook.ipynb...
Found 3 issues in notebook.ipynb:

2 violations found for image-missing-alt:
    Description: Ensure the presence of alt text in images
    WCAG Reference: WCAG 1.1.1
  - Cell 2 (markdown):
    Content: "![](chart.png)"
```

**Custom a11y Audit Tool output:**
```
================================================================================
JUPYTER NOTEBOOK ACCESSIBILITY AUDIT REPORT
================================================================================
Notebook: notebook.ipynb

SUMMARY
--------------------------------------------------------------------------------
Critical Issues: 1
Warnings: 2
Successful Checks: 4

CRITICAL ISSUES (Must Fix)
--------------------------------------------------------------------------------
1. MISSING_ALT_TEXT
   Location: Cell 2
   Message: Image is missing alt text description
   WCAG: WCAG 2.1 Level A - 1.1.1 Non-text Content
   How to Fix: Add descriptive alt text in square brackets
```

---

## Integration & Deployment

### JupyterLab-a11y-checker

**GitHub Actions:**
```yaml
steps:
  - uses: actions/checkout@v4
  - name: Scan notebooks
    uses: berkeley-dsep-infra/jupyterlab-a11y-checker@main
    with:
      files: "**/*.ipynb"
```

**Local Extension:**
```bash
pip install jupyterlab-a11y-checker
jupyter lab  # Extension auto-loads
```

**Requires:**
- Python 3.x
- Node.js (for CLI via npx)
- JupyterLab 3.x+ (for extension)

### Custom a11y Audit Tool

**CI Integration:**
```yaml
steps:
  - uses: actions/checkout@v4
  - name: Audit notebooks
    run: |
      python a11y_audit.py notebooks/*.ipynb
```

**Local Usage:**
```bash
# No installation needed
python a11y_audit.py notebook.ipynb
```

**Requires:**
- Python 3.6+
- No other dependencies

---

## Recommendation Matrix

| Scenario | Recommended Tool | Reason |
|----------|------------------|---------|
| Active notebook development | **JupyterLab-a11y-checker** | Real-time feedback in IDE |
| CI/CD pipeline | **Either** | Both support automation |
| Minimal dependencies | **Custom Tool** | Zero external dependencies |
| Comprehensive checking | **JupyterLab-a11y-checker** | Axe-core + VLM integration |
| Quick audits | **Custom Tool** | No installation required |
| Team collaboration | **JupyterLab-a11y-checker** | Better tooling and support |
| Custom requirements | **Custom Tool** | Easier to modify |
| Stakeholder reports | **Custom Tool** | HTML report generation |
| Research/education | **Custom Tool** | Simple, readable code |
| Production deployment | **JupyterLab-a11y-checker** | Professional maintenance |

---

## Complementary Use

These tools can work together:

1. **Development Phase**: Use JupyterLab-a11y-checker extension for real-time feedback
2. **Pre-commit**: Use Custom Tool for quick validation (no npm needed)
3. **CI/CD**: Use JupyterLab-a11y-checker CLI for comprehensive checks
4. **Reporting**: Use Custom Tool to generate HTML reports for stakeholders
5. **Auditing Legacy Content**: Use Custom Tool for batch processing existing notebooks

---

## Future Considerations

### JupyterLab-a11y-checker Roadmap
- Enhanced VLM/LLM integration
- More automated fixes
- Support for additional notebook elements
- Improved GitHub Actions integration

### Custom a11y Audit Tool Potential Enhancements
- Color contrast calculation (using Pillow)
- Duplicate heading detection
- Link text analysis
- Caption checking for tables
- Integration with LLMs for alt text generation
- JupyterLab extension version

---

## Conclusion

**Choose JupyterLab-a11y-checker if you:**
- Work primarily in JupyterLab
- Need comprehensive, research-backed accessibility checking
- Want AI-powered remediation
- Have access to Node.js ecosystem
- Prefer professional, maintained tools

**Choose Custom a11y Audit Tool if you:**
- Need a lightweight, portable solution
- Work in constrained environments
- Want zero dependencies
- Need easy customization
- Prefer simple, readable code
- Need HTML report generation

**Both tools are valuable** and address the critical need for accessible Jupyter Notebooks. The JupyterLab-a11y-checker is more feature-rich and integrated, while the Custom Tool is simpler and more flexible. Your choice depends on your specific needs, environment, and use case.

---

## References

- JupyterLab-a11y-checker: https://github.com/berkeley-dsep-infra/jupyterlab-a11y-checker
- Research Paper: ["Notably Inaccessible" (arXiv 2023)](https://arxiv.org/pdf/2308.03241)
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Axe-core: https://github.com/dequelabs/axe-core
