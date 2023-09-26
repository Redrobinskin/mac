import markdown
import sys
from datetime import datetime, timedelta
import random
import re

def sanitize_title(title):
    return re.sub(r'[^a-zA-Z0-9 -]', '', title)

def create_blog_post(article):
    # Generate markdown from the content
    markdown_content = article['rewritten_content']

    # Get the current date and time
    now = datetime.now()

    # Subtract a random number of days (up to 30) from the current date
    random_date = now - timedelta(days=random.randint(0, 30))

    # Format it as a string
    date_str = random_date.strftime("%Y-%m-%d %H:%M:%S +1000")

    # Use this string to create a unique filename
    sanitized_title = sanitize_title(article['original_title'])
    filename = f"my-blog/_posts/{random_date.strftime('%Y-%m-%d')}-{sanitized_title.replace(' ', '-').lower()}.markdown"

    # Create the blog post file
    with open(filename, 'w') as file:
        # Write the header to the file
        file.write(f'''---
layout: post
title:  "{article['original_title']}"
date:   {date_str}
categories: jekyll update
---

''')
        # Write the content to the file
        file.write(markdown_content)

def parse_input(input_str):
    lines = input_str.split('\n')
    article = {}
    content_start = False
    for line in lines:
        if line.startswith('ID:'):
            article['id'] = line[4:]
        elif line.startswith('Original Title:'):
            article['original_title'] = line[16:]
        elif line.startswith('Original Content:'):
            article['original_content'] = line[18:]
        elif line.startswith('Rewritten Content:'):
            article['rewritten_content'] = line[19:]
            content_start = True  # Start capturing the content from this point forward
        elif content_start:
            article['rewritten_content'] += '\n' + line  # Add each subsequent line to the content

    return article

# Read the piped input
piped_input = sys.stdin.read()


# Parse the input into an article dictionary
article = parse_input(piped_input)

# Call the function with the article dictionary
create_blog_post(article)
