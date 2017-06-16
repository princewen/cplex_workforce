#-*-coding:utf-8-*-#
import math
import random
from generate_demand import generate_sample

def init_para(wf,data):
        #时期数
        wf.T = data['periods']
        #设备种类数
        wf.I = data['device']
        #员工种类数
        wf.J = int(math.pow(2, wf.I))
        #折现率
        wf.R = data['discount']
        #招聘技术折扣
        wf.SR = data['hdiscount']
        #空闲工资率
        wf.FR = data['sdiscount']
        #工作工资率
        #wf.WR = 0.3
        #设备的生产力
        wf.equipment_capacity = []
        for i in range(1,wf.I+1):
            wf.equipment_capacity.append(data['dforce'][str(i)])
        #每期的生产需求
        #wf.demand = [32,35,146,231,431,549,739,835,896,970]
        #员工的聘请费用，分别为小白，4，3，2，1类
        wf.basic_hire_cost = [data['hcost']['0']]
        for i in range(wf.I,0,-1):
            wf.basic_hire_cost.append(data['hcost'][str(i)])
        #wf.basic_hire_cost = [x/100 for x in wf.basic_hire_cost]
        #聘请的每一类员工的薪水，分别为小白，4，3，2，1类
        wf.basic_hire_salary_cost = [data['hscost']['0']]
        for i in range(wf.I,0,-1):
            wf.basic_hire_salary_cost.append(data['hscost'][str(i)])
        #训练时间
        wf.basic_train_time = dict()
        for i in range(1,wf.I+1):
            wf.basic_train_time[pow(2,i-1)] = data['ttime'][str(i)]
        #训练费用
        wf.basic_train_cost = dict()
        for i in range(1,wf.I+1):
            wf.basic_train_cost[pow(2,i-1)]=data['tcost'][str(i)]

        #解雇花费,分别小白，4，3，2，1
        wf.basic_fire_cost = [data['fcost']['0']]
        for i in range(wf.I, 0, -1):
            wf.basic_fire_cost.append(data['fcost'][str(i)])
        #购买设备花费
        wf.basic_machine_cost = []
        for i in range(1,wf.I+1):
            wf.basic_machine_cost.append(data['mcost'][str(i)])
        #抛弃设备费用

        wf.basic_discard_machine_cost = []
        for i in range(1, wf.I + 1):
            wf.basic_discard_machine_cost.append(data['dmcost'][str(i)])
        #设备生产成本（指派成本）
        wf.basic_assignment_cost = [50,50,50,50]

def update_5_demand(wf, num):
    demands=[[200,400,650,940,1250,1100,1000,850,750,700],
         [1250,1100,1000,850,750,700,900,1050,1150,1300],
         [300,500,400,650,500,800,700,1000,850,1100],
         [300,500,760,650,500,720,940,830,700,1000],
         []
         ]
    for i in range(4):
        demands[i] = [x * 10 for x in demands[i] ]

    for i in range(10):
        demands[4].append(random.randint(200, 10000))

    wf.demand = demands[num]

def update_1_demand():
    demands =[200,500,800,550,300,600,900,650,400,700]
    return demands


#更改需求类型
    #0:线性 1:增速减小 2：增速增加 3：增速先增加后减小再增加再减小 4：增速先减小后增加再减小再增加
def update_demand(wf,type):
        demand = []
        init = 32
        demand.append(init)

        if type==0:
            speed=int(100+random.random()*100)
            for i in range(1,10):
                demand.append(init+i*speed)
            wf.demand=demand

        elif type==1:
            speed=int(100+random.random()*100)
            for i in range(1,10):
                speed-=int(random.random()*10)
                demand.append(demand[i-1]+speed)
            wf.demand = demand

        elif type==2:
            speed = int(100 + random.random() * 100)
            for i in range(1, 10):
                speed += int(random.random() * 10)
                demand.append(demand[i - 1] + speed)
            wf.demand = demand

        elif type==3:
            time1 = random.randint(2, 4)
            time2 = random.randint(time1, time1 + 5)

            speed = int(random.random() * 10)
            for i in range(1, time1):
                delta_speed = int(300 + random.random() * 100)
                demand.append(demand[i - 1] + delta_speed + speed)

            for i in range(time1, time2):
                delta_speed = int(30 + random.random() * 30)
                demand.append(demand[i - 1] + delta_speed + speed)

            for i in range(time2, 10):
                delta_speed = int(300 + random.random() * 100)
                demand.append(demand[i - 1] + delta_speed + speed)
            wf.demand = demand

        elif type == 4:
            time1=random.randint(2,4)
            time2=random.randint(time1,time1+5)

            speed = int(random.random() * 10)
            for i in range(1,time1):
                delta_speed = int(30 + random.random() * 30)
                demand.append(demand[i-1]+delta_speed+speed)


            for i in range(time1,time2):
                delta_speed = int(300 + random.random() * 100)
                demand.append(demand[i - 1] + delta_speed + speed)

            for i in range(time2,10):
                delta_speed = int(30 + random.random() * 30)
                demand.append(demand[i - 1] + delta_speed + speed)

            wf.demand = demand


def various_demand(wf, args):
    wf.demand = generate_sample(args)

def set_demand(wf,demand):
    wf.demand=demand
