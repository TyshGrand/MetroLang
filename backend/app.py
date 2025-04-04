from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
import itertools
from session import SessionData
from constants import Constants
import util
import sys
import scripts.prompts as promts
import asyncio
from database.connector import connector
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain.chains import create_sql_query_chain
from flask import Flask, request, jsonify
import requests
import gemini_models
import time


session = SessionData()
system_message = SystemMessagePromptTemplate.from_template("You are a helpful AI Assistant. You work as teacher for 5th grade students. You explain things in short and brief. Less than 50 words")

model = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')
db =  connector()

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response_text = gemini_models.get_gemini_response(question)
    return jsonify({"response": response_text})

def test_api():
    """ Function to test the API by making a request to itself """
    url = "http://127.0.0.1:5000/generate"
    data = {"question": "how many users have placed orders in the last month in every location"}
    time.sleep(2)  # Give Flask some time to start

    try:
        response = requests.post(url, json=data)
        print("API Response:", response.json())
    except Exception as e:
        print("Error hitting API:", e)


def agent():
    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    tools = toolkit.get_tools()
    print(tools)

    system_message = SystemMessage(content= promts.SQL_PREFIX)


    agent_executor = create_react_agent(model, tools, state_modifier=system_message, debug=False)
    question = "How many orders are there?"
    # question = "How many departments are there?"

    agent_executor.invoke({"messages": [HumanMessage(content=question)]})

    for s in agent_executor.stream(
        {"messages": [HumanMessage(content=question)]}
    ):
        print(s)
        print("----")

def sql_chain():
    sql_chain = create_sql_query_chain(model, db)
    sql_chain.get_prompts()[0].pretty_print()

    question = "how many orders are there? You MUST RETURN ONLY MYSQL QUERIES."
    response = sql_chain.invoke({'question': question}) 
    print(response)

    from scripts.llm import ask_llm
    from langchain_core.runnables import chain
    @chain
    def get_correct_sql_query(input):
        context = input['context']
        question = input['question']

        intruction = """
            Use above context to fetch the correct SQL query for following question
            {}

            Do not enclose query in ```sql and do not write preamble and explanation.
            You MUST return only single SQL query.
        """.format(question)

        response = ask_llm(context=context, question=intruction)

        return response
    response = get_correct_sql_query.invoke({'context': response, 'question': question})
    print(response)


@util.async_loader()
async def generate_response(chat_histroy):

    chat_template = ChatPromptTemplate.from_messages(chat_histroy)

    chain = chat_template|model|StrOutputParser()

    response = chain.invoke({})

    return response


def get_history():
    chat_history = [system_message]
    for chat in session.get(Constants.CHAT_HISTORY):
        prompt = HumanMessagePromptTemplate.from_template(chat['user'])
        chat_history.append(prompt)

        ai_message = AIMessagePromptTemplate.from_template(chat['assistant'])
        chat_history.append(ai_message)

    return chat_history

def main():
    
    # from multiprocessing import Process

    # flask_process = Process(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    # # flask_process.start()

    # # # Wait for server to start
    # time.sleep(3)  # Ensure Flask starts

    # # # Call the API
    # test_api()

    # # # Stop the Flask process (optional)
    # flask_process.terminate()

if __name__ == "__main__":
    main()
       

