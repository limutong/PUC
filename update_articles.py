from openai import OpenAI
import csv
import os
import random
import re
from datetime import datetime

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def fetch_news_articles():
    today = datetime.today().strftime('%Y-%b-%d')  # 比如 2025-Apr-26

    prompt = (
        f"Today is {today}. Please find 1 to 3 latest English news articles related to 'pyramid underground city', "
        f"'ancient civilization', or 'planetary generator'. For each article, return:\n"
        "- Title: (only clean title text)\n"
        "- Summary: (brief 1-2 sentences summary)\n"
        "- Link: (full direct article link, not homepage)\n"
        "- Image URL: (direct image URL from the article, if no image, leave empty)\n"
        "No markdown formatting. Only plain text output."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_articles(text):
    articles = []
    today = datetime.today().strftime('%Y-%b-%d')
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

            # 提取链接
            match = re.search(r'\((https?://[^\)]+)\)', link_line)
            if match:
                link = match.group(1)
            else:
                link = link_line

            # 提取图片链接
            match_img = re.search(r'\((https?://[^\)]+)\)', image_line)
            if match_img:
                image = match_img.group(1)
            else:
                image = image_line

            title = f"{today} {title_line}"
            # ✅ 正确处理：Summary正文 + [Read more](链接)
            if link:
                content = f"{summary_line} [Read more]({link})"
            else:
                content = summary_line

            articles.append((title, content, image))
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
