import feedparser
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os
import openai

openai.api_key = "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"

def generate_summary(text, max_tokens=50):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"请将以下正文简要概括为 {max_tokens} 个单词:\n\n{text}\n\n概括:",
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"生成摘要时出错: {str(e)}")
        return None

def generate_summary_feed(feed_url):
    try:
        parsed_feed = feedparser.parse(feed_url)

        if parsed_feed.bozo:
            raise Exception("无法解析 RSS 订阅源。请检查 URL 是否正确。")

        fg = FeedGenerator()
        fg.title(parsed_feed.feed.title)
        fg.link(href=parsed_feed.feed.link, rel='alternate')
        fg.description(parsed_feed.feed.description)

        for entry in parsed_feed.entries:
            content = BeautifulSoup(entry.get('summary', ''), 'html.parser').get_text()
            summary = generate_summary(content)
            if summary is None:
                summary = ' '.join(content.split()[:20]) + '...'
            fe = fg.add_entry()
            fe.title(entry.title)
            fe.link(href=entry.link, rel='alternate')
            fe.description(summary)

        return fg.rss_str(pretty=True)
    except Exception as e:
        return str(e)

def save_feed_to_file(feed_str, filename):
    if not os.path.exists('feeds'):
        os.makedirs('feeds')
    with open(f"feeds/{filename}", "wb") as f:
        f.write(feed_str)