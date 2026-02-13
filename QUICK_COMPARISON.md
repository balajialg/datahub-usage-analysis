# Quick Comparison: Accessibility Audit Tools

## Side-by-Side Feature Comparison

| Feature | JupyterLab-a11y-checker | Custom a11y Tool |
|---------|------------------------|------------------|
| **Installation** | `pip install` or `npx` | No installation |
| **Dependencies** | Node.js, Python | Python only |
| **File Size** | ~MB (full package) | ~35KB (single file) |
| **Language** | TypeScript/JavaScript | Python |
| **Lines of Code** | ~thousands (monorepo) | ~850 (single file) |
| **Real-time Checking** | ✅ Yes (Extension) | ❌ No |
| **CLI Tool** | ✅ Yes | ✅ Yes |
| **JupyterLab Extension** | ✅ Yes | ❌ No |
| **Axe-core Integration** | ✅ Yes | ❌ No |
| **AI/LLM Integration** | ✅ Yes (VLM/LLM) | ❌ No |
| **Detection Engine** | Axe + Custom Rules | Regex + Pattern Matching |
| **Standards** | WCAG 2.1 AA | WCAG 2.1/2.2 |

## Detection Coverage

| Issue Type | JupyterLab-a11y-checker | Custom a11y Tool |
|------------|------------------------|------------------|
| **Images** |
| Missing alt text | ✅ | ✅ |
| AI-generated alt text | ✅ | ⚠️ Placeholder |
| **Headings** |
| Missing H1 | ✅ | ✅ |
| Multiple H1s | ✅ | ❌ |
| Duplicate headings | ✅ | ❌ |
| Wrong order | ✅ | ✅ |
| Empty headings | ✅ | ❌ |
| **Tables** |
| Missing headers | ✅ | ✅ |
| Missing captions | ✅ | ❌ |
| Missing scope | ✅ | ⚠️ Detection |
| **Color** |
| Contrast ratio (images) | ✅ | ❌ |
| Color-only info | ❌ | ✅ |
| **Links** |
| Non-descriptive text | ✅ | ❌ |
| **Code** |
| Consecutive cells | ❌ | ✅ |

## Report Formats

| Format | JupyterLab-a11y-checker | Custom a11y Tool |
|--------|------------------------|------------------|
| Terminal/Console | ✅ | ✅ |
| JSON | ✅ (LLM-optimized) | ✅ |
| HTML | ❌ | ✅ |
| Real-time UI | ✅ (Extension) | ❌ |
| Severity Categories | No | ✅ Critical/Warning/Success |

## Remediation

| Capability | JupyterLab-a11y-checker | Custom a11y Tool |
|------------|------------------------|------------------|
| Automatic fixes | ✅ Interactive UI | ✅ CLI |
| AI-powered fixes | ✅ VLM/LLM | ❌ |
| Batch processing | ✅ | ✅ |
| Preview changes | ✅ | ❌ |
| One-click fixes | ✅ | ❌ |

## Integration

| Environment | JupyterLab-a11y-checker | Custom a11y Tool |
|-------------|------------------------|------------------|
| GitHub Actions | ✅ Pre-built | ⚠️ Manual |
| Local development | ✅ Extension | ✅ CLI |
| CI/CD pipelines | ✅ | ✅ |
| Offline/airgapped | ⚠️ Needs npm | ✅ |
| Docker containers | ✅ | ✅ |

## Use Case Fit

### Best for JupyterLab-a11y-checker
- ✅ Active JupyterLab development
- ✅ Need real-time feedback
- ✅ Want AI-powered features
- ✅ Comprehensive checks needed
- ✅ Team/organizational use

### Best for Custom a11y Tool
- ✅ Simple standalone audits
- ✅ Minimal dependencies
- ✅ Need customization
- ✅ Batch processing
- ✅ HTML reports for stakeholders
- ✅ Resource-constrained environments

## Quick Decision Tree

```
Do you work primarily in JupyterLab?
├─ Yes → JupyterLab-a11y-checker (Extension + CLI)
└─ No
   └─ Do you have Node.js available?
      ├─ Yes → JupyterLab-a11y-checker (CLI)
      └─ No → Custom a11y Tool

Do you need AI-generated alt text?
├─ Yes → JupyterLab-a11y-checker
└─ No → Either tool works

Do you need zero dependencies?
├─ Yes → Custom a11y Tool
└─ No → JupyterLab-a11y-checker

Do you need HTML reports?
├─ Yes → Custom a11y Tool
└─ No → Either tool works

Do you need real-time checking?
├─ Yes → JupyterLab-a11y-checker (Extension)
└─ No → Either tool works
```

## Performance Characteristics

| Metric | JupyterLab-a11y-checker | Custom a11y Tool |
|--------|------------------------|------------------|
| Startup time | Moderate (Node.js) | Fast (Python) |
| Memory usage | Higher (axe-core) | Lower (regex) |
| Analysis speed | Thorough (DOM) | Fast (pattern) |
| Accuracy | High (axe-core) | Good (patterns) |
| False positives | Low | Moderate |

## Maintenance & Support

| Aspect | JupyterLab-a11y-checker | Custom a11y Tool |
|--------|------------------------|------------------|
| Organization | Berkeley DSEP | Individual |
| Updates | Regular | As needed |
| Community | Growing | Small |
| Documentation | Comprehensive | Comprehensive |
| Research-backed | ✅ Yes | Partial |
| Issue tracking | GitHub | GitHub |

## Cost & Licensing

| Item | JupyterLab-a11y-checker | Custom a11y Tool |
|------|------------------------|------------------|
| License | Open Source | Open Source |
| Cost | Free | Free |
| API costs | Varies (LLM/VLM) | None |
| Infrastructure | Requires Node.js | Python only |

---

## Summary

**JupyterLab-a11y-checker**: Professional, feature-rich, ideal for teams actively developing in JupyterLab. Requires more infrastructure but provides comprehensive checking and AI-powered features.

**Custom a11y Tool**: Lightweight, portable, perfect for quick audits and batch processing. Zero dependencies make it ideal for constrained environments. Easier to customize and understand.

**Both are valuable** - choose based on your specific needs!

---

For detailed comparison, see [COMPARISON.md](COMPARISON.md)
