import sqlite3
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Fetch articles from the database.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-id', type=int, help='The ID of the article to fetch.')
group.add_argument('-list', action='store_true', help='List all article IDs and titles.')
group.add_argument('-remove', type=int, help='The ID of the article to remove.')
args = parser.parse_args()

# Connect to SQLite database
conn = sqlite3.connect('articles.db')

# Create a cursor object
cursor = conn.cursor()

if args.list:
    # Select all articles
    cursor.execute("SELECT id, title FROM articles")

    # Fetch all rows from the last executed statement
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        print(f'ID: {row[0]}, Title: {row[1]}')
elif args.remove is not None:
    # Delete the article with the provided ID
    cursor.execute("DELETE FROM articles WHERE id=?", (args.remove,))

    # Commit the changes
    conn.commit()

    print(f'Article with ID {args.remove} removed.')
else:
    # Select the article with the provided ID
    cursor.execute("SELECT * FROM articles WHERE id=?", (args.id,))

    # Fetch one row from the last executed statement
    row = cursor.fetchone()

    # Check if row exists
    if row is None:
        print(f'No article found with ID {args.id}')
    else:
        # Return the article as a string
        print(f'Title: {row[1]}\nContent: {row[2]}')

# Close connection
conn.close()
