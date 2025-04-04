from langchain_ollama import ChatOllama 

llama = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')

if __name__ == "__main__":
    print(llama.invoke('hi'))