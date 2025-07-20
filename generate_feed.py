import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://bct.comune.torino.it/eventi-attivita"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
event_blocks = soup.select(".views-row")

rss_items = []
for block in event_blocks[:10]:
    title_tag = block.select_one("h3 a")
    if not title_tag:
        continue
    title = title_tag.text.strip()
    link = "https://bct.comune.torino.it" + title_tag.get("href")
    description_tag = block.select_one(".field--name-field-sottotitolo")
    description = description_tag.text.strip() if description_tag else ""

    date_tags = block.select(".field--name-field-da-a time")
    if len(date_tags) >= 1:
        pub_date = datetime.strptime(date_tags[0].text.strip(), "%d/%m/%Y")
    else:
        pub_date = datetime.now()

    rss_items.append(f"""
    <item>
        <title>{title}</title>
        <link>{link}</link>
        <description>{description}</description>
        <pubDate>{pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    </item>
    """)

rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Eventi BCT Torino</title>
    <link>{URL}</link>
    <description>Ultimi eventi pubblicati sul sito delle Biblioteche civiche torinesi</description>
    <language>it-it</language>
    {''.join(rss_items)}
</channel>
</rss>
"""

with open("rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("Feed RSS generato in rss.xml")
