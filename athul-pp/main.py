import os
import requests
from dotenv import load_dotenv
from google import genai

# Load secret environment variables from .env
load_dotenv()

# ==========================================
# PHASE 1: The Data Gatherers
# ==========================================

def fetch_youtube_videos(topic):
    """Fetches top 5 videos from YouTube API based on a search topic."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("⚠️ Warning: YOUTUBE_API_KEY not found in environment.")
        return []

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": topic,
        "type": "video",
        "maxResults": 5,
        "key": api_key
    }

    try:
        # ADDED: timeout=5 prevents the app from hanging if YouTube servers lag
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            video_list = []
            
            # Loop through the items array returned by YouTube
            for item in data.get("items", []):
                title = item["snippet"]["title"]
                video_id = item["id"]["videoId"]
                link = f"https://www.youtube.com/watch?v={video_id}"
                
                video_list.append(f"- {title}: {link}")
            return video_list
        else:
            print(f"⚠️ YouTube API Error: Status {response.status_code}")
            return []
            
    # ADDED: Specific timeout error handling
    except requests.exceptions.Timeout:
        print("⚠️ YouTube API timed out. Moving on without videos...")
        return []
    except Exception as e:
        print(f"⚠️ Failed to fetch YouTube videos: {e}")
        return []


def fetch_open_library_books(topic):
    """Fetches top 5 books from the public Open Library API."""
    url = "https://openlibrary.org/search.json"
    params = {
        "q": topic,
        "limit": 5
    }

    try:
        # ADDED: timeout=5 prevents the app from hanging if Open Library lags
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            book_list = []
            
            # Loop through the docs array returned by Open Library
            for doc in data.get("docs", []):
                title = doc.get("title", "Unknown Title")
                
                # Author name comes as a list, convert it to a string
                authors = doc.get("author_name", ["Unknown Author"])
                author_str = ", ".join(authors)
                
                book_list.append(f"- {title} by {author_str}")
            return book_list
        else:
            print(f"⚠️ Open Library Error: Status {response.status_code}")
            return []
            
    # ADDED: Specific timeout error handling
    except requests.exceptions.Timeout:
        print("⚠️ Open Library API timed out. Moving on without books...")
        return []
    except Exception as e:
        print(f"⚠️ Failed to fetch Open Library books: {e}")
        return []


# ==========================================
# PHASE 2 & 3: The Aggregator & The Brain
# ==========================================

def generate_roadmap(topic, days, videos, books):
    """Formats the data into a prompt and uses Gemini to generate the learning plan."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return "⚠️ Error: GEMINI_API_KEY is missing from your .env file."

    # Initialize the Google GenAI production client
    client = genai.Client(api_key=gemini_key)
    
    # Format list arrays into plain text blocks
    videos_text = "\n".join(videos) if videos else "No specific videos found."
    books_text = "\n".join(books) if books else "No specific books found."
    
    # Construct the instruction prompt
    prompt = f"""
    You are a learning assistant.
    Create a structured day-wise learning roadmap based on the following data.
    
    Topic: {topic}
    Total Days: {days}
    
    You are given these resources:
    YouTube Videos:
    {videos_text}
    
    Books:
    {books_text}
    
    Task:
    1. Break the topic into a step-by-step learning plan.
    2. Distribute learning evenly across the given number of days.
    3. Each day should include:
       - What to study
       - Which videos to watch
       - Which book sections to refer (if applicable)
    4. Keep it beginner-friendly and structured.
    5. Output in clean day-wise format.
    Return only the roadmap.
    """
    
    print("🧠 Asking Gemini to build your roadmap... please wait.")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Generation Failed: {e}"


# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    print("Welcome to the AI Study Roadmap Generator!")
    topic = input("What topic do you want to learn? (e.g., React, Machine Learning): ")
    days = input("How many days do you have to learn this?: ")
    
    print("\n🔍 Gathering resources from the internet...")
    
    # Execution steps for data aggregation
    videos = fetch_youtube_videos(topic)
    books = fetch_open_library_books(topic)
    
    # Pass compiled data to the generation function
    final_roadmap = generate_roadmap(topic, days, videos, books)
    
    print("\n" + "="*50)
    print("YOUR PERSONALIZED ROADMAP:")
    print("="*50)
    print(final_roadmap)


if __name__ == "__main__":
    main()