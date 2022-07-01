import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
st.set_page_config(layout="wide",page_icon="rocket",page_title="CBSE XII Result Analysis")

# Remove and Inject CSS  
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            .row_heading.level0 {display:none;}
            .blank {display:none;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .css-17ziqus {visibility: hidden;}
            .viewerBadge_link__1S137 {visibility: hidden;}
            """

st.markdown(hide_st_style,unsafe_allow_html=True)

# Check Uplaoded File
data_file = st.file_uploader("upload")
#data_file = st.file_uploader("",type=["txt"],help="Uplaod File Recieved From CBSE. Don't Make Any Changes to the File Upload as it is after Downloading")
if not data_file:
  st.stop()
    #clean(data_file)
    #process_file()
    #st.balloons()
school_code = data_file.name[:-4]
clean_file = school_code+"_clean.txt"
excel_file = school_code+".xlsx"
# Cleaning File
with open(clean_file, "w") as f1:
    f1.write('R.No.'+','+'Name'+','+'SUB1'+','+'MRK1'+','+'GRD1'+','+\
    'SUB2'+','+'MRK2'+','+'GRD2'+','+'SUB3'+','+'MRK3'+','+'GRD3'+','+\
    'SUB4'+','+'MRK4'+','+'GRD4'+','+'SUB5'+','+'MRK5'+','+'GRD5'+','+\
    'SUB6'+','+'MRK6'+','+'GRD6'+','+'we'+','+'hp'+','+'gs'+','+'Res')
    f = data_file
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

# Making First Data Frame
headerRow = ['R.No.','Name','SUB1','MRK1','GRD1','SUB2','MRK2','GRD2',\
           'SUB3','MRK3','GRD3','SUB4','MRK4','GRD4','SUB5','MRK5',\
           'GRD5','SUB6','MRK6','GRD6','Res']
df = pd.read_csv(clean_file, skipinitialspace=True, usecols=headerRow)
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
df['SUB6'] = df['SUB6'].fillna("")
df['MRK6'] = df['MRK6'].fillna("")
df['GRD6'] = df['GRD6'].fillna("")

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Original')
    workbook = writer.book
    worksheet = writer.sheets['Original']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('W:W', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    workbook.close()
    return processed_data
df_xlsx = to_excel(df)
st.download_button(label='📥 Download Current Result',data=df_xlsx ,file_name= excel_file)
df1 = pd.read_excel(excel_file,sheet_name='Original')
st.dataframe(df1)
