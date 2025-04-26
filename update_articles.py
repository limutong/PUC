from openai import OpenAI
import csv
import os
import random
import re
from datetime import datetime

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def fetch_news_articles():
    prompt = (
        "Search for 1 to 3 of the latest English news articles related to 'pyramid underground city', "
        "'ancient civilization', or 'planetary generator'. For each article, return:\n"
        "- Title\n"
        "- Summary\n"
        "- Link\n"
        "- Image URL (if available, otherwise leave blank)\n"
        "Format it clearly and separately."
    )
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_articles(text):
    articles = []
    blocks = text.strip().split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            title_line = lines[0].replace('**Title**:', '').replace('Title:', '').strip()
            summary_line = lines[1].replace('**Summary**:', '').replace('Summary:', '').strip()
            link_line = lines[2].replace('**Link**:', '').replace('Link:', '').strip()
            image_line = ''
            if len(lines) > 3:
                image_line = lines[3].replace('**Image URL**:', '').replace('Image URL:', '').strip()

            # 处理link，提取出真正的URL
            match = re.search(r'\((https?://[^\)]+)\)', link_line)
            if match:
                link = match.group(1)
            else:
                link = link_line  # fallback

            # 处理image，提取URL
            match_img = re.search(r'\((https?://[^\)]+)\)', image_line)
            if match_img:
                image = match_img.group(1)
            else:
                image = image_line  # fallback

            content = f"{summary_line} [Read more]({link})"
            articles.append((title_line, content, image))
    return articles

def append_to_csv(articles):
    with open('articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for title, content, image in articles:
            writer.writerow([str(title), str(content), str(image)])

if __name__ == "__main__":
    try:
        raw_text = fetch_news_articles()
        articles = parse_articles(raw_text)
        if articles:
            append_to_csv(articles)
            print(f"✅ Update Success: Added {len(articles)} new articles.")
        else:
            print("⚠️ No valid articles found. GPT returned empty or invalid data.")
    except Exception as e:
        print(f"❌ Error during update: {str(e)}")
