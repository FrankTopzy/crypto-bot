import os
import requests
from dotenv import load_dotenv

# Load the variables from .env
load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Ask Reddit for an access token
response = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=(CLIENT_ID, CLIENT_SECRET),
    data={
        "grant_type": "client_credentials"
    },
    headers={
        "User-Agent": USER_AGENT
    }
)

print("Status:", response.status_code)
print("Response:", response.json())