import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Services
from books_service import fetch_top_books
from youtube_service import search_youtube_videos



load_dotenv()

# Gemini Client
ai_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_daywise_roadmap(topic: str, total_days: int, difficulty_level: str) -> str:
    """
    Generate a structured day-wise learning roadmap.
    """

    print(f"📦 Phase 1: Aggregating resources for '{topic}'...")

    # Fetch resources
    video_data = search_youtube_videos(
        topic,
        max_results=5
    )

    book_data = fetch_top_books(
        topic,
        max_results=5
    )

    # Format YouTube resources
    youtube_resources_str = "\n".join(
        [
            f"- {video['title']} ({video['link']})"
            for video in video_data
        ]
    )

    # Format Book resources
    books_resources_str = "\n".join(
        [
            f"- {book['title']} by {book['author']}"
            for book in book_data
        ]
    )

    # Prompt
    prompt = f"""
You are a learning assistant.

Create a structured day-wise learning roadmap based on the following data.

Topic: {topic}
Total Days: {total_days}
difficulty level: {difficulty_level}

You are given these resources.

YouTube Videos:
{youtube_resources_str}

Books:
{books_resources_str}

Task:

1. Break the topic into a logical step-by-step learning journey.

2. Distribute learning evenly across {total_days} days.

3. For each day provide:

   - Day number
   - Main learning objective
   - Topics to study
   - YouTube videos to watch from the provided resources
   - Book recommendations from the provided resources
   - Specific book chapters or sections if applicable
   - Study schedule divided into multiple sessions
   - Break times
   - Meal times
   - Estimated duration of each session
   - Daily practice exercises
   - A project related to the day's topics
Difficulty Guidelines(difficulty_level):

Beginner:
- Assume no prior knowledge.
- Start from fundamentals.
- Use simpler exercises.
- Include guided projects.

Intermediate:
- Assume basic familiarity.
- Move faster through fundamentals.
- Include moderate projects.
- Focus on practical application.

Advanced:
- Assume strong prior knowledge.
- Focus on advanced concepts.
- Include real-world projects.
- Cover optimization, architecture, and best practices.
4. Projects should progressively increase in difficulty.

5. Keep the roadmap beginner-friendly and practical.

6. Ensure the complete topic is covered within the specified number of days.

7. Use only the provided books and videos when recommending resources.

8. Every day should include:
   - objective
   - topics
   - videos
   - books
   - study_schedule
   - exercises
   - project

9. Output a complete day-wise roadmap.

Return ONLY valid JSON matching the provided schema.
"""

    print("🤖 Phase 2: Generating roadmap with Gemini...")

    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            )
        )

        return response.text

    except Exception as e:
        print(f"[Gemini Error]: {e}")
        return "{}"


if __name__ == "__main__":

    print("🚀 STUDY ROADMAP AGGREGATOR")

    user_topic = input(
        "\nEnter a topic to learn: "
    )

    while True:
        try:
            total_days = int(
                input("Enter number of learning days: ")
            )

            if total_days > 0:
                break

            print("Please enter a number greater than 0.")

        except ValueError:
            print("Please enter a valid integer.")
    difficulty_level = input("Choose difficulty (Beginner/Intermediate/Advanced): "
    ).strip().capitalize()

    print("\n----------------------------------")

    roadmap_json = generate_daywise_roadmap(
        user_topic,
        total_days,
        difficulty_level
    )

    print("\n🎉 ROADMAP GENERATED SUCCESSFULLY\n")
    print(roadmap_json)