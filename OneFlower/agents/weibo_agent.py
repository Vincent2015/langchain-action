from tools.search_tool import get_UID
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent,Tool
from langchain.agents import AgentType

def lookup_V(flower_type:str):
    llm = ChatOpenAI(temperature = 0,model="gpt-3.5-turbo")
    
    template = """given the {flower} ,I want you to get a related 微博 UID
    Your answer should contain only a UID.
    The URL always starts with https://weibo.com/u
    for example,if https://weibo.com/u/1669879400 is her 微博,then the 1669879400 is her UID
    This is only the example don't give me this,but the actual UID"""

    prompt_template = PromptTemplate(
        input_variables=["flower"],template = template
    )

    tools = [
        Tool(
            name = "Crawl Google for 微博 page",
            func = get_UID,
            description = "useful for when you need get the 微博 UID" 
        )
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose = True
    )

    ID = agent.run(prompt_template.format_prompt(flower=flower_type))

    return ID;

#lookup_V(flower_type = "白牡丹")