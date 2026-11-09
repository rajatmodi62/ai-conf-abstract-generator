import re
import sys
import requests
from bs4 import BeautifulSoup

year = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
out_name = 'neurips_titles_%d.txt' % year

r = requests.get('https://neurips.cc/virtual/%d/papers.html' % year)
r.raise_for_status()
soup = BeautifulSoup(r.content, 'html.parser')

pattern = re.compile(r'^/virtual/%d/poster/\d+$' % year)
titles = sorted({a.getText().strip() for a in soup.find_all('a', href=pattern) if a.getText().strip()}, key=str.lower)

with open(out_name, 'w', encoding='utf-8') as f:
    for title in titles:
        f.write(title + '\n')

print(len(titles), "titles ->", out_name)
