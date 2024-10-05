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

question = "For any year, you need to show top 10 batsman(rank them according to their total runs scored)"
description = "Analysis show rank of batsman according to runs scored by them on particular IPL. There is option to choose IPL year. Bar chart showing top 10 batsman is also shown which is categorize according to team. It also contain 4's ,6's hited, strike rate, highest score by batsman in that IPL."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()

def show_plot(df):
    col = list(df.columns)
    df = df.reset_index()
    fig = px.bar(df,
                y="Runs",
                x="Batsman",
                hover_data=col,
                height=500,
                width = 950,
                color="Team")

    fig.update_layout(plot_bgcolor = "black")
    st.plotly_chart(fig)

def create_df(grp,extra_df,boundary_df):
        fours = []
        sixes = []
        balls = []
        plyr_runs = []
        
        for x in grp:
            b_tmp = x[1].shape[0]
            lex_id = x[1][x[1]['extraRuns'] > 0]['id']
            count = 0
            if(len(lex_id) > 0):
                for y in lex_id :
                    if(extra_df[extra_df['id'] == y].shape[0] > 0) : count += 1
            balls.append(b_tmp-count)

            f_tmp = boundary_df[(boundary_df['batsman'] == x[0]) & (boundary_df['runs'] == 4)]
            s_tmp = boundary_df[(boundary_df['batsman'] == x[0]) & (boundary_df['runs'] == 6)]
            if(f_tmp.shape[0] != 0):
                fours.append(f_tmp['numbersOf'].iloc[0])
            else: fours.append(0)

            if(s_tmp.shape[0] != 0):
                sixes.append(s_tmp['numbersOf'].iloc[0])
            else: sixes.append(0)

            plyr_runs.append(x[1]['batsmanRuns'].sum())
            
        df_new = pd.DataFrame()
        df_new['Batsman'] = list(grp.groups.keys())
        df_new['Runs'] = plyr_runs
        df_new['Balls'] = balls
        df_new["4's"] = fours
        df_new["6's"] = sixes
        
        return df_new 


def scorecard_bat(match_id,teams_name):
    db_cursor.execute("select tossWin,tossDecision from matches where matchID={}".format(match_id))
    toss_temp = db_cursor.fetchall()[0]
    db_cursor.execute("select name from teams where teamID = {}".format(toss_temp[0]))
    toss_win_team = db_cursor.fetchall()[0][0]
    toss_deci = toss_temp[1]
    
    first_team = ''
    second_team = ''

    if(toss_win_team == teams_name[0]):
        if(toss_deci == "bat"):
            first_team = teams_name[0]
            second_team = teams_name[1]
        else : 
            first_team = teams_name[1]
            second_team = teams_name[0]
    else : 
        if(toss_deci == "bat"):
            first_team = teams_name[1]
            second_team = teams_name[0]
        else : 
            first_team = teams_name[0]
            second_team = teams_name[1]

    
    db_cursor.execute("select min(id),max(id) from ball_by_ball where matchID={}".format(match_id))
    min_max = db_cursor.fetchall()[0]

    extra_df = pd.read_sql("select id from extras where (id between {} and {}) and (type != 'wides') and (type != 'penalty_wides')".format(min_max[0],min_max[1]),db_conn)
    boundary_df = pd.read_sql("select batsman,runs,count(*) as numbersOf from boundary where (id between {} and {}) group by batsman,runs".format(min_max[0],min_max[1]),db_conn)
        
    n_innings = pd.read_sql("select unique(inning) from ball_by_ball where matchID={}".format(match_id),db_conn).shape[0]
    
    if(n_innings == 1):
        first_inning = pd.read_sql("select id,overs,ball,batsman,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=1 order by overs,ball".format(match_id),db_conn)

        grp1 = first_inning.groupby('batsman')
        out_first_inn = create_df(grp1,extra_df,boundary_df)
        out_first_inn["Team"] = [first_team for i in range(out_first_inn.shape[0])]

        return out_first_inn
        
                
    else: 
        first_inning = pd.read_sql("select id,overs,ball,batsman,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=1 order by overs,ball".format(match_id),db_conn)
        second_inning = pd.read_sql("select id,overs,ball,batsman,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=2 order by overs,ball".format(match_id),db_conn)
        
        grp1 = first_inning.groupby('batsman')
        grp2 = second_inning.groupby('batsman')

        out_first_inn = create_df(grp1,extra_df,boundary_df)
        out_second_inn = create_df(grp2,extra_df,boundary_df)
        out_first_inn["Team"] = [first_team for i in range(out_first_inn.shape[0])]
        out_second_inn["Team"] = [second_team for i in range(out_second_inn.shape[0])]

        return pd.concat([out_first_inn,out_second_inn],ignore_index=True)
    

             

def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","2 2/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    years = ["none"]
    db_cursor.execute("select unique(substr(date,1,4)) from matches")
    years.extend([x[0] for x in db_cursor.fetchall()])
    cols1 = st.columns((1,2,1))
    cols1[1].selectbox("IPL YEAR",years,index=0,key="batque2selectbox1")

    if(st.session_state.batque2selectbox1 != "none"):
        choosed_year = st.session_state.batque2selectbox1
        mat_id_teams = [["none","none"]]
        db_cursor.execute("select matchID,group_concat(name) as teams_playing from matches,teams where (date like '{}%') and (team1=teamID or team2=teamID) group by matchID".format(choosed_year))
        mat_id_teams.extend([[x[0],x[1]] for x in db_cursor.fetchall()])
        overall_df = pd.DataFrame()
        for x in mat_id_teams:
            if(x[0] == "none"):continue
            temp_df = scorecard_bat(x[0],x[1].split(','))
            overall_df = pd.concat([overall_df,temp_df],ignore_index=True)
    
        grp_overall = overall_df.groupby("Batsman")
        
        overall_df1 = grp_overall.sum()
        overall_df1["Strike Rate"] = [(overall_df1.loc[x[0],"Runs"]/overall_df1.loc[x[0],"Balls"])*100 for x in grp_overall]
        #overall_df1["Average"] = [overall_df1.loc[x[0],"Runs"]/x[1].shape[0] for x in grp_overall]
        overall_df1["Highest Score"] = [max(x[1].loc[:,"Runs"]) for x in grp_overall]
        overall_df1["Team"] = [x[1].iloc[0,-1] for x in grp_overall]
    
        overall_df1 = overall_df1.sort_values(by="Runs",ascending=False)
        st.dataframe(overall_df1)
        show_plot(overall_df1.iloc[0:10,:])