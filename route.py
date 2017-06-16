#-*-coding:utf-8-*-#

from flask import Flask
from flask import render_template
from flask import request
from workforce.main import *
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/t1',methods=['POST','GET'])
def t1():
    if request.method=='GET':
        return render_template('t1.html')
    if request.method=='POST':
        data = dict()
        data['periods'] = int(request.form['periods'])
        data['device'] = int(request.form['device'])
        data['dtype'] = int(request.form['dtype'])
        data['discount'] = float(request.form['discount'])
        data['hdiscount'] = float(request.form['hdiscount'])
        data['sdiscount'] = float(request.form['sdiscount'])
        mcost = dict()
        for i in range(1,data['device']+1):
            mcost[str(i)] = int(request.form['mcost'+str(i)])
        data['mcost'] = mcost

        dmcost = dict()
        for i in range(1,data['device']+1):
            dmcost[str(i)] = int(request.form['dmcost' + str(i)])
        data['dmcost'] = dmcost

        dforce = dict()
        for i in range(1,data['device']+1):
            dforce[str(i)] = int(request.form['dforce' + str(i)])
        data['dforce'] = dforce

        hcost = dict()
        for i in range(data['device']+1):
            hcost[str(i)] = int(request.form['hcost' + str(i)])
        data['hcost'] = hcost

        hscost = dict()
        for i in range(data['device']+1):
            hscost[str(i)] = int(request.form['hscost' + str(i)])
        data['hscost'] = hscost

        fcost = dict()
        for i in range(data['device']+1):
            fcost[str(i)] = int(request.form['fcost' + str(i)])
        data['fcost'] = fcost

        tcost = dict()
        for i in range(1,data['device']+1):
            tcost[str(i)] = int(request.form['tcost' + str(i)])
        data['tcost'] = tcost

        ttime = dict()
        for i in range(1,data['device']+1):
            ttime[str(i)] = int(request.form['ttime' + str(i)])
        data['ttime'] = ttime

        acost = dict()
        for i in range(1,data['device']+1):
            acost[str(i)] = int(request.form['acost' + str(i)])
        data['acost'] = acost
        print (data)

        data_og = dict()
        data_og['periods'] = int(request.form['periods'])
        data_og['device'] = int(request.form['device'])
        data_og['dtype'] = int(request.form['dtype'])
        data_og['discount'] = float(request.form['discount'])
        data_og['hdiscount'] = float(request.form['hdiscount'])
        data_og['sdiscount'] = float(request.form['sdiscount'])
        mcost = dict()
        for i in range(1, data['device'] + 1):
            mcost[str(i)] = int(request.form['1mcost' + str(i)])
        data_og['mcost'] = mcost

        dmcost = dict()
        for i in range(1, data['device'] + 1):
            dmcost[str(i)] = int(request.form['1dmcost' + str(i)])
        data_og['dmcost'] = dmcost

        dforce = dict()
        for i in range(1, data['device'] + 1):
            dforce[str(i)] = int(request.form['1dforce' + str(i)])
        data_og['dforce'] = dforce

        hcost = dict()
        for i in range(data['device'] + 1):
            hcost[str(i)] = int(request.form['1hcost' + str(i)])
        data_og['hcost'] = hcost

        hscost = dict()
        for i in range(data['device'] + 1):
            hscost[str(i)] = int(request.form['1hscost' + str(i)])
        data_og['hscost'] = hscost

        fcost = dict()
        for i in range(data['device'] + 1):
            fcost[str(i)] = int(request.form['1fcost' + str(i)])
        data_og['fcost'] = fcost

        tcost = dict()
        for i in range(1, data['device'] + 1):
            tcost[str(i)] = int(request.form['1tcost' + str(i)])
        data_og['tcost'] = tcost

        ttime = dict()
        for i in range(1, data['device'] + 1):
            ttime[str(i)] = int(request.form['1ttime' + str(i)])
        data_og['ttime'] = ttime

        acost = dict()
        for i in range(1, data['device'] + 1):
            acost[str(i)] = int(request.form['1acost' + str(i)])
        data_og['acost'] = acost
        print (data_og)

        rs,rso,filename = process(data,data_og)
        return render_template('t1_result.html',rs=rs,rso=rso,filename=filename)

@app.route('/t2',methods=['POST','GET'])
def t2():
    if request.method=='GET':
        return render_template('t2.html')
    if request.method=='POST':
        pass

@app.route('/t3',methods=['POST','GET'])
def t3():
    if request.method=='GET':
        return render_template('t3.html')
    if request.method=='POST':
        pass

@app.route('/t4',methods=['POST','GET'])
def t4():
    if request.method=='GET':
        return render_template('t4.html')
    if request.method=='POST':
        pass


@app.route('/test',methods=['POST','GET'])
def test_form():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        print (username,password)
        return render_template('hello.html',name=username)

@app.route('/openexcel',methods=['POST','GET'])
def open_excel():
    if request.method=='POST':
        filename = request.form['name']
        os.system('cd /Users/shixiaowen/python3/workforce_flask')
        os.system('open '+filename)
        return render_template('index.html')


if __name__ == '__main__':
    app.run()

