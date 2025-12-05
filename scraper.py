from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_contents_and_links(url):
    if "http" not in url:
        print(f"Warning: Invalid URL '{url}' - does not contain http")
        return [f"Invalid URL: {url}. If you are an LLM, simply ignore this and output that the page was not found due to invalid URL", []]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    validLinks = [link for link in links if link]
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return [(title + "\n\n" + text)[:2_000], validLinks]