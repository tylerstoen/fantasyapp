import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="Tyler's Fantasy Football App", 
                   initial_sidebar_state="expanded",
                   layout="wide", 
                   page_icon=":football:")

st.sidebar.title("Pages")

st.title("Tyler's Fantasy Football App")

st.subheader("Welcome to my Fantasy Football App")

#st.image(os.path.join(os.getcwd(), "static", "logo.png"), width=200)

st.markdown("Here you can find my latest player rankings and ADP. " \
            "You can also create your own rankings by dragging and dropping players. " \
            "Choose from the rankings options in the side.")

st.divider()

# st.subheader("Player Rankings")


# form_inputs = {
#     "Email": None
# }

# with st.form(key="signup_form"):
#     st.subheader("Sign Up")
#     form_inputs["Email"] = st.text_input("Email")
#     submit_button = st.form_submit_button(label="Submit")
#     if submit_button:
#         if form_inputs["Email"]:
#             st.success("Thank you for signing up!")
#         else:
#             st.error("Please enter a valid email address.")



