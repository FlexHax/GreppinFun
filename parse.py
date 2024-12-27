import json

# Main function of generating Markdown Report
def main(input_file="semgrep.sarif", output_file="report.md"):
    
    # Load the JSON data from the input file
    with open(input_file, "r") as f:
        data = json.load(f)

    markdown = []
    
    # Include Version Info
    markdown.append(f"# Analysis Report (Version {data.get('version', 'number')})\n")
    
    # Establishing Counter for Findings 
    finding_count = 1  

    # Process Results, Including Msgs, Locs, etc.
    markdown.append("\n## Results\n")
    for run in data.get("runs", []):
        
        for result in run.get("results", []):
            rule_id = result["ruleId"]
            message = result["message"]["text"]
            locations = result.get("locations", [])
            markdown.append(f"### Finding {finding_count}: Rule: {rule_id}\n")
            markdown.append(f"- **Message:** {message.strip()}\n")
            markdown.append(f"- **Locations:**\n")
            
            for loc in locations:
                pl = loc["physicalLocation"]
                file_path = pl["artifactLocation"]["uri"]
                region = pl["region"]
                start_line, end_line = region["startLine"], region["endLine"]
                snippet = region["snippet"]["text"]
                markdown.append(f"  - **File:** {file_path}\n    - **Lines:** {start_line}-{end_line}\n    - **Code Snippet:**\n```\n{snippet}\n```\n")
            
            finding_count += 1  # Increment the finding counter
    
    # Write to output file
    with open(output_file, "w") as f:
        f.write("\n".join(markdown))

# Generate the Markdown report
main()

# Success Indication in Terminal 
print("Markdown report generated: report.md")
