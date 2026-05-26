import os
import requests
from datetime import date, timedelta

def fetch_ai_news():
    API_KEY = os.environ["NEWSAPI_KEY"]
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "artificial intelligence OR AI",
        "language": "en",
        "sortBy": "popularity",
        "pageSize": 10,
        "apiKey": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    print(f"API status: {response.status_code}")
    print(f"Total results: {data.get('totalResults', 0)}")

    if response.status_code != 200:
        print(f"API Error: {data.get('message', 'Unknown error')}")
        raise SystemExit(1)

    articles = data.get("articles", [])

    if not articles:
        print("No articles found, creating placeholder file.")
        articles = []

    lines = [f"# 🤖 Top 3 AI News – {yesterday}\n"]
    for i, a in enumerate(articles[:3], 1):
        lines.append(f"## {i}. {a['title']}")
        lines.append(f"**Source:** {a['source']['name']}  ")
        lines.append(f"**URL:** {a['url']}  ")
        lines.append(f"\n{a.get('description', 'No description.')}\n")
        lines.append("---")

    if not articles:
        lines.append("*No AI news found for this date.*")

    output_path = f"news/{yesterday}.md"
    os.makedirs("news", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved: {output_path}")

if __name__ == "__main__":
    fetch_ai_news()