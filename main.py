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
    df['Per'] = df.iloc[:,cList].apply(pd.to_numeric, errors='coerce').sum(axis=1)/5
    df['Per'] = df['Per'].round(decimals = 3)
    df['Per'] = df['Per'].apply(str)
    df_original = df
    df_original['SUB6'] = df_original['SUB6'].fillna("")
    df_original['MRK6'] = df_original['MRK6'].fillna("")
    df_original['GRD6'] = df_original['GRD6'].fillna("")
    df_original=df_original.set_index('R.No.')
    st.dataframe(df_original.astype(str))
    #st.dataframe(df_original.style.format({"Total": "{:.0f}","Per": "{:.2f}"}).astype(str))
    
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
    #st.dataframe(df_sub)

    subs = df_sub_A['Sub'].unique().tolist()

    show_subs = st.selectbox('Choose Subjects to Display',subs)

    st.dataframe(df_sub_A.loc[(df_sub_A['Sub'] == show_subs)]) # display DataFrame of Selected Subject

    grade_count = df_sub_A.astype(str).groupby(['Sub','GRD']).size().reset_index(name='Count')
    
    st.dataframe(grade_count.loc[(grade_count['Sub'] == show_subs)]) # display DataFrame of Selected Subject


    # Calculating School Result
    school_qpi = round(df_sub_A.mean()[['MRK']],2)
    school_pass = df[(df['Res']=='PASS')].count()[['Res']]
    school_fail = df[(df['Res']=='FAIL')].count()[['Res']]
    school_comp = df[(df['Res']=='COMP')].count()[['Res']]
    
    school_fail_students = df[(df['Res']=='FAIL')]
    school_comp_students = df[(df['Res']=='COMP')]
    
    data = [["School QPI",float(school_qpi)],["Pass",int(school_pass)],["Fail",int(school_fail)],["Compartment",int(school_comp)]]
    qpi_df = pd.DataFrame(data, columns = ['Index', 'Values']) 
    
    #st.dataframe(df_sorted.head())
    st.write("School QPI: ",float(school_qpi))
    st.write("Pass: ",int(school_pass))
    st.write("Fail: ",int(school_fail))
    st.write("Compartment: ",int(school_comp))
    if not school_fail_students.empty:
      st.write('------- FAIL --------------')
      st.write(school_fail_students)
    if not school_comp_students.empty:
      st.write('------- COMPARTMENT --------------')
      st.write(school_comp_students)
    
    # <---------------  Creating Analysis DataFrames Subjectwise   ----------------------->
    
    df_count = df_sub_A.groupby('Sub').count()[['Name']]
    df_count.columns = ['Appeared']
    
    df_pass = df_sub_A[\
         (df_sub_A['GRD'] =='A1') | (df_sub_A['GRD'] =='A2') |\
         (df_sub_A['GRD'] =='B1') | (df_sub_A['GRD'] =='B2') |\
         (df_sub_A['GRD'] =='C1') | (df_sub_A['GRD'] =='C2') |\
         (df_sub_A['GRD'] =='D1') | (df_sub_A['GRD'] =='D2')\
         ].groupby('Sub').count()[['GRD']]
    df_pass.columns = ['Pass']
    
    df_fail = df_sub_A[\
         (df_sub_A['GRD'] !='A1') & (df_sub_A['GRD'] !='A2')&\
         (df_sub_A['GRD'] !='B1') & (df_sub_A['GRD'] !='B2')&\
         (df_sub_A['GRD'] !='C1') & (df_sub_A['GRD'] !='C2')&\
         (df_sub_A['GRD'] !='D1') & (df_sub_A['GRD'] !='D2')\
         ].groupby('Sub').count()[['GRD']]
    df_fail.columns = ['Fail']
    
    df_100 = df_sub_A[(df_sub_A['MRK']==100)].groupby('Sub').count()[['MRK']]
    df_100.columns = ['100']
    
    df_95 = df_sub_A[(df_sub_A['MRK']>95)].groupby('Sub').count()[['MRK']]
    df_95.columns = ['95 & Above']
    
    df_90 = df_sub_A[(df_sub_A['MRK']>90)].groupby('Sub').count()[['MRK']]
    df_90.columns = ['90 & Above']
    
    df_85 = df_sub_A[(df_sub_A['MRK']>85)].groupby('Sub').count()[['MRK']]
    df_85.columns = ['85 & Above']
    
    df_80 = df_sub_A[(df_sub_A['MRK']>80)].groupby('Sub').count()[['MRK']]
    df_80.columns = ['80 & Above']
    
    df_75 = df_sub_A[(df_sub_A['MRK']>75)].groupby('Sub').count()[['MRK']]
    df_75.columns = ['75 & Above']
    
    df_70 = df_sub_A[(df_sub_A['MRK']>70)].groupby('Sub').count()[['MRK']]
    df_70.columns = ['70 & Above']
    
    df_65 = df_sub_A[(df_sub_A['MRK']>65)].groupby('Sub').count()[['MRK']]
    df_65.columns = ['65 & Above']
    
    df_60 = df_sub_A[(df_sub_A['MRK']>60)].groupby('Sub').count()[['MRK']]
    df_60.columns = ['60 & Above']
    
    df_55 = df_sub_A[(df_sub_A['MRK']>55)].groupby('Sub').count()[['MRK']]
    df_55.columns = ['55 & Above']
    
    df_50 = df_sub_A[(df_sub_A['MRK']>50)].groupby('Sub').count()[['MRK']]
    df_50.columns = ['50 & Above']
    
    df_45 = df_sub_A[(df_sub_A['MRK']>45)].groupby('Sub').count()[['MRK']]
    df_45.columns = ['45 & Above']
    
    df_40 = df_sub_A[(df_sub_A['MRK']>40)].groupby('Sub').count()[['MRK']]
    df_40.columns = ['40 & Above']
    
    df_A1 = df_sub_A[(df_sub_A['GRD']=='A1')].groupby('Sub').count()[['GRD']]
    df_A1.columns = ['A1']
    
    df_A2 = df_sub_A[(df_sub_A['GRD']=='A2')].groupby('Sub').count()[['GRD']]
    df_A2.columns = ['A2']
    
    df_B1 = df_sub_A[(df_sub_A['GRD']=='B1')].groupby('Sub').count()[['GRD']]
    df_B1.columns = ['B1']
    
    df_B2 = df_sub_A[(df_sub_A['GRD']=='B2')].groupby('Sub').count()[['GRD']]
    df_B2.columns = ['B2']
    
    df_C1 = df_sub_A[(df_sub_A['GRD']=='C1')].groupby('Sub').count()[['GRD']]
    df_C1.columns = ['C1']
    
    df_C2 = df_sub_A[(df_sub_A['GRD']=='C2')].groupby('Sub').count()[['GRD']]
    df_C2.columns = ['C2']
    
    df_D1 = df_sub_A[(df_sub_A['GRD']=='D1')].groupby('Sub').count()[['GRD']]
    df_D1.columns = ['D1']
    
    df_D2 = df_sub_A[(df_sub_A['GRD']=='D2')].groupby('Sub').count()[['GRD']]
    df_D2.columns = ['D2']
    
    qpi = round(df_sub_A.groupby('Sub').mean()[['MRK']],2)
    qpi.columns = ['QPI']
    
    # Joining all Datatframes to make a single Analysis Dataframe
    analysis = pd.concat([qpi,df_count,df_pass,df_fail,\
                          df_100,df_95,df_90,df_85,df_80,df_75,df_70,df_65,df_60,df_55,df_50,df_45,df_40,\
                          df_A1,df_A2,df_B1,df_B2,df_C1,df_C2,df_D1,df_D2],axis=1,sort=False)
    st.dataframe(analysis)
  
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .row_heading.level0 {display:none;}
            .blank {display:none;}
            .css-17ziqus {visibility: hidden;}
            """
st.markdown(hide_st_style,unsafe_allow_html=True)

data_file = st.file_uploader("Add text file !",type=["txt"])
if data_file:
    clean(data_file)
    process_file()
    st.balloons()
