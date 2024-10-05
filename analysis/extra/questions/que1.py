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

question = "For any batsman, you need to show, against which bowler he got out most number of time."
description = "Analysis shows for any particular batsman ,which bowler he got out most of the time. Plot is also shown for same. There is option to check it for multiple batsman."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()

def show_plot():
    query = '''select b.bowler,count(*) as numbersOf from ball_by_ball as b, wicket as w where (b.id = w.id) and 
               (w.dismissalKind not in ("run out","retired hurt","obstructing the field")) and 
               (playerDismissed = "{}") 
               group by bowler 
               order by numbersOf desc 
               limit 10'''
    
    plyr_dic = {}
    z = 0
    n_plyr = len(st.session_state["analextramultisel"])
    n_containers = n_plyr
    cont_cols = []

    for  i in range(n_containers):
        tmp_cont = st.container()
        cont_cols.append(tmp_cont.columns((2,3,1)))

    for plyr in st.session_state["analextramultisel"]:
        plyr_dic[plyr] = pd.read_sql(query.format(plyr),db_conn)
        
        cont_cols[z][0].subheader(plyr)
        cont_cols[z][0].dataframe(plyr_dic[plyr])
        fig = px.bar(plyr_dic[plyr],x='bowler',y='numbersOf')
        fig.update_layout(plot_bgcolor = "black")
        cont_cols[z][1].plotly_chart(fig)
        
        z += 1

        
def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","5 1/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    players = pd.read_sql("select unique(batsman) from ball_by_ball",db_conn)

    cols = st.columns((1,3,1))
    with cols[1]:
        st.multiselect("Select players : ",players,key="analextramultisel")
        st.button("Play",key="analextrabutton")

    if(st.session_state["analextrabutton"]):
        show_plot()