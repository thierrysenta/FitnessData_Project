#######################################################################################################################
#######################################################################################################################
###                                             FITNESS DATA VIZUALISATION                                          ###
#######################################################################################################################
#######################################################################################################################

########################################################################################################################
###    00  -     PARAMETERS :                                                                                        ###
########################################################################################################################

###    00.1  -  Libraries :
import os
import sys    
import pandas as pd
pd.options.mode.chained_assignment = None  # avoid SettingWithCopy Warning

    

from flask import Flask, send_from_directory, render_template, request, jsonify, redirect, url_for
# Flask documents office site: https://flask.palletsprojects.com/en/1.1.x/
from flask_bootstrap import Bootstrap
# BOOTSTRAP site =>  https://getbootstrap.com/docs/5.0/getting-started/introduction/
# FLASK_BOOTSTRAP SITE: https://pythonhosted.org/Flask-Bootstrap/basic-usage.html
from sqlalchemy import create_engine
from pandasql import sqldf

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
repository = os.path.join(os.getcwd(),"PycharmProjects\FitnessData_Project")
rep_data = os.path.join(repository,"00_Data")
#print(rep_data)

activities_file = 'activities.csv'




###    00.3  -  SQLite settinngs :
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'  # The database URI that should be used for the connection.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to disable the modification tracking system and avoid the warning break risk
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)  # Cache time is set to 1 second, thus css and html reload when you change anything


########################################################################################################################
###    01  -     DATAMANAGEMENT :                                                                                    ###
########################################################################################################################
df_activities = pd.read_csv(os.path.join(rep_data,activities_file))


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
df_activities.to_sql('df_activities', con=engine, if_exists='replace', index=False)

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