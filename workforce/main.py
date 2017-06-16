#-*-coding:utf-8-*-#
from workforce import Workforce
from workforceOriginal import WorkforceOri
from wrExcel import wr_workbook,wr_workbook_2
import matplotlib.pyplot as plt
import datetime
from params import *
from decimal import getcontext, Decimal
import sys
import multiprocessing
import random

def demand_types():
    args1 = [{
                    'type': 0,
                    'a': 200,
                    'b': 300,
                    'len': 10,
                    'name':u'线性增长'
                },{

                    'type': 1,
                    'a': 200,
                    'b': 60,
                    'len': 10,
                    'exp': 1.5,
                    'name':u'加速增长'
                },{

                    'type': 2,
                    'a': 200,
                    'b': 40,
                    'len': 10,
                    'logbase': 1.5,
                    'name': u'减速增长'
                },{

                    'type': 3,
                    'a': 200,
                    'b': 50,
                    'len': 10,
                    'base':1000,
                    'name': u's型1'
                },{

                    'type': 4,
                    'a': 500,
                    'b': 300,
                    'len': 10,
                    'name': u's型2'
                },{
                    'type': 5,
                    'len': 10,
                    'a1':300,
                    'b1':200,
                    'a2':-250,
                    'name': u'先升后降'
                },{

                    'type': 6,
                    'len': 10,
                    'a1': -200,
                    'b1': 3000,
                    'a2': 250,
                    'name': u'先降后升'
                },{

                   'type':7,
                    'a1':300,
                    'a2':-250,
                    'b1':200,
                    'len':10,
                    'name': u'1期交替'
                },{

                    'type': 8,
                    'a1': 300,
                    'a2': -250,
                    'b1': 200,
                    'len': 10,
                    'name': u'2期交替'
                },{

                    'type':9,
                    'a': 200,
                    'b': 3000,
                    'len':10,
                    'name': u'随机模型'
                }]

    return args1

def change_demand_para(args2):
    id=args2['type']
    if id==0:
        args2['a']=random.randint(100,200)+100
        args2['b']=random.randint(100,200)+200
    elif id==1:
        args2['a'] = random.randint(100, 200) + 100
        args2['b']=random.randint(50,100)
        args2['exp']=float(Decimal(random.random()*0.6+0.2+1).quantize(Decimal('0.00')))
    elif id == 2:
        args2['a'] = random.randint(100, 200) + 100
        args2['b'] = random.randint(50, 100)
        args2['logbase'] = float(Decimal(random.random() * 0.6 + 0.2 + 1).quantize(Decimal('0.00')))
    elif id == 3:
        args2['base']=random.randint(800,1200)
    elif id == 4:
        args2['a'] = random.randint(400, 600)
        args2['b'] = random.randint(200, 400)
    elif id == 5:
        args2['a1'] = random.randint(250, 350)
        args2['b1'] = random.randint(150, 250)
        args2['a2']= random.randint(200,250)*-1

    elif id == 6:
        args2['a2'] = random.randint(250, 350)
        args2['b1'] = random.randint(2800, 3200)
        args2['a1'] = random.randint(200, 250) * -1
    elif id == 7:
        args2['a1'] = random.randint(250, 350)
        args2['b1'] = random.randint(150, 250)
        args2['a2'] = random.randint(200, 250) * -1
    elif id == 8:
        args2['a1'] = random.randint(250, 350)
        args2['b1'] = random.randint(150, 250)
        args2['a2'] = random.randint(200, 250) * -1
    elif id == 9:
        args2['a'] = random.randint(100, 200) + 100
        args2['b'] = random.randint(2000, 2500) + 200

    return args2


def process(data,data_og):
    name = [u'线性增长',u'加速增长',u'减速增长',u's型1',u's型2',u'先升后降',u'先降后升',u'1期交替',u'2期交替',u'随机模型']
    RSs = []
    RSOs = []
    arg2 = dict()
    arg2['type'] = data['dtype']
    arg2['len'] = data['periods']
    args = change_demand_para(arg2)
    wf = Workforce()
    init_para(wf,data)
    # update_5_demand(wf, i)                # i =0 to 4

    various_demand(wf, args)


    #print demand


    wf.solve_problem()
    rs = wf.out_result()
    rs['demand_type'] = name[data['dtype']]
    RSs.append(rs)

    wfo = WorkforceOri()
    init_para(wfo,data_og)
    set_demand(wfo,wf.demand)
    #various_demand(wfo, args1[i])
    wfo.solve_problem()
    rso = wfo.out_result()
    rso['demand_type'] = name[data['dtype']]
    RSOs.append(rso)
    now = datetime.datetime.now()
    filename = 'RS' + now.strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx'
    wr_workbook_2(filename, RSs, RSOs)
    return rs,rso,filename



if __name__ == "__main__":

    # RSs = []
    # RSOs = []
    for i in range(1):

        manager = multiprocessing.Manager()
        RSs = manager.list()
        RSOs= manager.list()
        ##这部分用于单个实验#
        # print u'2期交替'
        # wf = Workforce()
        # init_para(wf,i=4,t=10)
        # wf.demand = update_1_demand()
        # print(wf.demand)
        # wf.solve_problem()
        # rs = wf.out_result()
        # rs['demand_type'] = u'2期交替'
        # RSs.append(rs)
        ##结束：这部分用于单个实验#
        start()