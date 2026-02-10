#!/usr/bin/env python3
"""
Accessibility audit script for Jupyter notebooks.
Checks for common accessibility issues in notebook content.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

class NotebookA11yAuditor:
    def __init__(self, notebook_path):
        self.notebook_path = Path(notebook_path)
        self.notebook_name = self.notebook_path.name
        self.issues = defaultdict(list)
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
    
    def audit(self):
        """Run all accessibility checks"""
        self.check_heading_structure()
        self.check_images_alt_text()
        self.check_color_usage()
        self.check_tables()
        self.check_chart_descriptions()
        return self.issues
    
    def check_heading_structure(self):
        """Check markdown heading hierarchy"""
        headings = []
        for cell in self.notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                # Find all markdown headings
                for line in source.split('\n'):
                    match = re.match(r'^(#{1,6})\s+(.+)$', line)
                    if match:
                        level = len(match.group(1))
                        text = match.group(2)
                        headings.append((level, text))
        
        # Check for proper hierarchy
        if headings:
            prev_level = 0
            for i, (level, text) in enumerate(headings):
                if i == 0 and level > 1:
                    self.issues['heading_structure'].append(
                        f"First heading starts at level {level} instead of level 1: '{text}'"
                    )
                elif level > prev_level + 1:
                    self.issues['heading_structure'].append(
                        f"Heading level jumps from {prev_level} to {level}: '{text}'"
                    )
                prev_level = level
    
    def check_images_alt_text(self):
        """Check for images without alt text"""
        for i, cell in enumerate(self.notebook.get('cells', [])):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                # Check for markdown images
                md_images = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', source)
                for alt_text, img_path in md_images:
                    if not alt_text or alt_text.strip() == '':
                        self.issues['missing_alt_text'].append(
                            f"Cell {i+1}: Image '{img_path}' has no alt text"
                        )
                
                # Check for HTML images
                html_images = re.findall(r'<img[^>]*>', source, re.IGNORECASE)
                for img_tag in html_images:
                    if 'alt=' not in img_tag.lower():
                        self.issues['missing_alt_text'].append(
                            f"Cell {i+1}: HTML image has no alt attribute: {img_tag[:50]}..."
                        )
            
            # Check for output images (matplotlib, etc.)
            if cell.get('cell_type') == 'code':
                outputs = cell.get('outputs', [])
                for output in outputs:
                    if output.get('output_type') == 'display_data':
                        data = output.get('data', {})
                        if 'image/png' in data or 'image/jpeg' in data:
                            self.issues['missing_alt_text'].append(
                                f"Cell {i+1}: Chart/image output has no alt text or description"
                            )
    
    def check_color_usage(self):
        """Check for color-only information conveyance"""
        for i, cell in enumerate(self.notebook.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                
                # Check for matplotlib color usage
                if 'plt.' in source or 'matplotlib' in source:
                    # Check for pie charts (especially problematic)
                    if re.search(r'\.pie\s*\(', source):
                        self.issues['color_dependence'].append(
                            f"Cell {i+1}: Pie chart detected - may rely on color alone"
                        )
                    
                    # Check for custom colors without labels
                    if re.search(r'color\s*=', source) and not re.search(r'label\s*=', source):
                        self.issues['color_dependence'].append(
                            f"Cell {i+1}: Color used in plot - ensure not relying solely on color"
                        )
                
                # Check for Altair charts
                if 'alt.Chart' in source or 'import altair' in source:
                    if 'color=' in source or 'Color(' in source:
                        # Check if description is provided
                        if '.properties(title=' not in source and 'description=' not in source:
                            self.issues['color_dependence'].append(
                                f"Cell {i+1}: Altair chart uses color - consider adding description"
                            )
    
    def check_tables(self):
        """Check for accessible table structure"""
        for i, cell in enumerate(self.notebook.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                
                # Check for DataFrame display
                if 'DataFrame' in source or 'pd.DataFrame' in source:
                    # Check outputs for HTML tables
                    outputs = cell.get('outputs', [])
                    for output in outputs:
                        if output.get('output_type') == 'execute_result':
                            data = output.get('data', {})
                            if 'text/html' in data:
                                html = ''.join(data['text/html'])
                                if '<table' in html.lower():
                                    # Check for proper table headers
                                    if '<th' not in html.lower():
                                        self.issues['table_accessibility'].append(
                                            f"Cell {i+1}: DataFrame table may lack proper headers"
                                        )
    
    def check_chart_descriptions(self):
        """Check for chart descriptions and context"""
        for i, cell in enumerate(self.notebook.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                
                # Look for chart creation without nearby markdown explanation
                has_chart = (
                    'plt.figure' in source or 
                    'plt.plot' in source or 
                    'plt.bar' in source or
                    'alt.Chart' in source or
                    '.plot(' in source
                )
                
                if has_chart:
                    # Check if previous or next cell has markdown
                    has_description = False
                    
                    # Check previous cell
                    if i > 0 and self.notebook['cells'][i-1].get('cell_type') == 'markdown':
                        prev_source = ''.join(self.notebook['cells'][i-1].get('source', []))
                        if len(prev_source.strip()) > 20:  # Has substantial text
                            has_description = True
                    
                    # Check next cell
                    if i < len(self.notebook['cells']) - 1:
                        if self.notebook['cells'][i+1].get('cell_type') == 'markdown':
                            next_source = ''.join(self.notebook['cells'][i+1].get('source', []))
                            if len(next_source.strip()) > 20:
                                has_description = True
                    
                    if not has_description:
                        self.issues['missing_chart_description'].append(
                            f"Cell {i+1}: Chart without nearby textual description"
                        )

def main():
    notebooks_dir = Path('/home/runner/work/datahub-usage-analysis/datahub-usage-analysis/notebooks')
    all_issues = {}
    
    print("=" * 80)
    print("JUPYTER NOTEBOOK ACCESSIBILITY AUDIT")
    print("=" * 80)
    print()
    
    for notebook_path in sorted(notebooks_dir.glob('*.ipynb')):
        print(f"\nAuditing: {notebook_path.name}")
        print("-" * 80)
        
        auditor = NotebookA11yAuditor(notebook_path)
        issues = auditor.audit()
        
        if any(issues.values()):
            all_issues[notebook_path.name] = dict(issues)
            
            for category, issue_list in issues.items():
                if issue_list:
                    print(f"\n{category.replace('_', ' ').title()}:")
                    for issue in issue_list:
                        print(f"  - {issue}")
        else:
            print("  No accessibility issues detected")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_notebooks = len(list(notebooks_dir.glob('*.ipynb')))
    notebooks_with_issues = len(all_issues)
    
    print(f"\nTotal notebooks audited: {total_notebooks}")
    print(f"Notebooks with accessibility issues: {notebooks_with_issues}")
    
    # Count issues by category
    category_counts = defaultdict(int)
    for notebook_issues in all_issues.values():
        for category, issue_list in notebook_issues.items():
            category_counts[category] += len(issue_list)
    
    print("\nIssues by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  - {category.replace('_', ' ').title()}: {count}")
    
    # Save results to JSON
    output_path = Path('/tmp/a11y_audit_results.json')
    with open(output_path, 'w') as f:
        json.dump(all_issues, f, indent=2)
    print(f"\nDetailed results saved to: {output_path}")

if __name__ == '__main__':
    main()
