from openai import OpenAI

def get_llm_response(chunk_text):
    """Generates a response using the LLM based on the relevant chunk of text."""
    client = OpenAI(api_key="your_openai_api_key")

    messages = [
        {"role": "system", "content": "You are an assistant for driving and riding theory test preparation."},
        {"role": "user", "content": f"Summarize the following information and give key points:\n\n{chunk_text}"}
    ]

    response = client.chat_completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
