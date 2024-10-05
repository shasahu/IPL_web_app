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
import numpy as np

question = "Player entire Journey in IPL"
description = "Analysis show player journey from IPL to IPL. Teams they played with, Runs scored by them, Runs got hitted on there spell, Balls played by them, Overs bowled by them, 4's & 6's hitted by them, 4's & 6's hitted on them, Maiden over spelled, Wickets taken, Dot balls, noballs, wides by them included. Also included number of time they become Man of the Match, there batting average and strike rate, there bowling economy and there batting highest score. There are some of the additional plots given which shows there progress year wise."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor() 

def batting(grp,plyr) : 
    db_cursor.execute("select id from wicket where playerDismissed='{}'".format(plyr))
    dismis = set(x[0] for x in db_cursor.fetchall())

    fours = []
    sixes = []
    total_runs = []
    balls = []
    matches = []
    not_out = []
    team = []
    plyrOfMat = []

    for x in grp :
        db_cursor.execute("select team1,team2,tossWin,tossDecision,playerOfMatch from matches where matchID={}".format(x[0]))
        toss_plyr_info = db_cursor.fetchall()[0]
        teamidx=-1

        if(toss_plyr_info[3] == 'bat'):
            if(x[1].head(1)['inning'].iloc[0] == 1) : teamidx = toss_plyr_info[2]
            else : teamidx = toss_plyr_info[0] + toss_plyr_info[1] - toss_plyr_info[2]
        else : 
            if(x[1].head(1)['inning'].iloc[0] == 1) : teamidx = toss_plyr_info[0] + toss_plyr_info[1] - toss_plyr_info[2]
            else : teamidx = toss_plyr_info[2]

        db_cursor.execute("select name from teams where teamID = {}".format(teamidx))
        team.append(db_cursor.fetchall()[0][0])
        
        if(toss_plyr_info[4] == plyr) : plyrOfMat.append(1)
        else : plyrOfMat.append(0)
        
        mi = min(x[1].loc[:,'id'])
        ma = max(x[1].loc[:,'id'])
        
        que = ''
        if(len(x[1]['id']) == 1) : que = '({})'.format(x[1]['id'].values[0])
        else : que = str(tuple(x[1]['id']))
        
        extra_df_bat = pd.read_sql("select id from extras where (id in {}) and (type != 'wides')".format(que),db_conn)
        boundary_df_bat = pd.read_sql("select runs,count(*) as numbersOf from boundary where (id between {} and {}) and batsman='{}' group by runs".format(mi,ma,"CH Gayle"),db_conn)
        
        if(len(set(x[1]['id']).intersection(dismis)) > 0) : not_out.append(0)
        else : not_out.append(1)
            
        matches.append(x[0])
        total_runs.append(sum(x[1].loc[:,"batsmanRuns"]))
        balls.append(x[1].shape[0] - len(extra_df_bat))
        
        f_tmp = boundary_df_bat[boundary_df_bat['runs'] == 4]
        s_tmp = boundary_df_bat[boundary_df_bat['runs'] == 6]
        if(f_tmp.shape[0] != 0):
            fours.append(f_tmp['numbersOf'].iloc[0])
        else: fours.append(0)
            
        if(s_tmp.shape[0] != 0):
            sixes.append(s_tmp['numbersOf'].iloc[0])
        else: sixes.append(0)
        
    df = pd.DataFrame(index=matches)
    df["Bats Runs"] = total_runs
    df["balls"] = balls
    df["Bat 4's"] = fours
    df["Bat 6's"] = sixes
    df["Not_OUT"] = not_out
    df["Team"] = team
    df["Man Of the Match"] = plyrOfMat

    return df

