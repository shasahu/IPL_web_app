# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 16:34:41 2021

@author: 1605309
"""

import streamlit as st
from sqlalchemy import create_engine
from urllib.parse import quote
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import randint
from csv import writer
from datetime import datetime
import plotly.express as px

#st.set_option('deprecation.showPyplotGlobalUse', False)
question = "For each team you need to give the stadium name(venue) where that team have won the maximum match?"
description = "Analysis will give the stadium name(venue) where that team have won the maximum matches.This is can be Per Team-Wise or Combine for All Teams. In Per Team-Wise ,  there is option to choose team.  For the chosen team there is horizontal bar plot stadiums vs number of match won at that stadium. In Combine for All Teams ,  there are plots of maximum number of matches won by a  each team at some particular stadium vs number of matches won by particular team at that particular stadium. There is option to visualize it using barplot and pie chart. One can hover over each bar or sector to get in-depth information about that particular bar or sector.You can play with the selectbox given below."

sql_engine = create_engine("mysql://root:%s@localhost/ipl" % quote('Summer@1'),echo=False)
    
query = '''select t.name,l.venue,count(*) as win
           from teams as t,location as l,matches as m 
           where (m.venueID=l.venueID) and (m.winner is not NULL) and (m.winner=t.teamID) 
           group by t.name,l.venue'''
result = pd.read_sql(query,sql_engine)


def show_bar():
        x = st.session_state.selectTeam
        data = result[result["name"] == x]
        
        fig = px.bar(data,
                    y="venue",
                    x="win",
                    hover_data=["name"],
                    labels={'name':'Teams'},
                    height=500,
                    width = 950)

        fig.update_layout(plot_bgcolor = "black")
        st.plotly_chart(fig)
        
    
def combMaxBar() :
        idx = result.groupby(['name'])[['win']].transform(max) == result[['win']]
        idx = list(idx[idx["win"] == True].index)
        
        fig = px.bar(result.iloc[idx,:],
                    y="name",
                    x="win",
                    hover_data=["venue"],
                    labels={'name':'Teams'},
                    height=500,
                    width = 950,
                    color="name")

        fig.update_layout(plot_bgcolor = "black")
        st.plotly_chart(fig)

def combMaxPie() :
        idx = result.groupby(['name'])[['win']].transform(max) == result[['win']]
        idx = list(idx[idx["win"] == True].index)
        fig = px.pie(result.iloc[idx,:],
                    values="win",
                    names="name",
                    hover_data=["venue"],
                    labels={'name':'Team'})
        
        st.plotly_chart(fig)
    
            
    
def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","1 1/{}".format(question)])
            f.close()

    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    team_names = ["none"]
    team_names.extend(pd.unique(result['name']))
    options = ["none"]
    op1 = "For each Team"
    op2 = "Combine for all teams"
    options.append(op1)
    options.append(op2)
    
    cols = st.columns((1,2,1))
    cols[1].selectbox("Choose : ",options,index=0,key="que1SelectBox")

    cols1 = st.columns((1,2,1))
    with cols1[1]:
        if(st.session_state.que1SelectBox == op1):
                st.selectbox("Choose Team",team_names,index=0,key='selectTeam')
                
                
        elif(st.session_state.que1SelectBox == op2):
                st.selectbox("Choose plot type : ",["none","Bar Plot","Pie Plot"],index=0,key='analyRadio')
                

    if(st.session_state.que1SelectBox == op1):
                if(st.session_state["selectTeam"] != "none"):show_bar()
    elif(st.session_state.que1SelectBox == op2):
                if(st.session_state.analyRadio == "Bar Plot") : combMaxBar()
                elif(st.session_state.analyRadio == "Pie Plot") : combMaxPie()
