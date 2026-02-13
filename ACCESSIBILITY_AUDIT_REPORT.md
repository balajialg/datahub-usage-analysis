# Accessibility Audit Report for Jupyter Notebooks

## Executive Summary

An automated accessibility (a11y) audit was conducted on all 6 Jupyter notebooks in this repository. The audit identified **100 total accessibility issues** across **3 notebooks**. Three notebooks (`01-anonimize-hub-logs.ipynb`, `02-get-cloud-costs.ipynb`, and `02_5-munge-data.ipynb`) passed without issues.

### Summary Statistics
- **Total notebooks audited:** 6
- **Notebooks with issues:** 3
- **Notebooks passing:** 3
- **Total issues found:** 100

### Issues by Category
1. **Missing Alt Text:** 55 issues (55%)
2. **Missing Chart Description:** 28 issues (28%)
3. **Color Dependence:** 14 issues (14%)
4. **Heading Structure:** 3 issues (3%)

---

## Detailed Findings by Notebook

### ✅ 01-anonimize-hub-logs.ipynb
**Status:** No accessibility issues detected

### ✅ 02-get-cloud-costs.ipynb
**Status:** No accessibility issues detected

### ✅ 02_5-munge-data.ipynb
**Status:** No accessibility issues detected

---

### ⚠️ 03-visualize-cost-and-usage.ipynb
**Issues Found:** 3

#### Heading Structure (1 issue)
- First heading starts at level 2 instead of level 1: 'All graphs dealing w/any billing data are broken!'

#### Missing Chart Description (2 issues)
- Cell 17: Chart without nearby textual description
- Cell 39: Chart without nearby textual description

---

### ⚠️ logs_visualization_dashboard.ipynb
**Issues Found:** 47

#### Heading Structure (1 issue)
- Heading level jumps from 3 to 5: 'Making Graphs of Date of Usage Per Course'

#### Missing Alt Text (26 issues)
Charts and images rendered in the following cells lack alternative text descriptions:
- Cell 23, 24, 26, 28, 30, 33, 34, 35, 37, 39, 42, 43, 44, 45, 46, 48, 50, 51, 52, 53, 54, 58, 60, 61, 63, 64

#### Color Dependence (7 issues)
- Cell 24: Pie chart detected - may rely on color alone
- Cell 24: Color used in plot - ensure not relying solely on color
- Cell 30: Pie chart detected - may rely on color alone
- Cell 34: Pie chart detected - may rely on color alone
- Cell 35: Color used in plot - ensure not relying solely on color
- Cell 39: Color used in plot - ensure not relying solely on color
- Cell 60: Pie chart detected - may rely on color alone

#### Missing Chart Description (13 issues)
- Cell 23, 24, 26, 28, 30, 33, 34, 35, 39, 58, 61, 63, 64

---

### ⚠️ nbgitpuller_processing_visualization.ipynb
**Issues Found:** 50

#### Heading Structure (1 issue)
- Heading level jumps from 3 to 5: 'Making Graphs of Date of Usage Per Course'

#### Missing Alt Text (29 issues)
Charts and images rendered in the following cells lack alternative text descriptions:
- Cell 22, 23, 25, 27, 29, 32, 33, 34, 36, 38, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 57, 59, 60, 62, 63

#### Color Dependence (7 issues)
- Cell 23: Pie chart detected - may rely on color alone
- Cell 23: Color used in plot - ensure not relying solely on color
- Cell 29: Pie chart detected - may rely on color alone
- Cell 33: Pie chart detected - may rely on color alone
- Cell 34: Color used in plot - ensure not relying solely on color
- Cell 38: Color used in plot - ensure not relying solely on color
- Cell 59: Pie chart detected - may rely on color alone

#### Missing Chart Description (13 issues)
- Cell 22, 23, 25, 27, 29, 32, 33, 34, 38, 57, 60, 62, 63

---

## Accessibility Issues Explained

### 1. Missing Alt Text (55 issues - CRITICAL)
**Impact:** Screen reader users cannot access visual content

