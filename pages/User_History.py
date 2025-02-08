import streamlit as st
from pymongo import MongoClient 
import pandas as pd

connection_string = ""
client = MongoClient(connection_string)
db = client["hacknyu2025"]
collection = db["patient"]

def main():
    st.title("User History")
    # st.write(collection.find_one())
    result = collection.find({"patient_id": 1},{ "_id": 0, "patient_id": 0, "user_id": 0, "created_at": 0 })
    df = pd.DataFrame(list(result))
    st.dataframe(df)
    # if "userHistory" not in st.session_state:
    #     st.session_state["userHistory"] = [
    #     ]
    # for res in result:
    #     st.session_state.userHistory.append(list(result))
    

if __name__ == "__main__":
    main()