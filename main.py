import streamlit as st
st.write('Hello World')
txt = st.text_area('Text to analyze', "")
if st.button('Press Me'):
     st.write(txt)
