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

question = "For anyone match, you need to show the total runs scored by each batsman in that match and how they dismissed."
description = "Analysis will show Batting Scorecard for particular match of particular year. There is option to choose IPL year and then to choose any match of that IPL. Total score made by team is also shown. Scorecard is inning wise. In each Scorecard ,for each Batsman  runs scored by batsman, ball played by batsman to score runs, 4's and 6's hit by batsman, Strike Rate of that batsman, and dismissal information like bowler, Dismissal Kind, and Fielder is shown."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()

def create_df(inning,grp,extra_df,boundary_df,wicket_df):
        fours = []
        sixes = []
        balls = []
        plyr_runs = []
        strk_rate = []
        wic_bow = []
        wic_typ = []
        wic_fie = []

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

            
            w_tmp = wicket_df[wicket_df['playerDismissed'] == x[0]]
            if(w_tmp.shape[0] != 0):
                wic_typ.append(w_tmp['dismissalKind'].iloc[0])
                wic_fie.append(w_tmp['fielder'].iloc[0])
                bowler_tmp = inning[inning['id'] == w_tmp['id'].iloc[0]]['bowler'].iloc[0]
                wic_bow.append(bowler_tmp)
            else : 
                wic_typ.append('Not Out')
                wic_fie.append('Not Out')
                wic_bow.append('Not Out')

            
            plyr_runs.append(x[1]['batsmanRuns'].sum())
            strk_rate.append((plyr_runs[-1]/balls[-1])*100)
        
        df_new = pd.DataFrame()
        df_new['Batsman'] = list(grp.groups.keys())
        df_new['Runs'] = plyr_runs
        df_new['Balls'] = balls
        df_new["4's"] = fours
        df_new["6's"] = sixes
        df_new["Strike Rate"] = strk_rate
        df_new["Bowler"] = wic_bow
        df_new["Dismissal Kind"] = wic_typ
        df_new["Fielders"] = wic_fie

        return df_new 


def scorecard_bat():
    match_id = st.session_state.batques1selectbox2[0]
    teams_name = st.session_state.batques1selectbox2[1].split(',')
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

    extra_df = pd.read_sql("select id from extras where (id between {} and {}) and (type != 'wides')".format(min_max[0],min_max[1]),db_conn)
    boundary_df = pd.read_sql("select batsman,runs,count(*) as numbersOf from boundary where (id between {} and {}) group by batsman,runs".format(min_max[0],min_max[1]),db_conn)
    wicket_df = pd.read_sql("select * from wicket where (id between {} and {})".format(min_max[0],min_max[1]),db_conn)
        
    n_innings = pd.read_sql("select unique(inning) from ball_by_ball where matchID={}".format(match_id),db_conn).shape[0]
    
    if(n_innings == 1):
        first_inning = pd.read_sql("select id,overs,ball,batsman,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=1 order by overs,ball".format(match_id),db_conn)

        tot_runs1 = first_inning['totalRuns'].sum()
        tot_wic1 =  first_inning['isWicket'].sum()

        grp1 = first_inning.groupby('batsman')
        out_first_inn = create_df(first_inning,grp1,extra_df,boundary_df,wicket_df)
        
        st.markdown("<br /><h2>"+first_team+" : "+str(tot_runs1)+"/"+str(tot_wic1)+"</h4><br />",unsafe_allow_html=True)
        st.dataframe(out_first_inn)
        
    elif(n_innings == 2): 
        first_inning = pd.read_sql("select id,overs,ball,batsman,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=1 order by overs,ball".format(match_id),db_conn)
        second_inning = pd.read_sql("select id,overs,ball,batsman,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=2 order by overs,ball".format(match_id),db_conn)
        
        tot_runs1 = first_inning['totalRuns'].sum()
        tot_wic1 =  first_inning['isWicket'].sum()
        tot_runs2 = second_inning['totalRuns'].sum()
        tot_wic2 =  second_inning['isWicket'].sum()

        grp1 = first_inning.groupby('batsman')
        grp2 = second_inning.groupby('batsman')

        out_first_inn = create_df(first_inning,grp1,extra_df,boundary_df,wicket_df)
        out_second_inn = create_df(second_inning,grp2,extra_df,boundary_df,wicket_df)

        st.markdown("<br /><h2>"+first_team+" : "+str(tot_runs1)+"/"+str(tot_wic1)+"</h4><br />",unsafe_allow_html=True)
        st.dataframe(out_first_inn)
        st.write("")
        st.write("")
        st.markdown("<br /><h2>"+second_team+" : "+str(tot_runs2)+"/"+str(tot_wic2)+"</h4><br />",unsafe_allow_html=True)
        st.dataframe(out_second_inn)
            

             

def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","2 1/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    years = ["none"]
    db_cursor.execute("select unique(substr(date,1,4)) from matches")
    years.extend([x[0] for x in db_cursor.fetchall()])
    cols1 = st.columns((1,2,1))
    cols1[1].selectbox("IPL YEAR",years,index=0,key="batque1selectbox1")

    if(st.session_state.batque1selectbox1 != "none"):
        choosed_year = st.session_state.batque1selectbox1
        mat_id_teams = [["none","none"]]
        db_cursor.execute("select matchID,group_concat(name) as teams_playing from matches,teams where (date like '{}%') and (team1=teamID or team2=teamID) group by matchID".format(choosed_year))
        mat_id_teams.extend([[x[0],x[1]] for x in db_cursor.fetchall()])
        cols2 = st.columns((1,2,1))
        cols2[1].selectbox("{} Matches".format(choosed_year),mat_id_teams,index=0,format_func=lambda y : y[1],key="batques1selectbox2")
        
        if(st.session_state.batques1selectbox2[0] != "none"): scorecard_bat()

    
