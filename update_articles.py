# File: update_articles.py

import openai
import csv
import os
import random
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')

def fetch_news_articles():
    prompt = (
        "Search for 1 to 3 of the latest English news articles related to 'pyramid underground city', \
        'ancient civilization', or 'planetary generator'. For each article, return:\n"
        "- Title\n"
        "- Link\n"
        "- One-sentence summary\n"
        "- Image URL (if available, otherwise leave blank)\n"
        "Format it clearly and separately."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def parse_articles(text):
    articles = []
    blocks = text.strip().split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            title = lines[0].replace('Title: ', '').strip()
            summary = lines[1].replace('Summary: ', '').strip()
            link = lines[2].replace('Link: ', '').strip()
            image = lines[3].replace('Image: ', '').strip() if len(lines) > 3 else ''
            content = f"{summary} [Read more]({link})"
            articles.append((title, content, image))
    return articles

def append_to_csv(articles):
    with open('articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for title, content, image in articles:
            writer.writerow([title, content, image])

if __name__ == "__main__":
    try:
        raw_text = fetch_news_articles()
        articles = parse_articles(raw_text)
        if articles:
            append_to_csv(articles)
            print(f"Added {len(articles)} new articles.")
        else:
            print("No valid articles found.")
    except Exception as e:
        print(f"Error: {str(e)}")
