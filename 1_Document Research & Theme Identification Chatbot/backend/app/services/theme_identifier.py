from openai import OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def synthesize_themes(passages):
    prompt = (
        "Given the following document excerpts, identify common themes and return each "
        "theme with supporting document IDs:\n\n"
    )
    for i, (doc_id, text) in enumerate(passages):
        prompt += f"Document {doc_id}: {text}\n\n"
    prompt += "Return themes and citations."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response["choices"][0]["message"]["content"]
