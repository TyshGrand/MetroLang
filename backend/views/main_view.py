import streamlit as st
import scripts.prompts as prompt
import ai_models.gemini_models as gemini_model

import sys
import os
print(f"Current Working Directory: {os.getcwd()}")
print("Python Path:")
for path in sys.path:
    print(path)
import data_models.user as user

def main():
    st.set_page_config(page_title="MetroLang", page_icon="💬", layout="wide")
    st.sidebar.image("views/assets/logo.png", use_container_width=True)
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

    def app_bar():
        col1, col2, col3 = st.columns([3, 2, 2])  # Adjust ratios as needed

        with col1:
            st.header("MetroLang: Your SQL AI Assistant")

        with col2:
            option1 = st.selectbox("Select User", user.Role)

        with col3:
            option2 = st.selectbox("Select Model", ["Gemini Pro", "LLama 3.2.3"])

        return option1, option2

    selected_db, selected_model = app_bar()

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
if __name__ == "__main__":
    main()