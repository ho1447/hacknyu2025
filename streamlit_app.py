import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# initialization
GEMINI_API_KEY=""
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GEMINI_API_KEY
)

def generate_response(input_text):    
    # st.info(llm.invoke(input_text))
    response = llm.invoke(input_text)
    print(f"Gemini's Response: {response}")
    return response.content

def main():

    st.title("🦜🔗 Quickstart App")

    # with st.sidebar:
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
            {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Ask a question"):
        for history in st.session_state.userHistory:
            for hist in history:
                prompt = prompt + " " + hist
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