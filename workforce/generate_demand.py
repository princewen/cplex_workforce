#-*-coding:utf-8-*-#
import random
import matplotlib.pyplot as plt
import math

def generate_sample(args):
    type=args['type']
    demand=[]
    if type==0:
        demand=[x*args['a']+args['b'] for x in range(args['len'])]

    if type==1:
        demand=[args['a']*math.pow(x,args['exp'])+args['b'] for x in range(args['len'])]

    if type==2:
        demand=[args['a']*math.log(x,args['logbase'])+args['b'] for x in range(1,args['len']+1)]

    if type==3:
        demand = [args['base']/(1+math.exp(-0.5*(x-args['len']/2))) for x in range(args['len'])]

    if type==4:
        demand = [((x*1.0)/args['len'])*(5.0/6)*math.pi-math.pi*(5.0/12) for x in range(1,args['len']+1)]
        demand = [(math.sin(x)/math.cos(x)+2)*args['a']+args['b'] for x in demand]

    if type==5:
        demand=[x*args['a1']+args['b1'] for x in range(args['len']/2+1)]
        b2=demand[-1]+args['a2']*(-1)*(args['len']/2)
        demand.extend([x*args['a2']+b2 for x in range(args['len']/2+1,args['len'])])

    if type==6:
        demand = [x * args['a1'] + args['b1'] for x in range(args['len'] / 2 + 1)]
        b2 = demand[-1] + args['a2']*(-1) * (args['len'] / 2)
        demand.extend([x * args['a2'] + b2 for x in range(args['len'] / 2 + 1, args['len'])])

    if type==7:
        demand=[args['b1']]
        for i in range(1,args['len']):
            demand.append(demand[i-1]+args['a1'] if i%2==1 else demand[i-1]+args['a2'])

    if type==8:
        demand = [args['b1']]
        for i in range(1, args['len']):
            demand.append(demand[i - 1] + args['a1'] if ((i-1)/2) % 2 == 0 else demand[i - 1] + args['a2'])

    if type==9:
        demand=[random.randint(args['a'],args['b']) for x in range(args['len'])]

    return [int(x) for x in demand]


if __name__ == '__main__':

    args = {
                0:{
                    'type': 0,
                    'a': 200,
                    'b': 300,
                    'len': 10,
                    'name':u'线性增长'
                },

                1:{
                    'type': 1,
                    'a': 200,
                    'b': 60,
                    'len': 10,
                    'exp': 1.5,
                    'name':u'加速增长'
                },

                2:{
                    'type': 2,
                    'a': 200,
                    'b': 40,
                    'len': 10,
                    'logbase': 1.5,
                    'name': u'减速增长'
                },

                3:{
                    'type': 3,
                    'a': 200,
                    'b': 50,
                    'len': 10,
                    'exp': 1.5,
                    'logbase': 1.5,
                    'name': u's型1'
                },

                4:{
                    'type': 4,
                    'a': 500,
                    'b': 300,
                    'len': 10,
                    'name': u's型2'
                },

                5: {
                    'type': 5,
                    'len': 10,
                    'a1':300,
                    'b1':200,
                    'a2':-250,
                    'name': u'先升后降'
                },

                6:{
                    'type': 6,
                    'len': 10,
                    'a1': -200,
                    'b1': 3000,
                    'a2': 250,
                    'name': u'先降后升'
                },

                7:{
                   'type':7,
                    'a1':300,
                    'a2':-250,
                    'b1':200,
                    'len':10,
                    'name': u'1期交替'
                },

                8:{
                    'type': 8,
                    'a1': 300,
                    'a2': -250,
                    'b1': 200,
                    'len': 10,
                    'name': u'2期交替'
                },

                9:{
                    'type':9,
                    'a': 200,
                    'b': 5000,
                    'len':10,
                    'name': u'随机模型'
                }
            }

    for i in range(0,10):
        demand = generate_sample(args[i])
    #print demand
        plt.subplot('25'+str(i))
        plt.title(args[i]['name'])
        plt.plot(demand)
    plt.show()









