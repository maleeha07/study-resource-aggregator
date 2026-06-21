import requests
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

num=25 #number of youtube videos

topic=input("Enter the topic of interest that you need to learn:")
days=input("Enter the number of days :")
youtube_api=os.getenv("youtube_API_KEY")
url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults={num}&q={topic}&type=video&key={youtube_api}"

youtube_response=requests.get(url)


url2=f"https://openlibrary.org/search.json?q={topic}"
book_response=requests.get(url2)

video=num*1
if youtube_response.status_code==200:
    data=youtube_response.json()

    videos = []
    for item in data["items"]:
        video = {
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video)

else:
    print("Error in loading youtube api")
    exit()

if book_response.status_code==200:
    data2=book_response.json()
    books=[]
    for doc in data2["docs"]:
            book = {
            "title": doc.get("title", "Unknown"),
            "author": ", ".join(doc.get("author_name", ["Unknown"])),
            "link": (
                  f"https://openlibrary.org/books/{doc['cover_edition_key']}"
                  if "cover_edition_key" in doc
                  else "No book link available"
                  )
            }
            books.append(book)
else:
     print("Error in loading books api")
     exit()

gemini_api=os.getenv("gemini_API_KEY")
client = genai.Client(api_key=gemini_api)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""You are an expert learning assistant and curriculum designer. 
Create a highly structured, visually clean, day-wise learning roadmap based on the following data.

[DATA]
Topic: {topic}
Total Days: {days}

[RESOURCES]
YouTube Videos:
{videos}

Books:
{books}

[TASK & OBJECTIVES]
1. Break down the topic into a logical, step-by-step learning progression.
2. Distribute the learning workload evenly across the given number of days.
3. Keep the explanations, progression, and tone beginner-friendly yet highly professional.
4. Output ONLY the roadmap. Do not include introductory or concluding conversational filler.

[FORMATTING & STYLE REQUIREMENTS]
To ensure maximum readability, you must strictly follow this formatting structure for the output:

• Use 📌 for the main Day header.
• Use 🎯 for the daily learning objective.
• Use a downward arrow (↓) centered between days to clearly signify the progression to the next step.
• Use clean Markdown bolding and bullet points to organize the resources.

Each day must look exactly like this:

📌 Day X: [Insert Short, Clear Title]
🎯 Objective: [Insert what the learner will achieve today]
• 📝 What to Study: [Core concepts covered today]
• 🎥 Videos to Watch: [Specific video titles,channel name,links from the resources]
• 📖 Book Sections: [Book Title,authour,Specific chapters/pages from the resources, if applicable,link from the resources if available]

↓

📌 Day X+1: [Next Title]
...and so on. 

(Note: Do not place a downward arrow after the final day).

Generate the roadmap now:""")
print(response.text)
