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

question = "Scorecard of each IPL"
description = "Analysis shows scorecard for any IPL. There is option to choosed any IPL. Its also shows winner (W) and runner up (R)."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()

def scorecard_team():
    year = st.session_state.selectboxextraque2
    df = pd.read_sql("select team1,team2,winner from matches where date like '{}%' order by matchID".format(year),db_conn)

    first = df.iloc[-1,2]
    second = df.iloc[-1,0] + df.iloc[-1,1] - df.iloc[-1,2]

    if((year == 2008) or (year == 2009)) : df_new = df.iloc[0:-3,:]
    else : df_new = df.iloc[0:-4,:]
    df1 = pd.read_sql("select teamID,name from teams",db_conn,index_col='teamID')

    teamsid = list(set(df['team1'].values).union(df['team2'].values))

    win = []
    loss = []
    nr = []
    teams = []
    pld = []
    for t in teamsid:
        if(first == t) : teams.append(df1.iloc[t,0]+" (W)")
        elif(second == t) : teams.append(df1.iloc[t,0]+" (R)")
        else : teams.append(df1.iloc[t,0])
        
        tmp = df_new[(df_new['team1']==t) | (df_new['team2']==t)]
        pld.append(tmp.shape[0])
        win.append(tmp[tmp['winner']==t].shape[0])
        loss.append(tmp[(tmp['winner']>=0) & (tmp['winner']!=t)].shape[0])
        nr.append(tmp[tmp['winner']==-1].shape[0])

    pts_tab = pd.DataFrame(index = teams)
    pts_tab['Pld'] = pld
    pts_tab["Win"] = win
    pts_tab["Loss"] = loss
    pts_tab["N/R"] = nr
    pts_tab["Pts"] = (2*pts_tab['Win'])+(1*pts_tab["N/R"])

    pts_tab = pts_tab.sort_values(['Pts'],ascending=False)

    return pts_tab
        
def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","5 2/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    
    year = ["none"]
    db_cursor.execute("select unique(substr(date,1,4)) from matches")
    year.extend([x[0] for x in db_cursor.fetchall()])
    
    cols = st.columns((1,3,1))
    with cols[1]:
        st.selectbox("Select Year : ",year,key="selectboxextraque2")
        if(st.session_state.selectboxextraque2 != "none") :
            st.dataframe(scorecard_team())