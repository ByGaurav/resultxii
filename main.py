import streamlit as st
def clean(txt):
    for line in txt.splitlines():
        if '301' in line:
            st.write('\n')
            line1 = line.split()   #Reading first line in line1
            line=next(line)
            line = line.replace("F E", "FE")
            line2 =line.split() #Reading Second line in line2
            if len(line2)<12:
                line1.insert(line1.index('301')+5,'')
                for m in range(12-len(line2)):
                    line2.append('')
            # Starting adding rollnumber till name
            st.write(line1[0])
            st.write(',')
            #f1.write(line1[1])  # Uncomment to write gender
            #f1.write(',')   #Uncoment to write gender

#form = st.form(key='my-form')
#txt = form.text_area('Enter your Result')
#submit = form.form_submit_button('Submit')

#if submit:
    #st.write(f'hello {name}')
    #st.text(f'{name}')
#    clean(txt)



uploaded_file = st.file_uploader("Add text file !")
if uploaded_file:
    clean(uploaded_file)
    #for line in uploaded_file:
        #st.write(line)
