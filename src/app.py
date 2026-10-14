import streamlit as st

st.title("Alfred")

if "count" not in st.session_state :
    st.session_state["count"] = 0

clicked = st.button("+1")

st.write("Hello !")

if clicked :
    st.session_state["count"] += 1

st.write(f"Number of clicks : {st.session_state["count"]}")


