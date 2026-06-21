import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_youtube_client():
    if not YOUTUBE_API_KEY:
        return None

    return build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY
    )


def search_youtube_videos(topic: str, max_results: int = 5):
    """
    Fetch up to 5 YouTube videos for a user topic.
    """

    youtube = get_youtube_client()

    if youtube is None:
        return []

    try:
        request = youtube.search().list(
            q=topic,
            part="snippet",
            type="video",
            maxResults=min(max_results, 5),
            relevanceLanguage="en"
        )

        response = request.execute()

        videos = []

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]

            videos.append({
                "title": item["snippet"]["title"],
                "link": f"https://www.youtube.com/watch?v={video_id}"
            })

        return videos

    except Exception as e:
        print(f"[YouTube Service Error]: {e}")
        return []