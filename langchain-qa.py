import os
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")#'你的Open API Key'
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader

base_dir = "OneFlower"
documents=[]
for file in os.listdir(base_dir):
    file_path = os.path.join(base_dir,file)
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        loader = TextLoader(file_path)
        documents.extend(loader.load())

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

from langchain_community.vectorstores import Qdrant
#from langchain.embeddings import OpenAIEmbedding
#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

vertorstore = Qdrant.from_documents(
    documents = chunked_documents,
    embedding = OpenAIEmbeddings(),
    location = ":memory:",
    collection_name = "my_documents"
)

import logging
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
#from langchain_community.chains import RetrievaQA
from langchain.chains import RetrievalQA # RetrievalQA链

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

llm = ChatOpenAI(name="gpt-3.5-turbo",temperature =0)
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vertorstore.as_retriever(),llm=llm)

qa_chain = RetrievalQA.from_chain_type(llm,retriever=retriever_from_llm)

from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def home():
    if request.method == "POST":
        question = request.form.get("question")
        result = qa_chain({"query":question})
        return render_template('index.html',result=result)
    
    return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=5000)



    
   
