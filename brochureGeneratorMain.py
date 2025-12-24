import os
from dotenv import load_dotenv
from openai import OpenAI
from gptLinkCleanser import fetch_page_and_all_relevant_links
import gradio as gr

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
        model=model,
        stream=True
    )
    result = ""
    for chunk in response:
        result += chunk.choices[0].delta.content or ""
        yield result

url = "https://rieley.ca"
model = "gpt-5-nano"

gradio_interface = gr.Interface(
    fn=brochureGenerator,
    inputs=[gr.Textbox(label="Website URL"), gr.Dropdown(choices=["gpt-4o", "gpt-5-nano"], label="Model")],
    outputs="markdown",
    flagging_mode="never",
    title="Sales Brochure Generator",
    examples=[["https://rieley.ca", "gpt-5-nano"], ["https://sprypoint.com", "gpt-5-nano"]]
)

gradio_interface.launch(inbrowser=True, share=True)