import streamlit as st
def clean(data_file):
    with open("out.txt", "w") as f1:
        for line in data_file:
            line = line.decode('ascii')
            line=next(data_file)
            st.write(line)
            break
   
#form = st.form(key='my-form')
#txt = form.text_area('Enter your Result')
#submit = form.form_submit_button('Submit')

#if submit:
    #st.write(f'hello {name}')
    #st.text(f'{name}')
#    clean(txt)



data_file = st.file_uploader("Add text file !",type=["txt"])
if data_file:
    clean(data_file)
