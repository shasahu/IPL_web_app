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

question = "For anyone match, you need to show the total wicktes taken by all bowlers in that match."
description = "Analysis will show Bowling Scorecard for particular match of particular year. There is option to choose IPL year and then to choose any match of that IPL. Total score made by team is also shown. Scorecard is inning wise. In each Scorecard ,for each Bowler runs given by bowler, overs spelled by bowler, 4's and 6's hit on him, wickets taken, Maiden over spell, dot balls bowl by bowler, wides balls bowl, NoBalls bowl by baller, and Economy of the bowler."

db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
db_cursor = db_conn.cursor()

def create_df(grp,extra_df,boundary_df,wicket_df):
        bowler = []
        overs = []
        maiden = []
        runs_lst = []
        wicket = []
        econ = []
        zeroes = []
        fours = []
        sixes = []
        wides = []
        noballs = []

        for x in grp:
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
                    
                    if(y[1].iloc[l,6] == 1):
                        cri_tmp = wicket_df[wicket_df["id"] == y[1].iloc[l,0]].iloc[0,1]
                        if(cri_tmp in wicket_cri): wicket_tmp += 1
                        

                    if(y[1].iloc[l,5] == 0):
                        n_oballs += 1
                        dots_tmp += 1
                    elif(y[1].iloc[l,4]>0):
                        temp =  extra_df[extra_df['id'] == y[1].iloc[l,0]]

                        if(temp['type'].iloc[0] == "wides"):
                            wide_tmp += 1
                            runs_tmp += temp["runs"].iloc[0]

                        elif(temp["type"].iloc[0] == "penalty_wides") : 
                            wide_tmp += 1
                            runs_tmp += temp["runs"].iloc[0] - 5

                        elif((y[1].iloc[l,3] == 0)&(temp["type"].iloc[0] == "penalty")) : 
                            n_oballs += 1
                            dots_tmp += 1

                        elif((y[1].iloc[l,3] == 0)&((temp['type'].iloc[0]=="byes")|(temp["type"].iloc[0] == "legbyes"))) : 
                            n_oballs += 1
                            dots_tmp += 1

                        elif(temp['type'].iloc[0] == "noballs") : 
                            runs_tmp += temp["runs"].iloc[0]
                            noballs_tmp += 1
                        else : n_oballs += 1

                    else : 
                        runs_tmp += y[1].iloc[l,5]
                        n_oballs += 1
                    
                if(n_oballs >= 6):
                    if(runs_tmp == 0):maid_tmp += 1
                    ovrs += 1
                else : ovrs += n_oballs/10
                
                runs += runs_tmp
                
            
            f_tmp = boundary_df[(boundary_df['bowler'] == x[0]) & (boundary_df['runs'] == 4)]
            s_tmp = boundary_df[(boundary_df['bowler'] == x[0]) & (boundary_df['runs'] == 6)]
            if(f_tmp.shape[0] != 0):
                fours.append(f_tmp['numbersOf'].iloc[0])
            else: fours.append(0)

            if(s_tmp.shape[0] != 0):
                sixes.append(s_tmp['numbersOf'].iloc[0])
            else: sixes.append(0)
            
            
            bowler.append(x[0])
            overs.append('%.1f'%ovrs)
            maiden.append(maid_tmp)
            runs_lst.append(runs)
            wicket.append(wicket_tmp)
            econ.append(runs/ovrs)
            zeroes.append(dots_tmp)
            wides.append(wide_tmp)
            noballs.append(noballs_tmp)
        



        
        df_new = pd.DataFrame()
        df_new['Bowler'] = bowler
        df_new['Overs'] = overs
        df_new['Maiden'] = maiden
        df_new['Runs'] = runs_lst
        df_new['Wickets'] = wicket
        df_new['Economy'] = econ
        df_new["0's"] = zeroes
        df_new["4's"] = fours
        df_new["6's"] = sixes
        df_new["Wides"] = wides
        df_new["No Balls"] = noballs
        
        return df_new 


