import copy
from collections import defaultdict

import matplotlib.pyplot as plt
from Machine_Distribution_lastest._Job import Job
from Machine_Distribution_lastest._Machine import Machine_Time_window
import numpy as np
import pandas as pd
import Machine_Distribution_lastest._Time_Axis_Manager as _Time_Axis_Manager
from datetime import datetime, timedelta
import re
from collections import Counter


# from Data_Extraction_from_Excel import secondary_resource, switching_time, category, switching_cost, \
#     new_job_dict, axle_resource_num
# from pa_main import secondary_resource, switching_time, category, switching_cost, \
#     new_job_dict, axle_resource_num, color_machine_dict, machine_list, srn_type_dict, Machine_dict

# from pa_main_all import secondary_resource, switching_time, category, switching_cost, \
#     new_job_dict, axle_resource_num, color_machine_dict, machine_list, srn_type_dict, Machine_dict
# from pa_test_0322 import secondary_resource, switching_time, category, switching_cost, \
#     new_job_dict, axle_resource_num, color_machine_dict, machine_list, srn_type_dict, Machine_dict
# machine_start_time = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 14.0, 10, 10, 10, 15.0, 10, 10, 26.0, 10, 10,
#                       10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
#                       10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
#                       10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]


# 0320
# machine_list = [['514'], ['515'], ['905'], ['916'], ['907'], ['908'], ['815'], ['509'], ['603'], ['613'], ['704'], ['1013', '1014', '115', '116', '117', '118', '119', '712', '816'], ['1006', '1007', '209', '210', '211', '212', '213', '301', '711'], ['206', '207', '208', '304', '305', '508', '606', '701', '702', '707', '817', '910', '913'], ['1011', '1012', '507', '708', '710'], ['203', '204', '205', '302', '303', '609', '610', '611', '612'], ['1107', '308', '405', '407', '410'], ['1004', '501', '505', '605', '909'], ['604'], ['516'], ['310', '408', '409', '504'], ['820'], ['1003', '1110', '309', '312', '406', '608'], ['1106'], ['808'], ['503', '404'], ['819'], ['917', '919'], ['1105', '705'], ['1103'], ['1112'], ['1101', '402', '602'], ['206', '207', '208', '304', '305', '508', '606', '701', '702', '707', '817', '910', '913'], ['509', '603', '613', '704', '815'], ['1006', '1007', '209', '210', '211', '212', '213', '301', '711'], ['206', '207', '208', '304', '305', '508', '606', '701', '702', '707', '817', '910', '913'], ['1011', '1012', '507', '708', '710'], ['203', '204', '205', '302', '303', '609', '610', '611', '612'], ['407', '308', '405', '410', '1107'], ['1004', '501', '505', '605', '909'], ['516'], ['820', '409', '408', '310', '504'], ['1006', '1007', '209', '210', '211', '212', '213', '301', '711'], ['206', '207', '208', '304', '305', '508', '606', '701', '702', '707', '817', '910', '913'], ['1011', '1012', '507', '708', '710'], ['203', '204', '205', '302', '303', '609', '610', '611', '612'], ['407', '308', '405', '410', '1107'], ['1004', '501', '505', '605', '909'], ['604'], ['516'], ['820', '409', '408', '310', '504'], ['1003', '1110', '309', '312', '406', '608'], ['808'], ['819', '404', '503'], ['917', '919'], ['1006', '1007', '209', '210', '211', '212', '213', '301', '711'], ['203', '204', '205', '302', '303', '609', '610', '611', '612'], ['407', '308', '405', '410', '1107'], ['1004', '501', '505', '605', '909'], ['604'], ['516'], ['820', '409', '408', '310', '504'], ['1003', '1110', '309', '312', '406', '608'], ['808'], ['819', '404', '503'], ['917', '919'], ['1105', '705'], ['1103'], ['1112'], ['1101', '402', '602'], ['401', '601'], ['203', '204', '205', '302', '303', '609', '610', '611', '612'], ['407', '308', '405', '410', '1107'], ['1004', '501', '505', '605', '909'], ['820', '409', '408', '310', '504'], ['1003', '1110', '309', '312', '406', '608'], ['808'], ['819', '404', '503'], ['917', '919'], ['1105', '705'], ['1101', '402', '602'], ['1105', '705']]
# srn_type_dict = {'纱架': 32, '蚕丝架': 1, 'S': 9, 'M': 13, 'L': 16, 'Y': 10, 'G': 1}
# Machine_dict = {0: '514', 1: '515', 2: '905', 3: '916', 4: '907', 5: '908', 6: '815', 7: '509', 8: '603', 9: '613', 10: '704', 11: '115', 12: '116', 13: '117', 14: '118', 15: '119', 16: '712', 17: '816', 18: '1013', 19: '1014', 20: '209', 21: '210', 22: '211', 23: '212', 24: '213', 25: '301', 26: '711', 27: '1006', 28: '1007', 29: '206', 30: '207', 31: '208', 32: '304', 33: '305', 34: '508', 35: '606', 36: '701', 37: '702', 38: '707', 39: '817', 40: '910', 41: '913', 42: '507', 43: '708', 44: '710', 45: '1011', 46: '1012', 47: '203', 48: '204', 49: '205', 50: '302', 51: '303', 52: '609', 53: '610', 54: '611', 55: '612', 56: '308', 57: '405', 58: '407', 59: '410', 60: '1107', 61: '505', 62: '501', 63: '605', 64: '909', 65: '1004', 66: '604', 67: '516', 68: '408', 69: '409', 70: '310', 71: '504', 72: '820', 73: '309', 74: '312', 75: '1003', 76: '1110', 77: '406', 78: '608', 79: '1106', 80: '808', 81: '404', 82: '503', 83: '917', 84: '919', 85: '819', 86: '705', 87: '1105', 88: '1103', 89: '1112', 90: '402', 91: '602', 92: '1101', 93: '401', 94: '601'}


