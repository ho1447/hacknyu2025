import streamlit as st
import pandas as pd

if "userHistory" not in st.session_state:
    st.session_state["userHistory"] = {}
if 'illness_history' not in st.session_state:
    st.session_state.illness_history = []
if 'vaccination_history' not in st.session_state:
    st.session_state.vaccination_history = []
if 'username' not in st.session_state:
       st.session_state.username = ''

def main():
    st.title("User History")
    if st.session_state.username != '':
        st.write("## User Information")
        st.write(st.session_state.userHistory)
        st.write("## Illness History")
        st.dataframe(pd.DataFrame(st.session_state.illness_history))
        st.write("## Vaccination History")
        st.dataframe(pd.DataFrame(st.session_state.vaccination_history))
    else:
        st.warning("Please log in to view user history.")

    

if __name__ == "__main__":
    main()