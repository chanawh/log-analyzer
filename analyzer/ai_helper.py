import openai
import os
import json
import argparse

def get_ai_suggestion(error_message):
    """
    Get an AI-powered suggestion for resolving the given error message.
    
    Args:
        error_message (str): The error message to analyze.
        
    Returns:
        str: The suggested fix or an error message if the API call fails.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Suggest a possible fix for the following error:\n\n{error_message}\n\nFix suggestion:"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
            n=1,
            stop=None,
        )
        suggestion = response.choices[0].text.strip()
        return suggestion
    except Exception as e:
        return f"Error obtaining suggestion: {e}"

def generate_suggestions(parsed_logs):
    """
    Generate suggestions for each unique error log.
    
    Args:
        parsed_logs (list): List of parsed log entries.
        
    Returns:
        dict: Dictionary mapping error messages to AI suggestions.
    """
    error_logs = [log for log in parsed_logs if log.get("level") == "ERROR"]
    suggestions = {}
    unique_errors = set(log["message"] for log in error_logs)
    
    for error in unique_errors:
        suggestions[error] = get_ai_suggestion(error)
    
    return suggestions

def main():
    parser = argparse.ArgumentParser(
        description="Generate AI-powered fix suggestions based on log errors."
    )
    parser.add_argument("--errors", required=True, help="JSON file with parsed log entries")
    parser.add_argument("--output", required=True, help="Output text file for suggestions")
    args = parser.parse_args()

    with open(args.errors, 'r') as f:
        parsed_logs = json.load(f)
    
    suggestions = generate_suggestions(parsed_logs)
    with open(args.output, 'w') as outfile:
        for error, suggestion in suggestions.items():
            outfile.write(f"Error: {error}\nSuggestion: {suggestion}\n\n")
    print(f"AI suggestions generated and saved to {args.output}")

if __name__ == '__main__':
    main()