class Decode:
    def __init__(self, J, Processing_time, M_num, Priority, secondary_resource, switching_time, category,
                 switching_cost,
                 new_job_dict, axle_resource_num, color_machine_dict, machine_list, srn_type_dict, Machine_dict,
                 machine_start_time, machine_message, machine_pre_color, json_dict, Old_job_dict):
        self.Processing_time = Processing_time
        self.Scheduled = []  # 已经排产过的工序
        self.M_num = M_num  # 机器数
        self.Machines = []  # 存储机器类
        self.fitness = 0  # 适应度
        self.J = J  # 各工件对应工序数 1号工件3个工序 字典
        self.Priority = Priority  # 优先级
        self.sum_pri = 0  # 优先级*完工时间之和
        self.machine_start_time = machine_start_time
        for j in range(M_num):
            # self.Machines.append(Machine_Time_window(j))
            # self.Machines.append(Machine_Time_window(j, machine_message))
            self.Machines.append(Machine_Time_window(j, machine_message, self))
        for st in range(len(machine_start_time)):  # 更改机器开始可用时间
            self.Machines[st].End_time = self.machine_start_time[st]
        self.Machine_State = np.zeros(M_num, dtype=int)  # 在机器上加工的工件是哪个
        self.Jobs = []  # 存储工件类
        for k, v in J.items():  # k:key  v:value
            self.Jobs.append(Job(k, v))  # 几个工件创建多少个
        self.job_message_list = list(new_job_dict.values())
        # 新增
        self.new_job_dict = new_job_dict
        # self.machine_id_dict = {12:209, 13:210, 14:211, 15:212, 16:213, 17:301, 18:711, 19:1006, 20:1007}
        # self.machine_id_dict = {0: '514', 1: '515', 2: '905', 3: '916', 4: '907', 5: '908', 6: '815', 7: '509', 8: '603', 9: '613', 10: '704', 11: '115', 12: '116', 13: '117', 14: '118', 15: '119', 16: '712', 17: '816', 18: '1013', 19: '1014', 20: '209', 21: '210', 22: '211', 23: '212', 24: '213', 25: '301', 26: '711', 27: '1006', 28: '1007', 29: '206', 30: '207', 31: '208', 32: '304', 33: '305', 34: '508', 35: '606', 36: '701', 37: '702', 38: '707', 39: '817', 40: '910', 41: '913', 42: '507', 43: '708', 44: '710', 45: '1011', 46: '1012', 47: '203', 48: '204', 49: '205', 50: '302', 51: '303', 52: '609', 53: '610', 54: '611', 55: '612', 56: '308', 57: '405', 58: '407', 59: '410', 60: '1107', 61: '505', 62: '501', 63: '605', 64: '909', 65: '1004', 66: '604', 67: '516', 68: '408', 69: '409', 70: '310', 71: '504', 72: '820', 73: '309', 74: '312', 75: '1003', 76: '1110', 77: '406', 78: '608', 79: '1106', 80: '808', 81: '404', 82: '503', 83: '917', 84: '919', 85: '819', 86: '705', 87: '1105', 88: '1103', 89: '1112', 90: '402', 91: '602', 92: '1101', 93: '401', 94: '601'}
        self.machine_id_dict = Machine_dict
        # self.color_machine_dict = {'深色': [12, 17, 20], '中色': [13, 18], '浅色': [14, 19], '浅浅': [15], '增白': [16]}  # 从0开始
        # self.color_machine_dict = {
        #     '180': {'深色': [59, 60, 62], '中色': [56, 61], '浅色': [57], '浅浅': [58, 64], '增白': [63, 65]},
        #     '40': {'深色': [23, 27], '中色': [24, 28], '浅色': [20, 25], '浅浅': [21, 26], '增白': [22]}}
        self.color_machine_dict = color_machine_dict
        self.non_continuous_production = ['深色', '中色', '浅色']
        self.secondary_resource = secondary_resource
        self.switching_time = switching_time
        self.category = category
        self.switching_cost = switching_cost
        self.new_job_dict = new_job_dict
        self.axle_resource_num = axle_resource_num
        self.machine_list = machine_list
        self.srn_type_dict = srn_type_dict
        self.machine_message = machine_message
        self.Color_list = ['深色', '中色', '浅色', '浅浅', '增白']
        self.origin_machine_color = machine_pre_color
        self.time_axis = _Time_Axis_Manager.TimeAxisManager(json_dict)
        self.timeline = self.time_axis._generate_timeline(json_dict)
        # for i in range(M_num):
        #     self.origin_machine_color[i] = "深色"

        # 新增交期数据字典（从 new_job_dict 中提取）
        self.delivery_dates = self.Get_Delivery_Dates(Old_job_dict)
        # {
        #     job_info[0]['标识号']: datetime.strptime(job_info[0]['计划漂染完成日期'], "%Y-%m-%d %H:%M:%S")
        #     for job_id, job_info in new_job_dict.items()
        #     if job_info[0]['计划漂染完成日期']  # 过滤掉空字符串或 None
        # }
        # 初始化染色工序可行时间窗,
        self.time_windows, self.order_errors = self.calculate_time_intervals(json_dict)
        # 经向同批、纱轴同批
        # self.schedule_dict = self.get_schedule_dict(self.Machines)
        self.production_dict = self.get_production_dict(json_dict)
        self.warp_limit_days, self.yarn_limit_days = self.get_completion_days(json_dict)
        # 同一合作序号下订单安排在同一机台
        self.coop_dict = self.get_coop_dict(json_dict)

    # 时间顺序矩阵和机器顺序矩阵
    def Order_Matrix(self, MS):  # MS为CHS的一半，一行
        JM = []  # 机器顺序矩阵，JM[j，h]代表工件j的工序h的机器号
        T = []  # 时间顺序矩阵，T[j，h]代表工件j的工序h的加工时间
        Ms_decompose = []
        # print(MS)
        Site = 0
        for S_i in self.J.values():  # J.values() = 3, 4, 3, 3, 4, 3, 3, 4
            Ms_decompose.append(MS[Site:Site + S_i])  # MS存放机器索引-->[[0:3], [3:7]……]
            Site += S_i  # 更新Site，跳过已经填入的列
        # print("Ms_decompose = ", Ms_decompose)
        # print("len(Ms_decompose) = ", len(Ms_decompose))  # 8
        for i in range(len(Ms_decompose)):  # len(Ms_decompose) = 8
            JM_i = []  # 工件i的所有工序按优先顺序加工的各个机器号的排列
            T_i = []  # 时间排列
            for j in range(len(Ms_decompose[i])):
                # print("i,j",i,j)
                # print("Ms_decompose[i] = ", Ms_decompose[i])
                O_j = self.Processing_time[i][j]  # 工件i工序j的所有机器加工时间值
                M_ij = []
                T_ij = []
                for Mac_num in range(len(O_j)):  # 寻找MS对应部分的机器时间和机器顺序
                    if O_j[Mac_num] != 9999:
                        M_ij.append(Mac_num)  # O_j对应的机器索引值 real_index
                        T_ij.append(O_j[Mac_num])  # 记录时间
                    else:
                        continue
                # i = 0
                # i = i + 1
                # print(i)
                # print("M_ij",M_ij)
                JM_i.append(M_ij[Ms_decompose[i][j]])
                T_i.append(T_ij[Ms_decompose[i][j]])
            JM.append(JM_i)
            T.append(T_i)
        return JM, T

    def Earliest_Start(self, Job, O_num, Machine):  # JM[j，h]代表工件j的工序h的机器号，j-->Job, h-->O_num
        P_t = self.Processing_time[Job][O_num][Machine]  # 某工件的加工时间
        # P_t2 = self.Processing_time[Job][O_num-1][Machine2]  # 某工件上道工序的加工时间
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine = Machine

        M_window = self.Machines[Selected_Machine].Empty_time_window()  # 提取时间窗，判断是否可以插入
        M_Tstart = M_window[0]  # 开始
        M_Tend = M_window[1]  # 结束
        M_Tlen = M_window[2]  # 持续

        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)

        if M_Tlen is not None:  # 此处为全插入时窗
            for le_i in range(len(M_Tlen)):
                if M_Tlen[le_i] >= P_t:  # 空闲时间足以生产
                    if M_Tstart[le_i] >= last_O_end:  # 时间窗开始时间在上道工序完工之后
                        ealiest_start = M_Tstart[le_i]  # 提前
                        break
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:  # 时间窗开始时间在上道工序完工之前，到时间窗结束仍能生产
                        ealiest_start = last_O_end
                        break

        M_Ealiest = ealiest_start
        End_work_time = M_Ealiest + P_t  # 此工序的完工时间
        # End_work_time, gap = self.adjust_for_shift_gap(ealiest_start, P_t)  # 此工序的完工时间;尝试更改为此形式，还是不对
        return M_Ealiest, Selected_Machine, P_t, O_num, last_O_end, End_work_time
        # 返回某工件的 1、最早开始时间 2、选择机器 3、加工所需时间 4、工序号 5、上道工序完工时间 6、此工序的完工时间

    # def Earliest_Start_no_time_window(self, Job, O_num, Machine, last_job):
    #     """
    #     在计算最早开始时间，就考虑副资源释放以及切换时间？？？
    #     :param used_resource: 该作业使用的副资源
    #     :param Job: 当前要加工的作业
    #     :param O_num:
    #     :param Machine:
    #     :param last_job: 该机器上一个加工的作业
    #     :param releases_resource_time: 副资源释放时间
    #     :return:
    #     """
    #     P_t = self.Processing_time[Job][O_num][Machine]  # 某工件的加工时间
    #     last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间，其实都是0（单工序）
    #     Selected_Machine = Machine
    #     Machine_end_time = self.Machines[Selected_Machine].End_time  # 当前作业选择机器，上一作业的完工时间
    #     # 判断该机器上一个位置有没有作业
    #     if last_job >= 0:  # 该机器上一个位置有加工作业
    #         Machine_end_time_add_switch_time = Machine_end_time + self.switching_time[last_job - 1]  # 增加切换时间
    #     else:  # 没有加工作业
    #         Machine_end_time_add_switch_time = 0
    #     #############################################
    #     """
    #     在此处增加对于副资源数量的约束？？不够的情况下，将最早开始时间往后延迟
    #     """
    #     if Machine_end_time == 0:  # 机器上的第一个作业
    #         ealiest_start = 0
    #         # if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
    #         #     ealiest_start = min(releases_resource_time[used_resource])
    #         #     releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
    #         # else:
    #         #     ealiest_start = Machine_end_time_add_switch_time
    #     else:
    #         ealiest_start = max(last_O_end, Machine_end_time, Machine_end_time_add_switch_time)
    #         # found = any(element < Machine_end_time_add_switch_time for element in releases_resource_time[used_resource])
    #         # if found:
    #         #     ealiest_start = max(last_O_end, Machine_end_time_add_switch_time)
    #         #     releases_resource_time[used_resource].remove(min(releases_resource_time[used_resource]))  # 用后删除此时间
    #         # else:
    #         #     if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
    #         #         ealiest_start = min(releases_resource_time[used_resource])
    #         #         releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
    #         #     else:
    #         #         ealiest_start = Machine_end_time_add_switch_time
    #
    #     M_Ealiest = ealiest_start
    #     End_work_time = M_Ealiest + P_t  # 此工序的完工时间
    #     return M_Ealiest, Selected_Machine, P_t, O_num, last_O_end, End_work_time
    #     # 返回某工件的 1、最早开始时间 2、选择机器 3、加工所需时间 4、工序号 5、上道工序完工时间 6、此工序的完工时间

    # 加入班制班次
    def Earliest_Start_no_time_window(self, Job, O_num, Machine, last_job):
        """
        在计算最早开始时间，就考虑副资源释放以及切换时间？？？
        :param used_resource: 该作业使用的副资源
        :param Job: 当前要加工的作业
        :param O_num:
        :param Machine:
        :param last_job: 该机器上一个加工的作业
        :param releases_resource_time: 副资源释放时间
        :return:
        """
        P_t = self.Processing_time[Job][O_num][Machine]  # 某工件的加工时间
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间，其实都是0（单工序）
        Selected_Machine = Machine
        Machine_end_time = self.Machines[Selected_Machine].End_time  # 当前作业选择机器，上一作业的完工时间
        job_id = self.job_message_list[Job][0]['标识号']
        earliest_allowed, latest_allowed = self.time_windows.get(job_id, (datetime.now(), None))
        earliest_allowed = self.time_axis.datetime_to_minutes(earliest_allowed)
        # 判断该机器上一个位置有没有作业
        if last_job >= 0:  # 该机器上一个位置有加工作业
            switch_time = self.switching_time[last_job - 1]  # 上一个作业的切换时间 分钟
            # 处理切换时间跨越班次
            switch_start = self.time_axis.minutes_to_datetime(Machine_end_time)  # 转换为datetime
            switch_end, switch_gap = self.time_axis.adjust_for_shift_gap(switch_start,
                                                                         switch_time)  # 得到切换工序的结束时间以及切换时间中班次之间的空闲时间
            # Machine_end_time_add_switch_time = self.datetime_to_minutes(switch_end) + switch_gap  # 增加切换时间
            Machine_end_time_add_switch_time = self.time_axis.datetime_to_minutes(switch_end)
        else:  # 没有加工作业
            Machine_end_time_add_switch_time = 0
            # Machine_end_time_add_switch_time = Machine_end_time
        #############################################
        """
        在此处增加对于副资源数量的约束？？不够的情况下，将最早开始时间往后延迟
        """
        if Machine_end_time == 0:  # 机器上的第一个作业
            ealiest_start = 0
            # if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
            #     ealiest_start = min(releases_resource_time[used_resource])
            #     releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
            # else:
            #     ealiest_start = Machine_end_time_add_switch_time
        else:
            ealiest_start = max(last_O_end, Machine_end_time, Machine_end_time_add_switch_time)
            # Machine_end_time_add_switch_time
            # found = any(element < Machine_end_time_add_switch_time for element in releases_resource_time[used_resource])
            # if found:
            #     ealiest_start = max(last_O_end, Machine_end_time_add_switch_time)
            #     releases_resource_time[used_resource].remove(min(releases_resource_time[used_resource]))  # 用后删除此时间
            # else:
            #     if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
            #         ealiest_start = min(releases_resource_time[used_resource])
            #         releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
            #     else:
            #         ealiest_start = Machine_end_time_add_switch_time

        M_Ealiest = max(ealiest_start, earliest_allowed)
        start_datetime = self.time_axis.minutes_to_datetime(M_Ealiest)
        end_datetime, process_gap = self.time_axis.adjust_for_shift_gap(start_datetime, P_t)
        # End_work_time = self.datetime_to_minutes(end_datetime) + process_gap
        End_work_time = self.time_axis.datetime_to_minutes(end_datetime)
        # M_Ealiest = self.minutes_to_datetime(M_Ealiest)
        # last_O_end = self.minutes_to_datetime(last_O_end)
        # End_work_time = self.minutes_to_datetime(End_work_time)
        return M_Ealiest, Selected_Machine, P_t, O_num, last_O_end, End_work_time
        # 返回某工件的 1、最早开始时间 2、选择机器 3、加工所需时间 4、工序号 5、上道工序完工时间 6、此工序的完工时间

    # def Earliest_Start_for_waiting_job(self, Job, O_num, Machine, releases_resource_time, used_resource, last_job,
    #                                    releases_resource_num):
    #     """
    #     在计算最早开始时间，就考虑副资源释放以及切换时间？？？
    #     :param releases_resource_time: 副资源释放时间
    #     :param releases_resource_num: 副资源释放根数
    #     :param used_resource: 使用哪种副资源
    #     :param Job: 当前要加工的作业
    #     :param O_num:
    #     :param Machine:
    #     :param last_job: 该机器上一个加工的作业
    #     :return:
    #     """
    #     # print("releases_resource_time", releases_resource_time, Job)
    #     P_t = self.Processing_time[Job][O_num][Machine]  # 某工件的加工时间
    #     last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间，其实都是0（单工序）
    #     Selected_Machine = Machine
    #     Machine_end_time = self.Machines[Selected_Machine].End_time  # 当前作业选择机器，上一作业的完工时间
    #     # 判断该机器上一个位置有没有作业
    #     if last_job != -1:
    #         # 需要嵌套判断该班次剩余时间能否满足一次切换所需要的时间。
    #         Machine_end_time_add_switching_time = Machine_end_time + self.switching_time[last_job - 1]  # 增加切换时间
    #     else:
    #         Machine_end_time_add_switching_time = Machine_end_time
    #         # if not releases_resource_time[used_resource]:  # 为空
    #         #     Machine_end_time_add_switching_time = Machine_end_time
    #         # else:
    #         #     ealiest_start = min(releases_resource_time[used_resource])
    #         #     Machine_end_time_add_switching_time = ealiest_start
    #         #     releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
    #     if Machine_end_time == 0:  # 机器上的第一个作业
    #         if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
    #             # can_use_index = [index for index, value in enumerate(releases_resource_num[used_resource]) if value >=
    #             #                  self.job_message_list[Job][0]['根数']]  # 释放的大于需要使用的
    #             # can_use_time = [releases_resource_time[used_resource][idx] for idx in can_use_index]  # 释放的大于需要使用的 时间
    #             # if can_use_time:
    #             ealiest_start = min(releases_resource_time[used_resource])
    #             ealiest_start_idx = releases_resource_time[used_resource].index(ealiest_start)  # 最小元素索引
    #             # if releases_resource_num[used_resource][ealiest_start_idx]
    #             releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
    #             releases_resource_num[used_resource].pop(ealiest_start_idx)  # 删除此时间释放的副资源数量
    #             # else:
    #             #     ealiest_start = min(releases_resource_time[used_resource])
    #             #     ealiest_start_idx = releases_resource_time[used_resource].index(ealiest_start)  # 最小元素索引
    #             #     releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
    #             #     releases_resource_num[used_resource].pop(ealiest_start_idx)  # 删除此时间释放的副资源数量
    #         else:
    #             print("33333333333333333333333333333333333333333333333333333333333333333333333333")
    #             ealiest_start = Machine_end_time_add_switching_time
    #     else:
    #         found = any(
    #             element <= Machine_end_time_add_switching_time for element in releases_resource_time[used_resource])
    #         if found:
    #             ealiest_start = max(last_O_end, Machine_end_time_add_switching_time)
    #             # remove_element = min(releases_resource_time[used_resource])  # 需要删除的元素
    #             closest = None
    #             for num in releases_resource_time[used_resource]:
    #                 if num <= ealiest_start:
    #                     if closest is None or abs(num - ealiest_start) < abs(closest - ealiest_start):
    #                         closest = num
    #             remove_element = closest
    #             remove_element_idx = releases_resource_time[used_resource].index(remove_element)
    #             releases_resource_time[used_resource].remove(remove_element)  # 用后删除此时间
    #             releases_resource_num[used_resource].pop(remove_element_idx)  # 删除此时间释放的副资源数量
    #         else:
    #             if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
    #                 ealiest_start = min(releases_resource_time[used_resource])
    #                 ealiest_start_idx = releases_resource_time[used_resource].index(ealiest_start)  # 最小元素索引
    #                 releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
    #                 releases_resource_num[used_resource].pop(ealiest_start_idx)  # 删除此时间释放的副资源数量
    #             else:
    #                 ealiest_start = Machine_end_time_add_switching_time
    #     M_Ealiest = ealiest_start
    #     # 加判断（先假设染程的开始时间一定是在某一个班次内的）
    #     # 1.染程是否跨越班次，若跨越，则该染程的结束时间=染程开始时间+染程消耗时间+两个班次之间的空闲时间
    #     # 2.
    #     '''
    #      if 染程跨越班次(染程所用时间大于该班次的剩余时间)：
    #         End_work_time = M_Ealiest + P_t + 两个班次之间的空闲时间
    #             if
    #     else:
    #         End_work_time = M_Ealiest + P_t
    #     '''
    #     End_work_time = M_Ealiest + P_t  # 此工序的完工时间
    #     return M_Ealiest, Selected_Machine, P_t, O_num, last_O_end, End_work_time, releases_resource_time, releases_resource_num
    #     # 返回某工件的 1、最早开始时间 2、选择机器 3、加工所需时间 4、工序号 5、上道工序完工时间 6、此工序的完工时间

    def Earliest_Start_for_waiting_job(self, Job, O_num, Machine, releases_resource_time, used_resource, last_job,
                                       releases_resource_num):
        """
        在计算最早开始时间，就考虑副资源释放以及切换时间？？？
        :param releases_resource_time: 副资源释放时间
        :param releases_resource_num: 副资源释放根数
        :param used_resource: 使用哪种副资源
        :param Job: 当前要加工的作业
        :param O_num:
        :param Machine:
        :param last_job: 该机器上一个加工的作业
        :return:
        """
        # print("releases_resource_time", releases_resource_time, Job)
        P_t = self.Processing_time[Job][O_num][Machine]  # 某工件的加工时间
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间，其实都是0（单工序）
        Selected_Machine = Machine
        Machine_end_time = self.Machines[Selected_Machine].End_time  # 当前作业选择机器，上一作业的完工时间
        job_id = self.job_message_list[Job][0]['标识号']
        earliest_allowed, latest_allowed = self.time_windows.get(job_id, (datetime.now(), None))
        earliest_allowed = self.time_axis.datetime_to_minutes(earliest_allowed)
        # 判断该机器上一个位置有没有作业
        if last_job != -1:  # 如果机器上一个位置有作业。
            # 需要嵌套判断该班次剩余时间能否满足一次切换所需要的时间。
            switch_time = self.switching_time[last_job - 1]  # 上一个作业的切换时间 分钟
            # 处理切换时间跨越班次
            switch_start = self.time_axis.minutes_to_datetime(Machine_end_time)  # datetime
            switch_end, switch_gap = self.time_axis.adjust_for_shift_gap(switch_start, switch_time)
            # Machine_end_time_add_switching_time = self.datetime_to_minutes(switch_end) + switch_gap  # 增加切换时间 (错误)
            # Machine_end_time_add_switching_time = self.datetime_to_minutes(switch_start) + switch_time + switch_gap  # 增加切换时间
            Machine_end_time_add_switching_time = self.time_axis.datetime_to_minutes(switch_end)  # 增加切换时间
        else:
            Machine_end_time_add_switching_time = Machine_end_time
            # Machine_end_time_add_switching_time = 0
            # if not releases_resource_time[used_resource]:  # 为空
            #     Machine_end_time_add_switching_time = Machine_end_time
            # else:
            #     ealiest_start = min(releases_resource_time[used_resource])
            #     Machine_end_time_add_switching_time = ealiest_start
            #     releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
        if Machine_end_time == 0:  # 机器上的第一个作业
            if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
                # can_use_index = [index for index, value in enumerate(releases_resource_num[used_resource]) if value >=
                #                  self.job_message_list[Job][0]['根数']]  # 释放的大于需要使用的
                # can_use_time = [releases_resource_time[used_resource][idx] for idx in can_use_index]  # 释放的大于需要使用的 时间
                # if can_use_time:
                ealiest_start = min(releases_resource_time[used_resource])
                ealiest_start_idx = releases_resource_time[used_resource].index(ealiest_start)  # 最小元素索引
                # if releases_resource_num[used_resource][ealiest_start_idx]
                releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
                releases_resource_num[used_resource].pop(ealiest_start_idx)  # 删除此时间释放的副资源数量
                # else:
                #     ealiest_start = min(releases_resource_time[used_resource])
                #     ealiest_start_idx = releases_resource_time[used_resource].index(ealiest_start)  # 最小元素索引
                #     releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
                #     releases_resource_num[used_resource].pop(ealiest_start_idx)  # 删除此时间释放的副资源数量
            else:
                print("33333333333333333333333333333333333333333333333333333333333333333333333333")
                ealiest_start = Machine_end_time_add_switching_time
        else:
            found = any(
                element <= Machine_end_time_add_switching_time for element in releases_resource_time[used_resource])
            if found:
                ealiest_start = max(last_O_end, Machine_end_time_add_switching_time)
                # remove_element = min(releases_resource_time[used_resource])  # 需要删除的元素
                closest = None
                for num in releases_resource_time[used_resource]:
                    if num <= ealiest_start:
                        if closest is None or abs(num - ealiest_start) < abs(closest - ealiest_start):
                            closest = num
                remove_element = closest
                remove_element_idx = releases_resource_time[used_resource].index(remove_element)
                releases_resource_time[used_resource].remove(remove_element)  # 用后删除此时间
                releases_resource_num[used_resource].pop(remove_element_idx)  # 删除此时间释放的副资源数量
            else:
                if releases_resource_time[used_resource]:  # releases_resource_time[used_resource]不为空
                    ealiest_start = min(releases_resource_time[used_resource])
                    ealiest_start_idx = releases_resource_time[used_resource].index(ealiest_start)  # 最小元素索引
                    releases_resource_time[used_resource].remove(ealiest_start)  # 用后删除此时间
                    releases_resource_num[used_resource].pop(ealiest_start_idx)  # 删除此时间释放的副资源数量
                else:
                    ealiest_start = Machine_end_time_add_switching_time
        M_Ealiest = max(ealiest_start, earliest_allowed)
        # 加判断（先假设染程的开始时间一定是在某一个班次内的）
        start_datetime = self.time_axis.minutes_to_datetime(M_Ealiest)
        end_datetime, process_gap = self.time_axis.adjust_for_shift_gap(start_datetime, P_t)
        # End_work_time = self.datetime_to_minutes(end_datetime) + process_gap
        End_work_time = self.time_axis.datetime_to_minutes(end_datetime)
        # M_Ealiest = self.minutes_to_datetime(M_Ealiest)
        # last_O_end = self.minutes_to_datetime(last_O_end)
        # End_work_time = self.minutes_to_datetime(End_work_time)
        return M_Ealiest, Selected_Machine, P_t, O_num, last_O_end, End_work_time, releases_resource_time, releases_resource_num
        # 返回某工件的 1、最早开始时间 2、选择机器 3、加工所需时间 4、工序号 5、上道工序完工时间 6、此工序的完工时间

    def acknowledge_secondary_resource(self, job, machine, second_resource_type_num, srn_machine_list):
        """
        确定该作业选用的副资源，返回副资源索引
        :param srn_machine_list: [['514'], ['515'], ['905'], ['916'], ['907'], ['908'], ['815'], ['509'], ['603'], ['613'],
        :param second_resource_type_num: {'纱架': 32, '蚕丝架': 1, 'S': 9, 'M': 13, 'L': 16, 'Y': 10, 'G': 1}
        :param machine: 机器编号，从0开始
        :param machine_dict: 机器编号字典{0:401, 1:402,}
        :return:
        """
        machine_id = self.machine_id_dict[machine]  # 确定机器的真实编号如401
        # srn_type = '纱架'  # 获取副资源（架）类型
        srn_type = self.job_message_list[job][0]['轴型']  # 获取副资源（架）类型
        # print("srn_type", srn_type)
        # print(srn_type)
        # 切片
        total_length = len(srn_machine_list)  # 要切片的列表长度
        class_lengths = list(second_resource_type_num.values())  # 计算每类的长度
        start_index = 0  # 切片范围的起始索引
        sliced_classes = []  # 切片后的结果  三维列表
        for length in class_lengths:  # 对每个类进行切片
            slice_range = slice(start_index, start_index + length)  # 切片范围
            sliced_classes.append(srn_machine_list[slice_range])  # 将切片加入结果列表
            start_index += length  # 更新下一个切片的起始索引
        # print("sliced_classes", sliced_classes)
        srn_type_index = None  # 当前使用副资源类型所在索引
        for i, (key, value) in enumerate(second_resource_type_num.items()):
            # print("key", key, "srn_type", srn_type)
            if key == srn_type:
                srn_type_index = i
                break
        # print("srn_type_index", srn_type_index)
        # print("Job", job, self.job_message_list[job][0]["标识号"])
        srn_index = [index + sum(class_lengths[:srn_type_index]) for index, sublist in
                     enumerate(sliced_classes[srn_type_index]) if machine_id in sublist]  # 获取使用副资源的索引
        if not srn_index:
            print("副资源（架）类型与机器不匹配", "机器为", machine_id)
        return srn_index[0]

    def decrease_secondary_resource(self, job, secondary_resource_num, axle_resource_num, machine):
        """
        使用过程中减少副资源数量
        :param job: 作业id
        :param secondary_resource_num: 轴架纱架数量
        :param axle_resource_num: 轴的数量
        :return:
        """
        # 确定该作业使用的副资源
        secondary_resource_idx = self.acknowledge_secondary_resource(job, machine, self.srn_type_dict,
                                                                     self.machine_list)
        # 使用减少
        use_resource_num = self.job_message_list[job][0]['根数']
        use_axle_resource_num = self.job_message_list[job][0]['用轴数量']
        secondary_resource_num[secondary_resource_idx] -= use_resource_num
        # axle_resource_num[secondary_resource_idx] -= use_axle_resource_num

        return secondary_resource_num, axle_resource_num

    def increase_secondary_resource(self, job, secondary_resource_num, machine):
        # 确定该作业使用的副资源
        secondary_resource_idx = self.acknowledge_secondary_resource(job, machine, self.srn_type_dict,
                                                                     self.machine_list)
        # 使用增加
        use_resource_num = self.job_message_list[job][0]['根数']
        secondary_resource_num[secondary_resource_idx] += use_resource_num
        # secondary_resource_num[secondary_resource_idx] += 1
        return secondary_resource_num

    def Decode_1(self, CHS, Len_Chromo, Priority):  # 缺少副资源数量增加的考虑
        CHS = self.adjust_chs_for_coop(CHS, Len_Chromo)
        CHS = self.adjust_chs_for_coop1(CHS, Len_Chromo)
        CHS = self.adjust_chs_for_color(CHS, Len_Chromo)
        MS = list(CHS[0:Len_Chromo])
        # print("MS=", MS)
        OS = list(CHS[Len_Chromo:2 * Len_Chromo])
        # print(f"[DEBUG] MS长度: {len(MS)}, OS长度: {len(OS)}, CHS长度: {len(CHS)}")
        Needed_Matrix = self.Order_Matrix(MS)  # 此处有两个矩阵，时间顺序矩阵和机器顺序矩阵
        JM = Needed_Matrix[0]
        srn = copy.deepcopy(self.secondary_resource)  # 纱架轴架数量
        axle_srn = copy.deepcopy(self.axle_resource_num)  # 轴的数量
        each_job_end_time = {}  # 存放每一个作业的完工时间
        releases_resource_time = [[] for _ in range(len(srn))]  # 存放副资源的释放时间
        releases_resource_num = [[] for _ in range(len(srn))]  # 存放副资源的释放根数
        machine_requirement = 0  # 计算是否符合生产机器
        job_category = {}  # 每一个作业对应的颜色荧光类别
        for i, sublist in enumerate(self.category):  # 填充job_category
            for element in sublist:
                job_category[element] = i
        # print("###################当前染色体###############", OS)
        for idx, i in enumerate(OS):
            Job = i
            O_num = self.Jobs[Job].Current_Processed()
            Machine = JM[Job][O_num]
            # # 防止越界（比如合作组第一个订单已经调度过）
            # if O_num >= len(JM[Job]):
            #     continue
            # # print(O_num, Job)
            # Machine = JM[Job][O_num]
            # # ==== 获取副资源、上一个作业 ====
            # used_resource = self.acknowledge_secondary_resource(Job, Machine, self.srn_type_dict, self.machine_list)
            # if not self.Machines[Machine].assigned_task:
            #     last_job = -1
            # else:
            #     last_job = self.Machines[Machine].assigned_task[-1][0]
            #
            # # ==== 合作订单处理，仅由组内第一个订单调度 ====
            # if self._get_first_job_in_coop_group(Job) == Job:
            #     (current_time,
            #      releases_resource_time,
            #      releases_resource_num) = self.process_cooperative_orders(
            #         Job, Machine, self.Machines[Machine].End_time,
            #         used_resource, last_job,
            #         releases_resource_time, releases_resource_num
            #     )
            #     self.Machines[Machine].End_time = current_time
            #
            #     # 同步更新合作组内所有订单的完工时间
            #     coop_number = self.job_message_list[Job][0]['合作序号']
            #     coop_order_ids = self.coop_dict.get(coop_number, [])
            #
            #     for coop_id in coop_order_ids:
            #         for idx, job_info in enumerate(self.job_message_list):
            #             if job_info[0]['标识号'] == coop_id:
            #                 if self.Jobs[idx].J_end:  # 防止为空
            #                     each_job_end_time[idx] = self.Jobs[idx].J_end[-1]
            #     continue
            # ==================================================
            # 计算是否符合生产机器 ######################################################
            job_color = self.job_message_list[Job][0]['深浅色']  # 获取颜色
            job_machine_capacity = self.job_message_list[Job][0]['缸型']  # 获取该作业所用机器容量
            job_type = self.job_message_list[Job][0]['轴型']
            # best_machine_list = self.color_machine_dict[job_color]  # 获取该颜色最佳机器
            # print("=====", Job, self.job_message_list[Job][0]['标识号'])
            # print("job_color", job_color)
            # print("job_machine_capacity", job_machine_capacity)
            # print("job_type", job_type)
            # 选择机器成本
            # best_machine_list = self.color_machine_dict[job_machine_capacity][job_type][job_color]  # 获取该颜色最佳机器
            # if Machine not in best_machine_list:
            #     machine_requirement += 9999
            # 用切换成本来给非偏好颜色增加成本
            colors = []  # 填入选定机器的偏好颜色
            for key, value in self.color_machine_dict.items():
                for sub_key, sub_value in value.items():
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        if Machine in sub_sub_value:
                            colors.append(sub_sub_key)
            # colors = list(set(colors))
            # if len(colors) == 1:  # 有且只有一个偏好颜色（偏好颜色要么有一个，要么全是偏好颜色）
            #     color_index = self.Color_list.index(colors[0])
            #     machine_requirement += self.switching_cost[color_index][job_category[Job]]

            # 获取当前机器的偏好颜色
            machine_preference_color_list = self.machine_message[Machine]['Color']
            if machine_preference_color_list:
                machine_preference_color = machine_preference_color_list[0]
                # print(machine_preference_color)
                color_index = self.Color_list.index(machine_preference_color)
                machine_requirement += self.switching_cost[job_category[Job]][color_index]
            else:  # 没有偏好颜色的
                machine_requirement += 0

            # 判断机器上是否有作业
            if not self.Machines[Machine].assigned_task:
                last_job = -1  # 该机器上，上一个加工作业，-1为没有
            else:
                last_job = self.Machines[Machine].assigned_task[-1][0]  # 从1开始计数

            used_resource = self.acknowledge_secondary_resource(Job, Machine, self.srn_type_dict,
                                                                self.machine_list)  # 此作业使用的副资源
            # if used_resource == 14:
            #     print("订单", Job+1, self.job_message_list[Job][0]['标识号'], "机器 =", self.machine_id_dict[Machine], releases_resource_time[used_resource])
            # print("使用副资源", used_resource)
            unproduced_job = []  # 存放未生产的作业
            if srn[used_resource] >= self.job_message_list[Job][0]['根数']:  # 副资源数量够
                # print("################ 副资源数量够")
                Para = self.Earliest_Start_no_time_window(Job, O_num, Machine, last_job)
                self.Jobs[Job]._Input(Para[0], Para[5], Para[1])  # 输入 0、最早开始时间 5、此工序的完工时间 1、选择的机器 （更新信息）
                if Para[5] > self.fitness:
                    self.fitness = Para[5]
                self.Machines[Machine]._Input(Job, Para[0], Para[2], Para[3])  # 输入 工件号 0、最早开始时间 2、加工所需时间 3、工序号
                updata_resuorce_num = self.decrease_secondary_resource(Job, srn, axle_srn, Machine)  # 使用减少后副资源数量
                srn = updata_resuorce_num[0]
                axle_srn = updata_resuorce_num[1]
                # print("副资源数量(用轴减少)", axle_srn)
                # 存放每一个作业的完工时间
                each_job_end_time[Job] = Para[5]  # 索引从0开始
                # print("each_job_end_time", each_job_end_time)
                releases_resource_time[used_resource].append(Para[5] + self.switching_time[Job])
                releases_resource_num[used_resource].append(self.job_message_list[Job][0]['根数'])
                # print("releases_resource_time", releases_resource_time)
                # print("releases_resource_num", releases_resource_num)
            else:  # 副资源数量不够
                # unproduced_job.append(Job)
                # print("################ 副资源数量不够", used_resource, self.job_message_list[Job][0]['根数'], self.job_message_list[Job][0]['轴型'])
                # print("releases_resource_time", releases_resource_time)
                # print("releases_resource_num", releases_resource_num)

                Para = self.Earliest_Start_for_waiting_job(Job, O_num, Machine, releases_resource_time, used_resource,
                                                           last_job, releases_resource_num)
                self.Jobs[Job]._Input(Para[0], Para[5], Para[1])
                if Para[5] > self.fitness:
                    self.fitness = Para[5]
                self.Machines[Machine]._Input(Job, Para[0], Para[2], Para[3])
                updata_resuorce_num = self.decrease_secondary_resource(Job, srn, axle_srn, Machine)  # 使用减少后副资源数量
                srn = updata_resuorce_num[0]
                axle_srn = updata_resuorce_num[1]
                # print("副资源数量(用轴减少)", axle_srn)
                # print("副资源数量(减少)", srn)
                # 存放每一个作业的完工时间
                each_job_end_time[Job] = Para[5]  # 索引从0开始
                releases_resource_time = Para[6]
                releases_resource_num = Para[7]
                releases_resource_time[used_resource].append(Para[5] + self.switching_time[Job])
                releases_resource_num[used_resource].append(self.job_message_list[Job][0]['根数'])

            # print("=====", idx, i)
            # if used_resource == 14:
            #     if srn[used_resource] >= 0:
            #         print("副资源数量 =", srn[used_resource] + len(releases_resource_time[used_resource]), "订单 =", Job)
            #     else:
            #         print("副资源数量 =", len(releases_resource_time[used_resource]), "订单 =", Job)
            # if used_resource == 14:
            #     print("订单", Job+1, self.job_message_list[Job][0]['标识号'], "机器 =", self.machine_id_dict[Machine], releases_resource_time[used_resource])

        # 优先级部分加入目标
        # max_end_time = []
        # for k, v in Priority.items():
        #     max_end_time.append(max(self.Jobs[k - 1].J_end))
        # for i in Priority:
        #     self.sum_pri += Priority[i] * max_end_time[i - 1]
        # print("优先级+++++++", max_end_time)

        # 切换成本
        # 首先判断作业属于哪一类################################
        # job_category = {}  # 每一个作业对应的颜色荧光类别
        # for i, sublist in enumerate(self.category):  # 填充job_category
        #     for element in sublist:
        #         job_category[element] = i
        # print("job_category", job_category)
        # 计算总切换成本#######################################
        total_cost = 0
        for i in range(len(self.Machines)):
            assigned_list = [self.job_message_list[sublist[0] - 1][0]['深浅色'] for sublist in
                             self.Machines[i].assigned_task]  # 颜色列表
            occurrences = 0  # 出现不能连续生产的次数
            for tt in range(max(len(assigned_list) - len(self.non_continuous_production) + 1, 0)):
                if assigned_list[tt:tt + len(self.non_continuous_production)] == self.non_continuous_production:
                    occurrences += 1
            total_cost += occurrences * 999
            # print(f"in_list出现了 {occurrences} 次")
            # print("机器", i, "安排作业", assigned_list)
            # 与机器初始状态（颜色）之间的切换
            origin_color = self.origin_machine_color[i]  # 该机器上开始之前，原始染色状态
            if origin_color:
                origin_color_index = self.Color_list.index(origin_color)  # 颜色对应的索引
                if len(self.Machines[i].assigned_task) > 0:
                    first_job = self.Machines[i].assigned_task[0][0] - 1  # 该机器上第一个作业
                    total_cost += self.switching_cost[origin_color_index][job_category[first_job]] * 100
            else:
                continue
            for j in range(len(self.Machines[i].assigned_task) - 1):
                put_job_1 = self.Machines[i].assigned_task[j][0] - 1
                put_job_2 = self.Machines[i].assigned_task[j + 1][0] - 1
                total_cost += self.switching_cost[job_category[put_job_1]][job_category[put_job_2]]
        # 计算产能均衡 #########################################
        # total_jobs = len(self.Jobs)
        # total_machines = len(self.Machines)
        # mean_jobs = total_jobs / total_machines
        # equilibrium_capacity = 0
        # for i in range(len(self.Machines)):
        #     equilibrium_capacity += np.abs(len(self.Machines[i].assigned_task) - mean_jobs)
        # 方差
        equilibrium_capacity = 0
        job_number_on_machine = [len(self.Machines[i].assigned_task) for i in range(len(self.Machines))]
        equilibrium_capacity = np.var(job_number_on_machine)

        # 考虑到合作订单
        # job_number_on_machine = []
        # for machine in self.Machines:
        #     job_num = 0  # 该机器上的作业数量
        #     for job_order in machine.assigned_task:
        #         job = job_order[0]-1
        #         if len(self.job_message_list[job][0]['合作订单']) == 0:
        #             job_num += 1
        #         else:
        #             job_num += len(self.job_message_list[job][0]['合作订单'])
        #     job_number_on_machine.append(job_num)
        # equilibrium_capacity = np.var(job_number_on_machine)

        # 计算纱轴同批时间差
        # A_time = self.Jobs[1].J_end
        # B_time = self.Jobs[2].J_end
        # print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", A_time)
        # print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", B_time)
        # abs(A_time-B_time)
        # last_fitness = self.fitness + total_cost + 800000*equilibrium_capacity + machine_requirement + self.sum_pri
        # 交期软约束的惩罚项
        delivery_penalty = self.calculate_delivery_penalty()
        self.schedule_dict = self.get_schedule_dict(self.Machines)
        schedule_dict = self.schedule_dict
        production_dict = self.production_dict
        warp_limit_days = self.warp_limit_days
        yarn_limit_days = self.yarn_limit_days
        penalty = self.calculate_schedule_penalty(schedule_dict, production_dict, warp_limit_days, yarn_limit_days)
        last_fitness = 0 * self.fitness + total_cost + 0 * equilibrium_capacity + machine_requirement + self.sum_pri + delivery_penalty + penalty
        return last_fitness, self.fitness, total_cost, equilibrium_capacity, machine_requirement, self.sum_pri, delivery_penalty, penalty

    def Output_Result(self, Machines, iter):  # 输出所有工件信息
        All_of_O = []
        work_time = []
        for i in range(len(Machines)):
            total_time = 0  # 计算机器加工总时间
            Machine = Machines[i]
            Start_time = Machine.O_start
            End_time = Machine.O_end
            count = 1
            for i_1 in range(len(End_time)):
                # print("工件: ", Machine.assigned_task[i_1][0], "  开始时间: ", Start_time[i_1], "  结束时间: ", End_time[i_1],
                #       "  所选机器: ", i)
                # if self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'] is None:
                if len(self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单']) == 0:
                    temp = [Machine.assigned_task[i_1][0],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['生产物流号'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作序号'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['锅号'],
                            self.time_axis.minutes_to_datetime(Start_time[i_1]),
                            self.time_axis.minutes_to_datetime(End_time[i_1]), i,
                            self.machine_id_dict[i],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['续作机器'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['锁定机器'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型'],
                            self.switching_time[Machine.assigned_task[i_1][0] - 1],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['深浅色'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['色号'],
                            next((key for key, value_list in self.color_machine_dict[
                                self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型']]
                            [self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['轴型']].items() if
                                  i in value_list), None),
                            self.machine_message[i]['Color'],
                            self.machine_message[i]['PrevColor'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['荧光'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['轴型'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['优先级'], count,
                            Start_time[i_1], End_time[i_1],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作锁定顺序'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作生产物流号'],
                            self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时']]
                    count += 1
                    All_of_O.append(temp)
                else:
                    pt = 0
                    locked_order_list = self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作锁定顺序']
                    if len(locked_order_list) > 1:
                        sorted_locked_order = sorted(range(len(locked_order_list)),
                                                     key=lambda i1: locked_order_list[i1])
                        for job_index in sorted_locked_order:
                            temp = [Machine.assigned_task[i_1][0],
                                    # self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][job_index],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['生产物流号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作序号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['锅号'],
                                    Start_time[i_1] + pt,
                                    Start_time[i_1] +
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时'][
                                        job_index] + pt,
                                    i, self.machine_id_dict[i],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['续作机器'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['锁定机器'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型'],
                                    self.switching_time[Machine.assigned_task[i_1][0] - 1],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['深浅色'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['色号'],
                                    next((key for key, value_list in self.color_machine_dict[
                                        self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型']]
                                    [self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['轴型']].items() if
                                          i in value_list), None),
                                    self.machine_message[i]['Color'],
                                    self.machine_message[i]['PrevColor'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['荧光'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['轴型'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['优先级'], count,
                                    Start_time[i_1], End_time[i_1],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作锁定顺序'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作生产物流号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时']]
                            pt += self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时'][job_index] + \
                                  self.switching_time[Machine.assigned_task[i_1][0] - 1]
                            count += 1
                            All_of_O.append(temp)
                    else:
                        for job_index in range(
                                len(self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'])):
                            temp = [Machine.assigned_task[i_1][0],
                                    # self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][job_index],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['生产物流号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作序号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['锅号'],
                                    Start_time[i_1] + pt,
                                    Start_time[i_1] +
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时'][
                                        job_index] + pt,
                                    i, self.machine_id_dict[i],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['续作机器'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['锁定机器'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型'],
                                    self.switching_time[Machine.assigned_task[i_1][0] - 1],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['深浅色'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['色号'],
                                    next((key for key, value_list in self.color_machine_dict[
                                        self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型']]
                                    [self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['轴型']].items() if
                                          i in value_list), None),
                                    self.machine_message[i]['Color'],
                                    self.machine_message[i]['PrevColor'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['荧光'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['轴型'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['优先级'], count,
                                    Start_time[i_1], End_time[i_1],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作锁定顺序'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作生产物流号'],
                                    self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时']]
                            pt += self.job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时'][job_index] + \
                                  self.switching_time[Machine.assigned_task[i_1][0] - 1]
                            count += 1
                            All_of_O.append(temp)

            #     total_time += End_time[i_1] - Start_time[i_1]
            # work_time.append(total_time)
        test1 = pd.DataFrame(data=All_of_O)
        # test1.to_csv(
        #     'result\\output' + str(iter + 1) + '.csv',
        #     encoding='gbk', index=False,
        #     header=['工件', '作业标识号', '生产物流号', '合作序号', '锅号', '开始时间', '结束时间', '所选机器', '机器号', '续作机器', '锁定机器', '机器容量',
        #             '切换时间', '深浅色', '色号', '机器常染颜色1', '机器常染颜色2', '机器上一状态', '能否荧光', '轴型', '优先级', '生产顺序', '开始时间', '结束时间',
        #             '锁定顺序', '合作订单', '合作生产物流号',
        #             '合作染程用时'])
        # test2 = pd.DataFrame(data=work_time)
        # test2.to_csv(
        #     'work_time\\work_time' + str(iter + 1) + '.csv',
        #     encoding='gbk', index=False, header=['所选机器的总加工时间'])
        # print('输出第', iter + 1, '次的结果')

    def Output_Result_02(self, Jobs, iter):
        All_of_O = []
        for i in range(len(Jobs)):
            Machine = Jobs[i].J_machine
            start_time = Jobs[i].J_start
            end_time = Jobs[i].J_end
            for i_1 in range(len(Machine)):
                temp = [i + 1, self.job_message_list[i][0]['标识号'], start_time[i_1], end_time[i_1], Machine[i_1],
                        self.machine_id_dict[Machine[i_1]], self.switching_time[i],
                        self.job_message_list[i][0]['深浅色'],
                        next((key for key, value_list in
                              self.color_machine_dict[self.job_message_list[i][0]['缸型']].items() if
                              Machine[i_1] in value_list), None),
                        self.job_message_list[i][0]['轴型'], self.job_message_list[i][0]['优先级'],
                        self.job_message_list[i][0]['合作订单']]
                All_of_O.append(temp)
        test1 = pd.DataFrame(data=All_of_O)
        test1.to_csv(
            'result\\output_by_job_' + str(iter + 1) + '.csv',
            encoding='gbk', index=False, header=['工件', '标识号', '开始时间', '结束时间', '所选机器', '机器号',
                                                 '切换时间', '深浅色', '机器常染颜色', '轴型', '优先级', '合作订单'])

    # 甘特图需要修改
    def Gantt(self, Machines, iter):
        M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
             'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
             'navajowhite', 'navy', 'sandybrown', 'moccasin']
        plt.figure(figsize=(13, 6))
        for i in range(len(Machines)):
            Machine = Machines[i]
            Start_time = Machine.O_start
            End_time = Machine.O_end
            # Machine_index = Machine.  # 为加入机器索引
            # print("tttttttt", Machine.assigned_task)
            for i_1 in range(len(End_time)):
                # plt.barh(i,width=End_time[i_1]-Start_time[i_1],height=0.8,left=Start_time[i_1],\
                #          color=M[Machine.assigned_task[i_1][0]],edgecolor='black')
                # plt.text(x=Start_time[i_1]+0.1,y=i,s=Machine.assigned_task[i_1])
                plt.barh(i, width=End_time[i_1] - Start_time[i_1], height=0.8, left=Start_time[i_1], \
                         color='white', edgecolor='black')
                plt.text(x=Start_time[i_1] + 0.3, y=i - 0.3,
                         s='J =' + str(Machine.assigned_task[i_1][0]) + '  T =' + str(End_time[i_1] - Start_time[i_1]),
                         fontsize=6)  # Machine.assigned_task[i_1][0]安排的工件 y=i-0.3是数字位置
                # if i_1 != len(End_time) - 1:  # 不是最后一个作业/计划
                plt.barh(i, width=self.switching_time[Machine.assigned_task[i_1][0] - 1], height=0.8,
                         left=End_time[i_1],
                         color='navajowhite', edgecolor='red')
                plt.text(x=End_time[i_1] + self.switching_time[Machine.assigned_task[i_1][0] - 1] / 2 - 0.3, y=i - 0.3,
                         s='st =' + str(self.switching_time[Machine.assigned_task[i_1][0] - 1]), fontsize=6)
        # machine_list = [209,210,211,212,213,301,711,1006,1007]
        machine_list = ['209', '210', '211', '212', '213', '301', '711', '1006', '1007']
        plt.yticks(np.arange(12, 21, 1), machine_list)
        plt.title('Scheduling Gantt chart')
        plt.ylabel('Machines')
        plt.xlabel('Time')
        # plt.savefig('result\\Figure\\figure_' + str(iter + 1) + '.jpg', dpi=800)
        plt.show()
        plt.close()

    '''新增'''

    def minutes_to_datetime(self, minutes):
        """
        分钟数转时间对象
        minutes：int
        """
        if minutes is None or not isinstance(minutes, (int, float)):
            raise ValueError(f"[ERROR] 非法 minutes 值: {minutes}")
        return datetime.now().replace(microsecond=0) + timedelta(minutes=minutes)

    def datetime_to_minutes(self, dt):
        """
        时间对象转分钟数

        """
        # base_date = datetime(2025, 3, 10)  # 以传入工作日历的第一天的零点为基准时间
        base_date = datetime.now().replace(microsecond=0)  # 以当前时间为基准时间
        return (dt - base_date).total_seconds() // 60

    def adjust_for_shift_gap(self, start_time, duration):
        """
        核心时间调整函数：处理班次间隔和节假日
        start_time:datetime
        duration: int 分钟
        """
        current_time = self.time_axis.find_valid_time(start_time)
        # current_time = start_time
        remaining = duration
        total_gap = 0

        while remaining > 0:
            # 找到当前班次结束时间
            shift_end = self.time_axis._find_current_shift_end(current_time)
            if not shift_end:
                # print("找不到班次的结束时间")
                break

            # 计算当前班次剩余时间
            available_time = (shift_end - current_time).seconds // 60
            if available_time >= remaining:
                return current_time + timedelta(minutes=remaining), total_gap
            else:
                remaining -= available_time
                current_time = shift_end

                # 找到下一个班次开始时间
                next_shift_start = self.time_axis._find_next_shift_start(shift_end)
                if next_shift_start:
                    gap = (next_shift_start - shift_end).seconds // 60  # 分钟
                    total_gap += gap
                    current_time = next_shift_start  # + timedelta(minutes=remaining)
                else:
                    break

        return current_time, total_gap
        # 返回的值 1.切换时间或染程的结束时间，格式为datetime 2.班次之间的间隔时间,格式为 int 分钟

    # 计算交期软约束所用惩罚
    def calculate_delivery_penalty(self):
        """计算所有作业的交期延迟惩罚"""
        total_penalty = 0
        for job in self.Jobs:
            job_index = job.Job_index
            # 索引保护
            if job_index >= len(self.job_message_list):
                # print("索引错误")
                continue
            order_info = self.job_message_list[job_index][0]
            order_id = order_info['标识号']
            # for job in self.Jobs:
            # order_id = self.job_message_list[0][0]['标识号'] # job.Job_index
            # order_id = self.job_message_list[job][0]['标识号'] #
            # 获取计划结束时间（分钟转datetime）
            end_time = self.time_axis.minutes_to_datetime(job.J_end[-1]) if job.J_end else None
            # 获取交期时间
            delivery_date = self.delivery_dates.get(order_id)

            if end_time and delivery_date:
                if end_time > delivery_date:
                    # 计算延迟小时数（惩罚因子可调，这里假设每小时惩罚100，目前我先暂定这样）
                    delay_hours = (end_time - delivery_date).total_seconds() / 3600
                    total_penalty += 100 * delay_hours
        return total_penalty
        # 目前处理将计划漂染完成日期最大的日期赋值给计划漂染完成日期为空值的位置

    def Get_Delivery_Dates(self, new_job_dict):
        valid_dates = [
            datetime.strptime(job_info[0]['计划漂染完成日期'], "%Y-%m-%d %H:%M:%S")
            for job_id, job_info in new_job_dict.items()
            if job_info[0]['计划漂染完成日期'].strip()  # 过滤掉空字符串
        ]

        # 计算最晚的计划漂染完成日期
        max_date = max(valid_dates) if valid_dates else None

        # 赋值计划漂染完成日期，若为空则替换为 max_date
        delivery_dates = {}
        for job_id, job_info in new_job_dict.items():
            date_str = job_info[0].get('计划漂染完成日期', '').strip()
            if date_str:
                delivery_dates[job_info[0]['标识号']] = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                if max_date:
                    # print(f"标识号 {job_info[0].get('标识号', '未知')} 的计划漂染日期为空，已替换为 {max_date}")
                    delivery_dates[job_info[0]['标识号']] = max_date
        return delivery_dates

    def calculate_time_intervals(self, json_dict, buffer_days=3):
        """
        返回时间窗字典和错误字典
        time_windows: {订单ID: (最早开始时间 datetime, 最晚结束时间 datetime)}
        order_errors: 结构：{订单ID: {'error': str, 'warning': str}}
        """
        time_windows = {}
        order_errors = defaultdict(dict)

        for i in json_dict["Order"]:
            orders = json_dict["Order"][i]
            routings = json_dict["Routing"].get(i, {})

            for order in orders:
                order_id = order['OrderId']
                routing_key = order['Routing']
                dye_delivery_str = order.get('DyeDeliveryDate', '')
                now_time = datetime.now()
                opencard = order['OpenCardMark']
                error_info = {'error': None}

                # 尝试解析计划交期
                try:
                    dye_delivery = datetime.strptime(dye_delivery_str, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    dye_delivery = None
                    error_info['error'] = f"交期时间格式错误"

                # 默认的 earliest_start 和 latest_end
                earliest_start, _ = self.time_axis.adjust_for_shift_gap(now_time, 0)
                latest_end = dye_delivery - timedelta(days=buffer_days) if dye_delivery else None

                # 检查工艺路线是否存在
                if not routing_key or routing_key not in routings:
                    error_info['error'] = error_info['error'] or f"工艺路线'{routing_key}'不存在"
                    if latest_end:
                        time_windows[order_id] = (earliest_start, latest_end)
                    order_errors[order_id] = error_info
                    continue

                processes = routings[routing_key]
                sorted_processes = sorted(processes, key=lambda x: int(x['OperationNum']))

                # 查找染色工序
                dye_index = None
                for idx, process in enumerate(sorted_processes):
                    if '染色' in process['WorkCenter']:
                        dye_index = idx
                        break

                if dye_index is None:
                    error_info['error'] = error_info['error'] or "未找到染色工序"
                    if latest_end:
                        time_windows[order_id] = (earliest_start, latest_end)
                    order_errors[order_id] = error_info
                    continue

                # 正常计算上下游时间
                upstream = sorted_processes[:dye_index]
                downstream = sorted_processes[dye_index + 1:]

                try:
                    upstream_total = sum(
                        (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
                        for p in upstream
                    )
                    downstream_total = sum(
                        (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
                        for p in downstream
                    )
                except Exception as e:
                    error_info['error'] = "工序时间数据缺失或格式错误"
                    if latest_end:
                        time_windows[order_id] = (earliest_start, latest_end)
                    order_errors[order_id] = error_info
                    continue

                # 重新计算 earliest_start
                if opencard:
                    if upstream_total > 0:
                        # earliest_start = now_time
                        earliest_start, _ = self.time_axis.adjust_for_shift_gap(now_time, 0)
                else:
                    if upstream_total > 0:
                        earliest_start, _ = self.time_axis.adjust_for_shift_gap(now_time, upstream_total)

                # if upstream_total > 0:
                #     earliest_start, _ = self.time_axis.adjust_for_shift_gap(now_time, upstream_total)

                # 重新计算 latest_end
                if dye_delivery:
                    latest_end = dye_delivery - timedelta(days=buffer_days)

                time_windows[order_id] = (earliest_start, latest_end)

                if latest_end and latest_end < earliest_start:
                    error_info['error'] = "染色工序时间冲突"
                    order_errors[order_id] = error_info

        return time_windows, order_errors

    def calculate_schedule_penalty(self, schedule_dict, production_dict, warp_limit_days, yarn_limit_days):
        """
        计算因同一生产物流号下的订单排产时间跨度过大而产生的惩罚项。

        参数：
            schedule_dict: dict，格式为 {OrderId: datetime 对象（排产开始时间）}
            coop_dict: dict，格式为 {ProductionNumber: {'WarpCompletion': [...], 'YarnAxleCompletion': [...]}}
            warp_limit_days: int，经向完成的最大允许时间跨度（天）
            yarn_limit_days: int，纱轴完成的最大允许时间跨度（天）

        返回：
            总惩罚值（int）
        """
        total_penalty = 0

        for prod_num, routing_groups in production_dict.items():

            # 计算 WarpCompletion 惩罚（TZZJH、RSZJH）
            warp_orders = routing_groups.get("WarpCompletion", [])
            warp_times = [schedule_dict[oid] for oid in warp_orders if oid in schedule_dict]
            if len(warp_times) > 1:
                min_time = min(warp_times)
                max_time = max(warp_times)
                delta_days = (max_time - min_time).days
                if delta_days > warp_limit_days:
                    penalty = 100 * (delta_days - warp_limit_days)
                    total_penalty += penalty

            # 计算 YarnAxleCompletion 惩罚（RSJH + Warp）
            yarn_orders = routing_groups.get("YarnAxleCompletion", [])
            yarn_times = [schedule_dict[oid] for oid in yarn_orders if oid in schedule_dict]
            if len(yarn_times) > 1:
                min_time = min(yarn_times)
                max_time = max(yarn_times)
                delta_days = (max_time - min_time).days
                if delta_days > yarn_limit_days:
                    penalty = 100 * (delta_days - yarn_limit_days)
                    total_penalty += penalty

        return total_penalty

    def get_production_dict(self, json_dict):
        """
        获取以生产物流号（ProductionNumber）为键的字典，包含经向同批、纱轴同批的订单 ID 分组。

        返回结构：
        {
            '202404270220': {
                'WarpCompletion': ["OrderId1", "OrderId2"],
                'YarnAxleCompletion': ["OrderId3", "OrderId4"]
            },
            ...
        }
        """
        coop_dict = defaultdict(lambda: {'WarpCompletion': [], 'YarnAxleCompletion': []})

        for order_group in json_dict.get("Order", {}).values():
            for order in order_group:
                prod_num = order.get("ProductionNumber")
                order_id = order.get("OrderId")
                routing = order.get("Routing")

                if prod_num and order_id and routing:
                    if routing in ["TZZJH", "RSZJH"]:
                        coop_dict[prod_num]['WarpCompletion'].append(order_id)
                    if routing in ["TZZJH", "RSZJH", "RSJH"]:
                        coop_dict[prod_num]['YarnAxleCompletion'].append(order_id)

        # 仅保留 WarpCompletion 或 YarnAxleCompletion 含有多个订单的项
        production_dict = {
            k: v for k, v in coop_dict.items()
            if len(v['WarpCompletion']) > 1 or len(v['YarnAxleCompletion']) > 1
        }

        return production_dict

    def get_completion_days(self, json_dict):
        # 读取字符串字段
        warp_str = json_dict["Rule"].get("WarpCompletionDays", "")
        yarn_axle_str = json_dict["Rule"].get("YarnAxleCompletionDays", "")

        # 使用正则提取数字
        warp_days = int(re.search(r'\d+', warp_str).group()) if re.search(r'\d+', warp_str) else None
        yarn_axle_days = int(re.search(r'\d+', yarn_axle_str).group()) if re.search(r'\d+', yarn_axle_str) else None

        return warp_days, yarn_axle_days

    def get_schedule_dict(self, Machines):
        """
        返回字典 {作业标识号: datetime}，用于记录每个作业（包括合作订单）的开始时间。
        """
        # print(f"[DEBUG] 共 {len(Machines)} 台机器") # 调试
        schedule_dict = {}
        for i in range(len(Machines)):
            Machine = Machines[i]
            # print(f"[DEBUG] 机器 {i} 上有 {len(Machine.O_start)} 个开始时间记录 和 {len(Machine.assigned_task)} 个任务")
            Start_time = Machine.O_start
            End_time = Machine.O_end

            for i_1 in range(len(End_time)):
                job_index = Machine.assigned_task[i_1][0] - 1
                # print(f"[DEBUG] 当前任务对应的 job_index = {job_index}")
                job_info = self.job_message_list[job_index][0]
                # print(f"[DEBUG] job_info 标识号 = {job_info['标识号']}")

                # 情况1：非合作订单，直接赋值
                if len(job_info['合作订单']) == 0:
                    orderid = job_info['标识号']
                    schedule_dict[orderid] = self.time_axis.minutes_to_datetime(Start_time[i_1])
                else:
                    # 情况2：合作订单，根据合作锁定顺序排序
                    pt = 0
                    coop_list = job_info['合作订单']
                    coop_time_list = job_info['合作染程用时']
                    locked_order_list = job_info['合作锁定顺序']

                    # 如果有锁定顺序，先根据其排序
                    if len(locked_order_list) > 1:
                        sorted_idx = sorted(range(len(locked_order_list)), key=lambda i: locked_order_list[i])
                    else:
                        sorted_idx = range(len(coop_list))

                    for sub_idx in sorted_idx:
                        orderid = coop_list[sub_idx]  # 正确：合作订单的“标识号”
                        start_time = Start_time[i_1] + pt
                        schedule_dict[orderid] = self.time_axis.minutes_to_datetime(start_time)
                        pt += coop_time_list[sub_idx] + self.switching_time[job_index]  # 加上加工时间和切换时间
        # print(schedule_dict)
        return schedule_dict

    # def get_schedule_dict(self, Machines):
    #     """
    #     返回字典 {作业标识号: datetime}，用于记录每个作业（包括合作订单）的开始时间。
    #     """
    #     schedule_dict = {}
    #     for i in range(len(Machines)):
    #         Machine = Machines[i]
    #         Start_time = Machine.O_start
    #         End_time = Machine.O_end
    #
    #         for i_1 in range(len(End_time)):
    #             job_index = Machine.assigned_task[i_1][0] - 1
    #             job_info = self.job_message_list[job_index][0]
    #
    #             # 情况1：非合作订单，直接赋值
    #             if len(job_info['合作订单']) == 0:
    #                 orderid = job_info['标识号']
    #                 schedule_dict[orderid] = self.minutes_to_datetime(Start_time[i_1])
    #             else:
    #                 # 情况2：合作订单，按合作锁定顺序和合作染程用时拆分多个作业
    #                 pt = 0
    #                 coop_list = job_info['合作订单']
    #                 coop_time_list = job_info['合作染程用时']
    #                 for sub_idx in range(len(coop_list)):
    #                     orderid = coop_time_list[sub_idx]  # 此处合作订单本身就是“标识号”
    #                     start_time = Start_time[i_1] + pt
    #                     schedule_dict[orderid] = self.minutes_to_datetime(start_time)
    #                     pt += coop_time_list[sub_idx] + self.switching_time[job_index]  # 每段加工时间 + 切换时间
    #     # print(schedule_dict)
    #     return schedule_dict

    # 得到同一合作序号下的订单，同一合作序号下的订单需要安排在同一机台连续生产。
    # def get_coop_dict(self, json_dict):
    #     """
    #     生成合作号字典，保留包含多个订单的条目
    #     dict: 结构为 {合作号: [订单ID1, 订单ID2,...]} 的字典
    #     """
    #     # 初始化默认字典自动创建列表
    #     coop_dict = defaultdict(list)
    #     # 遍历所有工厂
    #     for order_group in json_dict["Order"].values():
    #         # 遍历工厂内的每个订单
    #         for order in order_group:
    #             # 提取合作号和订单ID
    #             coop_number = order.get("CooperativeNumber")
    #             order_id = order.get("OrderId")
    #
    #             # 当两个字段都存在时记录
    #             if coop_number and order_id:
    #                 coop_dict[coop_number].append(order_id)
    #     # 过滤只保留有多个订单的条目
    #     return {k: v for k, v in coop_dict.items() if len(v) > 1}

    def get_coop_dict(self, json_dict):
        """
        生成合作号字典，保留包含多个订单的条目
        dict: 结构为 {合作号: [订单ID1, 订单ID2,...]} 的字典
        新增条件：仅包含未被锁定的订单（LockedState为"0"）
        """
        coop_dict = defaultdict(list)

        for order_group in json_dict["Order"].values():
            for order in order_group:
                # 提取必要字段
                coop_number = order.get("CooperativeNumber")
                order_id = order.get("OrderId")
                locked_state = order.get("LockedState")

                # 新增锁定状态检查
                if all([
                    coop_number,
                    order_id,
                    locked_state == "0"  # 仅接受未锁定订单
                ]):
                    coop_dict[coop_number].append(order_id)

        # 过滤仅保留多个订单的条目
        coop_dict = {k: v for k, v in coop_dict.items() if len(v) > 1}
        return coop_dict

    # 处理合作序号订单的连续生产逻辑
    def process_cooperative_orders(self, job_id, machine, current_time, used_resource, last_job, releases_resource_time,
                                   releases_resource_num):
        """处理合作序号订单的连续生产逻辑"""
        skipped_jobs = []
        # 获取当前订单的合作号
        coop_number = self.job_message_list[job_id][0]['合作序号']

        # 如果没有合作号或单独生产，直接返回原数据
        if not coop_number or coop_number not in self.coop_dict:
            return current_time, releases_resource_time, releases_resource_num

        # 获取同合作号的所有订单索引（从0开始）
        coop_order_ids = self.coop_dict[coop_number]
        coop_jobs = [
            idx for idx, job in enumerate(self.job_message_list)
            if job[0]['标识号'] in coop_order_ids
        ]

        # 如果当前job不是合作组第一个，跳过（由第一个job处理整个组）
        if job_id != coop_jobs[0]:
            return current_time, releases_resource_time, releases_resource_num

        processed_jobs = []
        for coop_job in coop_jobs:
            # 检查工件索引是否有效
            if coop_job >= len(self.Processing_time):
                # print(f"无效的工件索引 {coop_job}")
                continue
            # 获取当前工序号
            O_num = self.Jobs[coop_job].Current_Processed()
            # 检查工序号是否有效
            if O_num >= len(self.Processing_time[coop_job]):
                # print(f"工件 {coop_job} 的工序号 {O_num} 越界")
                continue
            # 检查机器是否有效
            Machine = machine
            if Machine >= len(self.Processing_time[coop_job][O_num]):
                # print(f"机器索引 {Machine} 越界")
                continue

            if self.Processing_time[coop_job][O_num][Machine] == 9999:
                print(f"[跳过] 工件 {coop_job}（合作组）不可在机器 {Machine} 上加工")
                skipped_jobs.append(coop_job)
                continue
            # ========== 结束检查 ======================================

            # 计算连续生产的开始时间
            if not processed_jobs:  # 第一个订单
                start_time = current_time
            else:  # 后续订单紧接着前一个结束
                start_time = processed_jobs[-1]["end_time"] + self.switching_time[processed_jobs[-1]["job"]]

            # 计算生产时间（考虑班次间隔）
            start_datetime = self.time_axis.minutes_to_datetime(start_time)
            end_datetime, _ = self.time_axis.adjust_for_shift_gap(start_datetime,
                                                                  self.Processing_time[coop_job][O_num][Machine])
            end_time = self.time_axis.datetime_to_minutes(end_datetime)

            # 更新作业和机器状态
            self.Jobs[coop_job]._Input(start_time, end_time, Machine)
            self.Machines[Machine]._Input(coop_job, start_time,
                                          self.Processing_time[coop_job][O_num][Machine],
                                          O_num)

            # 更新副资源
            releases_resource_time[used_resource].append(end_time + self.switching_time[coop_job])
            releases_resource_num[used_resource].append(
                self.job_message_list[coop_job][0]['根数']
            )

            processed_jobs.append({
                "job": coop_job,
                "end_time": end_time
            })

        # 返回最后一个订单的结束时间作为当前时间
        return processed_jobs[-1]["end_time"], releases_resource_time, releases_resource_num

    def _get_first_job_in_coop_group(self, job_id):
        """获取合作组中的第一个job索引"""
        coop_number = self.job_message_list[job_id][0]['合作序号']
        if not coop_number or coop_number not in self.coop_dict:
            return None

        # 找到组内第一个job的索引
        for idx, job_info in enumerate(self.job_message_list):
            if job_info[0]['合作序号'] == coop_number:
                return idx
        return None

    def adjust_chs_for_coop(self, CHS, Len_Chromo):
        """
        调整染色体，使合作订单在 OS 中连续，且 MS 中使用同一机器
        如果订单池中，合作标识相同，且染机容量相同，开卡标记true，发纱标记true。 同一合作标识的订单放在同一个染机连续生产。
        需要按照锅号大小排序，先小后大
        先处理锁定再处理非锁定
        """
        MS = list(CHS[:Len_Chromo])
        # print(MS)
        OS = list(CHS[Len_Chromo:])
        # 构建合作组字典
        coop_groups = defaultdict(list)
        locked_groups = defaultdict(list)
        pot_numbers = {}  # 存储锅号用于排序
        # lockjoborders = {} # 存储锁定生产顺序

        # 需要建立合作标识相同，且染机容量相同，开卡标记true，发纱标记true，并且锁定状态为0的订单列表。
        for idx, job_info in enumerate(self.job_message_list):
            coop_num = job_info[0].get("合作序号", "")
            locked_state = job_info[0].get("锁定状态", "")
            machine_capacity = job_info[0].get("缸型", "")
            opencard = job_info[0].get("开卡标记", "") == "true"
            hairyarn = job_info[0].get("发纱标记", "") == "true"
            pot_number = int(job_info[0].get("锅号", 0))  # 获取锅号并转换为整数
            # 锁定生产顺序
            # lockorder = job_info[0].get("锁定顺序", "")

            # locked_groups[idx] = locked_state
            locked_groups[idx].append(locked_state)
            pot_numbers[idx] = pot_number

            # 满足四个条件的订单才分组
            if coop_num and opencard and hairyarn:
                group_key = (coop_num, machine_capacity)
                coop_groups[group_key].append(idx)
        # print(coop_groups)
        # print(locked_groups)
        # 重新排序 OS 并统一 MS 的机器选择
        reordered_OS = []
        remaining = [(job_id, i) for i, job_id in enumerate(OS)]
        # print(remaining)

        # 开始处理每一个合作组
        for group_key, job_ids in coop_groups.items():
            # 提取当前合作组在 remaining 中的条目
            group_entries = [entry for entry in remaining if entry[0] in job_ids]
            if not group_entries:
                continue

            # 按锅号排序（从小到大）
            group_entries.sort(key=lambda entry: pot_numbers[entry[0]])

            # 提取组内所有工序的机器选择，并验证可用性
            valid_machines = []
            # 读取同一合作序号下面
            for machine in set(MS[pos] for pos in [j for j, idx in group_entries]):
                valid_machines.append(machine)
            if not valid_machines:
                continue
            # 在更新机器时存在问题。因为同一个合作序号下的订单容量不同，并且可能存在一个锁定另一个没锁定的情况
            # 调整机器只要调整没有锁定状态的机器就可以
            most_common_machine = Counter(valid_machines).most_common(1)[0][0]  # 出现最多

            # 更新 MS 并保留原顺序(只对非锁定订单的机器进行调整)
            for job, pos in group_entries:
                if locked_groups[job] == '0':
                    MS[job] = most_common_machine
                # else:
                #     MS[job]

            # 将合作组订单连续排列
            reordered_OS.extend([job for job, _ in group_entries])
            remaining = [entry for entry in remaining if entry not in group_entries]

        reordered_OS.extend([job for job, _ in remaining])
        return np.array(MS + reordered_OS)

    # 对订单依据是否锁定分开进行处理。未锁定订单直接依据锅号进行排序，锁定订单先判断锁定生产顺序情况，之后根据锁定生产顺序情况对生产顺序进行调整。
    def adjust_chs_for_coop1(self, CHS, Len_Chromo):
        """
        调整染色体，使合作订单在 OS 中连续，且 MS 中使用同一机器
        如果订单池中，合作标识相同，且染机容量相同，开卡标记true，发纱标记true。
        同一合作标识的订单放在同一个染机连续生产。
        非锁定订单：按锅号从小到大排序
        锁定订单：锁定顺序为0时按锅号排序，不为0时按锁定顺序排序
        """
        MS = list(CHS[:Len_Chromo])
        OS = list(CHS[Len_Chromo:])

        # 构建数据结构
        coop_groups = defaultdict(list)  # 合作组字典
        locked_states = {}  # 锁定状态字典
        pot_numbers = {}  # 锅号字典
        lock_orders = {}  # 锁定顺序字典

        # 收集订单信息
        for idx, job_info in enumerate(self.job_message_list):
            job_data = job_info[0]
            coop_num = job_data.get("合作序号", "")
            locked_state = job_data.get("锁定状态", "0")
            machine_capacity = job_data.get("缸型", "")
            opencard = job_info[0].get("开卡标记", "") == "true"
            hairyarn = job_info[0].get("发纱标记", "") == "true"
            pot_number = int(job_data.get("锅号", 0))
            lock_order = job_data.get("锁定顺序", "0")

            # 存储订单属性
            locked_states[idx] = locked_state
            pot_numbers[idx] = pot_number
            lock_orders[idx] = lock_order

            # 满足四个条件的订单才分组
            if coop_num and opencard and hairyarn:
                group_key = (coop_num, machine_capacity)
                coop_groups[group_key].append(idx)

        # 重新排序 OS 并统一 MS 的机器选择
        reordered_OS = []
        remaining = [(job_id, i) for i, job_id in enumerate(OS)]

        # 处理每个合作组
        for group_key, job_ids in coop_groups.items():
            # 提取当前合作组在 remaining 中的条目
            group_entries = [entry for entry in remaining if entry[0] in job_ids]
            if not group_entries:
                continue

            # 将组内订单分为锁定和非锁定两部分
            locked_entries = []  # 锁定订单
            unlocked_entries = []  # 非锁定订单

            for entry in group_entries:
                job_id = entry[0]
                if locked_states[job_id] == "1":  # 锁定订单
                    locked_entries.append(entry)
                else:  # 非锁定订单
                    unlocked_entries.append(entry)

            # 对锁定订单进行排序（按锁定顺序或锅号）
            if locked_entries:
                # 分离锁定顺序为0和非0的订单
                lock_order_zero = []  # 锁定顺序为0的订单
                lock_order_nonzero = []  # 锁定顺序非0的订单

                for entry in locked_entries:
                    job_id = entry[0]
                    if lock_orders[job_id] == "0":
                        lock_order_zero.append(entry)
                    else:
                        lock_order_nonzero.append(entry)

                # 锁定顺序非0的订单按锁定顺序排序
                lock_order_nonzero.sort(key=lambda entry: int(lock_orders[entry[0]]))

                # 锁定顺序为0的订单按锅号排序
                lock_order_zero.sort(key=lambda entry: pot_numbers[entry[0]])

                # 合并锁定订单：先排锁定顺序非0的，再排锁定顺序为0的
                sorted_locked = lock_order_nonzero + lock_order_zero
            else:
                sorted_locked = []

            # 对非锁定订单按锅号排序
            unlocked_entries.sort(key=lambda entry: pot_numbers[entry[0]])

            # 合并排序后的订单：先排锁定订单，再排非锁定订单
            sorted_group_entries = sorted_locked + unlocked_entries

            # 确定组内最常用的机器
            valid_machines = [MS[job_id] for job_id, _ in sorted_group_entries]
            if not valid_machines:
                continue

            most_common_machine = Counter(valid_machines).most_common(1)[0][0]

            # 更新未锁定订单的机器选择
            for job_id, _ in sorted_group_entries:
                if locked_states[job_id] == "0":  # 仅调整未锁定订单
                    MS[job_id] = most_common_machine

            # 将排序后的订单加入新OS
            reordered_OS.extend([job_id for job_id, _ in sorted_group_entries])
            remaining = [entry for entry in remaining if entry not in group_entries]

        # 添加未分组的订单（保持原顺序）
        reordered_OS.extend([job_id for job_id, _ in remaining])

        return np.array(MS + reordered_OS)

    def adjust_chs_for_color(self, CHS, Len_Chromo):
        """
        调整 OS，使每个 ProductionNumber 下色纱（非增白）订单排在增白订单之前
        """
        MS = list(CHS[:Len_Chromo])
        OS = list(CHS[Len_Chromo:])

        # 构建生产物流号分组（过滤空值）
        prod_groups = defaultdict(list)
        for idx, job_info in enumerate(self.job_message_list):
            prod_num = job_info[0].get("ProductionNumber", "").strip()
            if prod_num:
                prod_groups[prod_num].append(idx)

        # 重构 OS 排序逻辑
        reordered_OS = []
        remaining = [(job_id, idx) for idx, job_id in enumerate(OS)]

        for prod_num, jobs in prod_groups.items():
            group_entries = [entry for entry in remaining if entry[0] in jobs]
            if not group_entries:
                continue

            # 分离色纱（非增白）和增白订单
            color_entries = []
            white_entries = []
            for job, idx in group_entries:
                color = self.job_message_list[job][0].get("深浅色", "")
                if color != "增白":
                    color_entries.append((job, idx))
                else:
                    white_entries.append((job, idx))

            # 保持原序，仅调整色纱在前
            reordered_OS.extend([job for job, _ in sorted(color_entries, key=lambda x: x[1])])
            reordered_OS.extend([job for job, _ in sorted(white_entries, key=lambda x: x[1])])

            # 移除已处理项
            remaining = [entry for entry in remaining if entry not in group_entries]

        reordered_OS.extend([job for job, _ in remaining])
        return np.array(MS + reordered_OS)
