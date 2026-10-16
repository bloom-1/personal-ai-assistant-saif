import streamlit as st
from alfred import save_history, start_messages, ask_alfred

AVATARS = {"user": "🦇", "assistant":"🤵"}

st.title("Alfred")

if "messages" not in st.session_state:
    st.session_state["messages"] = start_messages()   #loads alfred's personality + my info + history

for msg in st.session_state["messages"]:    #for every message in the st.session
    if msg["role"] != "system" :
        with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):      # show the role of the person talking   
            st.write(msg["content"])            # show the content of the person's message


user_inp = st.chat_input("Message Alfred : ")

if user_inp :
    st.session_state["messages"].append({"role" : "user", "content" : user_inp}) #saving my message in the list
    with st.chat_message("user", avatar= AVATARS["user"]):      # show the role of the person talking is user
        st.write(user_inp)  

    with st.spinner("Alfred is thinking..."):
        reply = ask_alfred(st.session_state["messages"])    #put the reply in a variable

    st.session_state["messages"].append({"role": "assistant", "content" : reply})   #add it to the list
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        st.write(reply)     # "print" it
    save_history(st.session_state["messages"])

