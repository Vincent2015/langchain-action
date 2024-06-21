import os
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
from langchain_openai import OpenAI
llm = OpenAI(model_name="gpt-3.5-turbo-instruct",max_tokens=200)
text = llm.invoke("请给我写一句情人节红玫瑰的中文宣传语")
print(text)
