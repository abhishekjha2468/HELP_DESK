import random
# from tqdm.notebook import tqdm
def create_suffled_option(DICTIONARY,A,B,C,D,E,CCO):
  CO=[A,B,C,D,E][int(CCO)]
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
#   [objective_answer_types([])]
#   [objective_all_shuffle([])]
  if len(L)==5:
    ols = f'[objective_answer_types([[string(),type(continuous(string(val(A))))],[string(),type(continuous(string(val(B))))],[string(),type(continuous(string(val(C))))],[string(),type(continuous(string(val(D))))],[string(),type(continuous(string(val(E))))]])]'
  elif len(L)==4:
    ols = f'[objective_answer_types([[string(),type(continuous(string(val(A))))],[string(),type(continuous(string(val(B))))],[string(),type(continuous(string(val(C))))],[string(),type(continuous(string(val(D))))]])]'
  elif len(L)==3:
    ols = f'[objective_answer_types([[string(),type(continuous(string(val(A))))],[string(),type(continuous(string(val(B))))],[string(),type(continuous(string(val(C))))]])]'
  elif len(L)==2:
    ols = f'[objective_answer_types([[string(),type(continuous(string(val(A))))],[string(),type(continuous(string(val(B))))]])]'
  elif len(L)==1:
    ols = f'[objective_answer_types([[string(),type(continuous(string(val(A))))]])]'
  else:
    ols = ""
  
  #########################################################
  return DICTIONARY,ols,f'[[val(O)]]',f'string(Hence, option latex(expr(O+1)) is correct.)'

#########################################################################################################################
import pandas as pd
import numpy as np
import math
import itertools
import numpy
from flask import Flask, request, render_template
from flask_ngrok import run_with_ngrok
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
# import sqlite3
# import mysql.connector
import requests
from firebase import firebase
import ast

app = Flask(__name__)
#run_with_ngrok(app) 

@app.route("/home", methods=['GET'])
def home2():
    f=open("cerebry_helpdesk.html","r")
    text=f.read()
    f.close()
    return text

@app.route("/", methods=['GET'])
def home():
    f=open("cerebry_helpdesk.html","r")
    text=f.read()
    f.close()
    return text

@app.route("/tool_submit", methods=['GET', 'POST'])
def tool():
    try: tool = request.form['University']
    except: return "Exception, Sorry tool is not selected properly"
    if tool=="shuffled_mcq_with_correct_option":
        f=open("tool1.html","r")
        text=f.read()
        f.close()
    elif tool=="generation_values":
        f=open("tool2.html","r")
        text=f.read()
        f.close()
    elif tool=="Project":
        f=open("cerbpro1.html","r")
        text=f.read()
        f.close()
    else:
        text="Sorry tool is not selected properly"
    return text


@app.route("/tool1_submit", methods=['GET', 'POST'])
def tool1():
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
 
####################################################################3
def read_input_type(s):
  return ast.literal_eval(s)

def format_list(l):
  L=[]
  for i in l[1:-1].split(","):
    try:
      L.append(read_input_type(i.strip()))
    except:
      L.append(i.strip())
  return L

def format_tuple(t):
  return list(range(t[0],t[1]+1))

def find_key_values(d):
  var_list=[]
  Keys=[]
  Values=[]
  if type(d)==str:
    d=read_input_type(d)
  for (k,v) in d.items():
    if type(v)==str:
      if v[0]=="[":
        val=format_list(v)
        # print(v,val,k)
        Keys.append(k)
        Values.append(val)
      elif v[0]=="(":
        val=format_tuple(read_input_type(v))
        # print(v,val,k)
        Keys.append(k)
        Values.append(val)
      elif "," not in list(v):
        Keys.append(k)
        try: Values.append([read_input_type(v)])
        except: Values.append([v])
      else:
        print("Wrong input format")
    else:
      Keys.append(k)
      Values.append([v])
  return Keys,Values

def find_all_comb(d):
  d=read_input_type(d)
  K,V=find_key_values(d)
  possible_values=list(itertools.product(*V))
  possible_combinations=list(map(lambda k,v: dict(zip(k,v)) ,[K]*len(possible_values),possible_values))
  return possible_combinations

