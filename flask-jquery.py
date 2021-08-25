# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import time
import datetime
import numpy as np
import math
app = Flask(__name__)
 
@app.route("/")
def index():
# 主页面
    return render_template("home1.html")
@app.route('/add')
def add_numbers():
    full_df = pd.read_csv('DummyData.csv',low_memory=False)
    minmaxData=full_df[['AC1','AC2','AC3','AC4']] 
    claf = joblib.load('RF_R_model.pkl')
    minmaxS=joblib.load('my_scaler.pkl')
    acuity = request.args.get('a', 0, type=int)
    timeslot = request.args.get('now')
    time_local = time.localtime(int(timeslot)/1000)
    currenttime = time.strftime("%Y-%m-%d %H:%M", time_local)
    Month=datetime.datetime.strptime(currenttime,'%Y-%m-%d %H:%M').month
    Hour=datetime.datetime.strptime( currenttime ,'%Y-%m-%d %H:%M').hour
    Minute=datetime.datetime.strptime( currenttime ,'%Y-%m-%d %H:%M').minute
    date=datetime.datetime.strptime(currenttime,'%Y-%m-%d %H:%M').weekday()
    a=[6,5,12,3,0]
    TimePeriod=Hour*4+math.floor(Minute/15)
    minmaxData.loc[len(minmaxData)] =np.array(a[1:5])
    transform=minmaxS.fit_transform(minmaxData)
    array=np.array(transform[len(transform)-1:])
    b=np.zeros((1,122))
    column = full_df.columns.values.tolist()
    del(column[0])
    new=np.concatenate((array,b),axis=1)
    new = pd.DataFrame(new,columns = column)
    if a[1]!=9:
          s="Stuff_level_"+str(a[0])
          new[s]=1
    if Month!=1: 
          smonth="Month_"+str(Month)  
          new[smonth]=1
    if TimePeriod!=52: 
          stime="TimePeriod_"+str(TimePeriod) 
          new[stime]=1
    if acuity!=1:
          sac="Acuity_Level_"+str(acuity)
          new[sac]=1
    if date!=1:
          sdate="WeekDay_"+str(date)
          new[sdate]=1
    my_prediction2 = claf.predict(new)    
    return (jsonify(result=my_prediction2.tolist()))


if __name__=="__main__":
    app.run(debug = True,use_reloader=False)
