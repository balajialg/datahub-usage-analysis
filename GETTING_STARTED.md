# Getting Started with Jupyter Notebook Accessibility Auditing

## Quick Start Guide

This repository now includes a comprehensive accessibility auditing system for Jupyter Notebooks. Here's everything you need to know to get started.

## 🎯 What This Tool Does

The Accessibility Auditor helps ensure your Jupyter Notebooks meet **WCAG 2.1/2.2 Level AA** standards, making them accessible to all users, including those using assistive technologies like screen readers.

## 🚀 Two Ways to Use the Tool

### Option 1: Interactive Mode (Recommended for Beginners)

The easiest way to use the tool - a guided, menu-driven interface:

```bash
python3 a11y_interactive.py
```

This will:
1. Show you all notebooks in the current directory
2. Let you choose what action to perform (audit, fix, or both)
3. Guide you through each step with clear prompts
4. Display results and save reports automatically

### Option 2: Command-Line Mode (For Advanced Users)

Direct command-line access for automation and scripting:

```bash
# Quick audit
python3 a11y_audit.py audit Demo.ipynb

# Fix issues automatically
python3 a11y_audit.py remediate Demo.ipynb --output Demo_fixed.ipynb

# Do everything at once
python3 a11y_audit.py full Demo.ipynb
```

## 📋 Example Workflow

### For First-Time Users

1. **Run the interactive tool:**
   ```bash
   python3 a11y_interactive.py
   ```

2. **Select your notebook** from the list (e.g., `Demo.ipynb`)

3. **Choose "Full Service"** to get both audit and remediation

4. **Review the results:**
   - Check the generated audit report (`.md` file)
   - Open the fixed notebook (`_accessible.ipynb`)
   - Manually update placeholder text where needed

### For Regular Use

Once you're familiar with the tool, you can use the command-line:

```bash
# Audit only (see what needs fixing)
python3 a11y_audit.py audit Demo.ipynb --format markdown --output report.md

# Fix and create accessible version
python3 a11y_audit.py remediate Demo.ipynb --output Demo_accessible.ipynb
```

## 📊 Understanding Your Results

### Audit Report Structure

The audit report is organized by severity:

- **🔴 Critical Issues** - Must fix (WCAG Level A failures)
  - Missing alt text on images
  - Broken accessibility features

- **⚠️ Warnings** - Should fix (WCAG Level AA recommendations)
  - Missing headings
  - Poor link text
  - Heading hierarchy issues

- **✅ Successful Checks** - Already accessible
  - Proper alt text
  - Good link descriptions
  - Proper structure

### Example Critical Issue

```markdown
### 1. Missing Alt Text

- **Cell:** 2
- **Description:** Image missing alt text: attachment:image.jpg
- **WCAG Standard:** WCAG 2.1 Level A - 1.1.1 Non-text Content
- **Remediation:** Add descriptive alt text for the image
```

## 🔧 What Gets Fixed Automatically

The remediation tool automatically handles:

1. **Missing Alt Text**
   - Adds placeholder: `![Descriptive image - please update](...)`
   - You should replace with actual description

2. **Missing Document Title**
   - Adds H1 heading: `# Notebook Title`
   - You should customize this

3. **Bare URLs**
   - Wraps in markdown: `[Link to URL](URL)`
   - You should improve the link text

## ✏️ Manual Fixes Required

Some issues need your expertise:

### 1. Writing Good Alt Text

**What the tool adds:**
```markdown
![Descriptive image - please update alt text](chart.png)
```

**What you should change it to:**
```markdown
![Bar chart showing 45% increase in student enrollment from 2020 to 2024](chart.png)
```

**Tips:**
- Be specific and concise
- Describe the important information
- Keep it under 125 characters when possible
- Don't start with "Image of..." (screen readers say this)

### 2. Improving Link Text

**What the tool creates:**
```markdown
[Link to https://example.com](https://example.com)
```

**What you should change it to:**
```markdown
[WCAG 2.1 Accessibility Guidelines](https://example.com)
```

### 3. Adding Missing Headings

If cells have substantial content but no heading, consider adding one:

