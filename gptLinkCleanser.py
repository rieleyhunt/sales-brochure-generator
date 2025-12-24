import os
from dotenv import load_dotenv
from scraper import fetch_website_contents_and_links
from openai import OpenAI
import json
from typing import List
from webpageSummary import analyze_content

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI()


# --- This function takes a list of links and filters out irrelevant ones ---
# --- Parameter links: the function takes in a list of strings ---
# --- Return: returns a list of strings ---
def cleanse_links(links: List[str], model) -> List[str]:

    role = """You are a part of a function that receives 
    "a list of links and filters out irrelevant ones.
    "More specifically, you are being used in a business
    "application to generate sales material for that business 
    "Those links are directly scrapped off the businesses page.
    "You need to determine which ones might be useful for generating sales"
    "material, and filter out ones that look like junk or not relevant.
    "Make sure that the link is valid http and leads to somewhere.
    "You are to provide the output as a JSON. For example the JSON might look like:
    {
        "links": [
            {"type": "about page", "url": "https://full.url/goes/here/about"},
            {"type": "careers page", "url": "https://another.full.url/careers"}
        ]
    }
    """
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": str(links)}
    ]

    response = openai.chat.completions.create(
        messages=messages,
        model=model,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def fetch_page_and_all_relevant_links(url, model):
    content = analyze_content(fetch_website_contents_and_links(url)[0], model)
    relevant_links = json.loads(cleanse_links(fetch_website_contents_and_links(url)[1], model))
    result = f"## Landing Page:\n\n{content}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += analyze_content(link['url'], model)
    return result