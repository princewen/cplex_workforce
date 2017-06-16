#-*-coding:utf-8-*-#
# from docplex.cp.model import *
from docplex.mp.model import Model
import numpy as np
import math

class Workforce():
    #初始化及参数定义
    def __init__(self):
        #时期数
        self.T = 0
        #设备种类数
        self.I = 0
        #员工种类数
        self.J = 0
        #折现率
        self.R = 0
        #招聘技术折扣
        self.SR = 0
        #空闲工资率
        self.FR = 0
        #工作工资率
        self.WR = 0
        #决策变量系数
        self.obj = []
        #约束条件
        self.subject = []
        #约束条件的系数值
        self.subject_value = []
        #约束条件的类型
        self.sense = ''
        #设备的生产力
        self.equipment_capacity = []
        #每期的生产需求
        self.demand = []
        #员工的聘请费用，分别为小白，4，3，2，1类
        self.basic_hire_cost = []
        #聘请的每一类员工的薪水，分别为小白，4，3，2，1类
        self.basic_hire_salary_cost = []
        #训练时间
        self.basic_train_time = {}
        #训练费用
        self.basic_train_cost = {}
        #解雇花费,分别小白，4，3，2，1
        self.basic_fire_cost=[]
        #购买设备花费
        self.basic_machine_cost = []
        #抛弃设备花费
        self.basic_discard_machine_cost=[]
        #排班成本
        self.basic_assignment_cost = []
        #规划目标值
        self.objective_value = 0

    #聘请员工的费用的费用
    def hire_cost(self):
        #得到每一类员工的聘请费用
        #小白的费用
        self.hire_cost_list = [math.pow(self.basic_hire_cost[0], self.SR)]
        #有技能的人的费用
        skill_cost = np.array(self.basic_hire_cost[1:])
        # print(self.basic_hire_cost[1:])
        # print(skill_cost)

        for j in range(1, self.J):
            #将十进制转化为二进制
            bin_list = np.array([int(x) for x in list(bin(j)[2:])])
            #得到每一种类员工的工资
            cost = math.pow(np.sum(skill_cost[-len(bin_list):] * bin_list), self.SR)
            self.hire_cost_list.append(cost)
        #print (self.hire_cost_part1)
        #
        self.hire_cost_matrix =np.array(self.hire_cost_list).reshape(-1,1)

        new_col=np.array(self.hire_cost_list).reshape(-1,1)
        for i in range(1,self.T):
            #每一期的聘请费用要乘以时间价值
            one_col=new_col*math.pow(self.R,i)
            #将每一期的拼接到最后的矩阵当中
            self.hire_cost_matrix=np.concatenate((self.hire_cost_matrix,one_col),axis=1)
        #self.hire_cost_matrix=self.hire_cost_matrix.reshape(-1,self.T)
        #print (self.hire_cost_matrix)
        #print (self.hire_cost_matrix.shape)

    #聘请员工时的薪水折现
    def hire_salary(self):

        #第一期小白的薪水
        self.hire_salary_list = [math.pow(self.basic_hire_salary_cost[0], self.FR)]
        skill_cost = np.array(self.basic_hire_salary_cost[1:])
        #同样的思路计算其他类员工的薪水
        for i in range(1,self.J):
            bin_list = np.array([int(x) for x in list(bin(i)[2:])])
            #print(bin_list)
            cost = math.pow(np.sum(skill_cost[-len(bin_list):] * bin_list), self.FR)
            self.hire_salary_list.append(cost)
        #print (self.hire_salary_list)
        self.hire_salary_matrix = np.array(self.hire_salary_list).reshape(-1, 1)
        new_col = np.array(self.hire_salary_list).reshape(-1, 1)
        #每期的薪水要乘上其时间价值
        for i in range(1, self.T):
            one_col = new_col * math.pow(self.R, i)
            self.hire_salary_matrix = np.concatenate((self.hire_salary_matrix, one_col), axis=1)
        # self.hire_cost_matrix=self.hire_cost_matrix.reshape(-1,self.T)
        # 每期的薪水是从当期到t期的总的薪水的折现之和
        for i in range(self.T):
            self.hire_salary_matrix[:,i]=self.hire_salary_matrix[:,i:].sum(axis=1)

        #print(self.hire_salary_matrix)
        #print(self.hire_salary_matrix.shape)

    #计算招聘成本的总和，等于招聘费用加上支付的工资成本折现
    def hire_cost_total(self):

        self.hire_cost_total=self.hire_cost_matrix+self.hire_salary_matrix

    #得到所有可能的训练对
    def train_time(self):
        self.train_pair=[]
        int_list=[]
        #得到[8,4,2,1]
        for i in range(self.I):
            int_list.append(int(math.pow(2,self.I-i-1)))

        int_array=np.array(int_list)
        #print (int_array)

        for i in range(self.J):
            #十进制转二进制
            bin_list = [int(x) for x in list(bin(i)[2:])]
            #不足四位的话，前面用0补齐
            #print (bin_list)
            while len(bin_list)<self.I:
                bin_list.insert(0,0)

            bin_array=np.array(bin_list)
            #每个数字的二进制位对位取反，与[8,4,2,1]相乘，得到培训之后员工可以变成的工资类型的差值
            #如3类型员工：二进制[0,0,1,1]--》对位取反[1,1,0,0],与[8,4,2,1]对位相乘，得到[8,4,0,0],那么3类型可以训练成为3+8=11类型，也可训练为3+4=77类型
            add_array=((1-bin_array)*int_array)
            for t in add_array:
                if t!=0:
                    #print (t)
                    #将原类型，训练之后类型，以及训练时间三元组加入列表
                    self.train_pair.append([i,i+t,self.basic_train_time[t]])
        # self.train_tuple=[Train(idx) for idx in range(self.train_pair.shape[0])]
        #print (self.train_pair)

    #得到每一训练的训练花费
    def train_cost(self):
        train_cost_list=[]

        #循环每一组训练对
        for i in range(len(self.train_pair)):
            #得到训练类型
            pair = self.train_pair[i]
            type = int(pair[1]-pair[0])
            #得到训练花费
            train_cost_list.append(self.basic_train_cost[type])
        #print (train_cost_list)
        #得到在不同期进行训练的折现值
        self.train_cost_matrix = np.array(train_cost_list).reshape(-1, 1)
        new_col = np.array(train_cost_list).reshape(-1, 1)
        for i in range(1, self.T):
            one_col = new_col * math.pow(self.R, i)
            #拼接成新的矩阵
            self.train_cost_matrix = np.concatenate((self.train_cost_matrix, one_col), axis=1)
        #print (self.train_cost_matrix)

    #得到每一组训练的工资变换的折现值
    def train_salary(self):
        #初始化训练矩阵
        self.train_salary_matrix=np.zeros((len(self.train_pair),self.T))
        #遍历每一组训练对
        for i in range(len(self.train_pair)):
            pair=self.train_pair[i]
            #遍历每一期
            for t in range(self.T):
                #训练完成的时间
                changeT=t+pair[2]
                #训练完成时间在t期内才计算工资变化
                if changeT<self.T:
                    #变换后类型得到的工资-变换前类型的工资
                    self.train_salary_matrix[i,t]+=self.hire_salary_matrix[pair[1],changeT]-self.hire_salary_matrix[pair[0],changeT]
        #print (self.train_salary_matrix)

    #得到训练成本=训练花费+工资变化
    def train_cost_total(self):
        self.train_cost_total_matrix=self.train_cost_matrix+self.train_salary_matrix

    #解雇成本
    def fire_cost(self):
        #小白的解雇费用
        fire_cost_list=[math.pow(self.basic_fire_cost[0],self.SR)]
        #print (fire_cost_list)
        skill_cost=np.array(self.basic_fire_cost[1:])
        #解雇非小白的费用
        for i in range(1,self.J):
            bin_list=np.array([int(x) for x in list(bin(i)[2:])])
            #print (bin_list)
            cost=math.pow(np.sum(skill_cost[-len(bin_list):]*bin_list),self.SR)
            fire_cost_list.append(cost)
        #print (self.hire_cost_part1)
        self.fire_cost_matrix=np.array(fire_cost_list).reshape(-1,1)
        new_col=np.array(fire_cost_list).reshape(-1,1)
        #得到在不同时期解雇员工的费用折现值
        for i in range(1,self.T):
            one_col=new_col*math.pow(self.R,i)
            self.fire_cost_matrix=np.concatenate((self.fire_cost_matrix,one_col),axis=1)
        #self.hire_cost_matrix=self.hire_cost_matrix.reshape(-1,self.T)
        #print(self.fire_cost_matrix[:,1])
        #print (self.hire_salary_matrix[:,1])
        #print self.fire_cost_matrix
        #print self.hire_salary_matrix
        ##解雇员工成本=解雇费用-未来应得工资的贴现
        self.fire_cost_matrix=self.fire_cost_matrix-self.hire_salary_matrix

        #print (self.fire_cost_matrix)
        #print (self.fire_cost_matrix.shape)

    #所有可能的排版矩阵
    def assignment_avail(self):
        avail_array=[]
        for i in range(self.J):
            #十进制转换为二进制
            bin_list = [int(x) for x in list(bin(i)[2:])]
        # print (bin_list)
            #补足为4位
            while len(bin_list) < self.I:
                bin_list.insert(0, 0)
            #将矩阵转置
            bin_list.reverse()
            #添加到矩阵中
            avail_array.append(bin_list)
        #print avail_array

            #print (bin_list)
        #可行的排班矩阵，0代表不可以排班，1代表可以排班，并转置（j,i)转换为（i，j）
        self.avail_array_matrix=np.array(avail_array).transpose()
        #print self.avail_array_matrix

    #排班花费
    def assignment_cost(self):
        #得到排班可行矩阵
        self.assignment_avail()
        #不考虑时间价值，排班费用均为50
        self.assignment_cost_matrix=np.full((self.I,self.J),50.0)
        #排班费用与可行排班矩阵进行相乘，那么不能排班的位置变为0，可以排班是50
        self.assignment_cost_matrix=(self.assignment_cost_matrix) *  self.avail_array_matrix
        #self.assignment_cost_matrix.replace(0,np.infinity)
        #我们将不能排班的位置将矩阵值变为特别大，如果进行排班就会有很高的惩罚
        self.assignment_cost_matrix=np.where(self.assignment_cost_matrix==0,10000000000,self.assignment_cost_matrix).reshape(self.I,self.J,1)

        one_term=self.assignment_cost_matrix
        t=1
        #得到每一期的排班费用
        while t < self.T:
            t += 1
            #
            self.assignment_cost_matrix=np.concatenate((self.assignment_cost_matrix,one_term*math.pow(self.R,t)),axis=2)

        # for t in range(self.T):
        #     self.assignment_cost_matrix[:,:,t]=self.assignment_cost_matrix[:,:,t]*math.pow(self.R,t)

        #print (self.assignment_cost_matrix[:,:,0])

    #购买设备花费
    def machine_cost(self):
        #得到每一期购买设备花费的折现值
        machine_cost_list=np.array(self.basic_machine_cost).reshape(-1,1)
        self.machine_cost_matrix=machine_cost_list
        for t in range(1,self.T):
            self.machine_cost_matrix=np.concatenate((self.machine_cost_matrix, machine_cost_list*math.pow(self.R,t)),axis=1)
        #print (self.machine_cost_matrix)

    #抛弃设备话费
    def discard_machine_cost(self):
        discard_machine_cost_list = np.array(self.basic_discard_machine_cost).reshape(-1, 1)
        self.discard_machine_cost_matrix = discard_machine_cost_list
        for t in range(1, self.T):
            self.discard_machine_cost_matrix = np.concatenate(
                (self.discard_machine_cost_matrix, discard_machine_cost_list * math.pow(self.R, t)), axis=1)
            # print (self.machine_cost_matrix)

    def add_var(self, model):
        #xit
        self.machine_cost()
        self.xit = []
        for i in range(self.I):
            onerow=[]
            for t in range(self.T):
                onerow.append(model.integer_var(lb=0,name='x'+str(i)+str(t)))
            self.xit.append(onerow)

        #vit
        self.discard_machine_cost()
        self.vit = []
        for i in range(self.I):
            onerow=[]
            for t in range(self.T):
                onerow.append(model.integer_var(lb=0,name='v'+str(i)+str(t)))
            self.vit.append(onerow)

        #yjt
        self.hire_cost()
        self.hire_salary()
        self.hire_cost_total()
        self.discard_machine_cost()
        self.yjt = []
        for j in range(self.J):
            onerow=[]
            for t in range(self.T):
                onerow.append(model.integer_var(lb=0,name='y'+str(j)+str(t)))
            self.yjt.append(onerow)

        # 添加训练员工部分ujjt
        self.train_time()
        self.train_cost()
        self.train_salary()
        self.train_cost_total()
        self.ujjt=[]
        for jj in range(self.train_cost_total_matrix.shape[0]):
            onerow=[]
            for t in range(self.T):
                onerow.append(model.integer_var(lb=0,name="u"+str(self.train_pair[jj][0])+str(self.train_pair[jj][1])+str(t)))
            self.ujjt.append(onerow)

        # 添加解雇员工部分wjt
        self.fire_cost()
        self.wjt = []
        for j in range(self.J):
            onerow=[]
            for t in range(self.T):
                onerow.append(model.integer_var(lb=0,name='w'+str(j)+str(t)))
            self.wjt.append(onerow)

        # 添加排班成本zijt
        self.assignment_cost()
        self.zijt=[]
        for i in range(self.I):
            onei=[]
            for j in range(self.J):
                onej=[]
                for t in range(self.T):
                    onej.append(model.integer_var(lb=0,name="z"+str(i)+str(j)+str(t)))
                onei.append(onej)
            self.zijt.append(onei)
        return model

    def my_docplex_obj(self, model):
        total_xit_cost=0
        total_xit_cost+=sum([self.xit[i][t] * self.machine_cost_matrix[i,t] for i in range(self.I) for t in range(self.T)])

        total_vit_cost = 0
        total_vit_cost += sum([self.vit[i][t] * self.discard_machine_cost_matrix[i, t] for i in range(self.I) for t in range(self.T)])

        # 添加雇佣员工部分yjt
        total_yjt_cost = 0
        total_yjt_cost += sum([self.yjt[j][t] * self.hire_cost_total[j, t] for j in range(self.J) for t in range(self.T)])

        # 添加训练员工部分ujjt
        total_ujjt_cost=0
        total_ujjt_cost+=sum([self.ujjt[jj][t] * self.train_cost_total_matrix[jj,t] for jj in range(self.train_cost_total_matrix.shape[0]) for t in range(self.T)])

        # 添加解雇员工部分wjt
        total_wjt_cost = 0
        total_wjt_cost += sum([self.wjt[j][t] * self.fire_cost_matrix[j, t] for j in range(self.J) for t in range(self.T)])

        # 添加排班成本zijt
        total_zijt_cost=0
        total_zijt_cost+=sum([self.zijt[i][j][t] * self.assignment_cost_matrix[i,j,t] for i in range(self.I) for j in range(self.J) for t in range(self.T)])

        additional_cost = sum([self.Dt[x] for x in range(self.T)])

        self.cost_total=total_ujjt_cost+total_zijt_cost+total_vit_cost+total_wjt_cost+total_xit_cost+total_yjt_cost+additional_cost*0.01
        # self.cost_total=total_ujjt_cost+total_zijt_cost+total_vit_cost+total_wjt_cost+total_xit_cost+total_yjt_cost
        model.minimize(self.cost_total)
        return model

    def add_Ancillary_var(self, model):

        b = int(math.sqrt(max(self.demand)/min(self.equipment_capacity)))
        if b < 6:
            b += 3
            if b > 9:
                b -= 3

        print('b = ' + str(b))
        # self.alpha=[math.pow(2,-1*t*b) for t in range(1,self.T+1)]
        # self.alpha = [math.pow(2, -1 * t * b) for t in range(1, self.T + 1)]
        self.alpha = [math.pow(2, -1 * 6) for t in range(1, self.T + 1)]
        self.beta = [x / 2 for x in self.alpha]
        self.gamma = [math.pow(2, -1) for t in range(1, self.T + 1)]

        self.Rt=[]
        self.Et=[]
        self.Dt=[]
        for t in range(self.T):
            self.Rt.append(model.integer_var(lb=0,name='R'+str(t)))
            self.Et.append(model.integer_var(lb=0,name='E'+str(t)))
            self.Dt.append(model.continuous_var(lb=-1,name='D'+str(t)))

        self.syjt=[]
        for j in range(self.J):
            onerow=[]
            for t in range(self.T):
                peoplecount=0
                peoplecount+=self.yjt[j][t]
                peoplecount-=self.wjt[j][t]

                for fromj in range(self.J):
                    if [fromj,j,0] in self.train_pair:
                        peoplecount+=self.ujjt[self.train_pair.index([fromj,j,0])][t]
                    elif [fromj,j,1] in self.train_pair and t>0:
                        #print self.train_pair.index([fromj, j, 1])
                        peoplecount += self.ujjt[self.train_pair.index([fromj, j, 1])][t-1]

                for toj in range(self.J):
                    if [j,toj,0] in self.train_pair:
                        peoplecount-=self.ujjt[self.train_pair.index([j,toj,0])][t]
                    elif [j,toj,1] in self.train_pair:
                        peoplecount -= self.ujjt[self.train_pair.index([j, toj, 1])][t]

                if t>0:
                    peoplecount+=onerow[t-1]
                onerow.append(peoplecount)
            self.syjt.append(onerow)

        return model

    def add_dt_constraint(self, model):
        for t in range(self.T):
            work_ability = 0
            for i in range(self.I):
                work_ability += sum([self.equipment_capacity[i]*self.zijt[i][j][t] for j in range(self.J)])
            model.add_constraint(work_ability >= (1 + self.Dt[t]) * self.demand[t])
            # model.add_constraint(work_ability >= self.Dt[t]*self.demand[t])
            # model.add_constraint(work_ability >= self.demand[t])

        return model

    def add_people_constraint(self, model):
        for i in range(self.I):
            for t in range(self.T):
                people_count = sum([self.zijt[i][j][t] for j in range(self.J)])
                machine_count = sum([self.xit[i][tt] for tt in range(0,t+1)])-sum([self.vit[i][tt] for tt in range(0,t+1)])
                model.add_constraint(people_count<=machine_count)
        return model

    def add_avail_people_constraint(self, model):
        for j in range(self.J):
            for t in range(self.T):
                people_count=sum([self.zijt[i][j][t] for i in range(self.I)])
                model.add_constraint(people_count<=self.syjt[j][t])

        return model

    def add_additional_constraint(self, model):

        for t in range(self.T):
            model.add_constraint(self.Rt[t]>=sum([self.wjt[j][t]-self.yjt[j][t] for j in range(self.J)]))
            model.add_constraint((self.Et[t]-self.Rt[t])==sum([self.yjt[j][t]-self.wjt[j][t] for j in range(self.J)]))

        # model.add_constraint(self.Rt[0] == 0)
        # model.add_constraint(self.Et[0] == 12)


        # model.add_constraint(self.Dt[0]==self.alpha[0]*self.Rt[0]-self.beta[0]*self.Et[0])
        model.add_constraint(self.Dt[0]==0)
        for t in range(1,self.T):
            model.add_constraint(self.Dt[t]==self.gamma[t]*self.Dt[t-1]+self.alpha[t]*self.Rt[t]-self.beta[t]*self.Et[t])

        # for t in range(self.T):
        #     model.add_constraint(self.Dt[t] >= -1)



        # for t in range(self.T):
        #     model.add_constraint(self.Rt[t]>=0)
        #     model.add_constraint(self.Et[t]>=0)


        return model

    def add_constraint(self, model):
        model = self.add_dt_constraint(model)
        model = self.add_people_constraint(model)
        model = self.add_avail_people_constraint(model)
        model = self.add_additional_constraint(model)

        return model

    def solve_problem(self):
        model = Model()
        model = self.add_var(model)
        model = self.add_Ancillary_var(model)
        model = self.my_docplex_obj(model)

        model.set_output_level = 0
        model = self.add_constraint(model)

        model.solve()

        self.objective_value = model.objective_value

    def out_result(self):
        rs = dict()

        rs['T'] = self.T
        rs['I'] = self.I
        rs['J'] = self.J

        rs['R'] = self.R
        rs['SR'] = self.SR
        rs['FR'] = self.FR

        rs['basic_hire_cost'] = self.basic_hire_cost
        rs['basic_fire_cost'] = self.basic_fire_cost
        rs['basic_hire_salary_cost'] = self.basic_hire_salary_cost

        rs['equipment_capacity'] = self.equipment_capacity
        rs['basic_machine_cost'] = self.basic_machine_cost
        rs['basic_assignment_cost'] = self.basic_assignment_cost

        rs['basic_train_cost'] = self.basic_train_cost
        rs['basic_train_time'] = self.basic_train_time

        rs['demand'] = self.demand

        rs['alpha'] = self.alpha
        rs['beta'] = self.beta
        rs['gamma'] = self.gamma

        rs['Rt'] = []
        for t in range(self.T):
            rs['Rt'].append(self.Rt[t].solution_value)
        rs['Et'] = []
        for t in range(self.T):
            rs['Et'].append(self.Et[t].solution_value)
        rs['Dt'] = []
        for t in range(self.T):
            rs['Dt'].append(self.Dt[t].solution_value)

        rs['objective_value'] = self.objective_value
        rs['machine_cost_total'] = sum([self.xit[i][t].solution_value * self.machine_cost_matrix[i, t]
                                        for i in range(self.I) for t in range(self.T)])
        rs['machine_discard_cost_total'] = sum([self.vit[i][t].solution_value * self.discard_machine_cost_matrix[i,t]
                                                for i in range(self.I) for t in range(self.T)])
        rs['hire_cost_total'] = sum([self.yjt[j][t].solution_value * self.hire_cost_total[j, t]
                                     for j in range(self.J) for t in range(self.T)])
        rs['train_cost_total'] = sum([self.ujjt[jj][t].solution_value * self.train_cost_total_matrix[jj, t]
                                      for jj in range(self.train_cost_total_matrix.shape[0]) for t in range(self.T)])
        rs['fire_cost_total'] = sum([self.wjt[j][t].solution_value * self.fire_cost_matrix[j, t]
                                     for j in range(self.J) for t in range(self.T)])
        rs['assignment_cost_total'] = sum([self.zijt[i][j][t].solution_value * self.assignment_cost_matrix[i, j, t]
                                            for i in range(self.I) for j in range(self.J) for t in range(self.T)])
        rs['additional_cost'] = sum([self.Dt[t].solution_value for t in range(self.T)])     # temporary cost

        rs['xit'] = []
        for i in range(self.I):
            newI = []
            for t in range(self.T):
                newI.append(self.xit[i][t].solution_value)
            rs['xit'].append(newI)

        rs['vit'] = []
        for i in range(self.I):
            newI = []
            for t in range(self.T):
                newI.append(self.vit[i][t].solution_value)
            rs['vit'].append(newI)

        rs['yjt'] = []
        for j in range(self.J):
            newJ = []
            for t in range(self.T):
                newJ.append(self.yjt[j][t].solution_value)
            rs['yjt'].append(newJ)

        rs['wjt'] = []
        for j in range(self.J):
            newJ = []
            for t in range(self.T):
                newJ.append(self.wjt[j][t].solution_value)
            rs['wjt'].append(newJ)

        rs['ujjt'] = []
        for jj in range(self.train_cost_total_matrix.shape[0]):
            newJJ = []
            for t in range(self.T):
                newJJ.append(self.ujjt[jj][t].solution_value)
            rs['ujjt'].append(newJJ)

        rs['train_pair'] = self.train_pair

        rs['zijt'] = []
        for i in range(self.I):
            newI = []
            for j in range(self.J):
                newJ = []
                for t in range(self.T):
                    newJ.append(self.zijt[i][j][t].solution_value)
                newI.append(newJ)
            rs['zijt'].append(newI)

        return rs
