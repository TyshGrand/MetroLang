import streamlit as st
from   ai_models.ai_models_enum import AiModels as ai_models
import data_models.prompts as prompt
import ai_models.gemini_models as gemini_model
import data_models.user as user

def add_new_prompt():
    if st.session_state.new_prompt_key and st.session_state.new_prompt_value:
        st.session_state.prompts[st.session_state.new_prompt_key] = st.session_state.new_prompt_value
        st.session_state.new_prompt_key = ""
        st.session_state.new_prompt_value = ""
        # st.rerun() # Force a re-render to update the UI

def app_bar():
    col1, col2, col3 = st.columns([3, 2, 2])  # Adjust ratios as needed

    with col1:
        st.header("MetroLang: Your SQL AI Assistant")

    with col2:
        option1 = st.selectbox("Select User", ["admin", "guest"], key="role_select", on_change=on_role_change, )

    with col3:
        option2 = st.selectbox("Select Model", list(ai_models), key="model_select", on_change=on_model_change)


def on_role_change():
    st.session_state.selected_role = st.session_state.role_select
    st.write(f"Roles changed to: {st.session_state.selected_role}")

def on_model_change():
    st.session_state.selected_model = st.session_state.model_select
    st.write(f"Model changed to: {st.session_state.selected_model}")

def add_chat_history(quest_ans: str):
    pass
     # Initialize an empty list for chat history
    
def give_feedback(index, feedback_type):
    st.session_state.chat_history[index]['feedback'] = feedback_type
    if feedback_type == "negative":
        st.session_state[f'feedback_reason_{index}'] = "" # Initialize reason input

def save_feedback_reason(index):
    st.session_state.chat_history[index]['feedback_reason'] = st.session_state[f'feedback_reason_{index}']
    if  st.session_state[f'feedback_query_{index}']:
        st.session_state.chat_history[index]['feedback_query'] =  st.session_state[f'feedback_query_{index}']

def main():
    st.set_page_config(page_title="MetroLang", page_icon="💬", layout="wide")
    st.sidebar.image("views/assets/logo.png", use_container_width=True)
    st.sidebar.title("Navigation")



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
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    if "selected_role" not in st.session_state:
        st.session_state.selected_role = str(user.Role.ADMIN)
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = str(ai_models.GEMINI_PRO)

    page_list: list[str] = ["Home", "Chat History"]
    if st.session_state.selected_role == "admin":
        page_list += ["Prompts", "Feedback"]
    page = st.sidebar.radio("Go to", page_list) 



    app_bar()
    # st.write(f"Current Role: {st.session_state.selected_role}")
    # st.write(f"Current Model: {st.session_state.selected_model}")

    if "prompts" not in st.session_state:
        st.session_state.prompts = prompt.prompts_map

    st.title(page)
    match page:
        case "Home":
            # st.title = page_list[0]
        # Sidebar with Logo


            question=st.text_input("Input: ",key="input")

            submit=st.button("Ask the question")

            # if submit is clicked
            if submit:
                with st.spinner("Generating response... Please wait ⏳"):  # Loading animation
                    print(st.session_state.prompts)
                    response= gemini_model.get_gemini_response(question,prompt= str(st.session_state.prompts))
                    print(response)
                    st.write(response)
                    st.session_state.chat_history.append({"user": question, "assistant": response})



        case "Prompts" :
            if st.session_state.selected_role == str(user.Role.ADMIN):

                # # st.title("Prompts")

                # # Expandable sections for each text input
                # with st.expander("📖 SQL PROMT"):
                #     st.write(prompt.SQL_PREFIX)

                # with st.expander("📚 SCHEMA_PROMPT"):
                #     st.write(prompt.SCHEMA_PROMPT)
                st.subheader("Current Prompts")
                for key, value in st.session_state.prompts.items():
                    with st.expander(f"📖 {key}"):
                        st.write(value)
                
                # pdb.set_trace()  # Execution will pause here in the terminal
            

                st.subheader("Add a New Prompt")
                col_new_prompt_key, col_new_prompt_value = st.columns([2, 3])
                with col_new_prompt_key:
                    st.text_input("Prompt Name:", key="new_prompt_key")
                    st.button("+ Add Prompt", on_click=add_new_prompt)
                with col_new_prompt_value:
                    st.text_area("Prompt Value:", height=100, key="new_prompt_value")
                   

        case "Chat History":
            st.subheader("Chat History")
            if st.session_state.chat_history:
                for index, chat in enumerate(st.session_state.chat_history):
                    st.markdown(f"**👤  :** {chat['user']}")
                    st.markdown(chat['assistant'])
                    st.markdown("---")
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("👍", key=f"thumb_up_{index}", on_click=give_feedback, args=(index, "positive")):
                            pass # Button doesn't need to display anything after click
                    with cols[1]:
                        if st.button("👎", key=f"thumb_down_{index}", on_click=give_feedback, args=(index, "negative")):
                            pass # Button doesn't need to display anything after click

                    if chat.get('feedback') == 'negative':

                        with st.expander("What went wrong?"):
                                st.text_area("Please provide details:", key=f"feedback_reason_{index}")
                        with st.expander("Correct SQL(optional)"):
                                st.text_area("", key=f"feedback_query_{index}")
                        if st.button("Submit Feedback", key=f"submit_feedback_{index}", on_click=save_feedback_reason, args=(index,)):
                                pass # Feedback submitted on next rerun
                        
                    elif chat.get('feedback'):
                        st.write(f"Feedback: {chat['feedback']}")

                    st.markdown("---")

            else:
                st.info("No chat history available yet.")
            pass
        case "Feedback":
            positive_chats, negative_chats = [], []
            for chat in st.session_state.chat_history:
                if chat.get('feedback') == 'positive':
                    positive_chats.append(chat)
                elif chat.get('feedback') == 'negative':
                    negative_chats.append(chat)

            tab1, tab2 = st.tabs(["Positive Feedback", "Negative Feedback"])

            with tab1:
                if positive_chats:
                    for chat in positive_chats:
                        st.markdown(f"**User:** {chat['user']}")
                        st.markdown(chat['assistant'])
                        st.write(f"Feedback: {chat['feedback']}")
                        st.markdown("---")
                else:
                    st.info("No chats have received positive feedback yet.")

            with tab2:
                if negative_chats:
                    for index, chat in enumerate(negative_chats): # You're using index here
                        with st.expander(f"Negative Feedback {index}"):
                            st.markdown(f"**User:** {chat['user']}")
                            st.write("Response")
                            st.markdown(chat['assistant'])
                            st.write(f"Feedback: {chat['feedback']}")
                            if chat.get('feedback_reason'):
                                st.write(f"Reason: {chat['feedback_reason']}")
                else:
                    st.info("No chats have received negative feedback yet.")
if __name__ == "__main__":
    main()