def filter_combination(possible_combinations,condition_string):
  filtered_combination=[]
  for i in possible_combinations:
    globals().update(i)
    # print(p,q,r,s)
    if eval(condition_string):
      filtered_combination.append(i)
  return filtered_combination

def find_filtered_combination(d,condition_string):
  possible_combinations=find_all_comb(d)
  return filter_combination(possible_combinations,condition_string)

def change(K):
  return str(K).replace("'","")

def find_filtered_combination2(d,condition):
  try:
    d=read_input_type(d)
    K,V=find_key_values(d)
    print(K,V)
    LL=[]
    print("".join([f'for {k} in {v}:\n{f"  "*(e+1)}' for e,(k,v) in enumerate(zip(K,V))])+f"if {condition}: LL.append({change(K)})")
    exec("".join([f'for {k} in {v}:\n{f"  "*(e+1)}' for e,(k,v) in enumerate(zip(K,V))])+f"if {condition}: LL.append({change(K)})")

    # possible_values=list(itertools.product(*V))
    # print("hello")
    possible_combinations=list(map(lambda k,v: dict(zip(k,v)) ,[K]*len(LL),LL))
    K=[]
    FLL=[]
    for i in LL:
      v=[]
      for j in i.values():
        if type(j)!=str: v.append(j)
      if v not in K:
        FLL.append(i)
      K.append(v)
    possible_combinations=FLL
    return False,possible_combinations
  except Exception as e: return True,str(e)

def condition_verify(d,condition_string):
  d=find_filtered_combination(d,"True")[0]
  globals().update(d)
  return eval(condition_string.replace(" and ",",").replace(" or ",","))

@app.route("/tool2_submit", methods=['GET', 'POST'])
def tool2():
    try: generation_string = request.form['generation_string']
    except: generation_string=""
    try: condition = request.form['condition']
    except: condition=""
    try: custom_values = request.form['custom_values']
    except: custom_values=""
    if custom_values!="":
      condition_check_result=str(condition_verify(custom_values,condition))
    else:
      condition_check_result=""
    flag,filtered_combination_set=find_filtered_combination2(generation_string,condition)
    filtered_combination_set=str(filtered_combination_set)
    if flag:
      return filtered_combination_set
    try:
        f=open("tool2result.html","r")
        text=f.read()
        f.close()
        text=text.replace("filtered_combination_set",filtered_combination_set).replace("condition_check_result",condition_check_result)
        return text
    except:
        return "SORRY SOMETHING WENT WRONG"
def pro_1_save_data(dvid,ch_n,tp_n,tch_l,alst_n,ti_l):
    f=firebase.FirebaseApplication("https://projectdeliverypankaj-default-rtdb.firebaseio.com/",None)
    data={
        "Deliveryid" :dvid,
        "Chaptername": ch_n,
        "Topicname"  : tp_n,
        "Teacherlead":tch_l,
        "Analystname": alst_n ,
        "Timeline" : ti_l  }
    result=f.post("https://projectdeliverypankaj-default-rtdb.firebaseio.com/Project",data)
    return result

def pro_1_read_data(index=""):
    f=firebase.FirebaseApplication("https://projectdeliverypankaj-default-rtdb.firebaseio.com/",None)
    r=f.get("https://projectdeliverypankaj-default-rtdb.firebaseio.com/Project",index)
    DF=pd.DataFrame()
    DF["Deliveryid"]=[i["Deliveryid"] for i in r.values()]
    DF["Chaptername"]=[i["Chaptername"] for i in r.values()]
    DF["Topicname"]=[i["Topicname"] for i in r.values()]
    DF["Teacherlead"]=[i["Teacherlead"] for i in r.values()]
    DF["Analystname"]=[i["Analystname"] for i in r.values()]
    DF["Timeline"]=[i["Timeline"] for i in r.values()]

    DF.index=[i for i in r.keys()]
    return DF



@app.route("/projectsavedata", methods=['GET','POST'])
def save():
    Analystname=request.form["ayst_n"]
    Deliveryid=request.form["did"]
    Chaptername=request.form["chp_name"]
    Teacherlead=request.form["tch_lead"]
    Topicname=request.form["tpc_name"]
    Timeline=request.form["time_line"]
    result=pro_1_save_data(Deliveryid,Chaptername,Topicname,Teacherlead,Analystname,Timeline)
    return f'Your Task id is {result["name"]}'
############################################################
#app.run()
