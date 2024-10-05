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

question = "IPL matches end up in Super Over for each IPL"
description = "A Super Over, also called a one-over eliminator or officially a one over per side eliminator, is a tie-breaking method used in limited-overs cricket matches, where both teams play a single, additional over of six balls to determine the winner of the match. A match which goes to a Super Over is officially declared a 'tie', and won by the team who score the most runs in the Super Over. Analysis show a bar chart which shows number of matches which end up with super over in each IPL."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()
           
def app():
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                write = writer(f)
                write.writerow([str(datetime.now()),"ANALYSIS","1 4/{}".format(question)])
                f.close()
        
        st.subheader(question)
        st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
        year_tie = pd.read_sql("select substr(date,1,4) as year,count(*) as numbersOf from matches where result='tie' group by year",con=db_conn)
        
        fig = px.bar(year_tie,y='numbersOf',x='year')

        fig.update_layout(plot_bgcolor = "black")
        st.plotly_chart(fig)