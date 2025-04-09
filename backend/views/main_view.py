import streamlit as st
import scripts.prompts as prompt
import ai_models.gemini_models as gemini_model
import os 
print(f"Current Working Directory: {os.getcwd()}")


st.set_page_config(page_title="MetroLang", page_icon="💬", layout="wide")
st.sidebar.image("backend/views/assets/logo.png", use_container_width=True)
st.sidebar.title("Navigation")

page_list: list[str] = ["Home", "Prompts", "Chat History", "Train"]
page_index = page_list.index(st.sidebar.radio("Go to", page_list)) # Get the index of the selected item

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
st.header("MetroLang: Your SQL AI Assistant")

st.title(page_list[page_index])
match page_index:
    case 0:
        # st.title = page_list[0]
    # Sidebar with Logo


        question=st.text_input("Input: ",key="input")

        submit=st.button("Ask the question")

        # if submit is clicked
        if submit:
            with st.spinner("Generating response... Please wait ⏳"):  # Loading animation
                response= gemini_model.get_gemini_response(question)
                print(response)
                st.write(response)


    case 1 :
        # st.title("Prompts")

        # Expandable sections for each text input
        with st.expander("📖 SQL PROMT"):
            st.write(prompt.SQL_PREFIX)

        with st.expander("📚 SCHEMA_PROMPT"):
            st.write(prompt.SCHEMA_PROMPT)

    case 2:
        pass
