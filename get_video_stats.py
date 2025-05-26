import os
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Define the scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]



def authenticate_youtube():
    """Authenticate and return the YouTube API client."""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for next run
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def get_uploads_playlist_id(youtube):
    """Fetch the uploads playlist ID."""
    response = youtube.channels().list(part="contentDetails", mine=True).execute()
    items = response.get("items", [])
    if not items:
        print("No channel content details found.")
        return None
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_video_ids(youtube, playlist_id):
    """Fetch video IDs from the uploads playlist."""
    video_ids = []
    next_page_token = None
    while True:
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        items = response.get("items", [])
        for item in items:
            video_ids.append(item["contentDetails"]["videoId"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def get_video_stats(youtube, video_ids):
    """Fetch statistics for each video."""
    stats = []
    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids[i:i+50])
        ).execute()
        items = response.get("items", [])
        for item in items:
            stats.append({
                "Day": datetime.now().strftime("%Y-%m-%d"),
                "Video ID": item["id"],
                "Title": item["snippet"]["title"],
                "Published At": item["snippet"]["publishedAt"],
                "Views": item["statistics"].get("viewCount"),
                "Likes": item["statistics"].get("likeCount"),
                "Comments": item["statistics"].get("commentCount")
            })
    return stats

def save_to_csv(data, filename):
    """Save data to CSV, appending if file exists."""
    df = pd.DataFrame(data)
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, mode='w', header=True, index=False)
    print(f"Data saved to {filename}")

def main():
    youtube = authenticate_youtube()
    playlist_id = get_uploads_playlist_id(youtube)
    if playlist_id:
        video_ids = get_video_ids(youtube, playlist_id)
        video_stats = get_video_stats(youtube, video_ids)
        if video_stats:
            save_to_csv(video_stats, "video_stats.csv")

if __name__ == "__main__":
    main()
