# YouTube Data API Setup and Usage

## Prerequisites
- Python installed
- Google Cloud Console account

## Installation
1. Install required dependencies:
```
pip install google-auth-oauthlib google-api-python-client pandas
```

## Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Navigate to **APIs & Services** > **Library**.
3. Enable **YouTube Data API v3**.
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client IDs**.
5. Set up the **OAuth Consent Screen**:
   - Add app information and scopes.
   - Choose **Desktop app** as the application type.
6. Download the `client_secret.json` file and save it in your project directory.
7. Add a test user in the **OAuth Consent Screen** > **Test Users** section.

## Fetching Data
1. To get the video related stats, Run the script:
```
python get_video_stats.py
```
2. To get the channel related stats, Run the script:
```
python get_channel_stats.py
```
Follow the authentication prompt to fetch your YouTube data. The data will be saved in csv format. If you already have fetched data once, running the script again will not delete the previous version, rather add new rows with updated data.