import keyring
import json
import os
import sys

SERVICE_NAME = "drivebox"
CREDENTIALS_KEY = "google_client_secrets"

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/store_credentials.py /path/to/credentials.json")
        sys.exit(1)

    creds_path = sys.argv[1]
    if not os.path.exists(creds_path):
        print(f"Error: {creds_path} does not exist")
        sys.exit(1)

    with open(creds_path, "r") as f:
        creds_json = f.read()

    # Validate JSON
    try:
        json.loads(creds_json)
    except json.JSONDecodeError:
        print("Error: credentials.json is not valid JSON")
        sys.exit(1)

    # Store in keyring
    keyring.set_password(SERVICE_NAME, CREDENTIALS_KEY, creds_json)
    print(f"✅ Stored Google client secrets in keyring under service '{SERVICE_NAME}'")

if __name__ == "__main__":
    main()