def scorecard_bowl():
    match_id = st.session_state.bowlques1selectbox2[0]
    teams_name = st.session_state.bowlques1selectbox2[1].split(',')
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

    extra_df = pd.read_sql("select id,runs,type from extras where (id between {} and {})".format(min_max[0],min_max[1]),db_conn)
    boundary_df = pd.read_sql("select bowler,runs,count(*) as numbersOf from boundary where (id between {} and {}) group by bowler,runs".format(min_max[0],min_max[1]),db_conn)
    wicket_df = pd.read_sql("select id,dismissalKind from wicket where (id between {} and {})".format(min_max[0],min_max[1]),db_conn)
        
    n_innings = pd.read_sql("select unique(inning) from ball_by_ball where matchID={}".format(match_id),db_conn).shape[0]
    
    if(n_innings == 1):
        first_inning = pd.read_sql("select id,overs,ball,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=1 order by overs,ball".format(match_id),db_conn)
        
        tot_runs1 = first_inning['totalRuns'].sum()
        tot_wic1 =  first_inning['isWicket'].sum()

        grp1 = first_inning.groupby('bowler')
        out_first_inn = create_df(grp1,extra_df,boundary_df,wicket_df)
        
        st.markdown("<br /><h2>"+first_team+" : "+str(tot_runs1)+"/"+str(tot_wic1)+"</h4><br />",unsafe_allow_html=True)
        st.dataframe(out_first_inn)
        
        
    elif(n_innings == 2): 
        first_inning = pd.read_sql("select id,overs,ball,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=1 order by overs,ball".format(match_id),db_conn)
        second_inning = pd.read_sql("select id,overs,ball,batsmanRuns,extraRuns,totalRuns,isWicket,bowler from ball_by_ball where matchID={} and inning=2 order by overs,ball".format(match_id),db_conn)
        
        tot_runs1 = first_inning['totalRuns'].sum()
        tot_wic1 =  first_inning['isWicket'].sum()
        tot_runs2 = second_inning['totalRuns'].sum()
        tot_wic2 =  second_inning['isWicket'].sum()

        grp1 = first_inning.groupby('bowler')
        grp2 = second_inning.groupby('bowler')

        out_first_inn = create_df(grp1,extra_df,boundary_df,wicket_df)
        out_second_inn = create_df(grp2,extra_df,boundary_df,wicket_df)

        st.markdown("<br /><h2>"+first_team+" : "+str(tot_runs1)+"/"+str(tot_wic1)+"</h4><br />",unsafe_allow_html=True)
        st.dataframe(out_first_inn)
        st.write("")
        st.write("")
        st.markdown("<br /><h2>"+second_team+" : "+str(tot_runs2)+"/"+str(tot_wic2)+"</h4><br />",unsafe_allow_html=True)
        st.dataframe(out_second_inn)
            

             

def app():
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"ANALYSIS","3 1/{}".format(question)])
            f.close()
    st.subheader(question)
    st.markdown("<br /><p><i>"+description+"</i></p><br />",unsafe_allow_html=True)
    years = ["none"]
    db_cursor.execute("select unique(substr(date,1,4)) from matches")
    years.extend([x[0] for x in db_cursor.fetchall()])
    cols1 = st.columns((1,2,1))
    cols1[1].selectbox("IPL YEAR",years,index=0,key="bowlque1selectbox1")

    if(st.session_state.bowlque1selectbox1 != "none"):
        choosed_year = st.session_state.bowlque1selectbox1
        mat_id_teams = [["none","none"]]
        db_cursor.execute("select matchID,group_concat(name) as teams_playing from matches,teams where (date like '{}%') and (team1=teamID or team2=teamID) group by matchID".format(choosed_year))
        mat_id_teams.extend([[x[0],x[1]] for x in db_cursor.fetchall()])
        cols2 = st.columns((1,2,1))
        cols2[1].selectbox("{} Matches".format(choosed_year),mat_id_teams,index=0,format_func=lambda y : y[1],key="bowlques1selectbox2")
        
        if(st.session_state.bowlques1selectbox2[0] != "none"): scorecard_bowl()

    
