import re
import json
import argparse

# Regex pattern to match log lines in the format:
# "YYYY-MM-DD HH:MM:SS, LEVEL, Message"
LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (?P<level>[A-Z]+), (?P<message>.+)'
)

def parse_log_line(line):
    """
    Parse a single log line.
    
    Args:
        line (str): A line from the log file.
        
    Returns:
        dict or None: Dictionary with 'timestamp', 'level', 'message'
                      if the line matches the expected format; None otherwise.
    """
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def parse_log_file(file_path):
    """
    Parse a log file and return a list of log entries.
    
    Args:
        file_path (str): Path to the input log file.
    
    Returns:
        list: List of dictionaries, each representing a log entry.
    """
    logs = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
    return logs

def main():
    parser = argparse.ArgumentParser(
        description="Parse log files and output the extracted data as JSON."
    )
    parser.add_argument("--input", required=True, help="Input log file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    logs = parse_log_file(args.input)
    with open(args.output, 'w') as outfile:
        json.dump(logs, outfile, indent=4)
    print(f"Parsed {len(logs)} log entries and saved to {args.output}")

if __name__ == '__main__':
    main()
