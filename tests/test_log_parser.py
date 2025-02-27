import os
from analyzer import log_parser

def test_parse_log_line_valid():
    line = "2025-02-27 14:35:10, INFO, Server started successfully."
    result = log_parser.parse_log_line(line)
    assert result is not None
    assert result["timestamp"] == "2025-02-27 14:35:10"
    assert result["level"] == "INFO"
    assert result["message"] == "Server started successfully."

def test_parse_log_line_invalid():
    line = "Invalid log format"
    result = log_parser.parse_log_line(line)
    assert result is None

def test_parse_log_file(tmp_path):
    log_content = (
        "2025-02-27 14:35:10, INFO, Server started successfully.\n"
        "2025-02-27 14:36:12, ERROR, Failed to connect to database.\n"
    )
    file = tmp_path / "test.log"
    file.write_text(log_content)
    logs = log_parser.parse_log_file(str(file))
    assert len(logs) == 2
    assert logs[1]["level"] == "ERROR"
