import streamlit as st
def clean(txt):
    with open("txt.txt","r") as f:
        for line in f:
            if '301' in line.split():
                st.write('\n')
                line1 = line.split()   #Reading first line in line1
                line=next(f)
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



txt = st.file_uploader("Add text file !")
if txt:
    clean(txt)
    #for line in uploaded_file:
        #st.write(line)
