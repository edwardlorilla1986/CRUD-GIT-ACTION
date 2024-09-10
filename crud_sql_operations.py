import base64
import json
import requests
import os

GITHUB_TOKEN = os.getenv('TOKEN')
REPO = os.getenv('REPOSITORY')
BRANCH = "main"
BASE_URL = f"https://api.github.com/repos/{REPO}/contents/database.sql"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_sql_file(sql_content):
    """Create a new SQL file in the repository."""
    encoded_content = base64.b64encode(sql_content.encode('utf-8')).decode('utf-8')
    data = {
        "message": "Create SQL file",
        "content": encoded_content,
        "branch": BRANCH
    }
    response = requests.put(BASE_URL, headers=headers, data=json.dumps(data))
    print(response.json())

def read_sql_file():
    """Read the SQL file from the repository."""
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        file_content = response.json()['content']
        decoded_content = base64.b64decode(file_content).decode('utf-8')
        print(decoded_content)
        return decoded_content
    else:
        print("File not found.")
        return None

def update_sql_file(new_sql_content):
    """Update the existing SQL file in the repository."""
    current_content = read_sql_file()
    if current_content:
        updated_content = current_content + "\n" + new_sql_content
        encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')
        sha = requests.get(BASE_URL, headers=headers).json()["sha"]
        data = {
            "message": "Update SQL file",
            "content": encoded_content,
            "sha": sha,
            "branch": BRANCH
        }
        response = requests.put(BASE_URL, headers=headers, data=json.dumps(data))
        print(response.json())

def delete_sql_file():
    """Delete the SQL file from the repository."""
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]
        data = {
            "message": "Delete SQL file",
            "sha": sha,
            "branch": BRANCH
        }
        response = requests.delete(BASE_URL, headers=headers, data=json.dumps(data))
        print(response.json())
    else:
        print("File not found.")

# Example usage
if __name__ == "__main__":
    action = os.getenv("ACTION")
    
    if action == "create":
        sql_content = """CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100)); INSERT INTO users (id, name) VALUES (1, 'John Doe');"""
        create_sql_file(sql_content)
    elif action == "read":
        read_sql_file()
    elif action == "update":
        new_sql_content = "INSERT INTO users (id, name) VALUES (2, 'Jane Doe');"
        update_sql_file(new_sql_content)
    elif action == "delete":
        delete_sql_file()
