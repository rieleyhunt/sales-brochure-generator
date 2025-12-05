import os
from dotenv import load_dotenv
from openai import OpenAI
from gptLinkCleanser import fetch_page_and_all_relevant_links

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

brochure_prompt = """You are a model that will receive a summary of a website and it's relevant pages
                     Your goal is to display this information in a beautiful brochure format.
                     It needs to appeal to potential clients for any sales business.
                     You are trying to sell something, without making it obvious you are selling something
                  """ 

def brochureGenerator(url, model):
    brochure_input = fetch_page_and_all_relevant_links(url, model)
    openai = OpenAI()

    messages = [
        {"role": "system", "content": brochure_prompt},
        {"role": "user", "content": brochure_input}
    ]
    response = openai.chat.completions.create(
        messages=messages,
        model=model
    )
    return response.choices[0].message.content

url = "https://sprypoint.com"
model = "gpt-5.1"
brochure = brochureGenerator(url, model)
print(brochure)