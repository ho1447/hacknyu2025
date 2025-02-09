import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from pymongo import MongoClient 

# Initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=st.secrets["GEMINI_API_KEY"]
)

client = MongoClient(st.secrets["connection_string"])
db = client["hacknyu2025"]

if 'illness_history' not in st.session_state:
    st.session_state.illness_history = []
if 'vaccination_history' not in st.session_state:
    st.session_state.vaccination_history = []
if "userHistory" not in st.session_state:
    st.session_state["userHistory"] = {}
if 'username' not in st.session_state:
       st.session_state.username = ''

def fetch_user_hist():
    result = db["patient"].find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "user_id": 0, "created_at": 0 })
    for res in result:
        st.session_state.userHistory.update(res)
def fetch_user_illness():
        r1 = db["illness_history"].find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "illness_id": 0, "created_at": 0 })
        for ill in r1:
            st.session_state.illness_history.append(ill)
def fetch_user_vacc():
    vacc = db["vaccination_history"].find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "vaccination_id": 0, "vaccine_batch": 0, "created_at": 0 })
    for v in vacc:
        st.session_state.vaccination_history.append(v)

def generate_response(input_text):    
    # st.info(llm.invoke(input_text))
    response = llm.invoke(input_text)
    print(f"Gemini's Response: {response}")
    return response.content


def main():
    fetch_user_hist()
    fetch_user_illness()
    fetch_user_vacc()

    st.title("SicklySage")

    if st.session_state.username != '':
        with st.sidebar:
            if st.session_state.userHistory != {}:
                st.metric("Emergency Contact", st.session_state.userHistory["emergency_contact"])
            with st.expander("See Illnesses"):
                for ill in st.session_state.illness_history:
                    st.write(ill["illness_name"])
            with st.expander("See Vaccinations"):
                for vacc in st.session_state.vaccination_history:
                    st.write(vacc["vaccine_name"])
            # "[![Open GitHub Repository](https://github.com/codespaces/badge.svg)](https://github.com/ho1447/hacknyu2025)"

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hi, SicklySage is here to answer your questions about any symptoms you have! How can I help you?"}
            ]
        
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])


        if prompt := st.chat_input(placeholder="Ask a question"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Prompt engineering
            init_prompt = "You are an assistant for diagnosing illnesses. Use six sentences maximum and keep the answer concise."
            prompt = init_prompt + prompt + " Illness History: " + str(st.session_state.illness_history) + " Vaccination History: " + str(st.session_state.vaccination_history)
            print(prompt)

            # Send user's message to Gemini and get the response
            gemini_response = generate_response(prompt)

            # Display Gemini's response
            with st.chat_message("assistant"):
                st.markdown(gemini_response)

            # Add user and assistant messages to the chat history
            st.session_state.messages.append({"role": "assistant", "content": gemini_response})
    else:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hi, SicklySage is here to answer your questions about any symptoms you have! Please login to start asking questions."}
            ]
        
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])


if __name__ == "__main__":
    main()