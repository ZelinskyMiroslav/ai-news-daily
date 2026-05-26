import os
import requests
from datetime import date, timedelta

API_KEY = os.environ.get("NEWSAPI_KEY")
if not API_KEY:
    raise EnvironmentError("NEWSAPI_KEY environment variable is not set.")

yesterday = date.today() - timedelta(days=1)
date_str = yesterday.isoformat()  # YYYY-MM-DD

url = "https://newsapi.org/v2/everything"
params = {
    "q": "artificial intelligence",
    "from": date_str,
    "to": date_str,
    "language": "en",
    "sortBy": "popularity",
    "pageSize": 3,
    "apiKey": API_KEY,
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()
data = response.json()

articles = data.get("articles", [])
if not articles:
    print("No articles found for yesterday.")
    exit(0)

output_path = f"{date_str}.md"

lines = [f"# AI News — {date_str}\n"]
for i, article in enumerate(articles, start=1):
    title = article.get("title") or "No title"
    source = (article.get("source") or {}).get("name") or "Unknown source"
    summary = article.get("description") or "No summary available."
    article_url = article.get("url") or ""

    lines.append(f"## {i}. {title}\n")
    lines.append(f"**Source:** {source}\n")
    lines.append(f"{summary}\n")
    lines.append(f"[Read more]({article_url})\n")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Saved {len(articles)} articles to {output_path}")
