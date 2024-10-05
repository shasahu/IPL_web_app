# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 16:34:41 2021

@author: 1605309
"""

import streamlit as st
from csv import writer
from datetime import datetime
import mysql.connector as mc
import plotly.express as px
import pandas as pd
import numpy as np

question = "Teams Journey"
description = "Analysis show journey of each team. Year they played there first IPL and year they played there last IPL. Also included number of IPL tropy they won in there journey. Bar plot is shown team vs trophy won. And Line plot winner vs year (showing year-wise winners)."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()

        
def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","5 3/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    teams = pd.read_sql("select * from teams",con=db_conn)
    k = pd.read_sql("select unique(substr(date,1,4)) as year, max(matchID) as m from matches group by year",con=db_conn)
    w = pd.read_sql("select winner from matches where matchID in {}".format(tuple(k['m'])),con=db_conn)
    k['winners'] = [teams[teams['teamID'] == w.iloc[y][0]].iloc[0,1] for y in range(w.shape[0])]
    teams.columns = ['teamID',"TEAMS","First Year","Last Year"]
    w_lst = [0]*len(teams)
    for x in w.groupby('winner') : w_lst[x[0]] = x[1].shape[0]
    teams["Trophy Wons"] = w_lst
    
    st.table(teams.iloc[:,1:])
    
    fig = px.bar(teams,x='TEAMS',y='Trophy Wons')
    fig.update_layout(plot_bgcolor = "black")
    st.plotly_chart(fig)
    
    fig1 = px.line(k,x='year',y='winners')
    fig1.update_layout(plot_bgcolor = "black")
    st.plotly_chart(fig1)