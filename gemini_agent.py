import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)


def call_gemini_api(text, domain):
    prompt = f"""
    You are an AI agent for legal data entry automation.
    Domain: {domain}
    Task: Extract, validate, and standardize key entities from the following legal document text.
    Return a JSON with fields: parties, dates, amounts, addresses, case_numbers, and any other relevant entities.
    After the JSON, provide a brief legal advice or recommendation based on the document and extracted data.
    Text:
    {text}
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
