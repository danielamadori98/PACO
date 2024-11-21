# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://157.27.201.126:1234/v1", api_key="lm-studio")
prompt = "Always answer in rhymes. Talk about the future, and the past, and the present times."
completion = client.chat.completions.create(
  model="lmstudio-community/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": "Introduce yourself."}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)

