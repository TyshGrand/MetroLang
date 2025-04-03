from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import itertools
from session import SessionData
from constants import Constants
import util
import sys
import asyncio


session = SessionData()
system_message = SystemMessagePromptTemplate.from_template("You are a helpful AI Assistant. You work as teacher for 5th grade students. You explain things in short and brief. Less than 50 words")

model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434/")

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




async def main():
    prompt = Constants.QUESTION_PROMT 
    print(prompt)


    chat_history = session.get(Constants.CHAT_HISTORY)

    chat_history.append(prompt)
    print("generating reponse")


    response = await generate_response(chat_history)

    session.insertChats({'user': prompt, 'assistant': response})

    print(response)

if __name__ == "__main__":
    asyncio.run(main())

       

