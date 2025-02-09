import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from pymongo import MongoClient 
import pandas as pd

# initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=st.secrets["GEMINI_API_KEY"]
)
connection_string = "mongodb+srv://phh242:hacknyu2025password@hacknyu2025.1lcf2.mongodb.net/?retryWrites=true&w=majority&appName=hacknyu2025"
client = MongoClient(connection_string)
db = client["hacknyu2025"]
collection = db["patient"]
illness = db["illness_history"]
vaccination = db["vaccination_history"]

if "userHistory" not in st.session_state:
    result = collection.find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "user_id": 0, "created_at": 0 })
    r1 = illness.find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "illness_id": 0, "created_at": 0 })
    vacc = vaccination.find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "vaccination_id": 0, "vaccine_batch": 0, "created_at": 0 })
    st.session_state["userHistory"] = {}
    for res in result:
        st.session_state.userHistory.update(res)
    print(st.session_state.userHistory)

def generate_response(input_text):    
    # st.info(llm.invoke(input_text))
    response = llm.invoke(input_text)
    print(f"Gemini's Response: {response}")
    return response.content

def main():

    st.title("SicklySage")

    with st.sidebar:
        st.metric("Emergency Contact", st.session_state.userHistory["emergency_contact"])
        with st.expander("See Illnesses"):
            st.write(["Amnesia", "Diabetes"])
            # st.metric("Emergency Contact", st.session_state.userHistory["emergency_contact"])
        # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        # "[![Open GitHub Repository](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    # with st.form("my_form"):
    #     text = st.text_area(
    #         "Enter text:",
    #         "What are the three key pieces of advice for learning how to code?",
    #     )
    #     submitted = st.form_submit_button("Submit")
    #     if submitted and openai_api_key.startswith("sk-"):
    #         generate_response(text)


    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, SicklySage is here to answer your questions about any symptoms you have! How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Ask a question"):
        prompt = prompt + " " + st.session_state.userHistory["emergency_contact"]
        print(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Send user's message to Gemini and get the response
        gemini_response = generate_response(prompt)

        # Display Gemini's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response)

        # Add user and assistant messages to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": gemini_response})

if __name__ == "__main__":
    main()