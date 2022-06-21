import streamlit as st
def clean(txt):
    for line in txt:
        st.text(txt)
form = st.form(key='my-form')
txt = form.text_area('Enter your Result')
submit = form.form_submit_button('Submit')

if submit:
    #st.write(f'hello {name}')
    #st.text(f'{name}')
    clean(txt)

