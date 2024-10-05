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

question = "You need to show that does winning toss increases the chance of victory."
description = "Analysis show pie chart which contain two sector. One sector for 'Toss winner also won match' which show number of times teams which won toss also won match. The another for 'Toss winner not won match' which show number of times teams which won toss does not end up winning that match. "

def app():
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                write = writer(f)
                write.writerow([str(datetime.now()),"ANALYSIS","1 2/{}".format(question)])
                f.close()
        
        st.subheader(question)
        st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
        db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
        db_cursor = db_conn.cursor()
        db_cursor.execute('''use ipl''')
        db_cursor.execute("select count(*) from matches")
        n_of_matches = db_cursor.fetchall()[0][0]
        db_cursor.execute("select count(*) from matches where tossWin=winner")
        n_mat_won_tossWin = db_cursor.fetchall()[0][0]
        db_conn.close()

        fig = px.pie(values=[n_mat_won_tossWin,n_of_matches-n_mat_won_tossWin],
                names=["Toss Winner also Won Match","Toss Winner not Won Match"],
                title="Chances of Victory",
                color_discrete_sequence = px.colors.sequential.GnBu[::-1])
        st.plotly_chart(fig)