import streamlit as st
from services.ai_assistant import AIAssistant

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

st.header("🤖 AI Domain Assistant")
st.caption("Ask questions about Cybersecurity, Data Science, or IT Operations.")

#1. Initialize the AI Service
if "ai_assistant" not in st.session_state:
    st.session_state["ai_assistant"]= AIAssistant()

assistant =st.session_state["ai_assistant"]

#2.Display Chat History
# we iterate through the history to show previous messages
for message in assistant._history:
    role =message["role"]
    content= message["content"]
    
    with st.chat_message(role):
        st.markdown(content)

#Chat Input & Response Logic
if prompt:= st.chat_input("How can I help you?"):
    #Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    #Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response=assistant.send_message(prompt)
            st.markdown(response)