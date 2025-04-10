import os
from dotenv import load_dotenv

import data_models.prompts as prompt
import google.generativeai as genai


load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model_prompt  = prompt.SQL_PREFIX + prompt.SCHEMA_PROMPT

def get_gemini_response(question, prompt : str = model_prompt):
    model=genai.GenerativeModel('gemini-2.0-pro-exp')
    response=model.generate_content([prompt,question])
    return response.text

def main():
    # models = genai.list_models()
    # for model in models:
    #     print(model.name)
    pass
       

if __name__ == "__main__":
    main()