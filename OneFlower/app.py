# 导入所需的库和模块
from flask import Flask, render_template, request, jsonify
from findbigV import find_bigV
import json


import os
#os.environ["OPENAI_API_KEY"] = 'your key'
#os.environ["SERPAPI_API_KEY"] = 'your key'
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
os.environ["SERPAI_API_KEY"] = ""
# 导入所取的库
import re
from agents.weibo_agent import lookup_V
from tools.general_tool import remove_non_chinese_fields
from tools.scraping_tool import get_data
from tools.textgen_tool import generate_letter

# 实例化Flask应用
app = Flask(__name__)

# 主页路由，返回index.html模板
@app.route("/")
def index():
    return render_template("index.html")

# 处理请求的路由，仅允许POST请求
@app.route("/process", methods=["POST"])
def dataprocess():
    # 获取提交的花的名称
    flower = request.form["flower"]
    # 使用find_bigV函数获取相关数据
    response_str = find_bigV(flower=flower)
    # 使用json.loads将字符串解析为字典
    response = json.loads(response_str)

    # 返回数据的json响应
    return jsonify(
        {
            "summary": response["summary"],
            "facts": response["facts"],
            "interest": response["interest"],
            "letter": response["letter"],
        }
    )  
  
# 判断是否是主程序运行，并设置Flask应用的host和debug模式
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



'''
from flask import Flask,render_template,request,jsonify
import findbigV 
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process",methods=["POST"])
def process():
    flower = request.form["flower"]
    response_str = findbigV.findbig_V(flower=flower)

    result = json.loads(response_str)

    return jsonify(
        {
            "summary": result["summary"],
            "facts": result["facts"],
            "interest":result["interests"],
            "letter":result["letter"]
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
    '''