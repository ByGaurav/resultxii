import streamlit as st
def clean(txt):
    for line in txt:
        if "301" in line:
                 st.write("\n")
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
                 #st.write(line1[1])  # Uncomment to write gender
                 #st.write(',')   #Uncoment to write gender
                 
                 
                 lock = line1.index('301')
                 for i in range (2,lock):
                     st.write(line1[i])
                     st.write(' ')
                 # finshed adding till name
                 j=0
                 for i in range(lock,len(line1)):
                     st.write(',')
                     st.write(line1[i])

                     if len(line2)>j:


                          for k in range(j,j+2):
                               st.write(",")
                               st.write(line2[k])
                               
                          j=j+2
form = st.form(key='my-form')
txt = form.text_area('Enter your Result')
submit = form.form_submit_button('Submit')

if submit:
    #st.write(f'hello {name}')
    #st.text(f'{name}')
    clean(txt)

