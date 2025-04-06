import streamlit as st
import scripts.prompts as prompt
import ai_models.gemini_models as gemini_model

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
            response= gemini_model.get_gemini_response(question)
            print(response)
            st.write(response)
elif page == "Prompts":
    st.title("Prompts")

    # Expandable sections for each text input
    with st.expander("📖 SQL PROMT"):
        st.write(prompt.SQL_PREFIX)
    
    with st.expander("📚 SCHEMA_PROMPT"):
        st.write(prompt.SCHEMA_PROMPT)

