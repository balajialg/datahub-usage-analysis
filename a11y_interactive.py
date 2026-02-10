#!/usr/bin/env python3
"""
Interactive Jupyter Notebook Accessibility Auditor
A user-friendly interface for accessibility auditing and remediation.
"""

import sys
import os
from pathlib import Path
import subprocess


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header():
    """Print the application header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  Jupyter Notebook Accessibility Auditor{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  WCAG 2.1/2.2 Compliance Tool{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")


def print_section(title):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'-' * len(title)}{Colors.END}")


def print_info(message):
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")


def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def find_notebooks(directory='.'):
    """Find all Jupyter notebooks in the given directory."""
    notebooks = list(Path(directory).glob('*.ipynb'))
    # Filter out checkpoint notebooks
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]
    return notebooks


def select_notebook():
    """Interactive notebook selection."""
    print_section("Select a Notebook")
    
    notebooks = find_notebooks()
    
    if not notebooks:
        print_error("No Jupyter notebooks found in the current directory.")
        return None
    
    print(f"\nFound {len(notebooks)} notebook(s):\n")
    for idx, nb in enumerate(notebooks, 1):
        size = nb.stat().st_size / 1024  # Size in KB
        print(f"  {idx}. {nb.name} ({size:.1f} KB)")
    
    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Enter notebook number (1-{len(notebooks)}) or 'q' to quit: {Colors.END}")
            if choice.lower() == 'q':
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(notebooks):
                return str(notebooks[idx])
            else:
                print_error(f"Please enter a number between 1 and {len(notebooks)}")
        except ValueError:
            print_error("Please enter a valid number")


def select_action():
    """Interactive action selection."""
    print_section("Select an Action")
    
    print("\nWhat would you like to do?\n")
    print("  1. Run Accessibility Audit (check for issues)")
    print("  2. Remediate Issues (automatically fix common problems)")
    print("  3. Full Service (audit + remediation in one step)")
    print("  4. View Accessibility Guidelines")
    print("  5. Quit")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Enter your choice (1-5): {Colors.END}")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print_error("Please enter a number between 1 and 5")


def select_report_format():
    """Select report format."""
    print("\nSelect report format:\n")
    print("  1. Markdown (recommended - formatted with emojis)")
    print("  2. Plain Text (simple terminal output)")
    print("  3. JSON (machine-readable)")
    
    formats = {'1': 'markdown', '2': 'text', '3': 'json'}
    
    while True:
        choice = input(f"\n{Colors.BOLD}Enter format choice (1-3): {Colors.END}")
        if choice in formats:
            return formats[choice]
        print_error("Please enter a number between 1 and 3")


def run_audit(notebook):
    """Run accessibility audit."""
    print_section("Running Accessibility Audit")
    
    report_format = select_report_format()
    
    # Determine file extension
    ext_map = {'markdown': '.md', 'text': '.txt', 'json': '.json'}
    ext = ext_map[report_format]
    
    notebook_name = Path(notebook).stem
    report_file = f"{notebook_name}_audit_report{ext}"
    
    print_info(f"Auditing: {notebook}")
    print_info(f"Report format: {report_format}")
    
    # Run the audit
    cmd = [sys.executable, 'a11y_audit.py', 'audit', notebook, 
           '--format', report_format, '--output', report_file]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Display summary from stderr/stdout
        if result.stdout:
            print("\n" + result.stdout)
        
        if result.returncode == 0:
            print_success(f"Audit completed! No critical issues found.")
        else:
            print_warning("Audit completed with critical issues found.")
        
        print_success(f"Report saved to: {report_file}")
        
        # Ask if user wants to view the report
        view = input(f"\n{Colors.BOLD}View the report now? (y/n): {Colors.END}")
        if view.lower() == 'y':
            if report_format == 'text':
                subprocess.run(['cat', report_file])
            elif report_format == 'markdown':
                # Try to use a markdown viewer if available
                if subprocess.run(['which', 'glow'], capture_output=True).returncode == 0:
                    subprocess.run(['glow', report_file])
                else:
                    subprocess.run(['cat', report_file])
            else:
                subprocess.run(['cat', report_file])
    
    except FileNotFoundError:
        print_error("Error: a11y_audit.py not found. Make sure it's in the current directory.")
    except Exception as e:
        print_error(f"Error running audit: {e}")


def run_remediation(notebook):
    """Run remediation on the notebook."""
    print_section("Remediating Accessibility Issues")
    
    notebook_name = Path(notebook).stem
    output_file = f"{notebook_name}_accessible.ipynb"
    
    # Check if output file already exists
    if Path(output_file).exists():
        overwrite = input(f"\n{Colors.YELLOW}{output_file} already exists. Overwrite? (y/n): {Colors.END}")
        if overwrite.lower() != 'y':
            output_file = input(f"{Colors.BOLD}Enter a different output filename: {Colors.END}")
    
    print_info(f"Remediating: {notebook}")
    print_info(f"Output will be saved to: {output_file}")
    
    # Run remediation
    cmd = [sys.executable, 'a11y_audit.py', 'remediate', notebook, '--output', output_file]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            print("\n" + result.stdout)
        
        if result.returncode == 0:
            print_success(f"Remediation completed!")
            print_success(f"Accessible notebook saved to: {output_file}")
            print_info("Note: Please review the changes and update placeholder text manually.")
        else:
            print_error("Remediation failed. Check the error messages above.")
    
    except FileNotFoundError:
        print_error("Error: a11y_audit.py not found. Make sure it's in the current directory.")
    except Exception as e:
        print_error(f"Error running remediation: {e}")


def run_full_service(notebook):
    """Run full audit and remediation."""
    print_section("Full Accessibility Service")
    
    notebook_name = Path(notebook).stem
    output_notebook = f"{notebook_name}_accessible.ipynb"
    report_file = f"{notebook_name}_audit_report.md"
    
    print_info(f"Processing: {notebook}")
    print_info("This will:")
    print("  1. Run a comprehensive accessibility audit")
    print("  2. Automatically fix common issues")
    print("  3. Generate a detailed report")
    
    confirm = input(f"\n{Colors.BOLD}Continue? (y/n): {Colors.END}")
    if confirm.lower() != 'y':
        print_info("Cancelled.")
        return
    
    # Run full service
    cmd = [sys.executable, 'a11y_audit.py', 'full', notebook,
           '--output-notebook', output_notebook,
           '--output-report', report_file,
           '--format', 'markdown']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            print("\n" + result.stdout)
        
        if result.returncode == 0:
            print_success("Full service completed!")
            print_success(f"Accessible notebook: {output_notebook}")
            print_success(f"Audit report: {report_file}")
            
            # Ask to view report
            view = input(f"\n{Colors.BOLD}View the audit report? (y/n): {Colors.END}")
            if view.lower() == 'y':
                subprocess.run(['cat', report_file])
        else:
            print_warning("Service completed with some issues.")
    
    except FileNotFoundError:
        print_error("Error: a11y_audit.py not found. Make sure it's in the current directory.")
    except Exception as e:
        print_error(f"Error running full service: {e}")


def show_guidelines():
    """Display accessibility guidelines."""
    print_section("Accessibility Guidelines")
    
    print(f"""
{Colors.BOLD}Key WCAG 2.1 Principles:{Colors.END}

