Study Resource Aggregator

A Python-based learning assistant that aggregates educational resources from multiple sources and generates a personalized learning roadmap using AI.

Project Overview

This application helps users learn a topic by:

Searching YouTube for relevant educational videos
Finding related books from Open Library
Using Google's Gemini AI to generate a structured day-wise study plan
Combining all resources into a beginner-friendly learning roadmap
Features
Topic-based resource aggregation
YouTube video recommendations
Book recommendations from Open Library
AI-generated study roadmap
Customizable learning duration
Environment variable support for API keys
Technologies Used
Python
YouTube Data API v3
Open Library API
Gemini API
Requests
Python Dotenv
Installation
1. Clone the Repository
git clone <repository-url>
cd study-resource-aggregator
2. Create a Virtual Environment
python -m venv venv

Activate the environment:

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root:

YOUTUBE_API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key
Obtaining API Keys
YouTube Data API
Create a Google Cloud project.
Enable YouTube Data API v3.
Generate an API key.
Gemini API
Visit Google AI Studio.
Create an API key.
Add the key to your .env file.
Usage

Run the application:

python main.py

Enter:

Enter the topic of interest that you need to learn:
Enter the number of days:

Example:

Enter the topic of interest that you need to learn: Embedded Systems
Enter the number of days: 7

The application will:

Retrieve educational videos from YouTube.
Retrieve relevant books from Open Library.
Generate a personalized study roadmap using Gemini AI.
Display the roadmap in the terminal.
Project Structure
study-resource-aggregator/
│
├── main.py
├── .env
├── requirements.txt
└── README.md
APIs Used
YouTube Data API v3
Open Library API
Gemini API
Future Improvements
Graphical user interface using Tkinter or Flutter
Resource caching to reduce API usage
Export roadmap to PDF
Progress tracking and daily checklists
Resource ranking and filtering
Web-based interface
Support for multiple AI providers
Learning Outcomes

This project demonstrates:

REST API integration
Environment variable management
JSON data processing
Resource aggregation
Prompt engineering
AI-assisted content generation
Python application development
Author
Sree Lekshmi H