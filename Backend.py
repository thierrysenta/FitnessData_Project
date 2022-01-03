#######################################################################################################################
#######################################################################################################################
###                                             FITNESS DATA VIZUALISATION                                          ###
#######################################################################################################################
#######################################################################################################################

########################################################################################################################
###    00  -     PARAMETERS :                                                                                        ###
########################################################################################################################

# -*- coding: utf-8 -*-

###    00.1  -  Libraries :
import os
import sys    
import pandas as pd
pd.options.mode.chained_assignment = None  # avoid SettingWithCopy Warning
import dtale
from pandasql import sqldf

import locale
from dateutil.parser import parse as parse_dt
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')   ## first I set locale

from flask import Flask, send_from_directory, render_template, request, jsonify, redirect, url_for
# Flask documents office site: https://flask.palletsprojects.com/en/1.1.x/
from flask_bootstrap import Bootstrap
# BOOTSTRAP site =>  https://getbootstrap.com/docs/5.0/getting-started/introduction/
# FLASK_BOOTSTRAP SITE: https://pythonhosted.org/Flask-Bootstrap/basic-usage.html

from sqlalchemy import create_engine


from collections import OrderedDict
from flask_sqlalchemy import SQLAlchemy

import datetime
from datetime import timedelta
from datetime import datetime as DT
from dateutil.relativedelta import relativedelta
#json
import json
# login
from flask_login import LoginManager, login_manager, login_user
from werkzeug.security import generate_password_hash
# werkzeug.security provide generate_password_hash methode which used "sha256" Encryption algorithm turning the string into ciphertext
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
# Excel
import xlwings as xw
import time
# download ppt
import win32com.client
import win32com
import pythoncom
import numpy as np



###    00.2  -  Parameters :
repository = os.path.join(os.getcwd())
rep_data = os.path.join(repository,"00_Data")
rep_data = os.path.join(repository,"PycharmProjects\\FitnessData_Project\\00_Data")
print(rep_data)

activities_file = 'activities.csv'


# Instantiate Bootstrap: to Help directly apply ready-made template html page.
app = Flask(__name__)
bootstrap = Bootstrap(app)

###    00.3  -  SQLite settinngs :
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'  # The database URI that should be used for the connection.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to disable the modification tracking system and avoid the warning break risk
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)  # Cache time is set to 1 second, thus css and html reload when you change anything


########################################################################################################################
###    01  -     DATAMANAGEMENT :                                                                                    ###
########################################################################################################################
pysqldf = lambda q: sqldf(q, globals())  # Use sql with Pandas and avoid specifying everytime

# Lecture de la table
df_activities = pd.read_csv(os.path.join(rep_data,activities_file), encoding='utf-8')
Columns_ini = df_activities.columns.tolist()
Columns_filter = list(filter(lambda x: (x.find("span") == -1), Columns_ini)) 
df_activities = df_activities[Columns_filter]
dtale.show(df_activities, ignore_duplicate = True).open_browser()

df_activities.dtypes


list_ini = ["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."]
list_fin = ["01","02","03","04","05","06","07","08","09","10","11","12"]
df_activities["Date_temp"] =df_activities["Date de l'activité"].replace(' à','',regex=True)
i = 0
for month in list_ini:
    i = i + 1
    print(str(i) + " - " + month + " ==> " + list_fin[i-1])
    df_activities["Date_temp"] = df_activities["Date_temp"].replace(month,list_fin[i-1],regex=True)

df_activities["Date"] = pd.to_datetime(df_activities["Date_temp"], format="%d %m %Y %H:%M:%S", exact=True, errors='coerce')
df_activities["Annee"] = df_activities["Date"].dt.year
print(df_activities["Annee"].drop_duplicates())

# KPIS aggrégés
Activities_AGG = """  select distinct "Type d'activité" , 
                                      Annee,  
                                      count("ID de l'activité") as N_activities  
                      FROM df_activities
                        group by "Type d'activité", Annee

                                       ; """
df_Activities_AGG = pysqldf(Activities_AGG)



########################################################################################################################
###    02  -     DB ENGINE and ROOTS :                                                                               ###
########################################################################################################################
###    02.1 -  Create the database Sqlite (once execute sqlite3.db in the repertory forever)
db = SQLAlchemy()
def init_db(app):
    db.init_app(app)

@app.route('/create_DB/')
def create_DB():
    db.create_all()
    return 'Database created successful'

###   2.2  -     Create engine to connect with Sqlite
engine = create_engine("sqlite:///sqlite3.db", encoding='utf-8')  # To final say the SQLAlchemy engine is created with Sqlite3
#data_stock.to_sql('data_stock', con=engine2, if_exists='replace', index=False)
df_Activities_AGG.to_sql('df_Activities_AGG', con=engine, if_exists='replace', index=False)

# Creation des années + années en YTD sur le meme horizon

###   2.3 -     Show first html home page with overview graphic
@app.route("/")
def FitnessData_overwiew():
    DATA_ACTIVITES_AGG = pd.read_sql("""
                                select 
                                        case when "Type d'activité" = 'Vélo' then  N_activities end  as N_activities_cycle ,
                                        case when "Type d'activité" = 'Course' then  N_activities end  as N_activities_course ,
                                        case when "Type d'activité" = 'PPG' then  N_activities end  as N_activities_PPG ,
                                        case when "Type d'activité" = 'Boxe' then  N_activities end  as N_activities_boxe ,
                                        "END" as END

                                from df_Activities_AGG ;
                                """, con=engine)

    return render_template("FitnessData_overwiew.html",
                               DATA_ACTIVITES_AGG=DATA_ACTIVITES_AGG,
                           )

########################################################################################################################
###    04  -     Run total Project DATAVIZ                                                                           ###
########################################################################################################################
import random, threading, webbrowser
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8090, debug=True)  # Auto refresh page
    port = 8090
    url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=8090, debug=True, use_reloader=False)  # Auto refresh page