import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build
from groq import Groq

load_dotenv()

Youtube_API = os.getenv("YOUTUBE_API")
Groq_API = os.getenv("GROQ_API")

client = Groq(api_key=Groq_API)

youtube = build("youtube", "v3", developerKey=Youtube_API)

# --- Cache Setup ---
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache.json")
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")

def load_cache():
    """Load the cache from disk. Returns an empty dict if no cache exists."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_cache(cache):
    """Persist the cache dictionary to disk."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_cached_resources(topic):
    """Return cached videos and books for a topic, or None if not cached."""
    cache = load_cache()
    key = topic.strip().lower()
    if key in cache:
        print(f"✅ Cache hit! Using saved resources for '{topic}'.")
        return cache[key]["videos"], cache[key]["books"]
    return None

def cache_resources(topic, videos, books):
    """Save fetched videos and books into the cache for future lookups."""
    cache = load_cache()
    key = topic.strip().lower()
    cache[key] = {
        "videos": videos,
        "books": books,
        "cached_at": datetime.now().isoformat()
    }
    save_cache(cache)

# --- Export Functions ---

def export_roadmap_txt(topic, days, roadmap_text):
    """Export the roadmap as a plain-text .txt file."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(" ", "_").lower()
    filename = f"roadmap_{safe_topic}_{timestamp}.txt"
    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(f"AI Study Roadmap: {topic}\n")
        f.write(f"Duration: {days} days\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(roadmap_text)

    return filepath

def export_roadmap_json(topic, days, videos, books, roadmap_text):
    """Export the roadmap as a structured .json file."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(" ", "_").lower()
    filename = f"roadmap_{safe_topic}_{timestamp}.json"
    filepath = os.path.join(EXPORT_DIR, filename)

    export_data = {
        "topic": topic,
        "duration_days": days,
        "generated_at": datetime.now().isoformat(),
        "resources": {
            "videos": videos,
            "books": books
        },
        "roadmap": roadmap_text
    }

    with open(filepath, "w") as f:
        json.dump(export_data, f, indent=2)

    return filepath

# --- Core Functions ---

def fetch_youtube_videos(topic):
    result = []
    
    try:
        request = youtube.search().list(
            part="snippet",
            q=topic,
            maxResults=5,
            type="video"
        )
        response = request.execute()
        
        for item in response.get("items", []):
            dic = {}
            
            # Fixed bracket syntax and typo
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            video_id = item["id"]["videoId"]

            dic["title"] = title
            dic["channel"] = channel
            dic["url"] = f"https://www.youtube.com/watch?v={video_id}"
            
            result.append(dic)
            
    except Exception as e:
        print(f"An error occurred while fetching YouTube videos: {e}")

    return result

def fetch_books(topic):
    url = f"https://openlibrary.org/search.json"
    params = {
        "q": topic
    }

    books = []

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()

            for book in data.get("docs", [])[:5]:
                title = book.get("title", "Unknown Title")
                author_names = book.get("author_name", [])
                author = author_names[0] if author_names else "Unknown Author"

                key = book.get("key", "")
                book_url = f"https://openlibrary.org{key}" if key else ""

                books.append({
                    "title": title,
                    "author": author,
                    "url": book_url
                })
        
    except Exception as e:
        print(f"An error occurred while fetching books: {e}")
    
    return books

def generate_roadmap(resource_bundle):
    topic = resource_bundle["topic"]
    days = resource_bundle["duration_days"]

    videos_str = json.dumps(resource_bundle["videos"], indent=2)
    books_str = json.dumps(resource_bundle["books"], indent=2)
    system_prompt = (
        """You are a learning assistant that creates structured learning roadmaps.

        Your task is to generate a day-wise learning plan using the resources provided by the user.

        Rules:
        1. Break the topic into a logical step-by-step learning sequence.
        2. Distribute the learning workload evenly across the specified number of days.
        3. Each day must include:
        - Topics to study
        - Videos to watch
        - Book references (when applicable)
        4. Assume the learner is a beginner unless stated otherwise.
        5. Keep the roadmap practical, progressive, and easy to follow.
        6. Use a clean day-wise format.
        7. Use the provided resources whenever possible.
        8. Return only the roadmap without introductions, explanations, or extra commentary."""
    )

    user_prompt = f"""Create a learning roadmap using the following information:

        Topic: {topic}

        Total Days: {days}

        YouTube Videos:
        {json.dumps(resource_bundle["videos"], indent=2)}

        Books:
        {json.dumps(resource_bundle["books"], indent=2)}
    """

    try:
        completion = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
        )

        roadmap_output = completion.choices[0].message.content
        return roadmap_output
    except Exception as e:
        return f"An error occured while generating the roadmap: {e}"

if __name__ == "__main__":

    print("Welcome to the AI Study Roadmap Generator")

    while True:

        print("\n--- Main Menu ---")
        print("1. Generate New Roadmap")
        print("2. View History (Coming Soon)")
        print("3. Clear Cache")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            topic_input = input("\nEnter a topic: ")
            days_input = int(input("Enter number of days: "))
            
            # Check cache first before making API calls
            cached = get_cached_resources(topic_input)

            if cached:
                videos, books = cached
            else:
                print(f"\nFetching resources for '{topic_input}'...")
                videos = fetch_youtube_videos(topic_input)
                books = fetch_books(topic_input)
                cache_resources(topic_input, videos, books)
                print("📦 Resources cached for future use.")

            resource_bundle = {
                "topic": topic_input,
                "duration_days": days_input,
                "videos": videos,
                "books": books
            }

            print("Generating AI Roadmap...")
            roadmap = generate_roadmap(resource_bundle)

            print("\n--- Learning Roadmap ---\n")
            print(roadmap)
            
            # Export prompt
            print("\n--- Export Options ---")
            print("1. Export as TXT")
            print("2. Export as JSON")
            print("3. Skip export")
            export_choice = input("Select an option (1-3): ").strip()

            if export_choice == '1':
                path = export_roadmap_txt(topic_input, days_input, roadmap)
                print(f"✅ Roadmap exported to: {path}")
            elif export_choice == '2':
                path = export_roadmap_json(topic_input, days_input, videos, books, roadmap)
                print(f"✅ Roadmap exported to: {path}")
            else:
                print("Export skipped.")

        elif choice == '2':
            print("\n[History Feature Not Yet Implemented]")
            # We will add this in Step 4!

        elif choice == '3':
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
                print("🗑️  Cache cleared successfully.")
            else:
                print("No cache file found.")
            
        elif choice == '4':
            print("\nGoodbye! Happy Learning! 🚀")
            break # This exits the while loop and ends the program
            
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")