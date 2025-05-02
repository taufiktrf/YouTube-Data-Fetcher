import os
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

# Define the scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def authenticate_youtube():
    """Authenticate and return the YouTube API client."""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def get_channel_stats(youtube):
    """Fetch channel statistics."""
    request = youtube.channels().list(part="snippet,statistics", mine=True)
    response = request.execute()
    items = response.get("items", [])
    if not items:
        print("No channel data found.")
        return None
    channel = items[0]
    data = {
        "Day": datetime.now().strftime("%Y-%m-%d"),
        "Channel Title": channel["snippet"]["title"],
        "Subscribers": channel["statistics"].get("subscriberCount"),
        "Total Views": channel["statistics"].get("viewCount"),
        "Total Videos": channel["statistics"].get("videoCount"),
        "Description": channel["snippet"].get("description"),
        "Published At": channel["snippet"].get("publishedAt")
    }
    return data

def save_to_csv(data, filename="channel_stats.csv"):
    """Save data to CSV, appending if file exists."""
    df = pd.DataFrame([data])
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, mode='w', header=True, index=False)
    print(f"Data saved to {filename}")

def main():
    youtube = authenticate_youtube()
    channel_stats = get_channel_stats(youtube)
    if channel_stats:
        save_to_csv(channel_stats)

if __name__ == "__main__":
    main()
