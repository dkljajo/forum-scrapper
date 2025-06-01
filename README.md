# 🕵️ LFCCro Forum Scraper

This Python tool uses **Selenium**, **Requests**, and **BeautifulSoup** to automatically log in and scrape posts from the [LFCCro](https://www.lfccro.com/forum/) forum. Extracted posts are saved into a CSV file for further analysis, searching, or visualization.

---

## 🚀 Features

- 🔐 Login via Selenium (requires credentials)
- 📑 Automatically collects all **boards**, **topics**, and **posts**
- 💾 Exports posts to `CSV` format (`posts.csv`)
- 💤 Includes polite scraping delays (`time.sleep`) for discreet and ethical usage

---

## 🧰 Requirements

- Python 3.7+
- [Google Chrome](https://www.google.com/chrome/) (or Firefox) + [ChromeDriver](https://chromedriver.chromium.org/) in your system `PATH`
- Required Python packages:

```bash
pip install selenium beautifulsoup4 requests

⚙️ Usage
Enter your forum credentials:

In the main section of the script (__main__), replace:

python
Copy
Edit
USERNAME = "user"
PASSWORD = "lozinka"
Run the script:

bash
Copy
Edit
python scraper.py
Result:
The script will generate a file called posts.csv containing:

topic_id

author

content

🧪 CSV Post-Processing Examples
You can analyze the exported data using:

Excel

Pandas (Python):

python
Copy
Edit
import pandas as pd
df = pd.read_csv("posts.csv")
print(df.head())



⚠️ Notes
Please respect the forum rules and use this tool strictly for educational or personal analytical purposes.

If the forum structure changes, some CSS selectors in the script may need to be updated.

📁 Project Structure
graphql
Copy
Edit
scraper.py        # Main scraping script
posts.csv         # Output CSV file (after running)
README.md         # This file
