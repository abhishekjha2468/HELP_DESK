import random
# from tqdm.notebook import tqdm
def create_suffled_option(DICTIONARY,A,B,C,D,E,CO):
  L=list(filter(lambda i: i!="", [A,B,C,D,E]))
  for i in DICTIONARY:
    l=random.sample(L,len(L))
    if len(L)==5:
      i["A"]=l[0]
      i["B"]=l[1]
      i["C"]=l[2]
      i["D"]=l[3]
      i["E"]=l[4]
      i["O"]=l.index(CO)
    elif len(L)==4:
      i["A"]=l[0]
      i["B"]=l[1]
      i["C"]=l[2]
      i["D"]=l[3]
      i["O"]=l.index(CO)
    elif len(L)==3:
      i["A"]=l[0]
      i["B"]=l[1]
      i["C"]=l[2]
      i["O"]=l.index(CO)
    elif len(L)==2:
      i["A"]=l[0]
      i["B"]=l[1]
      i["O"]=l.index(CO)
    elif len(L)==1:
      i["A"]=l[0]
      i["O"]=l.index(CO)
  
  ########################################################

  L=list(filter(lambda i: i!="", [A,B,C,D,E]))
  if len(L)==5:
    ols = f'[objective_all_shuffle([val(A)],[val(B)],[val(C)],[val(D)],[val(E)])]'
  elif len(L)==4:
    ols = f'[objective_all_shuffle([val(A)],[val(B)],[val(C)],[val(D)])]'
  elif len(L)==3:
    ols = f'[objective_all_shuffle([val(A)],[val(B)],[val(C)])]'
  elif len(L)==2:
    ols = f'[objective_all_shuffle([val(A)],[val(B)])]'
  elif len(L)==1:
    ols = f'[objective_all_shuffle([val(A)])]'
   else:
    ols = ""
  
  #########################################################
  return DICTIONARY,ols,f'[[val(O)]]',f'string(Hence, option latex(expr(O+1)) is correct.)'

#########################################################################################################################
import pandas as pd
import numpy as np
from flask import Flask, request, render_template
from flask_ngrok import run_with_ngrok
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
# import sqlite3
# import mysql.connector
import requests
# from firebase import firebase
import ast


app = Flask(__name__)
#run_with_ngrok(app) 

@app.route("/", methods=['GET'])
def home():
    f=open("cerebry_helpdesk.html","r")
    text=f.read()
    f.close()
    return text

@app.route("/tool_submit", methods=['GET', 'POST'])
def tool():
    try: tool = request.form['University']
    except: tool="shuffled_mcq_with_correct_option"
    if tool=="shuffled_mcq_with_correct_option":
        f=open("tool1.html","r")
        text=f.read()
        f.close()
    else:
        text="Sorry tool is not selected properly"
    return text

@app.route("/tool1_submit", methods=['GET', 'POST'])
def too1():
    try: option_1 = request.form['option_1']
    except: option_1=""
    try: option_2 = request.form['option_2']
    except: option_2=""
    try: option_3 = request.form['option_3']
    except: option_3=""
    try: option_4 = request.form['option_4']
    except: option_4=""
    try: option_5 = request.form['option_5']
    except: option_5=""
    try: correct_option = request.form['correct_option']
    except: correct_option=0
    try:
        gen_string = request.form['gen_string']
        gen_string = ast.literal_eval(gen_string)
    except: gen_string=[{"A":0}]
    DICTIONARY,ols,answer,sol=create_suffled_option(gen_string,option_1,option_2,option_3,option_4,option_5,correct_option)
    try:
        f=open("tool1result.html","r")
        text=f.read()
        f.close()
        text=text.replace("PLACEHOLDER_SOLUTION",sol).replace("PLACEHOLDER_ANSWER_TYPE",ols).replace("PLACEHOLDER_ANSWER",answer).replace("PLACEHOLDER_GENERATION_VALUES",str(DICTIONARY))
        return text
    except:
        return "SORRY SOMETHING WENT WRONG"
  
#app.run()
