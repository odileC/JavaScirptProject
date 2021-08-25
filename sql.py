# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 00:04:23 2021

@author: odile
"""
import datetime
from flask import Flask,request,render_template,url_for,session
import pymysql as mysql
import json
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import time
import datetime
import numpy as np
import math
import os
from datetime import timedelta

app = Flask(__name__)    #新建app
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
@app.route('/')         #设置路由
def index():           # 设置路由对应的函数
    return render_template("login.html")
@app.route('/predict',methods=['POST','GET'])
def predict():
 con = mysql.connect(user='root',password='882910',db="mydatabase")
 con.autocommit(True)
 cur = con.cursor()
 finalStr=""
 full_df = pd.read_csv('DummyData.csv',low_memory=False)
 minmaxData=full_df[['AC1','AC2','AC3','AC4']] 
 claf = joblib.load('RF_R_model.pkl')
 minmaxS=joblib.load('my_scaler.pkl')
 t1,t2,t3,t4,w1,w2,w3,w4,stuff=0,0,0,0,0,0,0,0,0
 t1Change=0
 t2Change=0
 t3Change=0
 t4Change=0
 w1Change=0
 w2Change=0
 w3Change=0
 w4Change=0 
 resultRatio=0
 if request.method == 'POST':
    Number = request.form['NHSnumber']
    session['NHSNumber']=Number
    session.permanent = True
    Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "SELECT * FROM hospital \
       WHERE Number= %s" % (Number)
    print(sql)
    cur.execute(sql)
    results = cur.fetchall()
    if len(results)==0:
      sql1 = "INSERT INTO hospital VALUES (%s,%s,%s,%s,Null,Null)" 
      values = [Time,Number,'0','Pending']
      cur.execute(sql1,values)
    else:
     Timeslot=results[0][0]
     sql2= "SELECT * FROM hospital \
             WHERE Time< '%s'" % (Timeslot)
     print(sql2)
     cur.execute(sql2)
     resultBefore = cur.fetchall()
     sql3= "SELECT * FROM hospital"
     cur.execute(sql3)
     resultAll = cur.fetchall()
     print(resultBefore)
     finalStr=""
     if results[0][3]=="Pending":
        countReg=0;
        for i in resultBefore:
         print (i[3])
         if i[3]=="Pending":
             countReg+=1
        for i in resultAll:
                 if i[3]=="Waiting":
                    if i[2]==1:
                     w1+=1
                    if i[2]==2:
                     w2+=1
                    if i[2]==3:
                     w3+=1  
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1   
        finalStr="Please wait for a consultant to help you complete registration. "
        if countReg==0:
            string="You are the next person!"
        else:
            string="There are "+str(countReg)+" patients in front of you for registration."
        finalStr+=string
        print(finalStr)
     elif results[0][3]=="Treating":
        finalStr="You are under the treatment. Please wait for it to complete"
     elif results[0][3]=="Waiting":
         Acuity=results[0][2]
         Month=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').month
         Hour=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').hour
         Minute=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').minute
         date=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').weekday()
         TimePeriod=Hour*4+math.floor(Minute/15) 
         if Acuity==1:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==1:
                     w1+=1
             for i in resultAll:
                 if i[3]=="Waiting":
                    if i[2]==2:
                     w2+=1
                    if i[2]==3:
                     w3+=1  
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1                                         
         if Acuity==2:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==2:
                     w2+=1
             for i in resultAll:
                 if i[3]=="Waiting":
                    if i[2]==3:
                     w3+=1  
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1 
         if Acuity==3:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==3:
                     w3+=1
             for i in resultAll:
                 if i[3]=="Waiting": 
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1 
         if Acuity==4:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1 
         for i in resultAll:
             if i[3]=="Treating":
                 stuff+=1     
         a=[w1,w2,w3,w4]
         minmaxData.loc[len(minmaxData)] =np.array(a)
         transform=minmaxS.fit_transform(minmaxData)
         array=np.array(transform[len(transform)-1:])
         b=np.zeros((1,122))
         column = full_df.columns.values.tolist()
         del(column[0])
         new=np.concatenate((array,b),axis=1)
         new = pd.DataFrame(new,columns = column)
         if stuff!=9:
           s="Stuff_level_"+str(6)
           new[s]=1
         if Month!=1: 
          smonth="Month_"+str(Month)  
          new[smonth]=1
         if TimePeriod!=52: 
          stime="TimePeriod_"+str(TimePeriod) 
          new[stime]=1
         if Acuity!=1:
          sac="Acuity_Level_"+str(Acuity)
          new[sac]=1
         if date!=1:
          sdate="WeekDay_"+str(date)
          new[sdate]=1
         my_prediction2 = claf.predict(new)
         my_prediction2=int(my_prediction2)
         my_prediction2=str(my_prediction2)
         finalStr="You are going to wait about "+my_prediction2+" minutes"
    sumBefore=w1+w2+w3+w4
    resultRatio=sumBefore/len(resultAll)
    session['w1']=w1
    session['w2']=w2
    session['w3']=w3
    session['w4']=w4
    session['t1']=t1
    session['t2']=t2
    session['t3']=t3
    session['t4']=t4  
 elif request.method == 'GET':
    Number=session.get('NHSNumber')
    T1=session.get('t1')
    T2=session.get('t2')
    T3=session.get('t3')
    T4=session.get('t4')
    W1=session.get('w1')
    W2=session.get('w2')
    W3=session.get('w3')
    W4=session.get('w4')
    t1,t2,t3,t4,w1,w2,w3,w4,stuff=0,0,0,0,0,0,0,0,0  
    Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "SELECT * FROM hospital \
       WHERE Number= %s" % (Number)
    print(sql)

    cur.execute(sql)
    results = cur.fetchall()
    if len(results)==0:
      sql1 = "INSERT INTO hospital VALUES (%s,%s,%s,%s,Null,Null)" 
      values = [Time,Number,'0','Pending']
      cur.execute(sql1,values)
    else:
     Timeslot=results[0][0]
     sql2= "SELECT * FROM hospital \
             WHERE Time< '%s'" % (Timeslot)
     print(sql2)
     cur.execute(sql2)
     resultBefore = cur.fetchall()
     sql3= "SELECT * FROM hospital"
     cur.execute(sql3)
     resultAll = cur.fetchall()

     finalStr=""
     if results[0][3]=="Pending":
        countReg=0;
        for i in resultBefore:
         print (i[3])
         if i[3]=="Pending":
             countReg+=1
        for i in resultAll:
                 if i[3]=="Waiting":
                    if i[2]==1:
                     w1+=1
                    if i[2]==2:
                     w2+=1
                    if i[2]==3:
                     w3+=1  
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1   
        finalStr="Please wait for a nurse to help you complete registration. "
        if countReg==0:
            string="You are the next person!"
        else:
            string="There are "+str(countReg)+" patients in front of you for registration."
        finalStr+=string
        print(finalStr)
     elif results[0][3]=="Treating":
        finalStr="You are under treatment. Please wait for it to complete"
     elif results[0][3]=="Waiting":
         Acuity=results[0][2]
         Month=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').month
         Hour=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').hour
         Minute=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').minute
         date=datetime.datetime.strptime(str(Timeslot),'%Y-%m-%d %H:%M:%S').weekday()
         TimePeriod=Hour*4+math.floor(Minute/15) 
         if Acuity==1:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==1:
                     w1+=1
             for i in resultAll:
                 if i[3]=="Waiting":
                    if i[2]==2:
                     w2+=1
                    if i[2]==3:
                     w3+=1  
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1                                         
         if Acuity==2:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==2:
                     w2+=1
             for i in resultAll:
                 if i[3]=="Waiting":
                    if i[2]==3:
                     w3+=1  
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1 
         if Acuity==3:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==3:
                     w3+=1
             for i in resultAll:
                 if i[3]=="Waiting": 
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1 
         if Acuity==4:
             for i in resultBefore:
                 if i[3]=="Waiting" and i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1 
             for i in resultAll:
                 if i[3]=="Waiting": 
                    if i[2]==4:
                     w4+=1
                 elif i[3]=="Treating":
                    if i[2]==1:
                     t1+=1                     
                    if i[2]==2:
                     t2+=1
                    if i[2]==3:
                     t3+=1  
                    if i[2]==4:
                     t4+=1                      
         for i in resultAll:
             if i[3]=="Treating":
                 stuff+=1
         a=[w1,w2,w3,w4]
         minmaxData.loc[len(minmaxData)] =np.array(a)
         transform=minmaxS.fit_transform(minmaxData)
         array=np.array(transform[len(transform)-1:])
         b=np.zeros((1,122))
         column = full_df.columns.values.tolist()
         del(column[0])
         new=np.concatenate((array,b),axis=1)
         new = pd.DataFrame(new,columns = column)
         if stuff!=9:
           s="Stuff_level_"+str(6)
           new[s]=1
         if Month!=1: 
          smonth="Month_"+str(Month)  
          new[smonth]=1
         if TimePeriod!=52: 
          stime="TimePeriod_"+str(TimePeriod) 
          new[stime]=1
         if Acuity!=1:
          sac="Acuity_Level_"+str(Acuity)
          new[sac]=1
         if date!=1:
          sdate="WeekDay_"+str(date)
          new[sdate]=1
         my_prediction2 = claf.predict(new)
         my_prediction2=int(my_prediction2)
         my_prediction2=str(my_prediction2)
         finalStr="You are going to wait about "+my_prediction2+" minutes"
    sumBefore=w1+w2+w3+w4
    resultRatio=sumBefore/len(resultAll)
    t1Change=t1-T1
    t2Change=t2-T2
    t3Change=t3-T3
    t4Change=t4-T4
    w1Change=w1-W1
    w2Change=w2-W2
    w3Change=w3-W3
    w4Change=w4-W4
    session.pop('w1')
    session.pop('w2')
    session.pop('w3')
    session.pop('w4')
    session.pop('t1')
    session.pop('t2')
    session.pop('t3')
    session.pop('t4')
    session['w1']=w1
    session['w2']=w2
    session['w3']=w3
    session['w4']=w4
    session['t1']=t1
    session['t2']=t2
    session['t3']=t3
    session['t4']=t4
 if resultRatio<=0.2:
     resultRatio=2
 elif 0.2<resultRatio and resultRatio<=0.4:
     resultRatio=4 
 elif 0.4<resultRatio and resultRatio<=0.6:
     resultRatio=6
 elif 0.6<resultRatio and resultRatio<=0.8:
     resultRatio=8 
 else:
     resultRatio=10
 Timenow = datetime.datetime.now().strftime('%H:%M:%S')
 
 timeUpdate="The last update was in "+str(Timenow)
 return render_template("result.html",stringInfo=finalStr,W1=w1,W2=w2,W3=w3,W4=w4,T1=t1,T2=t2,T3=t3,T4=t4,update=timeUpdate,w1change=w1Change,w2change=w2Change,w3change=w3Change,w4change=w4Change,t1change=t1Change,t2change=t2Change,t3change=t3Change,t4change=t4Change,ratio=resultRatio)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)