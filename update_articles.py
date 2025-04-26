# File: update_articles.py

import openai
import csv
import os
from datetime import datetime

# 读取环境变量里的OpenAI Key
openai.api_key = os.getenv('OPENAI_API_KEY')

def fetch_new_article():
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Generate a new short discovery related to ancient pyramid technology. Output strictly in this format:\nTitle: <title>\nContent: <content>\nImage: <image filename> (can be fictional)"}
        ]
    )
    text = response['choices'][0]['message']['content']
    lines = text.strip().split('\n')
    title = lines[0].replace('Title: ', '').strip()
    content = lines[1].replace('Content: ', '').strip()
    image = lines[2].replace('Image: ', '').strip()
    return title, content, image

def append_to_csv(title, content, image):
    with open('articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([title, content, image])

if __name__ == "__main__":
    title, content, image = fetch_new_article()
    append_to_csv(title, content, image)
    print(f"Added new article: {title}")
