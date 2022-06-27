import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
# Clean Txt File
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
                 line = line.decode('ascii')
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
    f1.close()
    
# Process Cleaned File
def process_file():
    import pandas as pd
    import numpy as np
    session ='2020-21'
    headerRow = ['R.No.','Name','SUB1','MRK1','GRD1','SUB2','MRK2','GRD2',\
           'SUB3','MRK3','GRD3','SUB4','MRK4','GRD4','SUB5','MRK5',\
           'GRD5','SUB6','MRK6','GRD6','Res']
    df = pd.read_csv('out.txt', skipinitialspace=True, usecols=headerRow)
    scode = {row[0] : row[1] for _, row in pd.read_csv("subject_code.csv").iterrows()}
    df['SUB1']=df['SUB1'].map(scode)
    df['SUB2']=df['SUB2'].map(scode)
    df['SUB3']=df['SUB3'].map(scode)
    df['SUB4']=df['SUB4'].map(scode)
    df['SUB5']=df['SUB5'].map(scode)
    df['SUB6']=df['SUB6'].map(scode)
    
    # Column List Index Containing Marks
    cList=[3,6,9,12,15]
    # Convert Text to Number
    #df = df[headerRow].apply(pd.to_numeric,errors='coerce').fillna(df)
    #Calculating Total
    df['Total']= df.iloc[:,cList].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    #Calculating Percentage
    df['Per']= df.iloc[:,cList].apply(pd.to_numeric, errors='coerce').sum(axis=1)/5
    df_original = df
    df_original['SUB6'] = df_original['SUB6'].fillna("")
    df_original['MRK6'] = df_original['MRK6'].fillna("")
    df_original['GRD6'] = df_original['GRD6'].fillna("")
    st.dataframe(df_original.style.format({"Total": "{:.0f}","Per": "{:.2f}"}))
    
    def analy(subject):
        df1 = df[ (df.SUB1 == subject)][['Name', 'SUB1','MRK1','GRD1']]
        df1.columns = ['Name', 'Sub','MRK','GRD']

        df2 = df[ (df.SUB2 == subject)][['Name', 'SUB2','MRK2','GRD2']]
        df2.columns = ['Name', 'Sub','MRK','GRD']

        df3 = df[ (df.SUB3 == subject)][['Name', 'SUB3','MRK3','GRD3']]
        df3.columns = ['Name', 'Sub','MRK','GRD']

        df4= df[ (df.SUB4 == subject)][['Name', 'SUB4','MRK4','GRD4']]
        df4.columns = ['Name', 'Sub','MRK','GRD']

        df5 = df[ (df.SUB5 == subject)][['Name', 'SUB5','MRK5','GRD5']]
        df5.columns = ['Name', 'Sub','MRK','GRD']


        # Consider Additional Subject
        #df6 = df[ (df.SUB6 == subject)][['Name', 'SUB6','MRK6','GRD6']]
        #df6.columns = ['Name', 'Sub','MRK','GRD']

        df_sub = df1.append(df2, ignore_index = True) 

        df_sub = df_sub.append(df3, ignore_index = True)

        df_sub = df_sub.append(df4, ignore_index = True)

        df_sub = df_sub.append(df5, ignore_index = True)

        #df_sub = df_sub.append(df6, ignore_index = True)

        # Sorted Dataframe of Subject
        df_sub = df_sub.loc[pd.to_numeric(df_sub.MRK, errors='coerce').sort_values(ascending=False).index]
        return(df_sub)
        
    df_sub = pd.DataFrame()
    for i in scode:
         df_sub = df_sub.append(analy(scode[i])) # Creating Dataframe of all the subjects using Function analy

    df_sub_A=df_sub[pd.to_numeric(df_sub['MRK'], errors='coerce').notnull()]

    # Converting Marks to Numbers
    df_sub_A=df_sub_A[['Name', 'Sub', 'MRK','GRD']].apply(pd.to_numeric,errors='coerce').fillna(df_sub_A)
    st.dataframe(df_sub)

    grade_count = df_sub_A.astype(str).groupby(['Sub','GRD']).size().reset_index(name='Observation')
    st.dataframe(grade_count,400,200)
    
  
    #Creating Pie Chart
    all_sub_pie = px.pie(df_sub_A,title="Subject Grades",values='GRD',names='Sub')
    st.plotly_chart(all_sub_pie)
    
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .css-17ziqus {visibility: hidden;}
            """
st.markdown(hide_st_style,unsafe_allow_html=True)

data_file = st.file_uploader("Add text file !",type=["txt"])
if data_file:
    clean(data_file)
    process_file()
    st.write('Hello')
