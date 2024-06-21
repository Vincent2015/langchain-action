from openai import OpenAI
import os
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
response = client.completions.create(
  model = "gpt-3.5-turbo-instruct",
  temperature = 0.5,
  max_tokens = 100,
  prompt = "请给我的花店起5个备选名字"
)

print(response.choices[0].text.strip())

