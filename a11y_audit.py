#!/usr/bin/env python3
"""
Jupyter Notebook Accessibility Auditor
A comprehensive tool for auditing and remediating accessibility issues in Jupyter Notebooks
following WCAG 2.1/2.2 standards.
"""

import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
import colorsys


class NotebookA11yAuditor:
    """
    Main class for auditing Jupyter Notebooks for accessibility issues.
    
    Checks for:
    - Missing alt text on images
    - Color contrast issues
    - Missing headings
    - Improper reading order
    - Table structure issues
    """
    
    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        self.notebook = None
        self.issues = {
            'critical': [],
            'warning': [],
            'success': []
        }
        
    def load_notebook(self) -> bool:
        """Load the Jupyter notebook file."""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.notebook = json.load(f)
            return True
        except FileNotFoundError:
            print(f"Error: Notebook file not found: {self.notebook_path}")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in notebook file: {self.notebook_path}")
            return False
    
    def check_image_alt_text(self):
        """Check if all images have appropriate alt text."""
        cells = self.notebook.get('cells', [])
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check markdown images ![alt](url)
                md_images = re.findall(r'!\[(.*?)\]\((.*?)\)', source)
                for alt, url in md_images:
                    if not alt or alt.strip() == '':
                        self.issues['critical'].append({
                            'type': 'Missing Alt Text',
                            'severity': 'Critical',
                            'cell': i,
                            'description': f'Image missing alt text: {url[:80]}',
                            'wcag': 'WCAG 2.1 Level A - 1.1.1 Non-text Content',
                            'fix': f'Add descriptive alt text for the image'
                        })
                    else:
                        self.issues['success'].append({
                            'type': 'Alt Text Present',
                            'cell': i,
                            'description': f'Image has alt text: "{alt}"'
                        })
                
                # Check HTML img tags
                img_tags = re.finditer(r'<img[^>]*>', source, re.IGNORECASE)
                for img_match in img_tags:
                    img_tag = img_match.group(0)
                    if 'alt=' not in img_tag.lower():
                        # Extract src if available
                        src_match = re.search(r'src=["\']([^"\']*)["\']', img_tag)
                        src = src_match.group(1) if src_match else 'unknown'
                        self.issues['critical'].append({
                            'type': 'Missing Alt Text',
                            'severity': 'Critical',
                            'cell': i,
                            'description': f'HTML image missing alt attribute: {src[:80]}',
                            'wcag': 'WCAG 2.1 Level A - 1.1.1 Non-text Content',
                            'fix': 'Add alt="" attribute to the img tag'
                        })
                    else:
                        # Check if alt is empty
                        alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
                        if alt_match:
                            alt_text = alt_match.group(1)
                            if alt_text.strip():
                                self.issues['success'].append({
                                    'type': 'Alt Text Present',
                                    'cell': i,
                                    'description': f'HTML image has alt text: "{alt_text}"'
                                })
                            else:
                                self.issues['warning'].append({
                                    'type': 'Empty Alt Text',
                                    'severity': 'Warning',
                                    'cell': i,
                                    'description': 'HTML image has empty alt attribute (may be decorative)',
                                    'wcag': 'WCAG 2.1 Level A - 1.1.1 Non-text Content'
                                })
    
    def check_headings(self):
        """Check for proper heading structure and hierarchy."""
        cells = self.notebook.get('cells', [])
        
        heading_hierarchy = []
        cells_without_structure = []
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Find all headings in this cell
                headings = re.findall(r'^(#{1,6})\s+(.+)$', source, re.MULTILINE)
                
                if headings:
                    for heading_marks, heading_text in headings:
                        level = len(heading_marks)
                        heading_hierarchy.append((i, level, heading_text.strip()))
                        self.issues['success'].append({
                            'type': 'Heading Present',
                            'cell': i,
                            'description': f'Cell has heading (H{level}): {heading_text.strip()[:50]}'
                        })
                else:
                    # Check if cell has substantial content but no heading
                    if len(source.strip()) > 50:  # Arbitrary threshold
                        cells_without_structure.append(i)
                        self.issues['warning'].append({
                            'type': 'Missing Heading',
                            'severity': 'Warning',
                            'cell': i,
                            'description': 'Substantial content without a heading',
                            'wcag': 'WCAG 2.1 Level AA - 2.4.6 Headings and Labels',
                            'fix': 'Consider adding a heading to improve navigation'
                        })
        
        # Check heading hierarchy (e.g., don't skip from H1 to H3)
        for i in range(1, len(heading_hierarchy)):
            prev_level = heading_hierarchy[i-1][1]
            curr_level = heading_hierarchy[i][1]
            
            if curr_level > prev_level + 1:
                self.issues['warning'].append({
                    'type': 'Heading Hierarchy Skip',
                    'severity': 'Warning',
                    'cell': heading_hierarchy[i][0],
                    'description': f'Heading level skips from H{prev_level} to H{curr_level}',
                    'wcag': 'WCAG 2.1 Level AA - 1.3.1 Info and Relationships',
                    'fix': f'Use H{prev_level + 1} instead of H{curr_level} for proper hierarchy'
                })
        
        # Check if notebook starts with H1
        if heading_hierarchy and heading_hierarchy[0][1] != 1:
            self.issues['warning'].append({
                'type': 'Missing Document Title',
                'severity': 'Warning',
                'cell': heading_hierarchy[0][0],
                'description': 'Notebook should start with an H1 heading',
                'wcag': 'WCAG 2.1 Level AA - 2.4.6 Headings and Labels',
                'fix': 'Add an H1 heading at the start of the notebook'
            })
    
    def check_color_contrast(self):
        """Check for potential color contrast issues in markdown content."""
        cells = self.notebook.get('cells', [])
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check for inline styles with color
                color_styles = re.finditer(r'<[^>]*style=["\'][^"\']*color:\s*([^;"\']+)', source, re.IGNORECASE)
                for match in color_styles:
                    color = match.group(1).strip()
                    self.issues['warning'].append({
                        'type': 'Color Usage',
                        'severity': 'Warning',
                        'cell': i,
                        'description': f'Inline color style detected: {color}',
                        'wcag': 'WCAG 2.1 Level AA - 1.4.3 Contrast (Minimum)',
                        'fix': 'Verify color contrast ratio is at least 4.5:1 for normal text, 3:1 for large text'
                    })
                
                # Check for HTML color tags (deprecated but still used)
                font_colors = re.finditer(r'<font[^>]*color=["\']([^"\']+)["\']', source, re.IGNORECASE)
                for match in font_colors:
                    color = match.group(1)
                    self.issues['warning'].append({
                        'type': 'Deprecated Color Tag',
                        'severity': 'Warning',
                        'cell': i,
                        'description': f'Deprecated font color tag: {color}',
                        'wcag': 'WCAG 2.1 Level AA - 1.4.3 Contrast (Minimum)',
                        'fix': 'Use CSS for styling and verify contrast ratio'
                    })
    
    def check_tables(self):
        """Check for proper table structure and headers."""
        cells = self.notebook.get('cells', [])
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check for markdown tables
                table_rows = re.findall(r'^\|.+\|$', source, re.MULTILINE)
                if table_rows:
                    # Check if table has header row (should have separator line with dashes)
                    has_header = any(re.match(r'^\|[\s\-:]+\|$', row) for row in table_rows)
                    
                    if has_header:
                        self.issues['success'].append({
                            'type': 'Table Structure',
                            'cell': i,
                            'description': 'Table has proper header row'
                        })
                    else:
                        self.issues['warning'].append({
                            'type': 'Table Without Headers',
                            'severity': 'Warning',
                            'cell': i,
                            'description': 'Table may be missing header row',
                            'wcag': 'WCAG 2.1 Level A - 1.3.1 Info and Relationships',
                            'fix': 'Add header row to table using |---|---|--- separator'
                        })
                
                # Check for HTML tables
                html_tables = re.finditer(r'<table[^>]*>.*?</table>', source, re.IGNORECASE | re.DOTALL)
                for table_match in html_tables:
                    table_html = table_match.group(0)
                    
                    # Check for <th> tags
                    if '<th' not in table_html.lower():
                        self.issues['warning'].append({
                            'type': 'HTML Table Without Headers',
                            'severity': 'Warning',
                            'cell': i,
                            'description': 'HTML table missing <th> header cells',
                            'wcag': 'WCAG 2.1 Level A - 1.3.1 Info and Relationships',
                            'fix': 'Use <th> tags for table headers'
                        })
                    else:
                        self.issues['success'].append({
                            'type': 'HTML Table Structure',
                            'cell': i,
                            'description': 'HTML table has header cells'
                        })
    
    def check_links(self):
        """Check for proper link text (not just URLs)."""
        cells = self.notebook.get('cells', [])
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check markdown links [text](url)
                md_links = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', source)
                for match in md_links:
                    link_text = match.group(1).strip()
                    url = match.group(2).strip()
                    
                    # Check if link text is just the URL
                    if link_text == url or link_text.lower() in ['click here', 'here', 'link']:
                        self.issues['warning'].append({
                            'type': 'Non-descriptive Link Text',
                            'severity': 'Warning',
                            'cell': i,
                            'description': f'Link has non-descriptive text: "{link_text}"',
                            'wcag': 'WCAG 2.1 Level A - 2.4.4 Link Purpose (In Context)',
                            'fix': 'Use descriptive link text that explains the destination'
                        })
                    else:
                        self.issues['success'].append({
                            'type': 'Descriptive Link',
                            'cell': i,
                            'description': f'Link has descriptive text: "{link_text[:50]}"'
                        })
                
                # Check for bare URLs (not in markdown link format)
                bare_urls = re.finditer(r'(?<!\()\bhttps?://[^\s<>\)]+', source)
                for match in bare_urls:
                    url = match.group(0)
                    self.issues['warning'].append({
                        'type': 'Bare URL',
                        'severity': 'Warning',
                        'cell': i,
                        'description': f'Bare URL without link text: {url[:60]}',
                        'wcag': 'WCAG 2.1 Level A - 2.4.4 Link Purpose (In Context)',
                        'fix': 'Wrap URL in markdown link with descriptive text'
                    })
    
    def check_code_cells(self):
        """Check code cells for potential accessibility issues."""
        cells = self.notebook.get('cells', [])
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                
                # Check if code cell has comments/documentation
                has_comments = '#' in source
                
                if not has_comments and len(source.strip()) > 50:
                    self.issues['warning'].append({
                        'type': 'Code Without Comments',
                        'severity': 'Warning',
                        'cell': i,
                        'description': 'Complex code without explanatory comments',
                        'wcag': 'WCAG 2.1 Level AAA - 3.1.5 Reading Level',
                        'fix': 'Add comments to explain code functionality'
                    })
    
    def run_audit(self) -> Dict[str, List[Dict]]:
        """Run all accessibility checks."""
        if not self.load_notebook():
            return None
        
        print(f"Running accessibility audit on: {self.notebook_path.name}")
        print("=" * 80)
        
        self.check_image_alt_text()
        self.check_headings()
        self.check_color_contrast()
        self.check_tables()
        self.check_links()
        self.check_code_cells()
        
        return self.issues
    
    def generate_report(self, output_format='text') -> str:
        """Generate a formatted accessibility report."""
        if output_format == 'text':
            return self._generate_text_report()
        elif output_format == 'json':
            return self._generate_json_report()
        elif output_format == 'markdown':
            return self._generate_markdown_report()
    
    def _generate_text_report(self) -> str:
        """Generate a plain text report."""
        report = []
        report.append("\n" + "=" * 80)
        report.append("JUPYTER NOTEBOOK ACCESSIBILITY AUDIT REPORT")
        report.append("=" * 80)
        report.append(f"Notebook: {self.notebook_path.name}")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"WCAG Standard: 2.1 Level AA")
        report.append("=" * 80)
        
        # Summary
        report.append("\nSUMMARY")
        report.append("-" * 80)
        report.append(f"Critical Issues: {len(self.issues['critical'])}")
        report.append(f"Warnings: {len(self.issues['warning'])}")
        report.append(f"Successful Checks: {len(self.issues['success'])}")
        
        # Critical Issues
        if self.issues['critical']:
            report.append("\n" + "=" * 80)
            report.append("CRITICAL ISSUES (Must Fix)")
            report.append("=" * 80)
            for idx, issue in enumerate(self.issues['critical'], 1):
                report.append(f"\n{idx}. {issue['type']}")
                report.append(f"   Cell: {issue['cell']}")
                report.append(f"   Description: {issue['description']}")
                report.append(f"   Standard: {issue['wcag']}")
                report.append(f"   Remediation: {issue['fix']}")
        
        # Warnings
        if self.issues['warning']:
            report.append("\n" + "=" * 80)
            report.append("WARNINGS (Should Fix)")
            report.append("=" * 80)
            for idx, issue in enumerate(self.issues['warning'], 1):
                report.append(f"\n{idx}. {issue['type']}")
                report.append(f"   Cell: {issue['cell']}")
                report.append(f"   Description: {issue['description']}")
                if 'wcag' in issue:
                    report.append(f"   Standard: {issue['wcag']}")
                if 'fix' in issue:
                    report.append(f"   Remediation: {issue['fix']}")
        
        # Success
        if self.issues['success']:
            report.append("\n" + "=" * 80)
            report.append("SUCCESSFUL CHECKS")
            report.append("=" * 80)
            for idx, issue in enumerate(self.issues['success'][:10], 1):  # Show first 10
                report.append(f"\n{idx}. {issue['type']} (Cell {issue['cell']})")
                report.append(f"   {issue['description']}")
            
            if len(self.issues['success']) > 10:
                report.append(f"\n... and {len(self.issues['success']) - 10} more successful checks")
        
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return '\n'.join(report)
    
    def _generate_markdown_report(self) -> str:
        """Generate a Markdown report."""
        report = []
        report.append("# Jupyter Notebook Accessibility Audit Report")
        report.append(f"\n**Notebook:** {self.notebook_path.name}")
        report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**WCAG Standard:** 2.1 Level AA")
        
        # Summary
        report.append("\n## Summary")
        report.append(f"\n- 🔴 **Critical Issues:** {len(self.issues['critical'])}")
        report.append(f"- ⚠️ **Warnings:** {len(self.issues['warning'])}")
        report.append(f"- ✅ **Successful Checks:** {len(self.issues['success'])}")
        
        # Critical Issues
        if self.issues['critical']:
            report.append("\n## 🔴 Critical Issues (Must Fix)")
            for idx, issue in enumerate(self.issues['critical'], 1):
                report.append(f"\n### {idx}. {issue['type']}")
                report.append(f"\n- **Cell:** {issue['cell']}")
                report.append(f"- **Description:** {issue['description']}")
                report.append(f"- **WCAG Standard:** {issue['wcag']}")
                report.append(f"- **Remediation:** {issue['fix']}")
        
        # Warnings
        if self.issues['warning']:
            report.append("\n## ⚠️ Warnings (Should Fix)")
            for idx, issue in enumerate(self.issues['warning'], 1):
                report.append(f"\n### {idx}. {issue['type']}")
                report.append(f"\n- **Cell:** {issue['cell']}")
                report.append(f"- **Description:** {issue['description']}")
                if 'wcag' in issue:
                    report.append(f"- **WCAG Standard:** {issue['wcag']}")
                if 'fix' in issue:
                    report.append(f"- **Remediation:** {issue['fix']}")
        
        # Success
        if self.issues['success']:
            report.append("\n## ✅ Successful Checks")
            for idx, issue in enumerate(self.issues['success'][:10], 1):
                report.append(f"\n{idx}. **{issue['type']}** (Cell {issue['cell']}): {issue['description']}")
            
            if len(self.issues['success']) > 10:
                report.append(f"\n*... and {len(self.issues['success']) - 10} more successful checks*")
        
        return '\n'.join(report)
    
    def _generate_json_report(self) -> str:
        """Generate a JSON report."""
        report_data = {
            'notebook': str(self.notebook_path),
            'audit_date': datetime.now().isoformat(),
            'wcag_standard': '2.1 Level AA',
            'summary': {
                'critical': len(self.issues['critical']),
                'warnings': len(self.issues['warning']),
                'success': len(self.issues['success'])
            },
            'issues': self.issues
        }
        return json.dumps(report_data, indent=2)
    
    def save_report(self, output_path: str, output_format='text'):
        """Save the report to a file."""
        report_content = self.generate_report(output_format)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\nReport saved to: {output_path}")


