#!/usr/bin/env python

import requests
import pandas as pd 
import StringIO
import json
from basicSim import *
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import os
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)
app.secret_key = "notSecret"

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    #import pdb; pdb.set_trace()
    return jsonify({'tasks': tasks})


@app.route('/get_sim', methods=['GET', 'POST'])
def get_sim():
    from basicSim import runSim
    params = {}
    defaults = {'vx':0, 'vy':0, 'D':0.01, 't':50, 'N':500}

    for key in ['vx', 'vy', 'D', 't', 'N']:
        if request.form[key] == u'':
            params[key] = defaults[key]
        else:
            params[key] = float(request.form[key])

    # flash(params)
    trajectory, xyhist = runSim( [ params['vx'], params['vy'] ], abs( params['D'] ), max( int( params['t'] ), 1), max( int( params['N'] ), 1) )
    
    sim_data = []
    for i in range(int(params['t'])):
        x= [i for j in range(len(trajectory[:,:,i].tolist()))]
        sim_data.append(zip(x,trajectory[:,0,i].tolist(),trajectory[:,1,i].tolist()))
    x = np.asarray(sim_data).tolist()
    data = [j[0] for j in x for j[0] in j]

    result = json.dumps([{"t": j[0], "x":j[1], "y": j[2]} for j in data])
    resulthist = json.dumps(xyhist)

    return render_template("working.html",\
                           diff=result,\
                           hist = resulthist,\
                           time = int(params['t']))


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    from basicSim import runSim
    params = {}
    defaults = {'vx':0, 'vy':0, 'D':0.01, 't':50, 'N':500}

    for key in ['vx', 'vy', 'D', 't', 'N']:
        if request.args.get(key) == u'':
            params[key] = defaults[key]
        else:
            params[key] = float(request.args.get(key))

    scatter, xyhist = runSim( [ params['vx'], params['vy'] ],\
                                abs( params['D'] ),\
                                max( int( params['t'] ), 1),\
                                max( int( params['N'] ), 1) )
    
    scatter_list = []
    for i in range(int(params['t'])):
        x= [i for j in range(len(scatter[:,:,i].tolist()))]
        scatter_list.append(zip(x,scatter[:,0,i].tolist(),scatter[:,1,i].tolist()))
    scatter_list =  [j[0] for j in\
                    np.asarray(scatter_list).tolist() for j[0] in j]

    result = json.dumps({'scatter':[{"t": j[0], "x":j[1], "y": j[2]} for j in scatter_list],\
                         'hist':xyhist})

    return result


@app.route('/results/more_<past_val>_hunches', methods=['GET'])
def more_results(past_val):
    import pdb; pdb.set_trace()
    data = pd.DataFrame.from_csv('static/data/data.tsv', sep='\t')
    return data.to_csv()





@app.route('/get_toy', methods="GET")
def get_toy():
    #gets toy model data
    pass




@app.route('/')
def home():
    #home page
    return render_template("home.html")

@app.route('/working')
def serverTest():
    #testing and debug page
    return render_template("working.html")

@app.route('/lesson1')
def lesson1():
    #home page
    return render_template("lesson1.html")

@app.route('/lesson2')
def lesson2():
    #home page
    return render_template("lesson2.html")

@app.route('/lesson3')
def lesson3():
    #home page
    return render_template("lesson3.html")

@app.route('/lesson4')
def lesson4():
    #home page
    return render_template("lesson4.html")

@app.route('/lesson5')
def lesson5():
    #home page
    return render_template("lesson5.html")

if __name__ == '__main__':
    app.run(debug=True)
