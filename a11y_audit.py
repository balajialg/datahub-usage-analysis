"""
Jupyter Notebook Accessibility (a11y) Audit Tool

This module provides comprehensive accessibility auditing for Jupyter Notebooks
following WCAG 2.1/2.2 standards.
"""

import json
import re
from typing import Dict, List, Tuple, Any
from collections import defaultdict
from pathlib import Path


class AccessibilityAuditor:
    """Main class for auditing Jupyter Notebooks for accessibility issues."""
    
    # WCAG 2.1 AA contrast ratios
    MIN_CONTRAST_NORMAL = 4.5
    MIN_CONTRAST_LARGE = 3.0
    
    def __init__(self, notebook_path: str):
        """
        Initialize the auditor with a notebook file.
        
        Args:
            notebook_path: Path to the .ipynb file to audit
        """
        self.notebook_path = Path(notebook_path)
        self.notebook_data = None
        self.issues = {
            'critical': [],
            'warning': [],
            'success': []
        }
        
    def load_notebook(self) -> bool:
        """
        Load the Jupyter notebook file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.notebook_data = json.load(f)
            return True
        except Exception as e:
            self.issues['critical'].append({
                'type': 'FILE_ERROR',
                'message': f'Failed to load notebook: {str(e)}',
                'location': str(self.notebook_path)
            })
            return False
    
    def audit(self) -> Dict[str, List[Dict]]:
        """
        Run a complete accessibility audit on the notebook.
        
        Returns:
            Dictionary containing categorized issues
        """
        if not self.load_notebook():
            return self.issues
        
        # Run all audit checks
        self._check_images()
        self._check_headings()
        self._check_tables()
        self._check_code_cells()
        self._check_markdown_structure()
        self._check_color_references()
        
        return self.issues
    
    def _check_images(self):
        """Check for images missing alt text."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        image_patterns = [
            r'!\[(.*?)\]\(.*?\)',  # Markdown image syntax
            r'<img\s+[^>]*src=["\'].*?["\'][^>]*>',  # HTML img tag
        ]
        
        cells = self.notebook_data.get('cells', [])
        images_found = 0
        images_with_alt = 0
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check Markdown images
                markdown_images = re.findall(image_patterns[0], source)
                for alt_text in markdown_images:
                    images_found += 1
                    if alt_text.strip():
                        images_with_alt += 1
                        self.issues['success'].append({
                            'type': 'IMAGE_ALT_TEXT',
                            'message': f'Image has alt text: "{alt_text}"',
                            'location': f'Cell {idx + 1}'
                        })
                    else:
                        self.issues['critical'].append({
                            'type': 'MISSING_ALT_TEXT',
                            'message': 'Image is missing alt text description',
                            'location': f'Cell {idx + 1}',
                            'wcag': 'WCAG 2.1 Level A - 1.1.1 Non-text Content',
                            'remediation': 'Add descriptive alt text in square brackets: ![description](image.png)'
                        })
                
                # Check HTML images
                html_images = re.findall(image_patterns[1], source)
                for img_tag in html_images:
                    images_found += 1
                    if 'alt=' in img_tag:
                        alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag)
                        if alt_match and alt_match.group(1).strip():
                            images_with_alt += 1
                            self.issues['success'].append({
                                'type': 'IMAGE_ALT_TEXT',
                                'message': f'HTML image has alt text: "{alt_match.group(1)}"',
                                'location': f'Cell {idx + 1}'
                            })
                        else:
                            self.issues['critical'].append({
                                'type': 'EMPTY_ALT_TEXT',
                                'message': 'HTML image has empty alt attribute',
                                'location': f'Cell {idx + 1}',
                                'wcag': 'WCAG 2.1 Level A - 1.1.1 Non-text Content',
                                'remediation': 'Add descriptive text to alt attribute: <img src="..." alt="description">'
                            })
                    else:
                        self.issues['critical'].append({
                            'type': 'MISSING_ALT_ATTRIBUTE',
                            'message': 'HTML image is missing alt attribute',
                            'location': f'Cell {idx + 1}',
                            'wcag': 'WCAG 2.1 Level A - 1.1.1 Non-text Content',
                            'remediation': 'Add alt attribute to img tag: <img src="..." alt="description">'
                        })
        
        if images_found == 0:
            self.issues['success'].append({
                'type': 'NO_IMAGES',
                'message': 'No images found in notebook',
                'location': 'Global'
            })
    
    def _check_headings(self):
        """Check for proper heading structure and hierarchy."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        heading_levels = []
        has_h1 = False
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check for headings
                heading_matches = re.finditer(r'^(#{1,6})\s+(.+)$', source, re.MULTILINE)
                for match in heading_matches:
                    level = len(match.group(1))
                    heading_text = match.group(2).strip()
                    heading_levels.append((level, idx + 1, heading_text))
                    
                    if level == 1:
                        has_h1 = True
        
        # Check if notebook has a title (H1)
        if not has_h1:
            self.issues['warning'].append({
                'type': 'MISSING_TITLE',
                'message': 'Notebook is missing a main title (H1 heading)',
                'location': 'Global',
                'wcag': 'WCAG 2.1 Level A - 2.4.2 Page Titled',
                'remediation': 'Add a # Main Title at the beginning of the notebook'
            })
        else:
            self.issues['success'].append({
                'type': 'HAS_TITLE',
                'message': 'Notebook has a main title',
                'location': 'Global'
            })
        
        # Check heading hierarchy
        prev_level = 0
        for level, cell_num, text in heading_levels:
            if prev_level > 0 and level > prev_level + 1:
                self.issues['warning'].append({
                    'type': 'HEADING_HIERARCHY',
                    'message': f'Heading level skipped (jumped from H{prev_level} to H{level})',
                    'location': f'Cell {cell_num}',
                    'wcag': 'WCAG 2.1 Level AA - 1.3.1 Info and Relationships',
                    'remediation': 'Use sequential heading levels (H1, H2, H3...)'
                })
            prev_level = level
    
    def _check_tables(self):
        """Check table structures for accessibility."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Check for Markdown tables
                if '|' in source:
                    lines = source.split('\n')
                    table_lines = [l for l in lines if l.strip().startswith('|')]
                    
                    if table_lines:
                        # Check if table has header separator
                        has_header = any('---' in line or '===' in line for line in table_lines)
                        
                        if has_header:
                            self.issues['success'].append({
                                'type': 'TABLE_HEADER',
                                'message': 'Table has proper header row',
                                'location': f'Cell {idx + 1}'
                            })
                        else:
                            self.issues['warning'].append({
                                'type': 'TABLE_NO_HEADER',
                                'message': 'Table may be missing header row',
                                'location': f'Cell {idx + 1}',
                                'wcag': 'WCAG 2.1 Level A - 1.3.1 Info and Relationships',
                                'remediation': 'Add header separator line with |---|---| format'
                            })
                
                # Check for HTML tables
                html_tables = re.findall(r'<table[^>]*>.*?</table>', source, re.DOTALL | re.IGNORECASE)
                for table in html_tables:
                    if '<th' in table.lower():
                        self.issues['success'].append({
                            'type': 'HTML_TABLE_HEADER',
                            'message': 'HTML table has header cells (th)',
                            'location': f'Cell {idx + 1}'
                        })
                    else:
                        self.issues['warning'].append({
                            'type': 'HTML_TABLE_NO_HEADER',
                            'message': 'HTML table is missing header cells (th)',
                            'location': f'Cell {idx + 1}',
                            'wcag': 'WCAG 2.1 Level A - 1.3.1 Info and Relationships',
                            'remediation': 'Use <th> tags for header cells instead of <td>'
                        })
                    
                    if 'scope=' not in table.lower():
                        self.issues['warning'].append({
                            'type': 'TABLE_SCOPE',
                            'message': 'HTML table headers missing scope attribute',
                            'location': f'Cell {idx + 1}',
                            'wcag': 'WCAG 2.1 Level A - 1.3.1 Info and Relationships',
                            'remediation': 'Add scope="col" or scope="row" to <th> elements'
                        })
    
    def _check_code_cells(self):
        """Check code cells for accessibility features."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        
        if code_cells:
            self.issues['success'].append({
                'type': 'CODE_CELLS',
                'message': f'Found {len(code_cells)} code cells',
                'location': 'Global',
                'note': 'Code cells are generally accessible if properly labeled'
            })
        
        # Check for code cells without preceding context
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'code' and idx > 0:
                prev_cell = cells[idx - 1]
                if prev_cell.get('cell_type') == 'code':
                    # Multiple code cells in a row without markdown explanation
                    self.issues['warning'].append({
                        'type': 'CODE_CONTEXT',
                        'message': 'Multiple code cells without markdown explanation',
                        'location': f'Cells {idx} and {idx + 1}',
                        'wcag': 'WCAG 2.1 Level AAA - 3.1.5 Reading Level',
                        'remediation': 'Add markdown cell explaining what the code does'
                    })
    
    def _check_markdown_structure(self):
        """Check overall markdown structure and semantic meaning."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        markdown_cells = [c for c in cells if c.get('cell_type') == 'markdown']
        
        if not markdown_cells:
            self.issues['warning'].append({
                'type': 'NO_MARKDOWN',
                'message': 'Notebook has no markdown cells for context',
                'location': 'Global',
                'wcag': 'WCAG 2.1 Level A - 2.4.2 Page Titled',
                'remediation': 'Add markdown cells to explain the notebook purpose and code'
            })
        else:
            self.issues['success'].append({
                'type': 'HAS_MARKDOWN',
                'message': f'Notebook has {len(markdown_cells)} markdown cells for context',
                'location': 'Global'
            })
    
    def _check_color_references(self):
        """Check for color-only information conveyance."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        color_keywords = ['red', 'green', 'blue', 'yellow', 'color', 'colored']
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', [])).lower()
                
                for keyword in color_keywords:
                    if keyword in source:
                        # Check if color is used to convey meaning
                        if 'see the ' + keyword in source or 'shown in ' + keyword in source:
                            self.issues['warning'].append({
                                'type': 'COLOR_ONLY',
                                'message': f'Content may rely on color perception ("{keyword}")',
                                'location': f'Cell {idx + 1}',
                                'wcag': 'WCAG 2.1 Level A - 1.4.1 Use of Color',
                                'remediation': 'Provide additional indicators beyond color (patterns, labels, text)'
                            })
                            break
    
    def generate_report(self, output_format: str = 'text') -> str:
        """
        Generate a formatted accessibility report.
        
        Args:
            output_format: Format for the report ('text', 'json', 'html')
            
        Returns:
            Formatted report as string
        """
        if output_format == 'json':
            return json.dumps(self.issues, indent=2)
        
        elif output_format == 'html':
            return self._generate_html_report()
        
        else:  # text format
            return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """Generate a text-based accessibility report."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("JUPYTER NOTEBOOK ACCESSIBILITY AUDIT REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Notebook: {self.notebook_path.name}")
        report_lines.append("")
        
        # Summary
        critical_count = len(self.issues['critical'])
        warning_count = len(self.issues['warning'])
        success_count = len(self.issues['success'])
        
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Critical Issues: {critical_count}")
        report_lines.append(f"Warnings: {warning_count}")
        report_lines.append(f"Successful Checks: {success_count}")
        report_lines.append("")
        
        # Critical issues
        if critical_count > 0:
            report_lines.append("CRITICAL ISSUES (Must Fix)")
            report_lines.append("-" * 80)
            for i, issue in enumerate(self.issues['critical'], 1):
                report_lines.append(f"{i}. {issue['type']}")
                report_lines.append(f"   Location: {issue['location']}")
                report_lines.append(f"   Message: {issue['message']}")
                if 'wcag' in issue:
                    report_lines.append(f"   WCAG: {issue['wcag']}")
                if 'remediation' in issue:
                    report_lines.append(f"   How to Fix: {issue['remediation']}")
                report_lines.append("")
        
        # Warnings
        if warning_count > 0:
            report_lines.append("WARNINGS (Should Fix)")
            report_lines.append("-" * 80)
            for i, issue in enumerate(self.issues['warning'], 1):
                report_lines.append(f"{i}. {issue['type']}")
                report_lines.append(f"   Location: {issue['location']}")
                report_lines.append(f"   Message: {issue['message']}")
                if 'wcag' in issue:
                    report_lines.append(f"   WCAG: {issue['wcag']}")
                if 'remediation' in issue:
                    report_lines.append(f"   How to Fix: {issue['remediation']}")
                report_lines.append("")
        
        # Successes
        if success_count > 0:
            report_lines.append("SUCCESSFUL CHECKS")
            report_lines.append("-" * 80)
            for i, issue in enumerate(self.issues['success'], 1):
                report_lines.append(f"{i}. {issue['type']}: {issue['message']} ({issue['location']})")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def _generate_html_report(self) -> str:
        """Generate an HTML-based accessibility report."""
        critical_count = len(self.issues['critical'])
        warning_count = len(self.issues['warning'])
        success_count = len(self.issues['success'])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Audit Report - {self.notebook_path.name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}
        .stat {{
            flex: 1;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }}
        .critical {{ background-color: #fee; border-left: 4px solid #d00; }}
        .warning {{ background-color: #ffe; border-left: 4px solid #f90; }}
        .success {{ background-color: #efe; border-left: 4px solid #0a0; }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .issue {{
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #ccc;
            background: #fafafa;
        }}
        .issue-critical {{ border-left-color: #d00; }}
        .issue-warning {{ border-left-color: #f90; }}
        .issue-success {{ border-left-color: #0a0; }}
        .issue-type {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        .issue-location {{
            color: #666;
            font-size: 0.9em;
        }}
        .issue-wcag {{
            color: #0066cc;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .issue-remediation {{
            background: #fff;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <h1>Jupyter Notebook Accessibility Audit Report</h1>
    <div class="summary">
        <h2>Notebook: {self.notebook_path.name}</h2>
        <div class="summary-stats">
            <div class="stat critical">
                <div class="stat-number">{critical_count}</div>
                <div>Critical Issues</div>
            </div>
            <div class="stat warning">
                <div class="stat-number">{warning_count}</div>
                <div>Warnings</div>
            </div>
            <div class="stat success">
                <div class="stat-number">{success_count}</div>
                <div>Successful Checks</div>
            </div>
        </div>
    </div>
"""
        
        # Critical issues
        if critical_count > 0:
            html += '<div class="section"><h2>Critical Issues (Must Fix)</h2>\n'
            for issue in self.issues['critical']:
                html += f'<div class="issue issue-critical">\n'
                html += f'<div class="issue-type">{issue["type"]}</div>\n'
                html += f'<div class="issue-location">Location: {issue["location"]}</div>\n'
                html += f'<div>{issue["message"]}</div>\n'
                if 'wcag' in issue:
                    html += f'<div class="issue-wcag">WCAG: {issue["wcag"]}</div>\n'
                if 'remediation' in issue:
                    html += f'<div class="issue-remediation"><strong>How to Fix:</strong> {issue["remediation"]}</div>\n'
                html += '</div>\n'
            html += '</div>\n'
        
        # Warnings
        if warning_count > 0:
            html += '<div class="section"><h2>Warnings (Should Fix)</h2>\n'
            for issue in self.issues['warning']:
                html += f'<div class="issue issue-warning">\n'
                html += f'<div class="issue-type">{issue["type"]}</div>\n'
                html += f'<div class="issue-location">Location: {issue["location"]}</div>\n'
                html += f'<div>{issue["message"]}</div>\n'
                if 'wcag' in issue:
                    html += f'<div class="issue-wcag">WCAG: {issue["wcag"]}</div>\n'
                if 'remediation' in issue:
                    html += f'<div class="issue-remediation"><strong>How to Fix:</strong> {issue["remediation"]}</div>\n'
                html += '</div>\n'
            html += '</div>\n'
        
        # Successes
        if success_count > 0:
            html += '<div class="section"><h2>Successful Checks</h2>\n'
            for issue in self.issues['success']:
                html += f'<div class="issue issue-success">\n'
                html += f'<div class="issue-type">{issue["type"]}</div>\n'
                html += f'<div>{issue["message"]} ({issue["location"]})</div>\n'
                html += '</div>\n'
            html += '</div>\n'
        
        html += """
</body>
</html>
"""
        return html
    
    def save_report(self, output_path: str, output_format: str = 'text'):
        """
        Save the accessibility report to a file.
        
        Args:
            output_path: Path to save the report
            output_format: Format for the report ('text', 'json', 'html')
        """
        report = self.generate_report(output_format)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)


class AccessibilityRemediator:
    """Class for automatically fixing accessibility issues in Jupyter Notebooks."""
    
    def __init__(self, notebook_path: str):
        """
        Initialize the remediator with a notebook file.
        
        Args:
            notebook_path: Path to the .ipynb file to remediate
        """
        self.notebook_path = Path(notebook_path)
        self.notebook_data = None
        self.changes_made = []
        
    def load_notebook(self) -> bool:
        """Load the Jupyter notebook file."""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.notebook_data = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading notebook: {e}")
            return False
    
    def remediate(self, auto_fix: bool = True) -> Dict[str, List[str]]:
        """
        Perform automatic remediation of accessibility issues.
        
        Args:
            auto_fix: Whether to automatically fix issues (vs. just identify them)
            
        Returns:
            Dictionary of changes made
        """
        if not self.load_notebook():
            return {'errors': ['Failed to load notebook']}
        
        if auto_fix:
            self._fix_missing_alt_text()
            self._fix_missing_title()
            self._add_table_headers()
        
        return {'changes': self.changes_made}
    
    def _fix_missing_alt_text(self):
        """Add placeholder alt text to images missing it."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                if isinstance(source, str):
                    source = [source]
                
                new_source = []
                modified = False
                
                for line in source:
                    # Fix markdown images with empty alt text
                    if '![](' in line:
                        line = re.sub(r'!\[\]\(([^)]+)\)', r'![Image description needed](\1)', line)
                        modified = True
                        self.changes_made.append(f'Added placeholder alt text to image in cell {idx + 1}')
                    
                    # Fix HTML images without alt attribute
                    if '<img' in line and 'alt=' not in line:
                        line = re.sub(r'(<img[^>]*)(>)', r'\1 alt="Image description needed"\2', line)
                        modified = True
                        self.changes_made.append(f'Added alt attribute to HTML image in cell {idx + 1}')
                    
                    # Fix HTML images with empty alt
                    new_line = re.sub(r'alt=["\']["\']', 'alt="Image description needed"', line)
                    if new_line != line:
                        modified = True
                        line = new_line
                    
                    new_source.append(line)
                
                if modified:
                    cell['source'] = new_source
    
    def _fix_missing_title(self):
        """Add a title to the notebook if missing."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        
        # Check if first cell is a markdown cell with H1
        has_title = False
        if cells and cells[0].get('cell_type') == 'markdown':
            source = ''.join(cells[0].get('source', []))
            if re.match(r'^#\s+', source):
                has_title = True
        
        if not has_title:
            # Add a title cell at the beginning
            title_cell = {
                'cell_type': 'markdown',
                'metadata': {},
                'source': [f'# {self.notebook_path.stem}\n', '\n', 'Notebook description goes here.\n']
            }
            cells.insert(0, title_cell)
            self.notebook_data['cells'] = cells
            self.changes_made.append('Added main title (H1) to notebook')
    
    def _add_table_headers(self):
        """Ensure tables have proper header rows."""
        if not self.notebook_data or 'cells' not in self.notebook_data:
            return
        
        cells = self.notebook_data.get('cells', [])
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                if isinstance(source, str):
                    source = [source]
                
                new_source = []
                modified = False
                in_table = False
                has_separator = False
                
                for i, line in enumerate(source):
                    if '|' in line and line.strip().startswith('|'):
                        if not in_table:
                            in_table = True
                            has_separator = False
                        
                        # Check if this is a separator line
                        if '---' in line or '===' in line:
                            has_separator = True
                        
                        new_source.append(line)
                        
                        # If this is the first row and next line is not separator, add one
                        if in_table and not has_separator and i + 1 < len(source):
                            next_line = source[i + 1]
                            if '|' not in next_line or ('---' not in next_line and '===' not in next_line):
                                # Count columns - handle both `| col |` and `col |` formats
                                cols = line.count('|')
                                # If table has leading and trailing pipes (standard format)
                                if line.strip().startswith('|') and line.strip().endswith('|'):
                                    cols = cols - 1  # subtract 1 for leading pipe
                                # Ensure we have at least 1 column
                                if cols > 0:
                                    separator = '| ' + ' | '.join(['---'] * cols) + ' |\n'
                                    new_source.append(separator)
                                    modified = True
                                    self.changes_made.append(f'Added header separator to table in cell {idx + 1}')
                                    has_separator = True
                    else:
                        in_table = False
                        new_source.append(line)
                
                if modified:
                    cell['source'] = new_source
    
    def save_remediated(self, output_path: str = None):
        """
        Save the remediated notebook to a file.
        
        Args:
            output_path: Path to save the remediated notebook.
                        If None, saves to original filename with '_accessible' suffix.
        """
        if output_path is None:
            output_path = self.notebook_path.parent / f"{self.notebook_path.stem}_accessible.ipynb"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.notebook_data, f, indent=1, ensure_ascii=False)
        
        return output_path


def main():
    """Main CLI interface for the accessibility audit tool."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Jupyter Notebook Accessibility (a11y) Audit Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit a notebook and display report
  python a11y_audit.py notebook.ipynb
  
  # Audit and save report to file
  python a11y_audit.py notebook.ipynb --output report.txt
  
  # Generate HTML report
  python a11y_audit.py notebook.ipynb --format html --output report.html
  
  # Audit and remediate
  python a11y_audit.py notebook.ipynb --remediate
  
  # Remediate and save to specific file
  python a11y_audit.py notebook.ipynb --remediate --remediated-output fixed.ipynb
        """
    )
    
    parser.add_argument('notebook', help='Path to Jupyter notebook (.ipynb) file')
    parser.add_argument('--output', '-o', help='Path to save the audit report')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'html'], 
                        default='text', help='Report format (default: text)')
    parser.add_argument('--remediate', '-r', action='store_true',
                        help='Automatically fix accessibility issues')
    parser.add_argument('--remediated-output', help='Path to save remediated notebook')
    
    args = parser.parse_args()
    
    # Run audit
    print(f"Auditing notebook: {args.notebook}")
    auditor = AccessibilityAuditor(args.notebook)
    issues = auditor.audit()
    
    # Generate and display/save report
    if args.output:
        auditor.save_report(args.output, args.format)
        print(f"Report saved to: {args.output}")
    else:
        report = auditor.generate_report(args.format)
        print(report)
    
    # Remediation
    if args.remediate:
        print("\nPerforming automatic remediation...")
        remediator = AccessibilityRemediator(args.notebook)
        changes = remediator.remediate(auto_fix=True)
        
        if changes.get('changes'):
            print("\nChanges made:")
            for change in changes['changes']:
                print(f"  - {change}")
            
            output_path = remediator.save_remediated(args.remediated_output)
            print(f"\nRemediated notebook saved to: {output_path}")
        else:
            print("No changes needed or possible.")
    
    # Summary
    critical = len(issues['critical'])
    warnings = len(issues['warning'])
    
    print(f"\n{'='*60}")
    print(f"Audit Summary: {critical} critical issues, {warnings} warnings")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
