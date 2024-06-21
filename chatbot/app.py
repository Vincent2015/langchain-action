import os
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

from langchain.schema import HumanMessage,SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain

class CommandLineChatBot:
    def __init__(self) -> None:
        self.chat = ChatOpenAI()
        self.message = [SystemMessage(content="你是一个新手爸爸")]

    def chat_loop(self):
        print("开始聊天了！输入'exit'退出程序")
        while True:
            user_input = input("你:")
            if user_input.lower() == 'exit':
                print("再见")
                break
            self.message.append(HumanMessage(content=user_input))
            response = self.chat(self.message)
            print(f"chatBot:{response.content}")
class ChatbotWithMemory:
    def __init__(self) -> None:
        self.llm = ChatOpenAI()
        self.prompt = ChatPromptTemplate(
            messages = [
                SystemMessagePromptTemplate.from_template(template="你是一个花卉行家，你通常的回答不超过30个字" ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )

        self.memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

        self.conversation =LLMChain(
            llm=self.llm,
            prompt = self.prompt,
            memory = self.memory,
            verbose = True,
        )
    def chat_loop(self):
        print("开始聊天了！输入'exit'退出程序")
        while True:
            user_input = input("你:")
            if user_input.lower() == 'exit':
                print("再见")
                break
            response = self.conversation({"question":user_input})
            print(f"chatBot:{response['text']}")
'''
class ChatbotWithRetrieval:
    def __init__(self,dir) -> None:
        base_dir =dir
        documents=[]
        for file in os.listdir(base_dir):
            file_path = os.path.join(base_dir,file)
            if file.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                loader = TextLoader(file_path)
                documents.extend(loader.load())
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=10)
        all_splits = text_splitter.split_documents(documents)

        self.vertorstore = Qdrant.from_documents(
            documents = all_splits,
            embedding = OpenAIEmbeddings(),
            location = ":memory:",
            collection_name = "my_documents"
        )

        self.llm = ChatOpenAI()

        self.memory = ConversationSummaryMemory(
            llm = self.llm,
            memory_key = "chat_history",
            return_message = True
        )
        retriever = self.vertorstore.as_retriever()
        self.qa = ConversationalRetrievalChain.from_llm(self.llm,retriever=retriever,memory=self.memory)

    def chat_loop(self):
        print("开始聊天了！输入'exit'退出程序")
        while True:
            user_input = input("你:")
            if user_input.lower() == 'exit':
                print("再见")
                break
            response = self.qa(user_input)
            print(f"chatBot:{response['answer']}")     
'''
# ChatBot类的实现-带检索功能
class ChatbotWithRetrieval:

    def __init__(self, dir):

        # 加载Documents
        base_dir = dir # 文档的存放目录
        documents = []
        for file in os.listdir(base_dir): 
            file_path = os.path.join(base_dir, file)
            if file.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                loader = TextLoader(file_path)
                documents.extend(loader.load())
        
        # 文本的分割
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        all_splits = text_splitter.split_documents(documents)
        
        # 向量数据库
        self.vectorstore = Qdrant.from_documents(
            documents=all_splits, # 以分块的文档
            embedding=OpenAIEmbeddings(), # 用OpenAI的Embedding Model做嵌入
            location=":memory:",  # in-memory 存储
            collection_name="my_documents",) # 指定collection_name
        
        # 初始化LLM
        self.llm = ChatOpenAI()
        
        # 初始化Memory
        self.memory = ConversationSummaryMemory(
            llm=self.llm, 
            memory_key="chat_history", 
            return_messages=True
            )
        
        # 设置Retrieval Chain
        retriever = self.vectorstore.as_retriever()
        self.qa = ConversationalRetrievalChain.from_llm(
            self.llm, 
            retriever=retriever, 
            memory=self.memory
            )

    # 交互对话的函数
    def chat_loop(self):
        print("Chatbot 已启动! 输入'exit'来退出程序。")
        while True:
            user_input = input("你: ")
            if user_input.lower() == 'exit':
                print("再见!")
                break
            # 调用 Retrieval Chain  
            response = self.qa(user_input)
            print(f"Chatbot: {response['answer']}")

if __name__ == "__main__":
    #bot = CommandLineChatBot()
    #bot = ChatbotWithMemory()
    folder="../OneFlower"
    bot = ChatbotWithRetrieval(folder)
    bot.chat_loop()