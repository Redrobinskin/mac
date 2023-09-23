import requests
from bs4 import BeautifulSoup
import sqlite3

# Krebs on Security URL
url = "https://krebsonsecurity.com/"

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('articles.db')

# Create a cursor object
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        url TEXT UNIQUE
    )
''')

# Get the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all articles
articles = soup.find_all('article')

for article in articles:
    # Extract title
    title = article.find('h2').text

    # Extract the URL of the full article
    url = article.find('a', class_='more-link')['href']

    # Check if article is already in database
    cursor.execute('SELECT * FROM articles WHERE url=?', (url,))
    if cursor.fetchone() is not None:
        print(f'Skipping {url} - already in database')
        continue

    # Send a GET request to the full article URL
    response = requests.get(url)

    # Parse the HTML content of the full article
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the content of the full article
    content = soup.find('div', class_='entry-content').text

    # Insert scraped data into table
    cursor.execute('''
        INSERT INTO articles (title, content, url) VALUES (?, ?, ?)
    ''', (title, content, url))

# Commit changes and close connection
conn.commit()
conn.close()
