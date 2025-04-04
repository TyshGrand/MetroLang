import sys
import os
from dotenv import load_dotenv
import scripts.prompts as prompt
import streamlit as st
import google.generativeai as genai


load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model_prompt  = prompt.SQL_PREFIX + prompt.SCHEMA_PROMPT

def get_gemini_response(question):
    model=genai.GenerativeModel('gemini-2.0-pro-exp')
    response=model.generate_content([model_prompt,question])
    return response.text

st.set_page_config(page_title="MetroLang", page_icon="💬", layout="wide")
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Prompts"])

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #5A5A5A !important;
        }
       
    </style>
    """,
    unsafe_allow_html=True
)
if page == "Home":
    st.header("MetroLang: Your SQL AI Assistant")
    # Sidebar with Logo


    question=st.text_input("Input: ",key="input")

    submit=st.button("Ask the question")

    # if submit is clicked
    if submit:
        with st.spinner("Generating response... Please wait ⏳"):  # Loading animation
            response=get_gemini_response(question)
            print(response)
            st.write(response)
elif page == "Prompts":
    st.title("Prompts")

    # Expandable sections for each text input
    with st.expander("📖 SQL PROMT"):
        st.write(prompt.SQL_PREFIX)
    
    with st.expander("📚 SCHEMA_PROMPT"):
        st.write(prompt.SCHEMA_PROMPT)


def main():
    # models = genai.list_models()
    # for model in models:
    #     print(model.name)
    pass



       

if __name__ == "__main__":
    main()