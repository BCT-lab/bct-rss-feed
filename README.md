# Feed RSS Eventi BCT Torino

Questo progetto genera un file RSS a partire dalla pagina eventi del sito delle Biblioteche civiche torinesi.

## Requisiti
- Python 3.x
- pacchetti `requests` e `beautifulsoup4`

## Uso
1. Installa i pacchetti:
   ```bash
   pip install requests beautifulsoup4
   ```

2. Esegui lo script:
   ```bash
   python generate_feed.py
   ```

3. Il file `rss.xml` verrà generato nella stessa cartella.

Puoi pubblicare questo file su GitHub Pages o Netlify per renderlo accessibile via web.