```markdown
## Data Analysis Results

Here are the findings from our analysis...
```

## 📁 File Organization

After running the tool, you'll have:

```
your-repo/
├── Demo.ipynb                      # Original notebook
├── Demo_audit_report.md            # Accessibility audit report
├── Demo_accessible.ipynb           # Fixed version (auto-generated)
├── a11y_audit.py                   # Command-line tool
├── a11y_interactive.py             # Interactive interface
└── A11Y_AUDIT_README.md           # Full documentation
```

**Note:** The `*_audit_report.*` and `*_accessible.ipynb` files are automatically excluded from git (via `.gitignore`) as they are generated outputs.

## 🎓 Learning Resources

### Quick Reference

**Good Alt Text Examples:**
- ✅ `![Line graph showing temperature increase over 10 years](temp.png)`
- ✅ `![UC Berkeley logo](logo.png)`
- ✅ `![Photo of students studying in library](students.jpg)`
- ❌ `![](image.png)` - No alt text
- ❌ `![image](chart.png)` - Not descriptive

**Good Link Text Examples:**
- ✅ `[Download 2024 Annual Report (PDF)](report.pdf)`
- ✅ `[Read WCAG 2.1 Guidelines](wcag-url)`
- ❌ `[Click here](url)` - Not descriptive
- ❌ `https://example.com` - Bare URL

### WCAG Standards Reference

This tool checks for compliance with:
- **Level A** (minimum): Essential accessibility features
- **Level AA** (recommended): Enhanced accessibility
- **Level AAA** (optimal): Highest level of accessibility

### External Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Alt Text Guide](https://webaim.org/techniques/alttext/)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Jupyter Accessibility](https://jupyter-accessibility.readthedocs.io/)

## 🆘 Troubleshooting

### "Command not found" Error

If you get an error running the scripts:

```bash
# Make sure Python 3 is installed
python3 --version

# Make scripts executable
chmod +x a11y_audit.py a11y_interactive.py

# Run with python3 explicitly
python3 a11y_audit.py audit Demo.ipynb
```

### "No module named..." Error

If Python can't find required modules, they should be built-in. Make sure you're using Python 3.6+:

```bash
python3 --version  # Should be 3.6 or higher
```

### Tool Reports False Positives

Some decorative images may intentionally have empty alt text. Review each issue and:
- Keep empty alt for purely decorative images: `![](decorative.png)`
- Add descriptive alt for informative images

### Need More Help?

1. Check the full documentation: `A11Y_AUDIT_README.md`
2. Run the interactive tool and select "View Accessibility Guidelines"
3. Review the generated audit report for specific guidance

## 🔄 Workflow Integration

### Before Committing Notebooks

```bash
# Check accessibility before committing
python3 a11y_audit.py audit *.ipynb
```

### Pre-commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Check notebook accessibility before commit
python3 a11y_audit.py audit *.ipynb
if [ $? -ne 0 ]; then
    echo "⚠️  Accessibility issues found. Please fix before committing."
    exit 1
fi
```

## ✅ Best Practices Checklist

Before publishing your notebook, ensure:

- [ ] All images have descriptive alt text
- [ ] Notebook starts with an H1 heading
- [ ] Headings follow proper hierarchy (H1 → H2 → H3)
- [ ] Links have descriptive text (not "click here")
- [ ] Tables have header rows
- [ ] Colors have sufficient contrast (check with external tool)
- [ ] Code has explanatory comments
- [ ] Ran accessibility audit with 0 critical issues

## 🎉 Next Steps

1. **Run your first audit:**
   ```bash
   python3 a11y_interactive.py
   ```

2. **Review the report** and understand the issues

3. **Let the tool fix** what it can automatically

4. **Manually improve** placeholder text and descriptions

5. **Run another audit** to verify fixes

6. **Share your accessible notebook!**

## 💡 Remember

Making notebooks accessible benefits everyone:
- Users with disabilities can access your content
- Content is more searchable and indexable
- Documentation is clearer and better organized
- Your work reaches a wider audience

**Thank you for making the web more accessible!** 🌐✨

---

For detailed documentation, see: `A11Y_AUDIT_README.md`