1. {Colors.BOLD}Perceivable{Colors.END} - Information must be presentable to users
   • Add alt text to all images
   • Ensure color contrast ratios meet standards (4.5:1 for text)
   • Use proper semantic structure

2. {Colors.BOLD}Operable{Colors.END} - Interface must be operable by all users
   • Provide descriptive link text (not "click here")
   • Ensure keyboard navigation works
   • Use proper heading hierarchy

3. {Colors.BOLD}Understandable{Colors.END} - Content must be understandable
   • Use clear, simple language
   • Maintain consistent navigation
   • Add explanatory comments to code

4. {Colors.BOLD}Robust{Colors.END} - Content must work with assistive technologies
   • Use valid markup
   • Follow semantic HTML structure
   • Test with screen readers

{Colors.BOLD}Quick Tips:{Colors.END}

• {Colors.GREEN}Alt Text:{Colors.END} "Bar chart showing 45% increase" not just "chart"
• {Colors.GREEN}Headings:{Colors.END} Use H1 → H2 → H3 hierarchy, don't skip levels
• {Colors.GREEN}Links:{Colors.END} "[WCAG Guidelines](url)" not "[click here](url)"
• {Colors.GREEN}Tables:{Colors.END} Always include header rows
• {Colors.GREEN}Colors:{Colors.END} Don't rely on color alone to convey information

{Colors.BOLD}Resources:{Colors.END}

• WCAG Quick Reference: https://www.w3.org/WAI/WCAG21/quickref/
• WebAIM Alt Text Guide: https://webaim.org/techniques/alttext/
• Contrast Checker: https://webaim.org/resources/contrastchecker/
    """)


def main():
    """Main application loop."""
    print_header()
    
    print(f"{Colors.BOLD}Welcome!{Colors.END}")
    print("This tool helps ensure your Jupyter Notebooks are accessible to everyone,")
    print("including users of assistive technologies like screen readers.\n")
    
    print_info("Working directory: " + os.getcwd())
    
    while True:
        action = select_action()
        
        if action == '5':  # Quit
            print(f"\n{Colors.GREEN}Thank you for making your notebooks more accessible! 👋{Colors.END}\n")
            break
        
        if action == '4':  # Guidelines
            show_guidelines()
            continue
        
        # For other actions, we need a notebook
        notebook = select_notebook()
        if not notebook:
            continue
        
        if action == '1':  # Audit
            run_audit(notebook)
        elif action == '2':  # Remediate
            run_remediation(notebook)
        elif action == '3':  # Full service
            run_full_service(notebook)
        
        # Ask if user wants to continue
        print(f"\n{Colors.BOLD}{'=' * 80}{Colors.END}")
        continue_choice = input(f"\n{Colors.BOLD}Perform another action? (y/n): {Colors.END}")
        if continue_choice.lower() != 'y':
            print(f"\n{Colors.GREEN}Thank you for making your notebooks more accessible! 👋{Colors.END}\n")
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user. Goodbye!{Colors.END}\n")
        sys.exit(0)
