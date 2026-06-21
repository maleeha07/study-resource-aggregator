# AI Study Roadmap Generator

A Python CLI tool that builds personalized day-wise learning roadmaps using real resources from the internet.

## What it does

- Fetches relevant **YouTube videos** and **books** (via OpenLibrary) for any topic you enter
- Uses **Groq AI (LLaMA 3.1)** to generate a structured, day-wise study plan from those resources
- **Caches** fetched resources locally so you don't waste API calls on repeated topics
- Lets you **export** the generated roadmap as a `.txt` or `.json` file

## Setup

1. Install dependencies:
   ```
   pip install requests python-dotenv google-api-python-client groq
   ```

2. Create a `.env` file with your API keys:
   ```
   YOUTUBE_API=your_youtube_api_key
   GROQ_API=your_groq_api_key
   ```

3. Run:
   ```
   python main.py
   ```

## Built with

- Python
- Groq API (LLaMA 3.1)
- YouTube Data API v3
- OpenLibrary API