**What it means:** Charts and images (primarily matplotlib visualizations) lack alternative text descriptions. When a blind or visually impaired user encounters these charts with a screen reader, they receive no information about what the visualization shows.

**Best practices to fix:**
- Add descriptive alt text to images using markdown: `![Description of chart](image.png)`
- For matplotlib charts, add a markdown cell immediately before or after explaining what the chart shows
- Include key insights in text form (e.g., "The chart shows daily active users peaking at 500 on March 15th")

### 2. Missing Chart Description (28 issues - HIGH)
**Impact:** Users without visual context cannot understand chart purpose

**What it means:** Charts are created without nearby explanatory text. Even users who can see the charts benefit from textual context explaining what to look for and why the visualization matters.

**Best practices to fix:**
- Add markdown cells before charts explaining what question the visualization answers
- Add markdown cells after charts summarizing key findings
- Include data interpretation and insights in text

### 3. Color Dependence (14 issues - MEDIUM)
**Impact:** Colorblind users and those with low vision may not distinguish information

**What it means:** Visualizations use color as the primary way to distinguish data, which may be inaccessible to ~8% of males and ~0.5% of females with color vision deficiencies.

**Best practices to fix:**
- Add patterns or textures to pie chart segments
- Use direct labels on pie charts instead of only legends
- Ensure sufficient color contrast (WCAG 2.1 Level AA requires 4.5:1 for text, 3:1 for graphics)
- Use colorblind-friendly palettes (e.g., viridis, ColorBrewer)
- Add markers/line styles to distinguish lines in line plots

### 4. Heading Structure (3 issues - LOW)
**Impact:** Screen reader navigation and document outline may be confusing

**What it means:** Markdown heading levels should follow a logical hierarchy (h1 → h2 → h3, not h1 → h3). Skipping levels can confuse screen reader users who navigate by headings.

**Best practices to fix:**
- Start notebooks with a level 1 heading (`#`)
- Don't skip heading levels (e.g., don't go from `###` to `#####`)
- Use heading levels to create a logical document outline

---

## Recommendations

### Priority 1 (Critical) - Address Missing Alt Text
Focus on the two visualization notebooks which contain the majority of accessibility issues:
- `logs_visualization_dashboard.ipynb` (26 charts without alt text)
- `nbgitpuller_processing_visualization.ipynb` (29 charts without alt text)

### Priority 2 (High) - Add Chart Descriptions
Add markdown explanations for all charts to provide context and key findings.

### Priority 3 (Medium) - Fix Color Dependence
- Replace pie charts with accessible alternatives (bar charts, tables)
- If pie charts are needed, add data labels directly on segments
- Use colorblind-friendly palettes

### Priority 4 (Low) - Fix Heading Hierarchy
Correct the heading structure in affected notebooks to ensure proper document outline.

---

## Testing Methodology

The audit was performed using a custom Python script that analyzes notebook JSON structure for common accessibility issues:

1. **Heading Structure Analysis:** Validates proper heading hierarchy (no skipped levels)
2. **Image Alt Text Detection:** Checks for alt attributes in markdown and HTML images
3. **Chart Output Analysis:** Identifies chart outputs without accompanying descriptions
4. **Color Usage Patterns:** Detects pie charts and color-dependent visualizations
5. **Context Analysis:** Checks for nearby markdown explanations for visualizations

---

## Next Steps

1. Review this audit report with the team
2. Prioritize fixes based on impact and effort
3. Create specific issues for each category of fixes if desired
4. Consider implementing accessibility checks in CI/CD pipeline
5. Document accessibility guidelines for future notebook development

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Jupyter Accessibility Guide](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html#accessibility)
- [ColorBrewer (Colorblind-safe palettes)](https://colorbrewer2.org/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Matplotlib Accessibility Tips](https://matplotlib.org/stable/users/explain/colors/colors.html)

---

**Audit Date:** 2026-02-10
**Audit Tool:** Custom Python accessibility checker
**Notebooks Audited:** 6
