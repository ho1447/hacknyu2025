import streamlit as st
import pymongo

# Initialize connection.
# # Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["connection_string"])

db = init_connection().get_database('hacknyu2025')

# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
if 'form' not in st.session_state:
       st.session_state.form = ''
if 'userid' not in st.session_state:
       st.session_state.userid = ''


def select_signin():
    st.session_state.username = ''
    st.session_state.userid = ''
    st.session_state.illness_history = []
    st.session_state.vaccination_history = []
    st.session_state["userHistory"] = {}
    st.session_state.form = 'signin_form'

def select_signup():
    st.session_state.form = 'signup_form'

def user_update(name):
    st.session_state.username = name

def userid_update(userid):
    st.session_state.userid = userid

def get_userid(username):
    result = db["users"].find({"email": username},{ "_id": 0, "user_id":1 })
    for res in result:
        return res['user_id']

if st.session_state.username != '':
    st.write(f"You are logged in as {st.session_state.username.upper()}")

# Initialize Sign In or Sign Up forms
if st.session_state.form == 'signup_form' and st.session_state.username == '':
  
    signup_form = st.form(key='signup_form', clear_on_submit=False)
    # new_username = signup_form.text_input(label='Enter Username*')
    new_first_name = signup_form.text_input(label='Enter First Name*')
    new_last_name = signup_form.text_input(label='Enter Last Name*')
    new_email = signup_form.text_input(label='Enter Email Address*')
    new_password = signup_form.text_input(label='Enter Password*', type='password')
    new_password_conf = signup_form.text_input(label='Confirm Password*', type='password')
    # new_dob = signup_form.date_input(label='Enter Date of Birth')
    # new_contact = signup_form.text_input(label='Enter Contact Number')
    note = signup_form.markdown('**required fields*')
    signup = signup_form.form_submit_button(label='Sign Up')
    
    if signup:
        if '' in [new_first_name, new_last_name, new_email, new_password]:
            st.error('Some fields are missing')
        else:
            # if user_db.find_one({'log' : new_username}):
                # st.error('Username already exists')
            if db.users.find_one({'email' : new_email}):
                st.error('Email is already registered')
            else:
                if new_password != new_password_conf:
                    st.error('Passwords do not match')
                else:
                    user_update(new_email)
                    userid_update(db.users.count_documents({}) + 1)
                    db.users.insert_one({'user_id': db.users.count_documents({}) + 1, 'first_name': new_first_name, 'last_name': new_last_name, 'email' : new_email, 'password' : new_password})
                    st.success('You have successfully registered!')
                    # st.success(f"You are logged in as {new_email.upper()}")
                    st.switch_page('pages/Chat_Bot.py')
                    del new_password, new_password_conf

    login_request = st.button('Sign In', on_click=select_signin)

elif st.session_state.username == '':
    login_form = st.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username')
    user_pas = login_form.text_input(label='Enter Password', type='password')
    
    if db.users.find_one({'email' : username, 'password' : user_pas}):
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        if login:
            # st.success(f"You are logged in as {username.upper()}")
            userid_update(get_userid(username))
            st.switch_page('pages/Chat_Bot.py')
            del user_pas
    else:
        login = login_form.form_submit_button(label='Sign In')
        if login:
            st.error("Username or Password is incorrect. Please try again or create an account.")
    
    signup_request = st.button('Create Account', on_click=select_signup)

else:
    logout = st.button(label='Log Out', on_click=select_signin)
    st.rerun()
    # if logout:
        # st.session_state.username = ''
        # st.session_state.form = 'signin_form'
        # user_update('')

# 'Create Account' button
# if st.session_state.username == "" and st.session_state.form != 'signup_form':
    # signup_request = st.button('Create Account', on_click=select_signup)
