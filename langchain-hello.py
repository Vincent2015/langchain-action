import os
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")#'你的Open API Key'
#from langchain.llms import OpenAI #0.1.0
#from langchain_community.llms import OpenAI #0.2.0
from langchain_openai import OpenAI #0.3.0
llm = OpenAI(  
    model="gpt-3.5-turbo-instruct",
    temperature=0.8,
    max_tokens=60,)
response = llm.invoke("请给我的花店起个名")
print(response)