def bowling(grp,plyr) : 
    matches = []
    overs = []
    maiden = []
    runs_lst = []
    wicket = []
    zeroes = []
    fours = []
    sixes = []
    wides = []
    noballs = []
    team = []
    plyrOfMat = []

    for x in grp :
        db_cursor.execute("select team1,team2,tossWin,tossDecision,playerOfMatch from matches where matchID={}".format(x[0]))
        toss_plyr_info = db_cursor.fetchall()[0]
        teamidx=-1

        if(toss_plyr_info[3] == 'field'):
            if(x[1].head(1)['inning'].iloc[0] == 1) : teamidx = toss_plyr_info[2]
            else : teamidx = toss_plyr_info[0] + toss_plyr_info[1] - toss_plyr_info[2]
        else : 
            if(x[1].head(1)['inning'].iloc[0] == 1) : teamidx = toss_plyr_info[0] + toss_plyr_info[1] - toss_plyr_info[2]
            else : teamidx = toss_plyr_info[2]

        db_cursor.execute("select name from teams where teamID = {}".format(teamidx))
        team.append(db_cursor.fetchall()[0][0])
        
        if(toss_plyr_info[4] == plyr) : plyrOfMat.append(1)
        else : plyrOfMat.append(0)
        
        mi = min(x[1].loc[:,'id'])
        ma = max(x[1].loc[:,'id'])
        
        que = ''
        if(len(x[1]['id']) == 1) : que = '({})'.format(x[1]['id'].values[0])
        else : que = str(tuple(x[1]['id']))
        
        extra_df_bowl = pd.read_sql("select id,runs,type from extras where (id in {})".format(que),db_conn)
        boundary_df_bowl = pd.read_sql("select runs,count(*) as numbersOf from boundary where (id between {} and {}) and (bowler='{}') group by runs".format(mi,ma,plyr),db_conn)
        wicket_df_bowl = pd.read_sql("select id,dismissalKind from wicket where (id in {})".format(que),db_conn)
        
        matches.append(x[0])
        wicket_cri = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']

        ovrs = 0
        maid_tmp = 0
        dots_tmp = 0
        runs = 0
        wide_tmp = 0
        noballs_tmp = 0
        wicket_tmp = 0

        for y in x[1].groupby("overs"):
            n_oballs = 0
            runs_tmp = 0

            for l in range(y[1].shape[0]):

                if(y[1].iloc[l,11] == 1):
                    cri_tmp = wicket_df_bowl[wicket_df_bowl["id"] == y[1].iloc[l,0]].iloc[0,1]
                    if(cri_tmp in wicket_cri): wicket_tmp += 1


                if(y[1].iloc[l,10] == 0):
                    n_oballs += 1
                    dots_tmp += 1
                elif(y[1].iloc[l,9]>0):
                    temp =  extra_df_bowl[extra_df_bowl['id'] == y[1].iloc[l,0]]

                    if(temp['type'].iloc[0] == "wides"):
                        wide_tmp += 1
                        runs_tmp += temp["runs"].iloc[0]

                    elif(temp["type"].iloc[0] == "penalty_wides") : 
                        wide_tmp += 1
                        runs_tmp += temp["runs"].iloc[0] - 5

                    elif((y[1].iloc[l,8] == 0)&(temp["type"].iloc[0] == "penalty")) : 
                        n_oballs += 1
                        dots_tmp += 1

                    elif((y[1].iloc[l,8] == 0)&((temp['type'].iloc[0]=="byes")|(temp["type"].iloc[0] == "legbyes"))) : 
                        n_oballs += 1
                        dots_tmp += 1

                    elif(temp['type'].iloc[0] == "noballs") : 
                        runs_tmp += temp["runs"].iloc[0]
                        noballs_tmp += 1
                    else : n_oballs += 1

                else : 
                    runs_tmp += y[1].iloc[l,10]
                    n_oballs += 1

            if(n_oballs >= 6):
                if(runs_tmp == 0):maid_tmp += 1
                ovrs += 1
            else : ovrs += n_oballs/10

            runs += runs_tmp


        f_tmp = boundary_df_bowl[(boundary_df_bowl['runs'] == 4)]
        s_tmp = boundary_df_bowl[(boundary_df_bowl['runs'] == 6)]
        if(f_tmp.shape[0] != 0):
            fours.append(f_tmp['numbersOf'].iloc[0])
        else: fours.append(0)

        if(s_tmp.shape[0] != 0):
            sixes.append(s_tmp['numbersOf'].iloc[0])
        else: sixes.append(0)


        overs.append(float('%.1f'%ovrs))
        maiden.append(maid_tmp)
        runs_lst.append(runs)
        wicket.append(wicket_tmp)
        zeroes.append(dots_tmp)
        wides.append(wide_tmp)
        noballs.append(noballs_tmp)



    df_new = pd.DataFrame(index=matches)
    df_new['Overs'] = overs
    df_new['Maiden'] = maiden
    df_new['Bowl Runs'] = runs_lst
    df_new['Wickets'] = wicket
    df_new["0's"] = zeroes
    df_new["Bowl 4's"] = fours
    df_new["Bowl 6's"] = sixes
    df_new["Wides"] = wides
    df_new["No Balls"] = noballs
    df_new["Team"] = team
    df_new["Man Of the Match"] = plyrOfMat

    return df_new

def merg(l) : 
    if(pd.isna(l[0])) : return l[1]
    return l[0]

