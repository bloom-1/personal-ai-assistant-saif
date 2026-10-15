import streamlit as st

st.title("Alfred")

if "messages" not in st.session_state:
    st.session_state["messages"] = []   #if "messages" is not in the st.session state, i create it so it won't cause an error

for msg in st.session_state["messages"]:    #for every message in the st.session
    with st.chat_message(msg["role"]):      # show the role of the person talking   
        st.write(msg["content"])            # show the content of the person's message


user_inp = st.chat_input("Message Alfred : ")

if user_inp :
    st.session_state["messages"].append({"role" : "user", "content" : user_inp}) #saving my message in the list
    with st.chat_message("user"):      # show the role of the person talking is user
        st.write(user_inp)  

    reply = "You said : " + user_inp    #put the reply in a variable
    st.session_state["messages"].append({"role": "assistant", "content" : reply})   #add it to the list
    with st.chat_message("assistant"):
        st.write(reply)     # "print" it

