import requests

try:
    r = requests.get("https://huggingface.co", timeout=10)
    print("HF:", r.status_code)
except Exception as e:
    print("HF ERROR:", e)

try:
    r = requests.get("https://api-inference.huggingface.co", timeout=10)
    print("API:", r.status_code)
except Exception as e:
    print("API ERROR:", e)