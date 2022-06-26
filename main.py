import streamlit as st
def clean(data_file):
    for line in data_file:
        if '301' in line:
            st.write(line)
   
#form = st.form(key='my-form')
#txt = form.text_area('Enter your Result')
#submit = form.form_submit_button('Submit')

#if submit:
    #st.write(f'hello {name}')
    #st.text(f'{name}')
#    clean(txt)



data_file = st.file_uploader("Add text file !")
if data_file:
    clean(data_file)
    #for line in uploaded_file:
        #st.write(line)
