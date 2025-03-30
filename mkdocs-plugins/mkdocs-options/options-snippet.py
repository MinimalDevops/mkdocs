from pathlib import Path

# Get the absolute path of the current script's directory
current_dir = Path(__file__).parent.resolve()

def fetch_md_file_paths(file_path):
    try:
        # Read the file content
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Filter lines containing ".md" but ignore "index.md" and "tags.md"
        md_lines = [
            line.strip() for line in lines 
            if ".md" in line and "index.md" not in line and "tags.md" not in line
        ]
        
        # Extract the last part of each file path, remove .md extension, and concatenate with commas
        md_files = [line.split('/')[-1].replace('.md', '') for line in md_lines]
        result = ",".join(md_files)
        
        return result
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Replace '../../mkdocs.yml' with the relative path to your file
file_path = (current_dir / "../../mkdocs.yml").resolve()
md_file_names = fetch_md_file_paths(file_path)

# Insert the concatenated string into the JSON structure
if md_file_names:
    json_snippet = f'''
    "md.command10": {{
        "scope": "markdown",
        "prefix": "mdreplace",
        "body": [
            "[[${{2|{md_file_names}|}}|${{TM_SELECTED_TEXT:${{1}}}}]]"
        ],
        "description": "Replace selected text with one of the predefined options"
    }},
    '''
    print(json_snippet)
else:
    print("No .md files found or an error occurred.")
