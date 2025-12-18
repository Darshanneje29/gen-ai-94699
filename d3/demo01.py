import streamlit as st

with st.form("registeration"):
    st.header("registeration form")
    first_name=st.text_input(key="fname",label="first_name")
    last_name=st.text_input(key="lname",label="last_name")
    age=st.slider("age",0,100,25,1)
    submit_button=st.form_submit_button("submit",type="primary")

if submit_button:
    err_message = ""
    is_error = False
    if not first_name:
        is_error = True
        err_message += "First name cannot be empty.\n"
    if not last_name:
        is_error = True
        err_message += "Last name cannot be empty.\n"
    if is_error:
        st.error(err_message)
    else:
        message = f"Successfully registered: {st.session_state['fname']} {st.session_state['lname']}.\nAge: {age}."
        st.success(message)