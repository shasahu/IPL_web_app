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

question = "Shows number of matches played in each stadium. And for each stadium show there Home Team."
description = "Analysis will show number of matches played per stadium over the year 2008-2020. Analysis will also show home teams for each of the stadium. Home teams of a particular stadium keep on changing over the year. We have shown from 2008-2020 for each stadium different Home Team associated to it."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()
           
def app():
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                write = writer(f)
                write.writerow([str(datetime.now()),"ANALYSIS","1 5/{}".format(question)])
                f.close()
        
        st.subheader(question)
        st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
        stadiums = pd.read_sql("select * from location",con=db_conn)
        stadiums['numbersOf'] = pd.read_sql("select count(*) as numbersOf from matches group by venueID",con=db_conn)
        
        fig = px.bar(stadiums,y='venue',x='numbersOf',hover_data=["city"])
        fig.update_layout(plot_bgcolor = "black")
        st.plotly_chart(fig)
        
        teams = pd.read_sql("select * from teams",con=db_conn)
        for i in range(stadiums.shape[0]):
                if(stadiums.iloc[i,3] != '-1'):
                        lst = [teams[teams['teamID'] == int(l)].iloc[0,1] for l in stadiums.iloc[i,3].split('-')]
                        st.write("Stadium "+stadiums.iloc[i,1]+","+stadiums.iloc[i,2]+" has home teams "+str(lst))
                else:
                        st.write("Stadium "+stadiums.iloc[i,1]+","+stadiums.iloc[i,2]+" is out of india , so no HOME TEAM") 
        