import feedparser

RSS_URL = "https://www.formula1.com/content/fom-website/en/latest/all.xml"


def get_news():
    feed = feedparser.parse(RSS_URL)

    message = ["📰 Top Headlines\n"]

    for article in feed.entries[:5]:
        message.append(f"• {article.title}")
        message.append(f"  {article.link}\n")

    return "\n".join(message)


if __name__ == "__main__":
    print(get_news())