#!/usr/bin/env python
"""
Test script for the Jupyter Notebook Accessibility Audit Tool

This script runs comprehensive tests on the a11y audit tool to verify
all functionality is working correctly.
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from a11y_audit import AccessibilityAuditor, AccessibilityRemediator


def create_test_notebook(issues_to_include):
    """Create a test notebook with specific accessibility issues."""
    cells = []
    
    # Add title or not based on test case
    if 'no_title' not in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['# Test Notebook\n']
        })
    
    # Add image issues
    if 'missing_alt' in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['![](test.png)\n']
        })
    
    if 'empty_alt' in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['<img src="test.png" alt="">\n']
        })
    
    if 'good_alt' in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['![A descriptive image](test.png)\n']
        })
    
    # Add table issues
    if 'table_no_header' in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['| Name | Score |\n', '| Alice | 95 |\n']
        })
    
    if 'table_good' in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['| Name | Score |\n', '|------|-------|\n', '| Alice | 95 |\n']
        })
    
    # Add heading hierarchy issues
    if 'heading_skip' in issues_to_include:
        cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['## Section\n', '#### Subsection\n']
        })
    
    return {
        'cells': cells,
        'metadata': {},
        'nbformat': 4,
        'nbformat_minor': 4
    }


def test_basic_audit():
    """Test basic auditing functionality."""
    print("Testing basic audit...")
    
    # Create test notebook with issues
    notebook_data = create_test_notebook(['missing_alt', 'no_title'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
        json.dump(notebook_data, f)
        temp_path = f.name
    
    try:
        auditor = AccessibilityAuditor(temp_path)
        issues = auditor.audit()
        
        # Verify we found the issues
        assert len(issues['critical']) >= 1, "Should find missing alt text"
        assert len(issues['warning']) >= 1, "Should find missing title"
        
        print("✓ Basic audit test passed")
        return True
    finally:
        os.unlink(temp_path)


def test_report_generation():
    """Test report generation in different formats."""
    print("Testing report generation...")
    
    notebook_data = create_test_notebook(['good_alt', 'table_good'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
        json.dump(notebook_data, f)
        temp_path = f.name
    
    try:
        auditor = AccessibilityAuditor(temp_path)
        auditor.audit()
        
        # Test text report
        text_report = auditor.generate_report('text')
        assert 'JUPYTER NOTEBOOK ACCESSIBILITY AUDIT REPORT' in text_report
        assert 'SUMMARY' in text_report
        
        # Test JSON report
        json_report = auditor.generate_report('json')
        report_data = json.loads(json_report)
        assert 'critical' in report_data
        assert 'warning' in report_data
        assert 'success' in report_data
        
        # Test HTML report
        html_report = auditor.generate_report('html')
        assert '<!DOCTYPE html>' in html_report
        assert 'Accessibility Audit Report' in html_report
        
        print("✓ Report generation test passed")
        return True
    finally:
        os.unlink(temp_path)


def test_remediation():
    """Test automatic remediation functionality."""
    print("Testing remediation...")
    
    notebook_data = create_test_notebook(['missing_alt', 'no_title', 'table_no_header'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
        json.dump(notebook_data, f)
        temp_path = f.name
    
    try:
        remediator = AccessibilityRemediator(temp_path)
        changes = remediator.remediate(auto_fix=True)
        
        # Verify changes were made
        assert len(changes['changes']) > 0, "Should make changes"
        
        # Save remediated version
        output_path = temp_path.replace('.ipynb', '_fixed.ipynb')
        remediator.save_remediated(output_path)
        
        # Audit the fixed version
        auditor = AccessibilityAuditor(output_path)
        issues = auditor.audit()
        
        # Should have fewer critical issues
        assert len(issues['critical']) == 0, "Fixed notebook should have no critical issues"
        
        os.unlink(output_path)
        print("✓ Remediation test passed")
        return True
    finally:
        os.unlink(temp_path)


def test_image_detection():
    """Test detection of various image formats."""
    print("Testing image detection...")
    
    notebook_data = create_test_notebook(['missing_alt', 'empty_alt', 'good_alt'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
        json.dump(notebook_data, f)
        temp_path = f.name
    
    try:
        auditor = AccessibilityAuditor(temp_path)
        issues = auditor.audit()
        
        # Should find both types of image issues
        critical_types = [issue['type'] for issue in issues['critical']]
        assert 'MISSING_ALT_TEXT' in critical_types or 'EMPTY_ALT_TEXT' in critical_types
        
        # Should also find the good image
        success_types = [issue['type'] for issue in issues['success']]
        assert 'IMAGE_ALT_TEXT' in success_types
        
        print("✓ Image detection test passed")
        return True
    finally:
        os.unlink(temp_path)


def test_table_detection():
    """Test detection of table accessibility issues."""
    print("Testing table detection...")
    
    notebook_data = create_test_notebook(['table_no_header', 'table_good'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
        json.dump(notebook_data, f)
        temp_path = f.name
    
    try:
        auditor = AccessibilityAuditor(temp_path)
        issues = auditor.audit()
        
        # Should find table without header
        warning_types = [issue['type'] for issue in issues['warning']]
        assert 'TABLE_NO_HEADER' in warning_types
        
        # Should find table with header
        success_types = [issue['type'] for issue in issues['success']]
        assert 'TABLE_HEADER' in success_types
        
        print("✓ Table detection test passed")
        return True
    finally:
        os.unlink(temp_path)


def test_heading_hierarchy():
    """Test heading hierarchy validation."""
    print("Testing heading hierarchy...")
    
    notebook_data = create_test_notebook(['heading_skip'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
        json.dump(notebook_data, f)
        temp_path = f.name
    
    try:
        auditor = AccessibilityAuditor(temp_path)
        issues = auditor.audit()
        
        # Should find heading hierarchy issue
        warning_types = [issue['type'] for issue in issues['warning']]
        assert 'HEADING_HIERARCHY' in warning_types
        
        print("✓ Heading hierarchy test passed")
        return True
    finally:
        os.unlink(temp_path)


def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*60)
    print("Running Accessibility Audit Tool Tests")
    print("="*60 + "\n")
    
    tests = [
        test_basic_audit,
        test_report_generation,
        test_remediation,
        test_image_detection,
        test_table_detection,
        test_heading_hierarchy,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
