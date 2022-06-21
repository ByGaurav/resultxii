import streamlit as st
def clean(txt):
    for line in txt:
<<<<<<< HEAD
        st.text(line)
=======
        if "301" in line:
            st.text("H")
>>>>>>> 69c4e01cbd19fe6386f4804609929ab5084e3349

form = st.form(key='my-form')
txt = form.text_area('Enter your Result')
submit = form.form_submit_button('Submit')

if submit:
    #st.write(f'hello {name}')
    #st.text(f'{name}')
    clean(txt)

