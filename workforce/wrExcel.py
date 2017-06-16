#-*-coding:utf-8-*-#
import xlsxwriter
import math


def wr_workbook(file_name, rs):
    wb = xlsxwriter.Workbook(file_name)
    for i in range(len(rs)):
        new_sheet = wb.add_worksheet(rs[i]['demand_type'])
        to_xlsx(rs[i], wb, new_sheet,startcol=0)
    wb.close()


def wr_workbook_2(file_name, rs, rso):
    print rs[0]['demand_type']
    wb = xlsxwriter.Workbook(file_name)
    for i in range(len(rs)):
        new_sheet = wb.add_worksheet(rs[i]['demand_type'])
        to_xlsx(rs[i], wb, new_sheet, startcol=0)
        to_xlsx(rso[i], wb, new_sheet, startcol=27)
    wb.close()

def to_xlsx(one_rs, wb, sheet, startcol):
    styleBlueBkg = wb.add_format({'bold':  True,'fg_color': 'blue',})# 80% like
    styleYellowBkg = wb.add_format({'bold':  True,'fg_color': 'yellow',})
    styleGrayBkg = wb.add_format({'bold':  True,'fg_color': 'gray',})

    T = one_rs['T']
    I = one_rs['I']
    J = one_rs['J']
    sheet.write(0, 0+startcol, 'T')
    sheet.write(0, 1+startcol, 'I')
    sheet.write(0, 2+startcol, 'J')
    sheet.write(1, 0+startcol, T, styleBlueBkg)
    sheet.write(1, 1+startcol, I, styleBlueBkg)
    sheet.write(1, 2+startcol, J, styleBlueBkg)

    sheet.write(2, 0+startcol, u'折现率')
    sheet.write(2, 1+startcol, one_rs['R'], styleBlueBkg)
    sheet.write(3, 0+startcol, u'招聘技术折扣')
    sheet.write(3, 1+startcol, one_rs['SR'], styleBlueBkg)
    sheet.write(4, 0+startcol, u'空闲工资率')
    sheet.write(4, 1+startcol, one_rs['FR'], styleBlueBkg)

    sheet.write(5, 0+startcol, u'招聘费用')
    basic_hire_cost = one_rs['basic_hire_cost']
    for i in range(len(basic_hire_cost)):
        if i == 0:
            sheet.write(6, i+startcol, basic_hire_cost[i], styleBlueBkg)
        else:
            sheet.write(6, i+startcol, basic_hire_cost[I + 1 - i], styleBlueBkg)

    sheet.write(7, 0+startcol, u'解雇费用')
    basic_fire_cost = one_rs['basic_fire_cost']
    for i in range(len(basic_fire_cost)):
        if i == 0:
            sheet.write(8, i+startcol, basic_fire_cost[i], styleBlueBkg)
        else:
            sheet.write(8, i+startcol, basic_fire_cost[I + 1 - i], styleBlueBkg)

    sheet.write(9, 0+startcol, u'工资成本')
    basic_hire_salary_cost = one_rs['basic_hire_salary_cost']
    for i in range(len(basic_hire_salary_cost)):
        if i == 0:
            sheet.write(10, i+startcol, basic_hire_salary_cost[i], styleBlueBkg)
        else:
            sheet.write(10, i+startcol, basic_hire_salary_cost[I + 1 - i], styleBlueBkg)

    sheet.write(11, 0+startcol, u'设备能力')
    equipment_capacity = one_rs['equipment_capacity']
    for i in range(len(equipment_capacity)):
        sheet.write(11, i + 1+startcol, equipment_capacity[i], styleBlueBkg)

    sheet.write(12, 0+startcol, u'设备单价')
    basic_machine_cost = one_rs['basic_machine_cost']
    for i in range(len(basic_machine_cost)):
        sheet.write(12, i + 1+startcol, basic_machine_cost[i], styleBlueBkg)

    sheet.write(13, 0+startcol, u'指派成本')
    basic_assignment_cost = one_rs['basic_assignment_cost']
    for i in range(I):
        sheet.write(13, i + 1 + startcol, basic_assignment_cost[i], styleBlueBkg)

    sheet.write(14, 0+startcol, u'培训费用')
    basic_train_cost = one_rs['basic_train_cost']
    for i in range(I):
        sheet.write(14, i + 1 + startcol, basic_train_cost[math.pow(2, i)], styleBlueBkg)

    sheet.write(15, 0+startcol, u'培训期')
    basic_train_time = one_rs['basic_train_time']
    for i in range(I):
        sheet.write(15, i + 1+startcol, basic_train_time[math.pow(2, i)], styleBlueBkg)

    sheet.write(16, 0+startcol, u'初始设备数')
    for i in range(I):
        sheet.write(16, i + 1+startcol, 0, styleBlueBkg)

    sheet.write(17, 0+startcol, u'需求')
    demand = one_rs['demand']
    for i in range(T):
        sheet.write(18, i+startcol, i+1)
        sheet.write(19, i+startcol, demand[i], styleBlueBkg)

    if 'Rt' in one_rs.keys():
        sheet.write(20, 0 + startcol, "Rt")
        Rt = one_rs['Rt']
        for t in range(T):
            sheet.write(21, t + startcol, Rt[t])

    if 'Et' in one_rs.keys():
        sheet.write(22, 0 + startcol, "Et")
        Et = one_rs['Et']
        for t in range(T):
            sheet.write(23, t + startcol, Et[t])

    if 'Dt' in one_rs.keys():
        sheet.write(24, 0+startcol, "Dt")
        Dt = one_rs['Dt']
        for i in range(T):
            sheet.write(25, i+startcol, Dt[i])

    if 'alpha' in one_rs.keys():
        sheet.write(26, 0 + startcol, "alpha")
        alpha = one_rs['alpha']
        for t in range(T):
            sheet.write(27, t + startcol, alpha[t])

    if 'beta' in one_rs.keys():
        sheet.write(28, 0 + startcol, "beta")
        beta = one_rs['beta']
        for t in range(T):
            sheet.write(29, t + startcol, beta[t])

    if 'gamma' in one_rs.keys():
        sheet.write(30, 0 + startcol, "gamma")
        gamma = one_rs['gamma']
        for t in range(T):
            sheet.write(31, t + startcol, gamma[t])

    chart = wb.add_chart({'type':'line'})

    sheet_name = one_rs['demand_type']

    # if startcol == 0:
    #     chart.add_series({
    #         'categories' : '= ' + sheet_name + '!$A$19:$J$19',
    #         'values' : '=' + sheet_name + '!$A$20:$J$20',
    #     })
    #
    #     chart.set_y_axis({'name': 'demand'})
    #     sheet.insert_chart('A44', chart)
    # else:
    #     chart.add_series({
    #         'categories': '=' + sheet_name + '!$AA$19:$AJ$19',
    #         'values': '=' + sheet_name + '!$AA$20:$AJ$20',
    #     })
    #     chart.set_y_axis({'name': 'demand'})
    #     sheet.insert_chart('AA44', chart)

    sheet.write(0, 12+startcol, 'solution', styleYellowBkg)
    for i in range(13, 19):
        sheet.write(0, i+startcol, '', styleYellowBkg)

    sheet.write(2, 12+startcol, 'object')
    sheet.write(2, 13+startcol, 'equipment_buy')
    sheet.write(2, 14+startcol, 'equipment_discard')
    sheet.write(2, 15+startcol, 'hire')
    sheet.write(2, 16+startcol, 'train')
    sheet.write(2, 17+startcol, 'fire')
    sheet.write(2, 18+startcol, 'assignment')
    # temporary cost
    if 'additional_cost' in one_rs.keys():
        sheet.write(2, 19+startcol, 'additional')

    sheet.write(3, 12+startcol, one_rs['objective_value'])
    sheet.write(3, 13+startcol, one_rs['machine_cost_total'] )
    sheet.write(3, 14+startcol, one_rs['machine_discard_cost_total'])
    sheet.write(3, 15+startcol, one_rs['hire_cost_total'])
    sheet.write(3, 16+startcol, one_rs['train_cost_total'])
    sheet.write(3, 17+startcol, one_rs['fire_cost_total'])
    sheet.write(3, 18+startcol, one_rs['assignment_cost_total'])
    # temporary cost
    if 'additional_cost' in one_rs.keys():
        sheet.write(3, 19+startcol, one_rs['additional_cost'])

    sheet.write(5, 12+startcol, 'x[i][t]', styleYellowBkg)
    xit = one_rs['xit']
    for i in range(T):
        sheet.write(5, 12 + i + 2+startcol, 't=' + str(i + 1))
    for i in range(I):
        sheet.write(5 + 1 + i, 12+startcol, 'i=' + str(i))
    for i in range(I):
        for t in range(T):
            sheet.write(6 + i, 14 + t+startcol, xit[i][t], styleGrayBkg)

    sheet.write(11, 12+startcol, 'v[i][t]', styleYellowBkg)
    vit = one_rs['vit']
    for i in range(T):
        sheet.write(11, 12 + i + 2+startcol, 't=' + str(i + 1))
    for i in range(I):
        sheet.write(11 + 1 + i, 12+startcol, 'i=' + str(i))
    for i in range(I):
        for t in range(T):
            sheet.write(12 + i, 14 + t+startcol, vit[i][t], styleGrayBkg)

    sheet.write(17, 12+startcol, 'y[j][t]', styleYellowBkg)
    yjt = one_rs['yjt']
    for i in range(T):
        sheet.write(17, 12 + i + 2+startcol, 't=' + str(i + 1))
    for i in range(J):
        sheet.write(17 + 1 + i, 12+startcol, 'j=' + str(i))
    for j in range(J):
        for t in range(T):
            sheet.write(18 + j, 14 + t+startcol, yjt[j][t], styleGrayBkg)

    sheet.write(35, 12+startcol, 'w[j][t]', styleYellowBkg)
    wjt = one_rs['wjt']
    for i in range(T):
        sheet.write(35, 12 + i + 2+startcol, 't=' + str(i + 1))
    for i in range(J):
        sheet.write(35 + 1 + i, 12+startcol, 'j=' + str(i))
    for j in range(J):
        for t in range(T):
            sheet.write(36 + j, 14 + t+startcol, wjt[j][t], styleGrayBkg)

    sheet.write(53, 12+startcol, 'u[j\'][j]t', styleYellowBkg)
    ujjt = one_rs['ujjt']
    train_pair = one_rs['train_pair']
    for i in range(T):
        sheet.write(53, 12 + i + 2+startcol, 't=' + str(i + 1))
    # train_result = np.array(train_result).reshape(-1, 10)
    row = 54
    for rows in range(len(ujjt)):
        if sum([ujjt[rows][t] for t in range(T)]) != 0:
            sheet.write(row, 12+startcol, 'j\'=' + str(train_pair[rows][0]))
            sheet.write(row, 13+startcol, 'j=' + str(train_pair[rows][1]))
            for t in range(T):
                if ujjt[rows][t] != 0:
                    sheet.write(row, 14 + t+startcol, ujjt[rows][t], styleGrayBkg)
            row += 1

    row += 2
    sheet.write(row, 12+startcol, 'z[ijt]', styleYellowBkg)
    zijt = one_rs['zijt']
    for i in range(T):
        sheet.write(row, 12 + i + 2+startcol, 't=' + str(i + 1))
    row += 1
    for i in range(I):
        for j in range(J):
            if sum([zijt[i][j][t] for t in range(T)]) > 0:
                sheet.write(row, 12+startcol, 'j=' + str(j))
                sheet.write(row, 13+startcol, 'i=' + str(i))
                for t in range(T):
                    if zijt[i][j][t] != 0:
                        sheet.write(row, 14 + t+startcol, zijt[i][j][t], styleGrayBkg)
                row += 1

                # return [value, machine_cost_total, hire_cost_total, train_cost_total, fire_cost_total, paiban_cost_total]