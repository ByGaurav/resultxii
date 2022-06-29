import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
st.set_page_config(layout="wide",page_icon="rocket",page_title="CBSE XII Result Analysis")

# Remove and Inject CSS  
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .row_heading.level0 {display:none;}
            .blank {display:none;}
            .css-17ziqus {visibility: hidden;}
            .viewerBadge_link__1S137 {visibility: hidden;}
            """

st.markdown(hide_st_style,unsafe_allow_html=True)

# Check Uplaoded File
data_file = st.file_uploader("",type=["txt"],help="Uplaod File Recieved From CBSE. Don't Make Any Changes to the File Upload as it is after Downloading")
if not data_file:
  st.stop()
    #clean(data_file)
    #process_file()
    #st.balloons()
school_code = data_file.name[:-4]
  
  