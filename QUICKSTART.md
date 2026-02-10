# Quick Start Guide: Jupyter Notebook Accessibility Audit Tool

## 🎯 What This Tool Does

The Jupyter Notebook Accessibility (a11y) Audit Tool ensures your notebooks are accessible to everyone, including people with disabilities. It checks for compliance with **WCAG 2.1/2.2 standards** and can automatically fix common issues.

## 🚀 Getting Started (3 Steps)

### Step 1: Audit Your Notebook

```bash
python a11y_audit.py notebooks/your-notebook.ipynb
```

This displays a report showing:
- ❌ **Critical Issues**: Must fix (e.g., missing alt text)
- ⚠️ **Warnings**: Should fix (e.g., heading hierarchy)
- ✅ **Success**: What's working correctly

### Step 2: Review the Report

The report shows exactly:
- **Where** the issue is (cell number)
- **What** the problem is
- **Why** it matters (WCAG guideline)
- **How** to fix it

### Step 3: Fix the Issues

**Option A: Automatic Fix (Recommended)**
```bash
python a11y_audit.py notebooks/your-notebook.ipynb --remediate
```
Creates: `notebooks/your-notebook_accessible.ipynb`

**Option B: Manual Fix**
Follow the "How to Fix" instructions in the report

## 📊 Generate Reports

### Text Report (Terminal/Email)
```bash
python a11y_audit.py notebook.ipynb --output report.txt
```

### HTML Report (Best for Sharing)
```bash
python a11y_audit.py notebook.ipynb --format html --output report.html
```
Open `report.html` in your browser to see a beautiful, styled report.

### JSON Report (For Automation)
```bash
python a11y_audit.py notebook.ipynb --format json --output report.json
```

## 🔧 Common Fixes

### 1. Missing Alt Text
**Before:**
```markdown
![](chart.png)
```

**After:**
```markdown
![Bar chart showing enrollment growth from 2020-2023](chart.png)
```

### 2. Missing Title
**Before:**
```markdown
## Data Analysis
```

**After:**
```markdown
# My Data Analysis Notebook
## Data Analysis
```

### 3. Table Without Header
**Before:**
```markdown
| Name | Score |
| Alice | 95 |
```

**After:**
```markdown
| Name | Score |
|------|-------|
| Alice | 95 |
```

## 📚 Example Workflow

```bash
# 1. Audit all notebooks in a directory
for notebook in notebooks/*.ipynb; do
    python a11y_audit.py "$notebook" --output "reports/$(basename "$notebook" .ipynb).txt"
done

# 2. Generate HTML report for stakeholders
python a11y_audit.py important-notebook.ipynb --format html --output stakeholder-report.html

# 3. Fix issues automatically
python a11y_audit.py notebook.ipynb --remediate

# 4. Verify fixes
python a11y_audit.py notebook_accessible.ipynb
```

## 🎓 Understanding the Results

### Critical Issues (Must Fix)
These violate **WCAG Level A** - the minimum level of accessibility:
- Missing alt text on images
- No alt attribute on HTML images
- Empty alt text

**Impact:** Screen readers can't describe images to visually impaired users.

### Warnings (Should Fix)
These improve accessibility but aren't critical:
- Missing main title (H1)
- Skipped heading levels
- Tables without headers
- Multiple code cells without explanation
- Content relying only on color

**Impact:** Reduces usability for everyone, especially people with disabilities.

### Success (Working Well)
- Images with descriptive alt text
- Proper heading hierarchy
- Tables with headers
- Good markdown structure

## 💡 Pro Tips

1. **Run Early, Run Often**: Check accessibility as you create content, not at the end
2. **Focus on Critical First**: Fix all critical issues before addressing warnings
3. **Test the Fixes**: Re-run the audit after fixing issues
4. **Educate Your Team**: Share the A11Y_AUDIT_README.md with colleagues
5. **Make it Automatic**: Add to your CI/CD pipeline or pre-commit hooks

## 🆘 Getting Help

### See Examples
```bash
# Open the example notebook to see how to use the tool
jupyter notebook notebooks/a11y-audit-example.ipynb
```

### Read Full Documentation
```bash
# View comprehensive documentation
cat A11Y_AUDIT_README.md
```

### Run Tests
```bash
# Verify everything is working
python test_a11y_audit.py
```

### View Sample Report
```bash
# See what a report looks like
open example-audit-report.html  # macOS
xdg-open example-audit-report.html  # Linux
start example-audit-report.html  # Windows
```

## 🎯 Quick Reference

| Command | Purpose |
|---------|---------|
| `python a11y_audit.py notebook.ipynb` | Basic audit |
| `python a11y_audit.py notebook.ipynb --output report.txt` | Save text report |
| `python a11y_audit.py notebook.ipynb --format html -o report.html` | HTML report |
| `python a11y_audit.py notebook.ipynb --remediate` | Auto-fix issues |
| `python a11y_audit.py notebook.ipynb --help` | Show all options |

## 🌟 Why Accessibility Matters

1. **Legal**: Many institutions must provide accessible content
2. **Ethical**: Everyone deserves equal access to information
3. **Practical**: Accessible design benefits all users
4. **Educational**: Makes learning materials available to all students

## 📖 Learn More

- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **WebAIM**: https://webaim.org/
- **Jupyter Accessibility**: https://jupyter-accessibility.readthedocs.io/

---

**Ready to make your notebooks accessible? Start now!**

```bash
python a11y_audit.py notebooks/your-notebook.ipynb
```
