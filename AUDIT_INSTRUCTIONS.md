# How to Create the GitHub Issue from This Audit

This directory contains a complete accessibility audit of all Jupyter notebooks in this repository.

## Files Created

1. **ACCESSIBILITY_AUDIT_REPORT.md** - Comprehensive audit report with 100 issues found
2. **accessibility_audit_results.json** - Raw audit data in JSON format for programmatic access

## Creating the GitHub Issue

### Option 1: Using GitHub CLI (Recommended)

```bash
gh issue create \
  --title "Accessibility Audit Report: 100 Issues Found in Jupyter Notebooks" \
  --body-file ACCESSIBILITY_AUDIT_REPORT.md \
  --label accessibility
```

### Option 2: Using GitHub Web Interface

1. Go to [Create New Issue](https://github.com/balajialg/datahub-usage-analysis/issues/new)
2. Title: `Accessibility Audit Report: 100 Issues Found in Jupyter Notebooks`
3. Copy the entire content from `ACCESSIBILITY_AUDIT_REPORT.md` into the issue body
4. Add label: `accessibility`
5. Click "Submit new issue"

### Option 3: Using GitHub API

```bash
gh api repos/balajialg/datahub-usage-analysis/issues \
  --method POST \
  --field title="Accessibility Audit Report: 100 Issues Found in Jupyter Notebooks" \
  --field body=@ACCESSIBILITY_AUDIT_REPORT.md \
  --field labels[]="accessibility"
```

## Audit Summary

- **Total notebooks audited:** 6
- **Notebooks with issues:** 3  
- **Total issues found:** 100
  - Missing Alt Text: 55 (55%)
  - Missing Chart Description: 28 (28%)
  - Color Dependence: 14 (14%)
  - Heading Structure: 3 (3%)

## Notebooks Affected

- ✅ `01-anonimize-hub-logs.ipynb` - No issues
- ✅ `02-get-cloud-costs.ipynb` - No issues
- ✅ `02_5-munge-data.ipynb` - No issues
- ⚠️ `03-visualize-cost-and-usage.ipynb` - 3 issues
- ⚠️ `logs_visualization_dashboard.ipynb` - 47 issues
- ⚠️ `nbgitpuller_processing_visualization.ipynb` - 50 issues

## Re-running the Audit

The audit script is available in `scripts/a11y_audit.py`. To re-run after making fixes:

```bash
# From repository root (auto-detects notebooks/ directory)
python3 scripts/a11y_audit.py

# Or specify a custom notebooks directory
python3 scripts/a11y_audit.py /path/to/notebooks
```

The script will output results to console and save detailed JSON results to `/tmp/a11y_audit_results.json`.
