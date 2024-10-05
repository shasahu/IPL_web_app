# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 17:06:50 2021

@author: 1605309
"""

import streamlit as st
from csv import writer
from datetime import datetime
import mysql.connector as mc
import plotly.express as px
import pandas as pd

question = "IPL matches which end up with Duckworth - Lewis - Stern method"
description = "The Duckworth–Lewis–Stern method (DLS) is a mathematical formulation designed to calculate the target score (number of runs needed to win) for the team batting second in a limited overs cricket match interrupted by weather or other circumstances. Analysis show a bar chart which shows number of matches which end up with Duckworth-Lewis-method year wise."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()
           
def app():
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                write = writer(f)
                write.writerow([str(datetime.now()),"ANALYSIS","1 3/{}".format(question)])
                f.close()
        
        st.subheader(question)
        st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
        year_dwlm = pd.read_sql("select substr(date,1,4) as year,count(*) numbersOf from duckworth_lewis_matches as m1, matches as m2 where m1.matchID = m2.matchID group by year",con=db_conn)
        
        fig = px.bar(year_dwlm,y='numbersOf',x='year')

        fig.update_layout(plot_bgcolor = "black")
        st.plotly_chart(fig)