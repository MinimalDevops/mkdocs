import os
import requests
from msal import PublicClientApplication

# Azure AD application credentials
CLIENT_ID = '4336ad88-dc84-4a91-a14c-353074a2739a'
SCOPES = ["Files.ReadWrite", "User.Read", "Notes.ReadWrite"]
AUTHORITY = 'https://login.microsoftonline.com/consumers'
REDIRECT_URI = "http://localhost"

# File and OneNote settings
FILE_PATH = 'index.md'
NOTEBOOK_NAME = "Tapinder's Notebook"
SECTION_NAME = 'Test'
PAGE_TITLE = 'test6'

if not os.path.exists(FILE_PATH):
    print(f"Error: File '{FILE_PATH}' not found.")
    # Optionally create the file if needed
    with open(FILE_PATH, 'w') as file:
        file.write("# Default Content\n")
    print(f"Created a new file at {FILE_PATH}.")

def authenticate():
    """Authenticate and get an access token for personal OneDrive."""
    app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    result = app.acquire_token_interactive(SCOPES)
    if "access_token" in result:
        print(f"Access Token: {result['access_token']}")
        return result["access_token"]
    else:
        raise Exception(f"Authentication failed: {result}")

def get_or_create_notebook(token, notebook_name):
    """Get or create a notebook."""
    headers = {'Authorization': f'Bearer {token}'}
    url = 'https://graph.microsoft.com/v1.0/me/onenote/notebooks'

    # Fetch existing notebooks
    response = requests.get(url, headers=headers)
    response_json = response.json()  # Parse response as JSON
    print("Notebook Fetch Response:", response.status_code, response_json)

    if 'error' in response_json:
        raise Exception(f"Error fetching notebooks: {response_json['error']['message']}")

    # Check if the notebook already exists
    for notebook in response_json.get('value', []):
        if notebook['displayName'] == notebook_name:
            return notebook['id']

    # Create a new notebook if not found
    response = requests.post(url, headers=headers, json={'displayName': notebook_name})
    response_json = response.json()  # Parse response as JSON
    if 'error' in response_json:
        raise Exception(f"Error creating notebook: {response_json['error']['message']}")
    if 'id' in response_json:
        return response_json['id']
    else:
        raise Exception(f"Unexpected response: {response_json}")


def get_or_create_section(token, notebook_id, section_name):
    """Get or create a section in a notebook."""
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections'
    response = requests.get(url, headers=headers).json()
    for section in response.get('value', []):
        if section['displayName'] == section_name:
            return section['id']
    # Create section if not found
    response = requests.post(url, headers=headers, json={'displayName': section_name}).json()
    if 'id' not in response:
        raise Exception(f"Error creating section: {response.get('error', response)}")
    return response['id']

def create_page(token, section_id, page_title, content):
    """Create a OneNote page."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/xhtml+xml',
    }
    # Convert content into structured HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{page_title}</title>
    </head>
    <body>
        <h1>{page_title}</h1>
        {content.replace("\n", "<br>")}  <!-- Preserve newlines -->
    </body>
    </html>
    """
    url = f'https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages'
    response = requests.post(url, headers=headers, data=html_content)
    if response.status_code == 201:
        print("Page created successfully!")
    else:
        print(f"Failed to create page: {response.status_code}, {response.text}")


def main():
    token = authenticate()
    notebook_id = get_or_create_notebook(token, NOTEBOOK_NAME)
    section_id = get_or_create_section(token, notebook_id, SECTION_NAME)
    with open(FILE_PATH, 'r') as file:
        content = file.read()
    create_page(token, section_id, PAGE_TITLE, content)

if __name__ == '__main__':
    main()
