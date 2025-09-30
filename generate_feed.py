import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html

# URL della pagina eventi
URL = "https://bct.comune.torino.it/eventi-attivita"

# Scarica la pagina
response = requests.get(URL, timeout=15)
soup = BeautifulSoup(response.content, "html.parser")

# Trova tutti i blocchi evento (usa la classe views-row)
event_blocks = soup.select(".views-row")

# Prepara struttura RSS
rss_items = []
# Limite di elementi: puoi aumentarlo se vuoi
for block in event_blocks[:50]:
    title_tag = block.select_one("h3 a")
    if not title_tag:
        continue

    # Titolo e link (escapati)
    raw_title = title_tag.text.strip()
    title = html.escape(raw_title)

    href = title_tag.get("href", "")
    if href.startswith("/"):
        link = "https://bct.comune.torino.it" + href
    else:
        link = href or URL
    link_escaped = html.escape(link)

    # Sottotitolo / descrizione
    description_tag = block.select_one(".field--name-field-sottotitolo")
    raw_description = description_tag.text.strip() if description_tag else ""
    description = html.escape(raw_description)

    # Date: cerca <time> all'interno del blocco
    date_tags = block.select(".field--name-field-da-a time")
    pub_date = None
    if len(date_tags) >= 1:
        date_text = date_tags[0].text.strip()
        try:
            # formato italiano dd/mm/YYYY
            pub_date = datetime.strptime(date_text, "%d/%m/%Y")
        except Exception:
            # fallback: prova l'attributo datetime se presente (es. 2025-03-21T12:00:00Z)
            dt_attr = date_tags[0].get("datetime", "")
            try:
                if dt_attr:
                    # fromisoformat richiede +00:00 al posto di Z
                    dt = dt_attr.replace("Z", "+00:00")
                    pub_date = datetime.fromisoformat(dt)
                else:
                    pub_date = datetime.utcnow()
            except Exception:
                pub_date = datetime.utcnow()
    else:
        pub_date = datetime.utcnow()

    pub_date_str = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Costruisce l'item RSS (valori già escapati)
    item = f"""    <item>
        <title>{title}</title>
        <link>{link_escaped}</link>
        <description>{description}</description>
        <pubDate>{pub_date_str}</pubDate>
    </item>
"""
    rss_items.append(item)

# Crea file RSS
rss_feed = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<rss version=\"2.0\">\n<channel>\n"
rss_feed += "    <title>Eventi BCT Torino</title>\n"
rss_feed += f"    <link>{html.escape(URL)}</link>\n"
rss_feed += "    <description>Ultimi eventi pubblicati sul sito delle Biblioteche civiche torinesi</description>\n"
rss_feed += "    <language>it-it</language>\n\n"
rss_feed += "".join(rss_items)
rss_feed += "</channel>\n</rss>\n"

# Scrivi su file XML
with open("rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("Feed RSS generato in rss.xml")