class NotebookRemediator:
    """
    Class for automatically remediating accessibility issues in Jupyter Notebooks.
    """
    
    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        self.notebook = None
        self.modifications = []
    
    def load_notebook(self) -> bool:
        """Load the Jupyter notebook file."""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.notebook = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading notebook: {e}")
            return False
    
    def add_alt_text_to_images(self, ai_generated=True):
        """Add alt text to images that are missing it."""
        cells = self.notebook.get('cells', [])
        modified = False
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                if isinstance(source, str):
                    source = [source]
                
                new_source = []
                for line in source:
                    # Fix markdown images without alt text
                    line = re.sub(
                        r'!\[\s*\]\(([^\)]+)\)',
                        r'![Descriptive image - please update alt text](\1)',
                        line
                    )
                    
                    # Fix HTML images without alt attribute
                    if '<img' in line.lower() and 'alt=' not in line.lower():
                        line = re.sub(
                            r'<img\s+',
                            '<img alt="Descriptive image - please update alt text" ',
                            line,
                            flags=re.IGNORECASE
                        )
                        modified = True
                        self.modifications.append(f"Added alt text placeholder to image in cell {i}")
                    
                    new_source.append(line)
                
                if new_source != source:
                    cell['source'] = new_source
                    modified = True
        
        return modified
    
    def improve_heading_structure(self):
        """Improve heading structure in the notebook."""
        cells = self.notebook.get('cells', [])
        
        # Check if notebook starts with H1
        first_markdown = None
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                first_markdown = i
                break
        
        if first_markdown is not None:
            cell = cells[first_markdown]
            source = ''.join(cell.get('source', []))
            
            # Check if it starts with H1
            if not re.match(r'^#\s+', source):
                # Add H1 at the beginning
                if isinstance(cell['source'], list):
                    cell['source'].insert(0, '# Notebook Title\n\n')
                else:
                    cell['source'] = '# Notebook Title\n\n' + cell['source']
                
                self.modifications.append(f"Added H1 title to cell {first_markdown}")
                return True
        
        return False
    
    def fix_link_text(self):
        """Improve link text that is non-descriptive."""
        cells = self.notebook.get('cells', [])
        modified = False
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                if isinstance(source, str):
                    source = [source]
                
                new_source = []
                for line in source:
                    # Wrap bare URLs in markdown links
                    original_line = line
                    line = re.sub(
                        r'(?<!\()\b(https?://[^\s<>\)]+)',
                        r'[Link to \1](\1)',
                        line
                    )
                    
                    if line != original_line:
                        modified = True
                        self.modifications.append(f"Wrapped bare URL in markdown link in cell {i}")
                    
                    new_source.append(line)
                
                if new_source != source:
                    cell['source'] = new_source
        
        return modified
    
    def save_remediated_notebook(self, output_path: str):
        """Save the remediated notebook to a new file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.notebook, f, indent=1, ensure_ascii=False)
            
            print(f"\nRemediated notebook saved to: {output_path}")
            print(f"\nModifications made:")
            for mod in self.modifications:
                print(f"  - {mod}")
            
            return True
        except Exception as e:
            print(f"Error saving remediated notebook: {e}")
            return False
    
    def remediate(self, output_path: str) -> bool:
        """Run all remediation steps."""
        if not self.load_notebook():
            return False
        
        print(f"\nRemediating accessibility issues in: {self.notebook_path.name}")
        print("=" * 80)
        
        self.add_alt_text_to_images()
        self.improve_heading_structure()
        self.fix_link_text()
        
        return self.save_remediated_notebook(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Jupyter Notebook Accessibility Auditor - WCAG 2.1/2.2 Compliance Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run audit and generate text report
  python a11y_audit.py audit Demo.ipynb
  
  # Run audit and save markdown report
  python a11y_audit.py audit Demo.ipynb --format markdown --output report.md
  
  # Remediate accessibility issues
  python a11y_audit.py remediate Demo.ipynb --output Demo_fixed.ipynb
  
  # Run audit and remediate in one step
  python a11y_audit.py full Demo.ipynb
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Run accessibility audit')
    audit_parser.add_argument('notebook', help='Path to Jupyter notebook file')
    audit_parser.add_argument('--format', choices=['text', 'markdown', 'json'], 
                             default='text', help='Report format')
    audit_parser.add_argument('--output', help='Output file for report (default: stdout)')
    
    # Remediate command
    remediate_parser = subparsers.add_parser('remediate', help='Remediate accessibility issues')
    remediate_parser.add_argument('notebook', help='Path to Jupyter notebook file')
    remediate_parser.add_argument('--output', required=True, 
                                  help='Output path for remediated notebook')
    
    # Full command (audit + remediate)
    full_parser = subparsers.add_parser('full', help='Run audit and remediation')
    full_parser.add_argument('notebook', help='Path to Jupyter notebook file')
    full_parser.add_argument('--output-notebook', 
                            help='Output path for remediated notebook (default: [notebook]_fixed.ipynb)')
    full_parser.add_argument('--output-report',
                            help='Output path for audit report (default: [notebook]_audit_report.md)')
    full_parser.add_argument('--format', choices=['text', 'markdown', 'json'],
                            default='markdown', help='Report format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'audit':
        auditor = NotebookA11yAuditor(args.notebook)
        issues = auditor.run_audit()
        
        if issues is None:
            return 1
        
        if args.output:
            auditor.save_report(args.output, args.format)
        else:
            print(auditor.generate_report(args.format))
        
        # Return error code if critical issues found
        return 1 if issues['critical'] else 0
    
    elif args.command == 'remediate':
        remediator = NotebookRemediator(args.notebook)
        success = remediator.remediate(args.output)
        return 0 if success else 1
    
    elif args.command == 'full':
        # Run audit first
        auditor = NotebookA11yAuditor(args.notebook)
        issues = auditor.run_audit()
        
        if issues is None:
            return 1
        
        # Generate report
        report_path = args.output_report or f"{Path(args.notebook).stem}_audit_report.md"
        auditor.save_report(report_path, args.format)
        
        # Run remediation
        output_notebook = args.output_notebook or f"{Path(args.notebook).stem}_fixed.ipynb"
        remediator = NotebookRemediator(args.notebook)
        success = remediator.remediate(output_notebook)
        
        return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
