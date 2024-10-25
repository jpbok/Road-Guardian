import requests
import os

API_URL = "https://litellm.govtext.gov.sg/chat/completions"
API_KEY = os.getenv("GOVTEXT_API_KEY")

if not API_KEY:
    raise EnvironmentError("API key for GovText not found. Ensure 'GOVTEXT_API_KEY' is set in the environment.")

def query_govtext_api(messages):
    input_json = {
        "model": "gpt-4o-prd-gcc2-lb",
        "messages": messages
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"
    }

    response = requests.post(url=API_URL, json=input_json, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error querying GovText API: {response.status_code}, {response.text}")

def get_response_from_llm(query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant for driving and riding theory."},
        {"role": "user", "content": query}
    ]
    return query_govtext_api(messages)
