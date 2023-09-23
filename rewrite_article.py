import openai
import sys
import sqlite3

# Read the article from standard input
article = sys.stdin.read()

# Set up the OpenAI API with your API key
openai.api_key = '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'

# Use the chat models, which work well for multi-turn conversations
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a professional, witty cybersecurity consultant."},
        {"role": "user", "content": article}
    ]
)

# Print the rewritten article
print(response['choices'][0]['message']['content'])

# Get the rewritten article
rewritten_article = response['choices'][0]['message']['content']

# Print the total tokens used
print(f'Total tokens used: {response["usage"]["total_tokens"]}')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('articles.db')

# Create a cursor object
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rewritten_articles (
        id INTEGER PRIMARY KEY,
        original_title TEXT,
        original_content TEXT,
        rewritten_content TEXT
    )
''')

# Insert rewritten data into table
cursor.execute('''
    INSERT INTO rewritten_articles (original_title, original_content, rewritten_content) VALUES (?, ?, ?)
''', (article.split('\n')[0], article.split('\n')[1], rewritten_article))

# Commit changes and close connection
conn.commit()
conn.close()
