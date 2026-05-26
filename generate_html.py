import os
import glob
from datetime import date
import re

def md_to_html(md_text):
    html = md_text
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', html)
    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
    html = html.replace('\n\n', '</p><p>')
    return '<p>' + html + '</p>'

files = sorted(glob.glob("news/*.md"), reverse=True)
articles_html = ""
for f in files:
    with open(f, encoding="utf-8") as fp:
        content = fp.read()
    date_str = os.path.basename(f).replace(".md", "")
    articles_html += '<div class="card"><div class="date">' + date_str + '</div>' + md_to_html(content) + '</div>\n'

if not articles_html:
    articles_html = "<p>No news yet.</p>"

template = open("template.html", encoding="utf-8").read() if os.path.exists("template.html") else None

html = "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>Daily AI News</title>\n</head>\n<body>\n<h1>Daily AI News</h1>\n" + articles_html + "\n<p>Last updated: " + str(date.today()) + "</p>\n</body>\n</html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated index.html")