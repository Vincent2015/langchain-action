from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from tools.ParsingTool import letter_parser

def generate_letter(information:str):
    
    letter_template = """
    下面是这个人的微博信息{information}
    请你帮我：
    1.写一个简单的总结
    2.挑两件有趣的事情说一说。
    3.找一些他比较感兴趣的事情
    4.写一篇热情洋溢的介绍信
    """

    prompt_template = PromptTemplate(
        input_variables=["information"],
        template = letter_template,
        partial_variables = {
            "format_insturctions": letter_parser.get_format_instructions()
        }
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm,prompt=prompt_template)

    result = chain.run(information= information);
    return result
