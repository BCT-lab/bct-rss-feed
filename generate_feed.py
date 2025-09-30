import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html

URL = "https://bct.comune.torino.it/eventi-attivita"
response = requests.get(URL, timeout=15)
soup = BeautifulSoup(response.content, "html.parser")
event_blocks = soup.select(".views-row")

rss_items = []
for block in event_blocks[:50]:
    title_tag = block.select_one("h3 a")
    if not title_tag:
        continue

    # Escaping per XML
    title = html.escape(title_tag.text.strip())

    href = title_tag.get("href", "")
    link = "https://bct.comune.torino.it" + href if href.startswith("/") else href or URL
    link = html.escape(link)

    description_tag = block.select_one(".field--name-field-sottotitolo")
    description = html.escape(description_tag.text.strip()) if description_tag else ""

    date_tags = block.select(".field--name-field-da-a time")
    if date_tags:
        date_text = date_tags[0].text.strip()
        try:
            pub_date = datetime.strptime(date_text, "%d/%m/%Y")
        except:
            dt_attr = date_tags[0].get("datetime", "")
            pub_date = datetime.fromisoformat(dt_attr.replace("Z", "+00:00")) if dt_attr else datetime.utcnow()
    else:
        pub_date = datetime.utcnow()

    pub_date_str = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')

    rss_items.append(f"""    <item>
        <title>{title}</title>
        <link>{link}</link>
        <description>{description}</description>
        <pubDate>{pub_date_str}</pubDate>
    </item>
""")

rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Eventi BCT Torino</title>
    <link>{html.escape(URL)}</link>
    <description>Ultimi eventi pubblicati sul sito delle Biblioteche civiche torinesi</description>
    <language>it-it</language>

{''.join(rss_items)}</channel>
</rss>
"""

with open("rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("Feed RSS generato in rss.xml")
