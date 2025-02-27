import json
from analyzer import report_generator

def test_generate_report(tmp_path):
    # Sample log data
    data = [
        {"timestamp": "2025-02-27 14:35:10", "level": "INFO", "message": "Server started successfully."},
        {"timestamp": "2025-02-27 14:36:12", "level": "ERROR", "message": "Failed to connect to database."}
    ]
    
    # Create a temporary Jinja2 template
    template_content = """
    <html>
      <head><title>Log Report</title></head>
      <body>
        <h1>Log Report</h1>
        {% for log in logs %}
          <div>
            <strong>{{ log.level }}</strong> - {{ log.timestamp }}: {{ log.message }}
          </div>
        {% endfor %}
      </body>
    </html>
    """
    template_file = tmp_path / "report_template.html"
    template_file.write_text(template_content)
    
    output_file = tmp_path / "report.html"
    
    report_generator.generate_report(data, str(template_file), str(output_file))
    
    report_content = output_file.read_text()
    assert "Log Report" in report_content
    assert "Server started successfully." in report_content
