import yfinance as yf

def get_company_news(ticker: str, limit: int = 5) -> list:
    """
    Retrieve latest news from Yahoo Finance.
    """

    stock = yf.Ticker(ticker)

    news = stock.news

    if not news:
        return []

    articles = []

    for article in news[:limit]:

        content = article.get("content", {})

        articles.append({
            "title": content.get("title"),
            "summary": content.get("summary"),
            "publisher": "Yahoo Finance",
            "published": content.get("pubDate"),
            "url": content.get("canonicalUrl", {}).get("url")
        })

    return articles