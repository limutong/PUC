from openai import OpenAI
import csv
import os
import random
import re
from datetime import datetime

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def fetch_news_articles():
    today = datetime.today().strftime('%Y-%b-%d')  # 例如 2025-Apr-26

    prompt = (
        f"Today is {today}. Based on the following background, imagine and create 3 realistic English news articles:\n\n"
        "**Background:** In 2025, scientists have discovered a massive underground structure beneath the pyramids — long, cylindrical architectural elements that suggest a possible function as ancient energy generators, potentially harnessing Earth's magnetic field.\n\n"
        "Articles should sound credible, inspired by real-world reporting styles (e.g., National Geographic, BBC News, Archaeology Today).\n\n"
        "For each article, return exactly:\n"
        "- Title: (pure text title only)\n"
        "- Summary: (short paragraph summary only)\n\n"
        "No markdown. No links. No images. Separate different articles with an empty line."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content


def parse_articles(text):
    print("====== RAW GPT RESPONSE ======")
    print(text)
    print("====== END OF RAW GPT RESPONSE ======")
    articles = []
    today = datetime.today().strftime('%Y-%b-%d')

    # 直接按每一行来处理
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    # 每两行配成一篇文章
    for i in range(0, len(lines) - 1, 2):
        title_line = lines[i].replace('**Title**:', '').replace('Title:', '').strip()
        summary_line = lines[i+1].replace('**Summary**:', '').replace('Summary:', '').strip()

        title = f"{today} {title_line}"
        content = summary_line
        image = ""  # 没有图片

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
