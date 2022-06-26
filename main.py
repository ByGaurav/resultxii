import streamlit as st
def clean(f):
    with open("out.txt", "w") as f1:
        f1.write('R.No.'+','+'Name'+','+'SUB1'+','+'MRK1'+','+'GRD1'+','+\
       'SUB2'+','+'MRK2'+','+'GRD2'+','+'SUB3'+','+'MRK3'+','+'GRD3'+','+\
       'SUB4'+','+'MRK4'+','+'GRD4'+','+'SUB5'+','+'MRK5'+','+'GRD5'+','+\
       'SUB6'+','+'MRK6'+','+'GRD6'+','+'we'+','+'hp'+','+'gs'+','+'Res')
        for line in f:
            line = line.decode('ascii')
             if "301" in line:
                 f1.write("\n")

                 line1 = line.split()   #Reading first line in line1
                 line=next(f)
                 line = line.replace("F E", "E")
                 line2 =line.split() #Reading Second line in line2
                 if len(line2)<12:
                      line1.insert(line1.index('301')+5,'')
                      for m in range(12-len(line2)):
                           line2.append('')

                 # Starting adding rollnumber till name
                 f1.write(line1[0].strip())
                 f1.write(',')
                 #f1.write(line1[1])  # Uncomment to write gender
                 #f1.write(',')   #Uncoment to write gender


                 lock = line1.index('301')
                 for i in range (2,lock):
                     f1.write(line1[i])
                     if i < lock-1:
                         f1.write(' ')
                 # finshed adding till name
                 j=0
                 for i in range(lock,len(line1)):
                     f1.write(',')
                     f1.write(line1[i])

                     if len(line2)>j:


                          for k in range(j,j+2):
                               f1.write(",")
                               f1.write(line2[k].strip())

                          j=j+2

   
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
