
# AI Study Resource Aggregator & Roadmap Generator

A Python-based data pipeline that fetches real-world educational resources and uses Google's Gemini AI to generate a structured, personalized learning schedule. 

## Features
* **Multi-Source Aggregation:** Fetches top video tutorials via the **YouTube Data API** and relevant books via the public **Open Library API**.
* **AI Integration:** Uses **Google Gemini (gemini-2.5-flash)** to process raw JSON data and construct a day-by-day study roadmap.
* **Secure Environment:** Implements `python-dotenv` to safely load and manage API keys outside of version control.
* **Error Handling:** Gracefully handles missing API keys and empty search results.

## Prerequisites
* Python 3.x
* Git
* YouTube Data API v3 Key (from Google Cloud Console)
* Gemini API Key (from Google AI Studio)

## Installation and Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   cd athul-pp

```

2. Create and activate a virtual environment.
3. Install the required dependencies:
```bash
pip install -r requirements.txt

```


4. Create a `.env` file in the root directory and add your API keys:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

```



## Usage

Run the script from your terminal:

```bash
python main.py

```

When prompted, enter the topic you wish to learn (e.g., "Machine Learning") and the number of days you have available to study.

## Author

Athul P P

```

