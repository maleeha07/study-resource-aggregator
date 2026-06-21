import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

# ========================
# ENV VARIABLES
# ========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


# ========================
# PROMPT BUILDER
# ========================
def build_prompt(topic, num_days, difficulty, videos, books):

    video_lines = "\n".join(
        [f"- {v.get('title')} by {v.get('channel')} ({v.get('url')})" for v in videos]
    )

    book_lines = "\n".join(
        [f"- {b.get('title')} by {b.get('author')} ({b.get('link')})" for b in books]
    )

    return f"""
You are an expert AI learning roadmap generator.

TOPIC: {topic}
DURATION: {num_days} days
DIFFICULTY: {difficulty}

VIDEOS:
{video_lines}

BOOKS:
{book_lines}

TASK:
- Create a structured {num_days}-day learning plan
- Use ONLY provided resources
- Include schedule, sessions, projects
- Keep it beginner-friendly
- Return ONLY valid JSON

JSON FORMAT:
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "total_days": {num_days},
  "days": [
    {{
      "day": 1,
      "focus": "topic title",
      "sessions": [
        {{
          "time": "9:00 AM - 10:30 AM",
          "activity": "study task"
        }}
      ],
      "videos": [],
      "books": [],
      "project": "small project",
      "notes": "summary"
    }}
  ]
}}
"""


# ========================
# GENERATE ROADMAP
# ========================
def generate_roadmap(topic, num_days, difficulty, videos, books):

    if not GEMINI_API_KEY:
        print("❌ Missing GEMINI_API_KEY in .env")
        return None

    prompt = build_prompt(topic, num_days, difficulty, videos, books)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        generated_text = response.text

    except Exception as e:
        print("❌ Gemini error:", e)
        return None

    if not generated_text:
        print("❌ Empty response from Gemini")
        return None

    # Clean markdown if Gemini adds it
    text = generated_text.replace("```json", "").replace("```", "").strip()

    # Extract JSON safely
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        print("❌ No JSON found in AI response")
        print(text)
        return None

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON")
        print(json_text)
        return None


# ========================
# PRETTY PRINTER
# ========================
def print_roadmap(roadmap):

    print("\n" + "=" * 60)
    print(f"📘 ROADMAP: {roadmap['topic']} ({roadmap['difficulty']})")
    print(f"⏳ Duration: {roadmap['total_days']} days")
    print("=" * 60)

    for day in roadmap.get("days", []):

        print(f"\n📅 DAY {day.get('day')}: {day.get('focus')}")
        print("-" * 50)

        print("🕒 Schedule:")
        for session in day.get("sessions", []):
            print(f"  {session.get('time')} → {session.get('activity')}")

        if day.get("videos"):
            print("\n🎥 Videos:", ", ".join(day["videos"]))

        if day.get("books"):
            print("📚 Books:", ", ".join(day["books"]))

        if day.get("project"):
            print("\n🛠 Project:", day["project"])

        print("\n📝 Notes:", day.get("notes"))


# ========================
# TEST RUN
# ========================
if __name__ == "__main__":

    from youtube_service import get_youtube_videos
    from books_service import get_books

    topic = "React"
    num_days = 5
    difficulty = "Beginner"

    print("🔎 Fetching resources...")

    videos = get_youtube_videos(topic, max_results=5)
    books = get_books(topic, max_results=5)

    print("🚀 Generating roadmap...")

    roadmap = generate_roadmap(
        topic,
        num_days,
        difficulty,
        videos,
        books
    )

    if roadmap:
        print_roadmap(roadmap)

        with open("last_roadmap.json", "w", encoding="utf-8") as f:
            json.dump(roadmap, f, indent=2)

        print("\n✅ Saved to last_roadmap.json")

    else:
        print("\n❌ Roadmap generation failed")