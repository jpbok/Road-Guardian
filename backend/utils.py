import openai

def get_llm_response(chunk_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for driving and riding theory."},
            {"role": "user", "content": f"Summarize the following text:\n\n{chunk_text}"}
        ],
        temperature=0.1,
        max_tokens=300
    )
    return response.choices[0].message["content"].strip()
