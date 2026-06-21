import os
import requests
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_videos(topic, max_results=5):
    """
    Fetches top YouTube videos for a given topic.
    Returns a list of dicts with title, channel, and url.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{topic} tutorial",
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

  
    if "items" not in data:
        print("YouTube API error:", data)
        return []

    videos = []
    for item in data["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            "title": title,
            "channel": channel,
            "url": video_url
        })

    return videos



if __name__ == "__main__":
    results = get_youtube_videos("React")
    for v in results:
        print(v)