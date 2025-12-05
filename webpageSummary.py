import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI()

# --- This function summarizes the content of a single web page ---
# --- Parameter content: full text of a webpage ---
# --- Return: returns a summary of the website ---
def analyze_content(content, model):
    messages = [
        {"role": "system", "content": "you are a website analyzer. You are going to take in text content from a website and provide a long detailed summary to the user"},
        {"role": "user", "content": str(content)}
    ]
    response = openai.chat.completions.create(
        messages=messages,
        model=model
    )
    return response.choices[0].message.content