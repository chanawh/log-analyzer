import json
import argparse
import os
from jinja2 import Environment, FileSystemLoader

def generate_report(data, template_path, output_path):
    """
    Generate an HTML report from log data using a Jinja2 template.
    
    Args:
        data (list): List of log entries.
        template_path (str): File path to the Jinja2 HTML template.
        output_path (str): File path for the output HTML report.
    """
    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    report = template.render(logs=data)
    with open(output_path, 'w') as f:
        f.write(report)
    print(f"Report generated at {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate an HTML report from parsed log data."
    )
    parser.add_argument("--input", required=True, help="Input JSON file with parsed logs")
    parser.add_argument("--template", required=True, help="Path to the Jinja2 HTML template")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = json.load(f)
    
    generate_report(data, args.template, args.output)

if __name__ == '__main__':
    main()
