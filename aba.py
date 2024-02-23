import requests
import nltk

nltk.download('punkt')
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def scrape_and_summarize(url):
    try:
        # Fetch HTML content of Wikipedia article
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content of the article
        paragraphs = soup.select(".mw-parser-output p")
        article_content = "\n".join([p.text for p in paragraphs])

        # Tokenize the content
        parser = PlaintextParser.from_string(article_content, Tokenizer("english"))

        # Summarize the content to 50% of its size using LSA
        lsa_summarizer = LsaSummarizer()
        lsa_summary = lsa_summarizer(parser.document, sentences_count=int(len(parser.document.sentences) * 0.5))

        # Summarize the content to 50% of its size using LexRank
        lexrank_summarizer = LexRankSummarizer()
        lexrank_summary = lexrank_summarizer(parser.document, sentences_count=int(len(parser.document.sentences) * 0.5))
        return lsa_summary, lexrank_summary
    except Exception as e:
        print("Error:", e)


def main():
    num_urls = int(input("Enter the number of URLs to scrape: "))
    urls = []
    for i in range(num_urls):
        url = input(f"Enter URL {i + 1}: ")
        urls.append(url)

    for url in urls:
        print("\nScraping URL:", url)
        lsa_summary, lexrank_summary = scrape_and_summarize(url)
        if lsa_summary and lexrank_summary:
            print("LSA Summary Preview:")
            for sentence in lsa_summary:
                print(sentence)
            print("\nLexRank Summary Preview:")
            for sentence in lexrank_summary:
                print(sentence)
            print()


if _name_ == "_main_":
    main()