def player_detail():
    plyr = st.session_state.playerque1selectbox1
    df_overall = pd.read_sql("select * from ball_by_ball where batsman='{}' or bowler='{}'".format(plyr,plyr),db_conn)
    total_matchID = list(set(int(x) for x in df_overall['matchID'].values))

    bats = df_overall[df_overall["batsman"] == plyr]
    bowl = df_overall[df_overall["bowler"] == plyr]
    grp_bat = bats.groupby("matchID")
    grp_bowl = bowl.groupby("matchID")

    df_bat = batting(grp_bat,plyr)
    df_bowl = bowling(grp_bowl,plyr)
    
    df_bat_bowl = pd.concat([df_bat,df_bowl],axis=1,join='outer')
    df_bat_bowl['TEAMS'] = df_bat_bowl[['Team']].apply(lambda x : merg(x),axis=1)
    df_bat_bowl['MAN OF THE MATCH'] = df_bat_bowl[['Man Of the Match']].apply(lambda x : merg(x),axis=1)
    df_bat_bowl.drop(['Team','Man Of the Match'],axis=1,inplace=True)
    
    query = ''
    if(len(total_matchID) == 1) : query = '({})'.format(total_matchID)
    else : query = str(tuple(total_matchID))
    
    full_final = pd.read_sql("select matchID,substr(date,1,4) as year from matches where matchID in {}".format(query),db_conn,index_col='matchID')
    full_final = pd.concat([full_final,df_bat_bowl],axis=1,join='inner')
    full_final = full_final.fillna(0)

    grp = full_final.groupby('year')
    full_final = full_final.groupby(['year','TEAMS']).sum()

    high_score = []
    avg = []
    strike_rate = []
    economy = []
    for z in grp :
        mx=-1
        out=-1
        tmp_cnt=0
        tmp_sum=0
        tmp_ball=0
        tmp_ovr=0
        tmp_runs=0
        for z1 in z[1].loc[:,['Bats Runs','Not_OUT','balls','Bowl Runs','Overs']].values :
            tmp_runs += z1[3]
            tmp_ovr += z1[4]
            tmp_sum += z1[0]
            tmp_cnt += 1 - z1[1]
            tmp_ball += z1[2]
            if(mx < z1[0]) : 
                mx = z1[0]
                out = z1[1]
        if(tmp_ovr > 0) : economy.append(tmp_runs/tmp_ovr)
        else : economy.append(tmp_runs)
        if(tmp_ball > 0) : strike_rate.append((tmp_sum/tmp_ball)*100)
        else : strike_rate.append(tmp_sum*100)
        if(tmp_cnt > 0) : avg.append(tmp_sum/tmp_cnt)
        else : avg.append(tmp_sum)
        if(out == 1) : high_score.append(str(mx)+"*")
        else : high_score.append(str(mx))

    full_final['Highest Score'] = high_score
    full_final['Average'] = avg
    full_final['Strike Rate'] = strike_rate
    full_final['Economy'] = economy
    
    full_final.fillna(0,inplace=True)
    full_final.drop(['Not_OUT'],axis=1,inplace=True)

    return full_final

def show_plot(df) : 
    idx = st.session_state.playerque1selectbox2
    if(idx == 16): 
        y_idx = []
        for x in df.iloc[:,16].values :
            y_idx.append(int(x.split('.')[0]))
        fig = px.bar(df,x='year',y=y_idx,color='TEAMS')
    else : fig = px.bar(df,x='year',y=df.columns[idx],color='TEAMS')
    fig.update_layout(plot_bgcolor = "black")
    st.plotly_chart(fig)

def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","4 1/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)

    players = ["none"]
    db_cursor.execute("select unique(batsman) from ball_by_ball")
    pl_tmp = set(x[0] for x in db_cursor.fetchall())
    db_cursor.execute("select unique(nonStriker) from ball_by_ball")
    pl_tmp = pl_tmp.union(set(x[0] for x in db_cursor.fetchall()))
    db_cursor.execute("select unique(bowler) from ball_by_ball")
    players.extend(list(pl_tmp.union(set(x[0] for x in db_cursor.fetchall()))))
    cols1 = st.columns((1,2,1))
    cols1[1].selectbox("Players",players,index=0,key="playerque1selectbox1")
    
    if(st.session_state.playerque1selectbox1 != "none"):
        player_info = player_detail()
        player_info.reset_index(inplace=True)
        st.dataframe(player_info)
        col = player_info.columns
        plt_lst = [i for i in range(2,len(col))]
        cols2 = st.columns((1,2,1))
        with cols2[1]:
            st.selectbox("Select Plot : ",plt_lst,index=0,format_func = lambda x : "Plot "+col[x],key="playerque1selectbox2")
            show_plot(player_info)

        
