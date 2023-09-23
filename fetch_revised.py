import sqlite3
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Fetch rewritten articles from the database.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-id', type=int, help='The ID of the rewritten article to fetch.')
group.add_argument('-list', action='store_true', help='List all rewritten article IDs and titles.')
args = parser.parse_args()

# Connect to SQLite database
conn = sqlite3.connect('articles.db')

# Create a cursor object
cursor = conn.cursor()

if args.list:
    # Select all rewritten articles' IDs and original titles
    cursor.execute("SELECT id, original_title FROM rewritten_articles")

    # Fetch all rows from the last executed statement
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        print(f'ID: {row[0]}, Original Title: {row[1]}')
else:
    # Select the rewritten article with the provided ID
    cursor.execute("SELECT * FROM rewritten_articles WHERE id=?", (args.id,))

    # Fetch one row from the last executed statement
    row = cursor.fetchone()

    # Check if row exists
    if row is None:
        print(f'No rewritten article found with ID {args.id}')
    else:
        # Print the row
        print(f'ID: {row[0]}')
        print(f'Original Title: {row[1]}')
        print(f'Original Content: {row[2]}')
        print(f'Rewritten Content: {row[3]}\n')

# Close connection
conn.close()
