import copy
import os

import numpy as np
import random
from Machine_Distribution_lastest._Decode_New import Decode
from Machine_Distribution_lastest._Encode import Encode
import matplotlib.pyplot as plt
import matplotlib
import time
import json
from datetime import datetime, timedelta

from Machine_Distribution_lastest._Time_Axis_Manager import TimeAxisManager
from Machine_Distribution_lastest.pa_main import manage_data
import Machine_Distribution_lastest.input_fun as input_fun
from tqdm import trange


# from Parameters_and_Input import create_para_and_input
matplotlib.use('TkAgg')


class GA:
    def __init__(self, populationSize, crossoverRate, mutationRate, n_elite, iterationNumber, jsonDict):
        # args = create_para_and_input()
        # self.Pop_size = args.pop_size  # 种群数量
        # self.Pop_size = 250  # 种群数量
        self.Pop_size = populationSize  # 种群数量
        self.P_c = crossoverRate  # 交叉概率
        self.P_m = mutationRate  # 变异概率
        self.Max_Itertions = 3  # 最大迭代次数
        self.N_elite = int(n_elite * populationSize) # 选择精英的个数
        self.choose_num = iterationNumber  # 轮盘赌选择的个数
        # self.color_list = ['浅浅', '浅色', '深色', '中色', '增白']
        # self.color_list = Color_list
        # self.job_message = list(new_job_dict.values())
        # self.color_machine_dict = {'深色': [12, 17, 20], '中色': [13, 18], '浅色': [14, 19], '浅浅': [15], '增白': [16]}
        # self.color_machine_dict = {'180': {'深色': [59, 60, 62], '中色': [56, 61], '浅色': [57], '浅浅': [58, 64], '增白': [63, 65]},
        #  '40': {'深色': [23, 27], '中色': [24, 28], '浅色': [20, 25], '浅浅': [21, 26], '增白': [22]}}
        # self.color_machine_dict = color_machine_dict
        # self.Machine_dict = Machine_dict
        # self.switching_time = switching_time
        self.neighbour_size = 20
        self.json_dict = jsonDict
        self.parameter_list = manage_data(self.json_dict)
        self.J_num = self.parameter_list[0]
        self.jobIndex_to_orderID_dict = self.parameter_list[1]
        self.J = self.parameter_list[2]
        self.O_num = self.parameter_list[3]
        self.M_num = self.parameter_list[4]
        self.Priority = self.parameter_list[5]
        self.Processing_time = self.parameter_list[6]
        self.secondary_resource = self.parameter_list[7]
        self.Old_Job_dict = self.parameter_list[8]
        self.new_job_dict = self.parameter_list[9]
        self.switching_time = self.parameter_list[10]
        self.switching_cost = self.parameter_list[11]
        self.color_list = self.parameter_list[12]
        self.category = self.parameter_list[13]
        self.axle_resource_num = self.parameter_list[14]
        self.color_machine_dict = self.parameter_list[15]
        self.machine_list = self.parameter_list[16]
        self.srn_type_dict = self.parameter_list[17]
        self.Machine_dict = self.parameter_list[18]
        self.Locked_job = self.parameter_list[19]
        self.continue_job = self.parameter_list[20]
        self.job_message = list(self.new_job_dict.values())
        self.start_time = self.parameter_list[21]
        self.locked_job_order = self.parameter_list[22]
        self.machine_message = self.parameter_list[23]
        self.locked_job = self.parameter_list[24]
        self.stop_machine = self.parameter_list[25]
        self.machine_pre_color = self.parameter_list[26]
        self.machine_class_dict = self.parameter_list[27]
        self.machine_class_dict_white = self.parameter_list[28]
        self.average_quantity = self.parameter_list[29]

        self.time_axis_manager = TimeAxisManager(jsonDict)  # 正确实例化时间轴管理器
        self.timeline = self.time_axis_manager.timeline  # 获取生成的时间轴数据
        # print("lllllllllllllllllllll", self.job_message[108])
        # print("self.machine_message", self.machine_message)

    def fitness(self, CHS, Len):  # 算CHS中每一个方案的适应度
        Fit = []
        for i in range(len(CHS)):
            d = Decode(self.J, self.Processing_time, self.M_num, self.Priority, self.secondary_resource,
                       self.switching_time, self.category, self.switching_cost,
                       self.new_job_dict, self.axle_resource_num, self.color_machine_dict, self.machine_list,
                       self.srn_type_dict, self.Machine_dict, self.start_time, self.machine_message,
                       self.machine_pre_color, self.json_dict, self.Old_Job_dict)
            Fit.append(d.Decode_1(CHS[i], Len, self.Priority)[0])  # 返回一个适应度（最大完工时间）
        return Fit

    def two_point_crossover_ms(self, CHS1, CHS2, T0):
        """
        机器片段交叉
        :param CHS1: 染色体1
        :param CHS2: 染色体2
        :param T0: 总操作数
        :return: 两条新染色体
        """
        os1 = CHS1[T0:2 * T0]
        os2 = CHS2[T0:2 * T0]
        ms1 = list(CHS1[0:T0])
        ms2 = list(CHS2[0:T0])
        pos1 = random.randint(0, len(ms1) - 1)  # 随机选取两个交叉位置
        pos2 = random.randint(0, len(ms1) - 1)
        if pos1 > pos2:
            pos2, pos1 = pos1, pos2
        # print('位置', pos1, pos2)
        offspring1 = ms1[:]
        # print("len(offspring1)", len(offspring1))
        if pos1 != pos2:  # 两个位置不相等，进行交叉
            offspring1 = ms1[:pos1] + ms2[pos1:pos2] + ms1[pos2:]
        # print("len(offspring1)", len(offspring1))
        offspring2 = ms2[:]
        if pos1 != pos2:
            offspring2 = ms2[:pos1] + ms1[pos1:pos2] + ms2[pos2:]
        new_CHS1 = np.hstack((offspring1, os1))  # 若两个交叉位置相同则不进行交叉
        new_CHS2 = np.hstack((offspring2, os2))
        return new_CHS1, new_CHS2

    def pox_crossover_os(self, CHS1, CHS2, T0):
        """
        pox交叉
        :param CHS1: 染色体1
        :param CHS2: 染色体2
        :param T0: 总操作数
        :param J_num: 作业数
        :return: 两条新染色体
        """
        OS_1 = CHS1[T0:2 * T0]
        OS_2 = CHS2[T0:2 * T0]
        MS_1 = CHS1[0:T0]
        MS_2 = CHS2[0:T0]
        Job_list = [i for i in range(self.J_num)]  # J_num:工件数，Job_list工件索引
        random.shuffle(Job_list)  # 随机打乱
        r = random.randint(1, self.J_num - 1)  # 在区间[1,J_num - 1]内产生一个整数r
        Set1 = Job_list[0:r]  # Job_list分为两段
        new_os1 = [-1 for i in range(T0)]
        new_os2 = [-1 for i in range(T0)]
        for k, v in enumerate(OS_1):
            if v in Set1:  # os1中Set1内的作业位置保持不变，放入新的os1
                new_os1[k] = v
        for i in OS_2:  # os2中不在Set1内的作业放入新os1，顺序不变
            if i not in Set1:
                Site = new_os1.index(-1)
                new_os1[Site] = i
        for k, v in enumerate(OS_2):
            if v in Set1:  # os2中Set1内的作业位置保持不变，放入新的os2
                new_os2[k] = v
        for i in OS_1:
            if i not in Set1:  # os1中不在Set1内的作业放入新os2，顺序不变
                Site = new_os2.index(-1)
                new_os2[Site] = i
        new_CHS1 = np.hstack((MS_1, new_os1))
        new_CHS2 = np.hstack((MS_2, new_os2))
        return new_CHS1, new_CHS2

    def reduction(self, num, T0):
        """
        根据ms部分的索引，找到是哪一个作业，哪一个工序
        :param num: 机器部分索引
        :param J: 作业字典
        :param T0: 总操作数
        :return: [作业编号，工序编号]，均从0开始计数
        """
        Job = 0
        O_num = 0
        T0 = [j for j in range(T0)]  # [0, 1, 2,……, T0-1]
        K = []  # 存放每一个作业的索引列表（二维）
        Site = 0
        for k, v in self.J.items():
            K.append(T0[Site:Site + v])  # K二维数组，J_num个小数组构成，小数组内有 工序 个数
            Site += v
        for i in range(len(K)):  # len(K) = J_num
            if num in K[i]:  # 作业编号在K中某一个小列表内
                Job = i  # 获得作业编号，从0开始
                O_num = K[i].index(num)  # 工序编号，从0开始
                break
        return Job, O_num  # 两个数，指K中能够找到num的索引

    def change_mutation_ms(self, CHS, T0):
        """
        替换机器变异
        :param CHS: 染色体
        :param O: 时间矩阵
        :param T0: 总操作数
        :param J: 作业字典
        :return: 新染色体
        """
        Tr = [i_num for i_num in range(T0)]  # [0, 1, 2,……, T0-1]
        MS = CHS[0:T0]  # 机器部分编码
        OS = CHS[T0:2 * T0]  # 工序部分
        # 机器选择部分
        r = random.randint(1, T0 - 1)  # 在变异染色体中选择r个位置
        random.shuffle(Tr)  # 随机打乱Tr
        T_r = Tr[0:r]  # 取Tr部分（0 ~ r-1）
        for i in T_r:  # 选取Tr个点进行变异
            Job = self.reduction(i, T0)  # 此处Job为数组
            # print("Job = " , Job)
            O_i = Job[0]  # 作业编号
            O_j = Job[1]  # 工序编号
            Machine_using = self.Processing_time[O_i][O_j]  # 此处O为processing_time,使用的机器的具体生产时间
            Machine_time = []
            for j in Machine_using:
                if j != 9999:
                    Machine_time.append(j)  # 存放非9999的时间
            # Min_index = Machine_time.index(min(Machine_time))  # 找出最短时间
            # Min_index = random.randint(0, len(Machine_time) - 1)  # 随机选择机器
            if len(Machine_time) >= 2:  # 若可用机器大于等于2
                Min_index = np.random.choice(np.delete(np.arange(len(Machine_time)), MS[i]))  # 去除原先选择，随机选择一台
            else:
                Min_index = random.randint(0, len(Machine_time) - 1)  # 随机选择一台
            MS[i] = Min_index  # 替换为时间短的机器
        new_CHS = np.hstack((MS, OS))
        return new_CHS

    def swap_mutation_os(self, CHS1, T0):
        """
        作业交换变异
        :param CHS1:  染色体
        :param T0: 总操作数
        :return: 变异之后的染色体
        """
        os = CHS1[T0:2 * T0]
        ms = CHS1[0:T0]
        D = len(os)
        c1 = os.copy()
        r = np.random.uniform(size=D)  # 生成0-1序列，长度等于os长度
        for idx1, val in enumerate(os):
            if r[idx1] <= 0.5:  # 小于0.5则随机选择另外一个点位进行变异
                idx2 = np.random.choice(np.delete(np.arange(D), idx1))
                c1[idx1], c1[idx2] = c1[idx2], c1[idx1]
        new_chs = np.hstack((ms, c1))
        return new_chs

    def crossoverOS(self, CHS1, CHS2, T0):
        """
        OS部分选择哪一种交叉
        :param CHS1: 染色体1
        :param CHS2: 染色体2
        :param T0: 总操作数
        :param J_num: 作业数量
        :return: 两条新染色体
        """
        return self.pox_crossover_os(CHS1, CHS2, T0)

    def crossoverMS(self, CHS1, CHS2, T0):
        """
        MS部分选择何种变异
        :param CHS1: 染色体1
        :param CHS2: 染色体2
        :param T0: 总操作数
        :return:
        """
        return self.two_point_crossover_ms(CHS1, CHS2, T0)

    def mutationOS(self, CHS1, T0):
        """
        OS部分选择何种变异
        :param CHS1:
        :param T0:
        :return:
        """
        return self.swap_mutation_os(CHS1, T0)

    def mutationMS(self, CHS, T0):
        """
        MS部分选择何种变异
        :param CHS: 染色体
        :param O: 时间矩阵
        :param T0: 总操作数
        :param J: 作业字典
        :return:
        """
        return self.change_mutation_ms(CHS, T0)

    def crossover_operator(self, C, T0):
        """
        交叉集成
        :param C: 种群
        :param T0: 总操作数
        :param J_num: 作业数量
        :return: 一个新种群
        """
        newPop = []  # 存放新染色体
        i = 0
        while i < len(C):
            CHS1 = C[i]  # 选择染色体进入交叉
            CHS2 = C[i + 1]
            if random.random() < self.P_c:  # 小于交叉概率
                new_chs1, new_chs2 = self.crossoverOS(CHS1, CHS2, T0)
                new_chs1, new_chs2 = self.crossoverMS(new_chs1, new_chs2, T0)
                newPop.append(new_chs1)
                newPop.append(new_chs2)
            else:
                newPop.append(CHS1)
                newPop.append(CHS2)
            i = i + 2
        return newPop

    def mutation_operator(self, C, T0):
        """
        集成变异
        :param C: 种群
        :param O: 时间矩阵
        :param T0: 总操作数
        :param J: 作业字典
        :return: 新种群
        """
        new_Pop = []
        for i in range(len(C)):
            if random.random() < self.P_m:
                new_chs1 = self.mutationOS(C[i], T0)
                new_chs2 = self.mutationMS(new_chs1, T0)
                new_Pop.append(new_chs2)
            else:
                new_Pop.append(C[i])
        return new_Pop

    def elite_selection(self, Fit):
        """
        精英选择，返回列表
        :param Fit: 当前种群的适应度列表
        :return: 最优个体索引
        """
        # print("Fit", Fit)
        Fit_dict = dict(enumerate(Fit))  # 创建字典
        Fit_dict = list(sorted(Fit_dict.items(), key=lambda x: x[1]))  # 按照适应度排序
        idx = []
        for i in range(self.N_elite):
            idx.append(Fit_dict[i][0])  # 存放索引
        return idx

    def tournament_selection(self, Fit):
        """
        轮盘赌选择
        :param Fit: 当前种群的适应度
        :return: 选择两个，返回适应度更好的那一个
        """
        idx_list = []  # 存放索引
        fit_list = []  # 存放适应度
        for i in range(self.choose_num):
            idx = random.randint(0, len(Fit) - 1)
            idx_list.append(idx)
            fit_list.append(Fit[idx])
        # print(idx_list, fit_list)
        min_fit = min(fit_list)
        min_fit_idx = idx_list[fit_list.index(min_fit)]
        return min_fit_idx

    def select(self, C, Fit):
        """
        选择，精英+锦标赛
        :param C: 当前种群
        :param Fit: 当前种群适应度
        :return: 一个新的种群
        """
        new_Pop = []
        elite_idx = self.elite_selection(Fit)  # 选择的精英的索引
        for i in elite_idx:  # 精英加入种群
            new_Pop.append(C[i])
        while len(new_Pop) < len(C):  # 若没有达到种群大小
            idx = self.tournament_selection(Fit)  # 轮盘赌选择
            new_Pop.append(C[idx])
        return new_Pop

    def adjust_for_priority_by_machine(self, chs):  # 各机器上作业按照优先级排序
        # print("优先级", self.Priority)
        # print("染色体长度", len(chs), chs)
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        # print("ms部分", ms)
        # print("os部分", os)
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_idx in range(len(ms)):
            # m_idx = ms[job_idx]+12  # 机器索引
            m_idx = self.transform_machine_available_to_real(job_idx, ms[job_idx], self.Processing_time)  # 机器真实索引（唯一）
            job_on_machine[m_idx].append(job_idx)  # 存放订单索引
        # print("job_on_machine", job_on_machine)
        # new_job_on_machine = job_on_machine[12:21]  # 重新提取，去除空列表
        # print("new_job_on_machine", new_job_on_machine)
        os_adjust = copy.deepcopy(os)
        # for lst in new_job_on_machine:  # lst为一个机器上的作业索引
        #     job_priority = {}
        #     for jj in lst:  # jj为作业索引
        #         job_priority[jj] = Priority[jj+1]  # 优先级提取
        #     # 使用优先级对元素进行排序
        #     sorted_keys = sorted(job_priority.keys(), key=lambda x: job_priority[x], reverse=True)
        #     # 提取要排序的元素
        #     elements_to_sort = [list(os_adjust).index(key) for key in sorted_keys]
        #     # 按照值的顺序重新排序元素
        #     elements_sorted = sorted(elements_to_sort)
        #     # 将重新排序后的元素替换回原始列表中的位置
        #     for i, new_index in enumerate(elements_sorted):
        #         os_adjust[new_index] = os[elements_to_sort[i]]
        # print(os)
        # print(os_adjust)
        for lst in job_on_machine:  # lst为一个机器上的作业索引
            job_priority = {}
            for jj in lst:  # jj为作业索引
                job_priority[jj] = self.Priority[jj + 1]  # 优先级提取
            # print("job_priority", job_priority)
            sorted_keys = sorted(job_priority.keys(), key=lambda x: job_priority[x], reverse=True)  # 使用优先级对元素进行排序
            # print("sorted_keys", sorted_keys)
            elements_to_sort = [list(os_adjust).index(key) for key in sorted_keys]  # 提取要排序的订单所在索引
            # print("elements_to_sort", elements_to_sort)
            elements_sorted = sorted(elements_to_sort)  # 按照值的顺序重新排序元素
            # 将重新排序后的元素替换回原始列表中的位置
            for i, new_index in enumerate(elements_sorted):
                os_adjust[new_index] = os[elements_to_sort[i]]
        new_chs = np.hstack((ms, os_adjust))
        return new_chs

    def adjust_for_priority_by_machine_2(self, chs, copy_priority):  # 各机器上作业按照优先级排序
        # print("优先级", self.Priority)
        # print("染色体长度", len(chs), chs)
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        # print("ms部分", ms)
        # print("os部分", os)
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_idx in range(len(ms)):
            # m_idx = ms[job_idx]+12  # 机器索引
            m_idx = self.transform_machine_available_to_real(job_idx, ms[job_idx], self.Processing_time)  # 机器真实索引（唯一）
            job_on_machine[m_idx].append(job_idx)  # 存放订单索引
        # print("job_on_machine", job_on_machine)
        # new_job_on_machine = job_on_machine[12:21]  # 重新提取，去除空列表
        # print("new_job_on_machine", new_job_on_machine)
        os_adjust = copy.deepcopy(os)
        # for lst in new_job_on_machine:  # lst为一个机器上的作业索引
        #     job_priority = {}
        #     for jj in lst:  # jj为作业索引
        #         job_priority[jj] = Priority[jj+1]  # 优先级提取
        #     # 使用优先级对元素进行排序
        #     sorted_keys = sorted(job_priority.keys(), key=lambda x: job_priority[x], reverse=True)
        #     # 提取要排序的元素
        #     elements_to_sort = [list(os_adjust).index(key) for key in sorted_keys]
        #     # 按照值的顺序重新排序元素
        #     elements_sorted = sorted(elements_to_sort)
        #     # 将重新排序后的元素替换回原始列表中的位置
        #     for i, new_index in enumerate(elements_sorted):
        #         os_adjust[new_index] = os[elements_to_sort[i]]
        # print(os)
        # print(os_adjust)
        for lst in job_on_machine:  # lst为一个机器上的作业索引
            job_priority = {}
            for jj in lst:  # jj为作业索引
                job_priority[jj] = copy_priority[jj + 1]  # 优先级提取
            # print("job_priority", job_priority)
            sorted_keys = sorted(job_priority.keys(), key=lambda x: job_priority[x], reverse=True)  # 使用优先级对元素进行排序
            # print("sorted_keys", sorted_keys)
            elements_to_sort = [list(os_adjust).index(key) for key in sorted_keys]  # 提取要排序的订单所在索引
            # print("elements_to_sort", elements_to_sort)
            elements_sorted = sorted(elements_to_sort)  # 按照值的顺序重新排序元素
            # 将重新排序后的元素替换回原始列表中的位置
            for i, new_index in enumerate(elements_sorted):
                os_adjust[new_index] = os[elements_to_sort[i]]
        new_chs = np.hstack((ms, os_adjust))
        return new_chs

    def adjust_for_priority_by_color(self, chs):  # 各颜色作业按照优先级排序
        # print("染色体长度", len(chs), chs)
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        # print("ms部分", ms)
        # print("os部分", os)
        job_on_color = [[] for _ in range(len(self.color_list))]  # 存放各个颜色的订单索引
        for job_idx in os:
            job_color = self.job_message[job_idx][0]['深浅色']  # 提取作业颜色
            color_idx = self.color_list.index(job_color)
            job_on_color[color_idx].append(job_idx)  # 存放订单索引
        os_adjust = copy.deepcopy(os)
        for lst in job_on_color:  # lst为各个颜色作业索引
            job_priority = {}
            for jj in lst:  # jj为作业索引
                job_priority[jj] = self.Priority[jj + 1]  # 优先级提取
            # 使用优先级对元素进行排序
            sorted_keys = sorted(job_priority.keys(), key=lambda x: job_priority[x], reverse=True)
            # 提取要排序的元素
            elements_to_sort = [list(os_adjust).index(key) for key in sorted_keys]
            # 按照值的顺序重新排序元素
            elements_sorted = sorted(elements_to_sort)
            # 将重新排序后的元素替换回原始列表中的位置
            for i, new_index in enumerate(elements_sorted):
                os_adjust[new_index] = os[elements_to_sort[i]]
            # print(os)
            # print(os_adjust)
        new_chs = np.hstack((ms, os_adjust))
        return new_chs

    def transform_machine_real_to_available(self, job, macine, pt):
        """
        将原本的实际机器编号转换为可用机器编号
        :param job: 作业id，从0开始
        :param macine: 实际机器id，从0开始，唯一
        :param pt: 处理时间矩阵
        :return:
        """
        # print("job", job, "machine", macine)
        job_pt = pt[job][0]  # 该订单在所有机器上的生产时间
        can_use_machine_list = [index for index, value in enumerate(job_pt) if value != 9999]  # 所有可用机器的实际索引
        # print(can_use_machine_list)
        new_machine_index = can_use_machine_list.index(macine)  # 固定机器在其可用机器列表中的索引
        return new_machine_index

    def transform_machine_available_to_real(self, job, macine, pt):
        """
        将可用索引像实际索引转换
        :param job:
        :param macine: 可用机器的索引
        :param pt:
        :return:
        """
        job_pt = pt[job][0]
        # print("job_pt", job_pt)
        can_use_machine_list = [index for index, value in enumerate(job_pt) if value != 9999]  # 所有可用机器的实际索引
        real_machine_index = can_use_machine_list[macine]
        return real_machine_index

    def adjust_color(self, chs, log):
        """
        将计划调整至最佳生产颜色机器上，按照负载最小的规则
        :param chs:
        :return:
        """
        log.write(f"偏好颜色处理阶段 \n\n")
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_idx in range(len(ms)):
            # m_idx = ms[job_idx] + 12  # 机器索引
            m_idx = self.transform_machine_available_to_real(job_idx, ms[job_idx], self.Processing_time)
            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXX", m_idx, m_idx_2)
            job_on_machine[m_idx].append(
                [job_idx, self.job_message[job_idx][0]['深浅色'], self.job_message[job_idx][0]['缸型']])  # 存放[订单索引, 颜色, 缸型]
        # print("job_on_machine", job_on_machine)
        # new_job_on_machine = job_on_machine[12:21]  # 重新提取，去除空列表
        # print("new_job_on_machine", len(new_job_on_machine), new_job_on_machine)
        no_change = []  # 存放不需要调整的订单索引
        # for lst_idx in range(len(new_job_on_machine)):
        #     machine_id = lst_idx + 12  # 选择机器的id
        #     sub_lst = new_job_on_machine[lst_idx]  # 每一台机器上的[订单索引, 颜色]
        #     sub_no_change = []  # 存放每一台机器上不需要调整的订单索引
        #     for job_color in sub_lst:  # 每一个计划的索引+颜色
        #         job_id = job_color[0]  # 计划索引
        #         color = job_color[1]  # 该计划的颜色
        #         best_color = next((key for key, value_list in self.color_machine_dict.items() if machine_id in value_list),
        #                       None)  # 提取该机器上最优的生产颜色
        #         if color == best_color:  # 与常染颜色相同
        #             sub_no_change.append(job_id)  # 存放不需要调整的订单索引，从0开始
        #     no_change.append(sub_no_change)
        # print('no_change1', no_change)
        for lst_idx in range(len(job_on_machine)):
            machine_id = lst_idx
            sub_lst = job_on_machine[lst_idx]  # 每一台机器上的[订单索引, 颜色，]
            sub_no_change = []  # 存放每一台机器上不需要调整的订单索引
            for job_color in sub_lst:  # 每一个计划的索引+颜色
                job_id = job_color[0]  # 计划索引
                color = job_color[1]  # 该计划的颜色
                machine_capacity = job_color[2]
                job_type = self.job_message[job_id][0]["轴型"]

                # best_color = next(
                #     (key for key, value_list in self.color_machine_dict[machine_capacity][job_type].items() if
                #      machine_id in value_list),
                #     None)  # 提取该机器上最优的生产颜色
                # if color == best_color:  # 与常染颜色相同
                #     sub_no_change.append(job_id)  # 存放不需要调整的订单索引，从0开始

                best_color = self.machine_message[machine_id]['Color']  # 提取该机器上最优的生产颜色
                if (color in best_color) or best_color == []:
                    sub_no_change.append(job_id)  # 存放不需要调整的订单索引，从0开始

            no_change.append(sub_no_change)
        # print('1 no_change', no_change)
        ms_adjust = copy.deepcopy(ms)
        for job in range(self.J_num):
            log.write(f"偏好颜色处理阶段 当前处理订单为: {self.job_message[job][0]['标识号']}\n")
            try:
                if_need_to_adjust = any(job in sublist for sublist in no_change)  # 判断是否需要调整，不需要调整返回true
                if not if_need_to_adjust:  # 需要进行调整的计划
                    color2 = self.job_message[job][0]['深浅色']  # 该计划的颜色
                    machine_capacity2 = self.job_message[job][0]['缸型']  # 该计划的缸型
                    job_type = self.job_message[job][0]['轴型']
                    # stop_machine_id = [self.stop_machine[i][1] for i in range(len(self.stop_machine))]
                    # print("stop_machine_id", stop_machine_id)
                    # if len(self.job_message[job][0]["续作机器"]) > 0 and self.job_message[job][0]["续作机器"][0] not in stop_machine_id:
                    #     for k, v in self.Machine_dict.items():
                    #         if v == self.job_message[job][0]["续作机器"][0]:
                    #             can_use = [k]
                    #             break
                    # else:
                    #     can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
                    can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
                    # print("canuse", can_use)
                    if can_use:
                        chosen_machine_idx = can_use.index(
                            min(can_use, key=lambda i: len(no_change[i])))  # 负载最少的可用机器????规则可调整
                        chosen_machine = can_use[chosen_machine_idx]  # 此处为真实的机器的索引
                        chosen_available_machine = self.transform_machine_real_to_available(job, chosen_machine,
                                                                                            self.Processing_time)
                        # print("XXXXXX", chosen_machine, chosen_machine_2)
                        # ms_adjust[job] = chosen_machine-12  # 更改选择机器
                        ms_adjust[job] = chosen_available_machine  # 更改选择机器
                        # 更新 no_change
                        no_change[chosen_machine].append(job)
                        # print('2 no_change', no_change)
                    else:  # 需要调整但是没有可用偏好颜色机器，不调整
                        # continue  # 可修改为调整到非增白
                        current_machine_available = ms[job]  # 当前选择机器
                        current_machine_real = self.transform_machine_available_to_real(job, current_machine_available,
                                                                                        self.Processing_time)
                        if self.machine_message[current_machine_real]["Color"][0] == "增白":  # 当前为增白
                            can_use = [index for index, value in enumerate(self.Processing_time[job][0]) if
                                       value != 9999]
                            can_adjust = [i for i in can_use if self.machine_message[i]["Color"][0] != "增白"]  # 提取非增白
                            if can_adjust:
                                chosen_machine = random.choice(can_adjust)  # 此处为真实的机器的索引，随机选择一个
                                chosen_available_machine = self.transform_machine_real_to_available(job, chosen_machine,
                                                                                                    self.Processing_time)
                                ms_adjust[job] = chosen_available_machine
                else:  # 不需要调整，在偏好颜色机器上
                    continue
            except Exception as e:
                print("处理订单 ", self.job_message[job][0]['标识号'], " 出错，错误信息：", e, " 偏好颜色处理阶段")
                log.close()
                break
        new_chs = np.hstack((ms_adjust, os))
        # print(new_chs)
        log.write(f"偏好颜色处理阶段完成 \n\n")
        return new_chs

    def adjust_color_2(self, chs):
        """
        将计划调整至最佳生产颜色机器上，按照负载最小的规则
        :param chs:
        :return:
        """
        job_category = {}  # 每一个作业对应的颜色荧光类别
        for i, sublist in enumerate(self.category):  # 填充job_category
            for element in sublist:
                job_category[element] = i
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_idx in range(len(ms)):
            # m_idx = ms[job_idx] + 12  # 机器索引
            m_idx = self.transform_machine_available_to_real(job_idx, ms[job_idx], self.Processing_time)
            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXX", m_idx, m_idx_2)
            job_on_machine[m_idx].append(
                [job_idx, self.job_message[job_idx][0]['深浅色'], self.job_message[job_idx][0]['缸型']])  # 存放[订单索引, 颜色, 缸型]
        # print("job_on_machine", job_on_machine)
        # new_job_on_machine = job_on_machine[12:21]  # 重新提取，去除空列表
        # print("new_job_on_machine", len(new_job_on_machine), new_job_on_machine)
        no_change = []  # 存放不需要调整的订单索引
        for lst_idx in range(len(job_on_machine)):
            machine_id = lst_idx
            sub_lst = job_on_machine[lst_idx]  # 每一台机器上的[订单索引, 颜色，]
            sub_no_change = []  # 存放每一台机器上不需要调整的订单索引
            for job_color in sub_lst:  # 每一个计划的索引+颜色
                job_id = job_color[0]  # 计划索引
                color = job_color[1]  # 该计划的颜色
                machine_capacity = job_color[2]
                job_type = self.job_message[job_id][0]["轴型"]
                # best_color = next(
                #     (key for key, value_list in self.color_machine_dict[machine_capacity][job_type].items() if
                #      machine_id in value_list),
                #     None)  # 提取该机器上最优的生产颜色
                best_colors = []  # 填入选定机器的偏好颜色
                for key, value in self.color_machine_dict[machine_capacity][job_type].items():
                    if machine_id in value:
                        best_colors.append(key)
                # print("==================best_colors===================", best_colors)
                # if color == best_color:  # 与常染颜色相同
                if color in best_colors:
                    sub_no_change.append(job_id)  # 存放不需要调整的订单索引，从0开始
            no_change.append(sub_no_change)
        # print('1 no_change', no_change)
        ms_adjust = copy.deepcopy(ms)
        need_adjust_job = []
        need_adjust_job_priority = []
        for job in range(self.J_num):
            if_need_to_adjust = any(job in sublist for sublist in no_change)  # 判断是否需要调整，不需要调整返回true
            if not if_need_to_adjust:  # 需要进行调整的计划
                need_adjust_job.append(job)
                need_adjust_job_priority.append([job, self.job_message[job][0]['优先级']])  # 存放订单及其优先级
        adjust_number = int(len(need_adjust_job) / 2)
        if adjust_number < 1:
            random_half = need_adjust_job
        else:
            # random_half = random.sample(need_adjust_job, adjust_number)  # 提取需要调整的订单(怎么选，低优先级？)
            sorted_need_adjust_job_priority = sorted(need_adjust_job_priority, key=lambda x: x[1],
                                                     reverse=True)  # 优先级从高到低排序
            random_half_temp = sorted_need_adjust_job_priority[adjust_number:]
            random_half = [element[0] for element in random_half_temp]  # 提取需要调整的订单，低优先级的一半
        for job in random_half:
            color2 = self.job_message[job][0]['深浅色']  # 该计划的颜色
            machine_capacity2 = self.job_message[job][0]['缸型']  # 该计划的缸型
            job_type = self.job_message[job][0]['轴型']
            can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
            # print("canuse", can_use)
            if can_use:
                chosen_machine_idx = can_use.index(
                    min(can_use, key=lambda i: len(no_change[i])))  # 负载最少的可用机器????规则可调整
                chosen_machine = can_use[chosen_machine_idx]  # 此处为真实的机器的索引
                chosen_available_machine = self.transform_machine_real_to_available(job, chosen_machine,
                                                                                    self.Processing_time)
                # print("XXXXXX", chosen_machine, chosen_machine_2)
                # ms_adjust[job] = chosen_machine-12  # 更改选择机器
                ms_adjust[job] = chosen_available_machine  # 更改选择机器
                # 更新 no_change
                no_change[chosen_machine].append(job)
                # print('2 no_change', no_change)
            else:  # 需要调整但是没有可用偏好颜色机器，不调整（调整到靠近的机器上）
                m_idx = self.transform_machine_available_to_real(job, ms[job], self.Processing_time)
                job_pt = self.Processing_time[job][0]
                prefer_color = self.machine_message[m_idx]['Color'][0]  # 可用机器的偏好颜色
                machine_color_index = self.color_list.index(prefer_color)
                job_color_index = job_category[job]
                if self.switching_cost[machine_color_index][job_color_index] == 99999:  # 在不合理机器上
                    can_choose_machine = [index for index, value in enumerate(job_pt) if value != 9999]
                    all_color_switching_cost = []  # 可用机器的所有偏好颜色
                    for j in can_choose_machine:
                        prefer_color = self.machine_message[j]['Color'][0]  # 可用机器的偏好颜色
                        machine_color_index = self.color_list.index(prefer_color)
                        # job_color_index = job_category[job]
                        all_color_switching_cost.append(self.switching_cost[machine_color_index][job_color_index])
                    # print("all_color_switching_cost", all_color_switching_cost)
                    if min(all_color_switching_cost) != 99999:
                        cost = 99999
                        cost_index = 0
                        while cost == 99999:  # 相当于随机选择
                            cost_index = random.choice(np.arange(len(all_color_switching_cost)))
                            cost = all_color_switching_cost[cost_index]
                        chosen_machine = can_choose_machine[cost_index]  # 此处为真实的机器的索引
                        chosen_available_machine = self.transform_machine_real_to_available(job, chosen_machine,
                                                                                            self.Processing_time)
                        ms_adjust[job] = chosen_available_machine  # 更改选择机器
        new_chs = np.hstack((ms_adjust, os))
        # print(new_chs)
        return new_chs

    def adjust_color_3(self, chs):
        """
        给定平均生产订单数
        将计划调整至最佳生产颜色机器上，按照负载最小的规则
        :param chs:
        :return:
        """

        job_category = {}  # 每一个作业对应的颜色荧光类别
        for i, sublist in enumerate(self.category):  # 填充job_category
            for element in sublist:
                job_category[element] = i
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        real_machine_list = []  # 平均值
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_index, machine in enumerate(ms):
            real_machine_index = self.transform_machine_available_to_real(job_index, machine, self.Processing_time)
            real_machine_list.append(real_machine_index)
            job_on_machine[real_machine_index].append(
                job_index)  # 存放[订单索引, 颜色, 缸型]

        # average_num = int(len(os) / len(list(set(real_machine_list))))
        average_num = {}
        for key, value in self.machine_class_dict.items():
            temp_sum = 0
            temp_job_on_machine = job_on_machine[value[0]: value[-1] + 1]
            for part_machine in temp_job_on_machine:
                temp_sum += len(part_machine)
            for machine_idd in value:
                average_num[machine_idd] = max(int(temp_sum / len(value)), 1)
        # print("各个机器平均值", average_num, len(average_num))

        adjust_job_dict = {}
        for index, job_list in enumerate(job_on_machine):
            adjust_job_dict[index] = max(0, len(job_list) - average_num[index])
        adjust_job_list = []  # 需要调整订单列表，暂考虑随机抽样
        for real_index, adjust_num in adjust_job_dict.items():
            random_list = random.sample(job_on_machine[real_index], adjust_num)
            adjust_job_list.extend(random_list)
        for adjust_job in adjust_job_list:  # 需要进行调整的计划
            color2 = self.job_message[adjust_job][0]['深浅色']  # 该计划的颜色
            if color2 != "增白":
                # machine_capacity2 = self.job_message[adjust_job][0]['缸型']  # 该计划的缸型
                # job_type = self.job_message[adjust_job][0]['轴型']
                # can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
                available_machine_adjust_job = ms[adjust_job]  # adjust_job的可用染机索引
                # adjust_job的实际机器索引
                real_machine_adjust_job = self.transform_machine_available_to_real(adjust_job,
                                                                                   available_machine_adjust_job,
                                                                                   self.Processing_time)

                can_use = [index for index, value in enumerate(self.Processing_time[adjust_job][0]) if value != 9999]
                # print("canuse", can_use)
                if can_use:
                    chosen_machine_idx = can_use.index(
                        min(can_use, key=lambda x: len(job_on_machine[x])))  # 负载最少的可用机器????规则可调整
                    chosen_machine = can_use[chosen_machine_idx]  # 此处为真实的机器的索引
                    chosen_available_machine = self.transform_machine_real_to_available(adjust_job, chosen_machine,
                                                                                        self.Processing_time)
                    # print("XXXXXX", chosen_machine, chosen_machine_2)
                    # ms_adjust[job] = chosen_machine-12  # 更改选择机器
                    ms[adjust_job] = chosen_available_machine  # 更改选择机器
                    # 更新 no_change
                    job_on_machine[real_machine_adjust_job].remove(adjust_job)  # 从原机器剔除一个
                    job_on_machine[chosen_machine].append(adjust_job)  # 更新后机器增加一个
                    # print('2 no_change', no_change)
                else:  # 需要调整但是没有可用机器，不调整
                    continue
        new_chs = np.hstack((ms, os))
        # print(new_chs)
        return new_chs

    def adjust_color_4(self, chs, log):
        """
        给定平均生产订单数
        将计划调整至最佳生产颜色机器上，按照负载最小的规则
        :param chs:
        :return:
        """
        log.write(f"均衡处理阶段 \n\n")
        # job_category = {}  # 每一个作业对应的颜色荧光类别
        # for i, sublist in enumerate(self.category):  # 填充job_category
        #     for element in sublist:
        #         job_category[element] = i
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        real_machine_list = []
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_index, machine in enumerate(ms):
            real_machine_index = self.transform_machine_available_to_real(job_index, machine, self.Processing_time)
            real_machine_list.append(real_machine_index)
            job_on_machine[real_machine_index].append(
                job_index)  # 存放[订单索引, 颜色, 缸型]
        # print("job_on_machine", job_on_machine)
        # average_num = int(len(os) / len(list(set(real_machine_list))))
        average_num = copy.deepcopy(self.machine_class_dict)  # 分类后平均值
        all_average_num = {}  # 整体平均值
        # self.machine_class_dict = {"30":{"SS":[0,1,2], "QQ":[4,5]}}
        for key, value in self.machine_class_dict.items():  # key容量，value{"SS":[0,1,2], "QQ":[4,5]}
            all_temp_sum = 0
            except_white = []  # 存放该容量下，去除增白的机器
            for key2, value2 in value.items():  # key深浅，value[0,1,2]机器索引
                temp_sum = 0
                for machine_idx in value2:
                    for job in job_on_machine[machine_idx]:
                        if self.job_message[job][0]["深浅色"] != "增白":
                            temp_sum += 1
                temp_average = max(int(temp_sum / len(value2)), 1)  # 容量下，这一个类下的平均值
                average_num[key][key2] = temp_average  # 填充
                except_white.extend(value2)
                # if value2:
                #     temp_average = max(int(temp_sum/len(value2)), 1)  # 容量下，这一个类下的平均值
                #     average_num[key][key2] = temp_average  # 填充
                #     except_white.extend(value2)
                # else:
                #     average_num[key][key2] = 0
            for machine_idx in except_white:
                all_temp_sum += len(job_on_machine[machine_idx])
            all_temp_average = max(int(all_temp_sum / len(except_white)), 1)  # 这一个容量之下的平均值
            all_average_num[key] = all_temp_average
            # if except_white:
            #     all_temp_average = max(int(all_temp_sum/len(except_white)), 1)  # 这一个容量之下的平均值
            #     all_average_num[key] = all_temp_average
            # else:
            #     all_average_num[key] = 0

        # print("average_num", average_num)
        # print("all_average_num", all_average_num)
        per_machine_average = {}  # 分类后，各个机器的平均值
        all_per_machine_average = {}  # 不分类，各个机器的平均值
        for key, value in self.machine_class_dict.items():
            for key2, value2 in value.items():
                for machine_idx in value2:
                    per_machine_average[machine_idx] = average_num[key][key2]
                    all_per_machine_average[machine_idx] = all_average_num[key]
        # 筛选出平均值小于等于4的颜色大类和平均值大于4的颜色大类
        adjust_machine_1 = []  # 存放分类后平均值小于等于4的机器
        adjust_machine_2 = []  # 存放整体平均值大于4的机器
        for key, value in average_num.items():
            for key2, value2 in value.items():
                if value2 <= self.average_quantity:
                    adjust_machine_1.append(self.machine_class_dict[key][key2])
                else:
                    adjust_machine_2.append(self.machine_class_dict[key][key2])

        # 先调整增白
        adjust_machine_white = []
        for key, value in self.machine_class_dict_white.items():
            for key2, value2 in value.items():
                adjust_machine_white.append(value2)
        for machine_list in adjust_machine_white:
            adjust_job_dict = {}  # 存放各个机器上需要调整的订单数量
            white_job_num = 0  # 这部分增白机器总归增白订单数量
            for machine_index in machine_list:
                white_job_num += len(job_on_machine[machine_index])
            average_white = max(int(white_job_num / len(machine_list)), 1)  # 这部分增白机器的平均值
            for machine_index in machine_list:
                adjust_job_dict[machine_index] = max(0, len(job_on_machine[machine_index]) - average_white)
            adjust_job_list = []  # 需要调整订单列表，暂考虑随机抽样
            for real_index, adjust_num in adjust_job_dict.items():
                random_list = random.sample(job_on_machine[real_index], adjust_num)  # 随机选择
                adjust_job_list.extend(random_list)
                # job_priority = [
                #     [job_on_machine[real_index][i], self.job_message[job_on_machine[real_index][i]][0]["优先级"]]
                #     for i in range(len(job_on_machine[real_index]))]  # 按照优先级选择
                # sorted_need_adjust_job_priority = sorted(job_priority, key=lambda x: x[1])  # 优先级从低到高排序
                # adjust_job_list_temp = sorted_need_adjust_job_priority[: adjust_num]
                # part_adjust_job_list = [element[0] for element in adjust_job_list_temp]  # 提取需要调整的订单，低优先级的一半
                # adjust_job_list.extend(part_adjust_job_list)
            for adjust_job in adjust_job_list:  # 需要进行调整的计划
                log.write(f"处理增白订单均衡: {self.job_message[adjust_job][0]['标识号']}\n")
                try:
                    # color2 = self.job_message[adjust_job][0]['深浅色']  # 该计划的颜色
                    # machine_capacity2 = self.job_message[adjust_job][0]['缸型']  # 该计划的缸型
                    # job_type = self.job_message[adjust_job][0]['轴型']
                    # can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
                    available_machine_adjust_job = ms[adjust_job]  # adjust_job的可用染机索引
                    # adjust_job的实际机器索引
                    real_machine_adjust_job = self.transform_machine_available_to_real(adjust_job,
                                                                                       available_machine_adjust_job,
                                                                                       self.Processing_time)
                    can_use = [index for index in machine_list if self.Processing_time[adjust_job][0][index] != 9999]
                    # print("canuse", can_use)
                    if can_use:
                        chosen_machine_idx = can_use.index(
                            min(can_use, key=lambda x: len(job_on_machine[x])))  # 负载最少的可用机器????规则可调整
                        chosen_machine = can_use[chosen_machine_idx]  # 此处为真实的机器的索引
                        chosen_available_machine = self.transform_machine_real_to_available(adjust_job, chosen_machine,
                                                                                            self.Processing_time)
                        # print("XXXXXX", chosen_machine, chosen_machine_2)
                        # ms_adjust[job] = chosen_machine-12  # 更改选择机器
                        ms[adjust_job] = chosen_available_machine  # 更改选择机器
                        # 更新 no_change
                        job_on_machine[real_machine_adjust_job].remove(adjust_job)  # 从原机器剔除一个
                        job_on_machine[chosen_machine].append(adjust_job)  # 更新后机器增加一个
                        # print('2 no_change', no_change)
                    else:  # 需要调整但是没有可用机器，不调整
                        continue
                except Exception as e:
                    print("处理订单 ", self.job_message[adjust_job][0]['标识号'], " 出错，错误信息：", e, " 处理增白订单均衡阶段")
                    log.close()
                    break
            log.write(f"处理增白订单均衡完成\n")

        # 先调整平均值小于等于4的颜色大类，调整时以颜色大类的订单平均数作为标准
        for machine_list in adjust_machine_1:
            adjust_job_dict = {}  # 存放各个机器上需要调整的订单数量
            for machine_index in machine_list:
                adjust_job_dict[machine_index] = max(0, len(job_on_machine[machine_index]) - per_machine_average[
                    machine_index])
            adjust_job_list = []  # 需要调整订单列表，暂考虑随机抽样
            for real_index, adjust_num in adjust_job_dict.items():
                # random_list = random.sample(job_on_machine[real_index], adjust_num)  # 随机选择
                # adjust_job_list.extend(random_list)
                job_priority = [
                    [job_on_machine[real_index][i], self.job_message[job_on_machine[real_index][i]][0]["优先级"]]
                    for i in range(len(job_on_machine[real_index]))]  # 按照优先级选择
                sorted_need_adjust_job_priority = sorted(job_priority, key=lambda x: x[1])  # 优先级从低到高排序
                adjust_job_list_temp = sorted_need_adjust_job_priority[: adjust_num]
                part_adjust_job_list = [element[0] for element in adjust_job_list_temp]  # 提取需要调整的订单，低优先级的一半
                adjust_job_list.extend(part_adjust_job_list)
            for adjust_job in adjust_job_list:  # 需要进行调整的计划
                log.write(f"处理均值小于设定值订单均衡: {self.job_message[adjust_job][0]['标识号']}\n")
                try:
                    color2 = self.job_message[adjust_job][0]['深浅色']  # 该计划的颜色
                    # machine_capacity2 = self.job_message[adjust_job][0]['缸型']  # 该计划的缸型
                    # job_type = self.job_message[adjust_job][0]['轴型']
                    # can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
                    if color2 != "增白":
                        available_machine_adjust_job = ms[adjust_job]  # adjust_job的可用染机索引
                        # adjust_job的实际机器索引
                        real_machine_adjust_job = self.transform_machine_available_to_real(adjust_job,
                                                                                           available_machine_adjust_job,
                                                                                           self.Processing_time)
                        can_use = [index for index in machine_list if
                                   self.Processing_time[adjust_job][0][index] != 9999]
                        # print("canuse", can_use)
                        if can_use:
                            chosen_machine_idx = can_use.index(
                                min(can_use, key=lambda x: len(job_on_machine[x])))  # 负载最少的可用机器????规则可调整
                            chosen_machine = can_use[chosen_machine_idx]  # 此处为真实的机器的索引
                            chosen_available_machine = self.transform_machine_real_to_available(adjust_job,
                                                                                                chosen_machine,
                                                                                                self.Processing_time)
                            # print("XXXXXX", chosen_machine, chosen_machine_2)
                            # ms_adjust[job] = chosen_machine-12  # 更改选择机器
                            ms[adjust_job] = chosen_available_machine  # 更改选择机器
                            # 更新 no_change
                            job_on_machine[real_machine_adjust_job].remove(adjust_job)  # 从原机器剔除一个
                            job_on_machine[chosen_machine].append(adjust_job)  # 更新后机器增加一个
                            # print('2 no_change', no_change)
                        else:  # 需要调整但是没有可用机器，不调整
                            continue
                except Exception as e:
                    print("处理订单 ", self.job_message[adjust_job][0]['标识号'], " 出错，错误信息：", e, " 处理均值小于设定值订单均衡阶段")
                    log.close()
                    break
            log.write(f"处理均值小于设定值订单均衡完成\n")
        # 再调整平均值大于4的颜色大类，但调整时以所有可用机器的订单平均数作为标准
        for machine_list in adjust_machine_2:
            adjust_job_dict = {}
            for machine_index in machine_list:
                adjust_job_dict[machine_index] = max(0, len(job_on_machine[machine_index]) - all_per_machine_average[
                    machine_index])
            adjust_job_list = []  # 需要调整订单列表，暂考虑随机抽样
            for real_index, adjust_num in adjust_job_dict.items():
                # random_list = random.sample(job_on_machine[real_index], adjust_num)
                # adjust_job_list.extend(random_list)
                job_priority = [
                    [job_on_machine[real_index][i], self.job_message[job_on_machine[real_index][i]][0]["优先级"]]
                    for i in range(len(job_on_machine[real_index]))]  # 按照优先级选择
                sorted_need_adjust_job_priority = sorted(job_priority, key=lambda x: x[1])  # 优先级从低到高排序
                adjust_job_list_temp = sorted_need_adjust_job_priority[: adjust_num]
                part_adjust_job_list = [element[0] for element in adjust_job_list_temp]  # 提取需要调整的订单，低优先级的一半
                adjust_job_list.extend(part_adjust_job_list)
            for adjust_job in adjust_job_list:  # 需要进行调整的计划
                log.write(f"处理均值大于设定值订单均衡: {self.job_message[adjust_job][0]['标识号']}\n")
                try:
                    color2 = self.job_message[adjust_job][0]['深浅色']  # 该计划的颜色
                    # machine_capacity2 = self.job_message[adjust_job][0]['缸型']  # 该计划的缸型
                    # job_type = self.job_message[adjust_job][0]['轴型']
                    # can_use = self.color_machine_dict[machine_capacity2][job_type][color2]  # 可用的机器
                    if color2 != "增白":
                        available_machine_adjust_job = ms[adjust_job]  # adjust_job的可用染机索引
                        # adjust_job的实际机器索引
                        real_machine_adjust_job = self.transform_machine_available_to_real(adjust_job,
                                                                                           available_machine_adjust_job,
                                                                                           self.Processing_time)
                        can_use = [index for index, value in enumerate(self.Processing_time[adjust_job][0]) if
                                   value != 9999]
                        # print("canuse", can_use)
                        if can_use:
                            chosen_machine_idx = can_use.index(
                                min(can_use, key=lambda x: len(job_on_machine[x])))  # 负载最少的可用机器????规则可调整
                            chosen_machine = can_use[chosen_machine_idx]  # 此处为真实的机器的索引
                            chosen_available_machine = self.transform_machine_real_to_available(adjust_job,
                                                                                                chosen_machine,
                                                                                                self.Processing_time)
                            # print("XXXXXX", chosen_machine, chosen_machine_2)
                            # ms_adjust[job] = chosen_machine-12  # 更改选择机器
                            ms[adjust_job] = chosen_available_machine  # 更改选择机器
                            # 更新 no_change
                            job_on_machine[real_machine_adjust_job].remove(adjust_job)  # 从原机器剔除一个
                            job_on_machine[chosen_machine].append(adjust_job)  # 更新后机器增加一个
                            # print('2 no_change', no_change)
                        else:  # 需要调整但是没有可用机器，不调整
                            continue
                except Exception as e:
                    print("处理订单 ", self.job_message[adjust_job][0]['标识号'], " 出错，错误信息：", e, " 处理均值大于设定值订单均衡阶段")
                    log.close()
                    break
            log.write(f"处理均值大于设定值订单均衡完成\n")
        new_chs = np.hstack((ms, os))
        # print(new_chs)
        return new_chs

    def adjust_continue_job(self, chs, log):
        """
        调整续作订单机器
        :param chs:
        :return:
        """
        log.write(f"续作处理阶段 \n\n")
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        for job_machine in self.continue_job:
            job = job_machine[0]
            log.write(f"续作当前处理订单为: {self.job_message[job][0]['标识号']}\n")
            try:
                machine = job_machine[1]
                ms[job] = machine
            except Exception as e:
                print("处理订单 ", self.job_message[job][0]['标识号'], " 出错，错误信息：", e, " 续作处理阶段")
                log.close()
                break
        log.write(f"续作处理阶段完成 \n\n")
        new_chs = np.hstack((ms, os))
        return new_chs

    def judge_middle_color(self, same_machine, job_on_machine):  # 未完成0414
        """
        调整可用中色
        :param same_machine: 同类型机器
        :param job_on_machine: 二维列表，内部存放机器上的订单 [订单索引, 颜色, 缸型]
        :return:
        """
        sub_list = ["深色", "中色", "中色", "浅色"]
        each_machine_middle_color = []  # 存放每个机器上中色数量
        unavailable_index = [[] for _ in range(len(same_machine))]  # 存放每个机器上不可用的中色索引
        for machine_id in same_machine:
            color_on_machine = [i[1] for i in job_on_machine[machine_id]]
            middle_color_idx = [idx for idx, val in enumerate(color_on_machine) if val == '中色']  # 中色的索引
            each_machine_middle_color.append(middle_color_idx)
            flag = 0  # 标识，是否存在不可调整的情况，1为存在，即有深中中浅
            if len(color_on_machine) >= 4:
                for i in range(len(color_on_machine) - len(sub_list) + 1):
                    if color_on_machine[i:i + len(sub_list)] == sub_list:
                        unavailable_index[same_machine.index(machine_id)].append(i + 1)
                        unavailable_index[same_machine.index(machine_id)].append(i + 2)
                        flag = 1
        available_middle_color = []  # 存放每一个机器上的可用调整中色 [机器索引, 可用中色在该机器上的索引]
        for i in range(len(each_machine_middle_color)):
            if len(each_machine_middle_color[i]) > len(unavailable_index[i]):  # 拥有可用用于调整的中色
                for_adjudt = [x for x in each_machine_middle_color[i] if x not in unavailable_index[i]]  # i机器上用于调整的中色
                machine_index = same_machine[i]  # i机器的索引
                available_middle_color.append([machine_index, for_adjudt])  # [机器索引, 可用中色在该机器上的索引]
        for i in range(2):  # 取两个中色
            sorted_available_middle_color = sorted(available_middle_color, key=lambda x: len(x[1]), reverse=True)
            # 从sorted_available_middle_color[0]中取中色
            chosen_machine = sorted_available_middle_color[0]
            chosen_job = sorted_available_middle_color[1][-1]  # 取可用的最后一个（索引）
            job_index = job_on_machine[chosen_machine][chosen_job][0]  # 获取调整订单的索引
            # 再根据索引，调整染色体 0414

            # 怎么判断可用的中色 0410
            # if len(middle_color_idx) == 2:
            #     if middle_color_idx[0]+1 == middle_color_idx[1]:
            #         if middle_color_idx[0] > 0 and middle_color_idx[1] < len(job_on_machine[machine_id]-1):
            #             if color_on_machine[middle_color_idx[0]]

    def adjust_continue_color(self, chs):  # 未完成0414
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个机器生产的订单索引
        for job_idx in range(len(ms)):
            m_idx = self.transform_machine_available_to_real(job_idx, ms[job_idx], self.Processing_time)
            job_on_machine[m_idx].append(
                [job_idx, self.job_message[job_idx][0]['深浅色'], self.job_message[job_idx][0]['缸型']])  # 存放[订单索引, 颜色, 缸型]
        for job_machine in self.continue_job:  # self.continue_job 二维列表，订单编号+可用机器集合中的索引
            job = job_machine[0]
            available_machine_idx = job_machine[1]
            real_machine_idx = self.transform_machine_available_to_real(job, ms[job], self.Processing_time)
            color = self.job_message[job][0]['深浅色']
            # 提取续作订单在该机器上的索引
            continue_job_position = job_on_machine[real_machine_idx].index([job, self.job_message[job][0]['深浅色'],
                                                                            self.job_message[job][0]['缸型']])
            if color == '深色':
                # 判断其后一个作业是不是浅色
                if continue_job_position < len(job_on_machine[real_machine_idx]) - 1:
                    if job_on_machine[real_machine_idx][continue_job_position + 1][1] == '浅色':
                        # 需要调整
                        # pt = self.Processing_time[job][0]  # 该作业可用机器
                        # 同类型机器
                        same_machine_idx = [idx for idx, val in enumerate(self.Processing_time[job][0]) if val != 9999]
                        # 0410

            if color == '浅色':
                # 判断其前一个作业是不是深色
                if continue_job_position > 0:
                    if job_on_machine[real_machine_idx][continue_job_position - 1][1] == '深色':
                        # 需要调整
                        same_machine_idx = [idx for idx, val in enumerate(self.Processing_time[job][0]) if val != 9999]
                    # 0410

    def change_locked_job_order(self, chs, log):
        """
        调整锁定状态生产顺序
        :param chs:
        :param lockedjob: {'201':[[12,1], [13,2], [14,3]]} 121314锁定生产，顺序分别为123，暂未传入，从input中读取
        :return:
        """
        log.write(f"锁定订单生产顺序处理阶段 \n\n")
        # print("locked_job_order", self.locked_job_order)
        ms = chs[:int(len(chs) / 2)]
        os = chs[int(len(chs) / 2):]
        new_os = copy.deepcopy(os)
        new_os = list(new_os)
        # print("locked_job_order", self.locked_job_order)
        # print("before", new_os)
        for machine, lock_job in self.locked_job_order.items():
            sort_lock_job = sorted(lock_job, key=lambda x: x[1], reverse=True)  # 倒序顺序
            for job in sort_lock_job:
                # print(job)
                log.write(f"锁定顺序当前处理订单为: {self.job_message[job[0]][0]['标识号']}\n")
                try:
                    new_os.remove(job[0])  # 剔除
                    new_os.insert(0, job[0])  # 添加到os列表首
                except Exception as e:
                    print("处理订单 ", self.job_message[job[0]][0]['标识号'], " 出错，错误信息：", e, " 锁定订单生产顺序处理阶段")
                    log.close()
                    break
        # print("afterr", new_os)
        log.write(f"锁定订单生产顺序处理阶段完成 \n\n")
        new_chs = np.hstack((ms, new_os))
        return new_chs

    def adjust_initial_color_state(self, chs):
        # print("开始调整")
        copy_priority = copy.deepcopy(self.Priority)
        ms = chs[:int(len(chs) / 2)]
        os = list(chs[int(len(chs) / 2):])
        job_on_machine = [[] for _ in range(self.M_num)]  # 存放各个工厂生产的订单索引
        for job_index in os:
            available_machine_idx = ms[job_index]
            real_machine_index = self.transform_machine_available_to_real(job_index, available_machine_idx,
                                                                          self.Processing_time)
            job_on_machine[real_machine_index].append(job_index)  # 存放订单索引
        for i in range(len(job_on_machine)):
            job_list = job_on_machine[i]  # 第i台机器上安排的作业
            if job_list:  # 不为空
                first_job = job_list[0]
                first_job_color = self.job_message[first_job][0]['深浅色']
                first_job_color_idx = self.color_list.index(first_job_color)
                initial_color = self.machine_pre_color[i]
                if initial_color != '':  # 需要判断调整
                    initial_color_idx = self.color_list.index(initial_color)
                    if self.switching_cost[initial_color_idx][first_job_color_idx] == 99999:  # 需要调整
                        if initial_color == '深色' and first_job_color == '浅色':  # 找两个中色
                            temp_adjust = []
                            for job in job_list:
                                if self.job_message[job][0]['深浅色'] == '中色':
                                    temp_adjust.append(job)
                            if temp_adjust:  # 可用于调整的不为空
                                if len(temp_adjust) >= 2:
                                    for j in range(2):  # 取两个中色
                                        adjust_job = random.choice(temp_adjust)
                                        # first_job_location = os.index(first_job)
                                        # os.insert(first_job_location, adjust_job)
                                        copy_priority[adjust_job + 1] = 200
                                        # self.job_message[adjust_job][0]['优先级'] = 200
                                    # print("调整成功 深色-浅色", "机器", i)
                                else:
                                    adjust_job = temp_adjust[0]
                                    # first_job_location = os.index(first_job)
                                    # os.insert(first_job_location, adjust_job)
                                    copy_priority[adjust_job + 1] = 200
                                    # self.job_message[adjust_job][0]['优先级'] = 200
                        elif initial_color == '深色' and first_job_color == '浅浅':  # 找两个中色
                            temp_adjust = []
                            for job in job_list:
                                if self.job_message[job][0]['深浅色'] == '中色':
                                    temp_adjust.append(job)
                            if temp_adjust:  # 可用于调整的不为空
                                if len(temp_adjust) >= 2:
                                    for j in range(2):  # 取两个中色
                                        adjust_job = random.choice(temp_adjust)
                                        # first_job_location = os.index(first_job)
                                        # os.insert(first_job_location, adjust_job)
                                        copy_priority[adjust_job + 1] = 200
                                        # self.job_message[adjust_job][0]['优先级'] = 200
                                    # print("调整成功 深色-浅浅", "机器", i)
                                else:
                                    adjust_job = temp_adjust[0]
                                    # first_job_location = os.index(first_job)
                                    # os.insert(first_job_location, adjust_job)
                                    copy_priority[adjust_job + 1] = 200
                                    # self.job_message[adjust_job][0]['优先级'] = 200
                        elif initial_color == '深色' and first_job_color == '增白':  # 找两个中色
                            temp_adjust = []
                            for job in job_list:
                                if self.job_message[job][0]['深浅色'] == '中色':
                                    temp_adjust.append(job)
                            if temp_adjust:  # 可用于调整的不为空
                                if len(temp_adjust) >= 2:
                                    for j in range(2):  # 取两个中色
                                        adjust_job = random.choice(temp_adjust)
                                        # first_job_location = os.index(first_job)
                                        # os.insert(first_job_location, adjust_job)
                                        copy_priority[adjust_job + 1] = 200
                                        # self.job_message[adjust_job][0]['优先级'] = 200
                                else:
                                    adjust_job = temp_adjust[0]
                                    # first_job_location = os.index(first_job)
                                    # os.insert(first_job_location, adjust_job)
                                    copy_priority[adjust_job + 1] = 200
                                    # self.job_message[adjust_job][0]['优先级'] = 200
                            temp_adjust = []
                            for job in job_list:
                                if self.job_message[job][0]['深浅色'] == '浅色':
                                    temp_adjust.append(job)
                            if temp_adjust:  # 可用于调整的不为空
                                adjust_job = random.choice(temp_adjust)
                                copy_priority[adjust_job + 1] = 200
                                # self.job_message[adjust_job][0]['优先级'] = 200
                                # print("调整成功 深色-增白", "机器", i)
                        elif initial_color == '中色' and first_job_color == '增白':  # 找两个中色
                            temp_adjust = []
                            for job in job_list:
                                if self.job_message[job][0]['深浅色'] == '浅色' or self.job_message[job][0]['深浅色'] == '浅浅':
                                    temp_adjust.append(job)
                            if temp_adjust:  # 可用于调整的不为空
                                adjust_job = random.choice(temp_adjust)
                                copy_priority[adjust_job + 1] = 200
                                # self.job_message[adjust_job][0]['优先级'] = 200
                                # print("调整成功 中色-增白", "机器", i)
                        elif initial_color == '增白' and first_job_color == '中色':  # 找两个中色
                            pass
                        elif initial_color == '增白' and first_job_color == '浅色':  # 找两个中色
                            pass
                        elif initial_color == '增白' and first_job_color == '浅浅':  # 找两个中色
                            pass
                        else:
                            print("颜色判断存在问题")
        # new_chs = np.hstack((ms, os))
        new_chs = chs
        return new_chs, copy_priority

    def adjust_chs(self, chs, log):
        """
        邻域搜索，用于调整计划生产优先级
        将相同颜色的计划调整至同一台机器上
        :param chs: 未调整的染色体
        :return:
        """
        # print("=========优先级========", self.Priority)
        new_chs = self.adjust_color(chs, log)  # 调整偏好颜色
        # new_chs = self.adjust_color_2(chs)  # 调整偏好颜色
        # new_chs = self.adjust_color_3(new_chs)  # 调整偏好颜色（二次调整，均衡
        # new_chs = self.adjust_continue_job(new_chs)  # 调整续作订单机器（先调整一次
        new_chs = self.adjust_color_4(new_chs, log)  # 调整偏好颜色（二次调整，均衡
        new_chs2 = self.adjust_continue_job(new_chs, log)  # 调整续作订单机器
        new_chs3 = self.check_fixed_job_chs(new_chs2, log)  # 调整锁定状态的机器
        new_chs3, copy_priority = self.adjust_initial_color_state(new_chs3)  # 初始状态的调整
        # new_chs4 = self.adjust_for_priority_by_machine(new_chs3)  # 按照优先级调整顺序
        new_chs4 = self.adjust_for_priority_by_machine_2(new_chs3, copy_priority)  # 按照优先级调整顺序
        # new_chs2 = self.adjust_for_priority_by_color(new_chs)
        # 调整深浅切换
        new_chs5 = self.change_locked_job_order(new_chs4, log)  # 调整锁定状态生产顺序
        return new_chs5

    # def neighbourhood_search(self, C, Len_Chromo):
    #     """
    #     选取部分最优染色体进入邻域搜索
    #     :param C:
    #     :return:
    #     """
    #     all_fit = self.fitness(C, Len_Chromo)
    #     Fit_idx = list(enumerate(all_fit))
    #     sorted_Fit = sorted(Fit_idx, key=lambda x: x[1])[:self.neighbour_size]  # 找出最优部分染色体
    #     for idx, value in sorted_Fit:
    #         chs = C[idx]
    #         new_chs = self.adjust_chs(chs)
    #         d = Decode(self.J, self.Processing_time, self.M_num, self.Priority, self.secondary_resource,
    #                    self.switching_time, self.category, self.switching_cost,
    #                    self.new_job_dict, self.axle_resource_num, self.color_machine_dict, self.machine_list,
    #                    self.srn_type_dict, self.Machine_dict, self.start_time)  # 画甘特图  增加优先级
    #         new_chs_result = d.Decode_1(new_chs, Len_Chromo, self.Priority)[0]
    #         if new_chs_result < value:
    #             C[idx] = new_chs
    #     return C

    def neighbourhood_search_2(self, C, log):
        new_C = []
        # locked_job = self.change_locked_state_job()
        for chs in C:
            new_chs = self.adjust_chs(chs, log)
            # new_chs = self.check_chs(new_chs, locked_job)  # 外部调整锁定状态
            new_C.append(new_chs)
        return new_C

    def acquire_condition(self, result_json, judge_time):
        """
        获取某一时刻，所有作业的工作状态，获取副资源数量
        :param judge_time:
        :param secondary_resource:
        :param result_json:
        :return:
        """
        machine_start_time = [judge_time for _ in range(self.M_num)]  # 重新记录各个机器的开始时间
        copy_secondary_resource = copy.deepcopy(self.secondary_resource)
        for job_message in result_json:
            start_time = job_message[2]
            end_time = job_message[3]
            switch_time = job_message[6]
            if end_time <= judge_time:
                job_message.append('已完成')
            elif start_time < judge_time < end_time + switch_time:
                job_message.append('生产中')
                job_resource = job_message[9]  # 占用的副资源
                machine_start_time[job_message[4]] = end_time + switch_time  # 更新可用时间
                if job_resource == '纱架':
                    copy_secondary_resource[0] -= 1
                elif job_resource == 'S':
                    copy_secondary_resource[1] -= 1
                elif job_resource == 'M':
                    copy_secondary_resource[2] -= 1
                elif job_resource == 'L':
                    copy_secondary_resource[3] -= 1
                else:
                    copy_secondary_resource[4] -= 1
            else:
                job_message.append('未生产')
        return result_json, copy_secondary_resource, machine_start_time

    def check_fixed_job_chs(self, chs, log):
        """
        染色体修复，有些订单有固定的生产机器，将选择机器改变，变为其可用机器内的索引
        :param fixed_job: 固定机器的作业[[job, machine], [job, machine]]
        :param chs: 需要修复的染色体
        :return:
        """
        log.write(f"确定锁定机器处理阶段 \n\n")
        for job_machine in self.locked_job:
            job_id = job_machine[0]
            try:
                log.write(f"续作当前处理订单为: {self.job_message[job_id][0]['标识号']}\n")
                machine_id = job_machine[1]
                chs[job_id] = machine_id  # 更改生产机器
            except Exception as e:
                # print(e)
                print("处理订单 ", self.job_message[job_id][0]['标识号'], " 出错，错误信息：", e, " 确定锁定机器处理阶段")
                log.close()
                break
        log.write(f"确定锁定机器处理阶段完成 \n\n")
        return chs

    def main(self):  # 增加优先级
        current_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
        log_message = open('log_message_' + current_time + '.txt', 'w')
        e = Encode(self.Processing_time, self.Pop_size, self.J, self.J_num, self.M_num,
                   self.job_message)  # 可以返回3个CHS, 大小180*54等……
        Len_Chromo = e.Len_Chromo  # 计算总工序（各工件工序和）
        print("++++++++++++++++++++++", Len_Chromo)
        C = e.Random_initial(log_message)
        # print("C[0]", len(C[0]), C[0])
        Optimal_fit = np.inf
        Optimal_CHS = 0
        x = np.linspace(0, self.Max_Itertions, self.Max_Itertions)
        Best_fit = []
        best_json = 0
        for i in trange(self.Max_Itertions):
            # log_message = open('log_message.txt', 'w')
            # log_message.write(f"当前迭代次数: {i+1}\n\n")
            Fit = self.fitness(C, Len_Chromo)  # 最小最大化完工时间，增加优先级
            # print("全体适应度", Fit)
            Best = C[Fit.index(min(Fit))]  # Fit.index(min(Fit)):C中最小适应度的索引，再反选出CHS中的某一方案
            if i == 0:
                best_fitness = min(Fit) + 10 ** 10  # 更新最小适应度
            else:
                best_fitness = min(Fit)  # 更新最小适应度
            if best_fitness < Optimal_fit:
                Optimal_fit = best_fitness  # 更换Optimal_fit
                Optimal_CHS = Best  # 填入数组，即方案
                Best_fit.append(Optimal_fit)  # 暂存Optimal_fit，画图用
                print("No.", i + 1, " Best方案 = ", Best)
                print("迭代次数", i + 1, 'best_fitness', best_fitness)

                # 原始Optimal_chs
                d = Decode(self.J, self.Processing_time, self.M_num, self.Priority, self.secondary_resource,
                           self.switching_time, self.category, self.switching_cost,
                           self.new_job_dict, self.axle_resource_num, self.color_machine_dict, self.machine_list,
                           self.srn_type_dict, self.Machine_dict, self.start_time, self.machine_message,
                           self.machine_pre_color, self.json_dict, self.Old_Job_dict)  # 画甘特图  增加优先级
                result3 = d.Decode_1(Optimal_CHS, Len_Chromo, self.Priority)
                print("迭代次数", i + 1, '时间', result3[1])
                print("迭代次数", i + 1, '切换成本', result3[2])
                print("迭代次数", i + 1, '均衡成本', result3[3])
                print("迭代次数", i + 1, '选择机器成本', result3[4])
                print("迭代次数", i + 1, '优先级策略', result3[5])
                print("迭代次数", i + 1, '交期惩罚', result3[6])
                print("迭代次数", i + 1, '同批惩罚', result3[7])

                # 调整Optimal_CHS
                # new_optimal_chs = self.adjust_chs(Optimal_CHS)  # 调整染色体
                # d = Decode(J, Processing_time, M_num, Priority)  # 画甘特图  增加优先级
                # result4 = d.Decode_1(new_optimal_chs, Len_Chromo, Priority)
                # print("迭代次数", i + 1, '时间', result4[1])
                # print("迭代次数", i + 1, '切换成本', result4[2])
                # print("迭代次数", i + 1, '均衡成本', result4[3])
                # print("迭代次数", i + 1, '选择机器成本', result4[4])
                # print("迭代次数", i + 1, '优先级策略', result4[5])
                #
                # if result4[0] < Optimal_fit:
                #     Optimal_fit = result4[0]

                # 输出结果
                d.Output_Result(d.Machines, i)
                self.Machines = d.Machines
                # d.Output_Result_02(d.Jobs, i)

                # best_json = d.output_json(d.Jobs, i)
                # d.Gantt(d.Machines, i)  # 输出甘特图
            else:
                Best_fit.append(Optimal_fit)
                # print("No.", i + 1, " Not_Best方案 = ", Best)  # 循环打印最小方案，展示迭代次数
                print("迭代次数", i + 1, 'not_best_fitness', Optimal_fit)
            # log_message.write(f"当前迭代完成: {i + 1}\n\n")

            C = self.select(C, Fit)  # 精英+3元锦标赛
            crossover_C = self.crossover_operator(C, Len_Chromo)  # 交叉
            mutation_C = self.mutation_operator(crossover_C, Len_Chromo)  # 变异
            C = mutation_C  # 获得更新后的种群C
            # C = self.neighbourhood_search(C, Len_Chromo)
            C = self.neighbourhood_search_2(C, log_message)
            # log_message.close()

        log_message.write(f"程序结束\n\n")
        log_message.close()
        log_file_path = 'log_message_' + current_time + '.txt'
        os.remove(log_file_path)
        final_json = out_put_json(self.Machines, self.job_message, self.Machine_dict, self.switching_time,
                                  self.json_dict)
        # plt.plot(x, Best_fit, '-k')
        # plt.title('flexible job shop scheduling problem')
        # plt.ylabel('Cmax')
        # plt.xlabel('Test Num')
        # plt.show()
        return final_json


# 输出
def out_put_json(Machines, job_message_list, machine_id_dict, switching_time, json_dict):

    current_datatime = datetime.now()
    factoryId = list(json_dict["Factory"].keys())[0]
    AllDict = {}
    orderDict = {}
    orderDict_1 = {}
    MachineDict = {}
    machineDict = {}
    for i in range(len(Machines)):
        Machine = Machines[i]
        if len(Machine.assigned_task) != 0:
            print("机器", machine_id_dict[i], "订单", Machine.assigned_task)
            Start_time = Machine.O_start
            End_time = Machine.O_end
            count = 1
            tempMachineDict = {}
            for i_1 in range(len(End_time)):
                tempDict = {}
                # print("sssssss", job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'])
                if len(job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单']) == 0:
                    tempDict["CooperativeNumber"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作序号']
                    tempDict["MachineCapacity"] = int(job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型'])
                    tempDict["ColourNumber"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['色号']
                    tempDict["Color"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['深浅色']
                    tempDict["OrderId"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']
                    tempDict["MachineId"] = machine_id_dict[i]
                    tempDict["ProductionSequence"] = count
                    tempDict["OrderStatus"] = "已排产"
                    tempDict["StartTime"] = (current_datatime + timedelta(minutes=Start_time[i_1])).strftime(
                        "%Y-%m-%d %H:%M")
                    tempDict["EndTime"] = (current_datatime + timedelta(minutes=End_time[i_1])).strftime(
                        "%Y-%m-%d %H:%M")
                    # tempDict["StartTime"] = Start_time[i_1]
                    # tempDict["EndTime"] = End_time[i_1]
                    start_time = (current_datatime + timedelta(minutes=Start_time[i_1])).strftime("%Y-%m-%d %H:%M")
                    end_time = (current_datatime + timedelta(minutes=End_time[i_1])).strftime("%Y-%m-%d %H:%M")
                    routing = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['工艺路线']
                    opencard = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['开卡标记']
                    process_times = compute_process_times(json_dict, routing, start_time, end_time, opencard)
                    count += 1
                    orderDict[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']] = tempDict
                    orderDict_1[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']] = copy.deepcopy(tempDict)
                    orderDict_1[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']].update(process_times)
                    tempMachineDict[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']] = orderDict[
                        job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']]
                else:
                    pt = 0
                    locked_order_list = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作锁定顺序']
                    if len(locked_order_list) > 1:
                        sorted_locked_order = sorted(range(len(locked_order_list)),
                                                     key=lambda i1: locked_order_list[i1])
                        for job_index in sorted_locked_order:
                            # print("job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单']", job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'])
                            tempDict["CooperativeNumber"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0][
                                '合作序号']
                            tempDict["MachineCapacity"] = int(
                                job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型'])
                            tempDict["ColourNumber"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['色号']
                            tempDict["Color"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['深浅色']
                            tempDict["OrderId"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][
                                job_index]
                            tempDict["MachineId"] = machine_id_dict[i]
                            tempDict["ProductionSequence"] = count
                            tempDict["OrderStatus"] = "已排产"
                            tempDict["StartTime"] = (
                                    current_datatime + timedelta(minutes=Start_time[i_1] + pt)).strftime(
                                "%Y-%m-%d %H:%M")
                            tempDict["EndTime"] = (current_datatime + timedelta(minutes=Start_time[i_1] +
                                                                                        job_message_list[
                                                                                            Machine.assigned_task[i_1][
                                                                                                0] - 1][0]['合作染程用时'][
                                                                                            job_index] + pt)).strftime(
                                "%Y-%m-%d %H:%M")
                            # routing = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['工艺路线']
                            start_time = (current_datatime + timedelta(minutes=Start_time[i_1])).strftime(
                                "%Y-%m-%d %H:%M")
                            end_time = (current_datatime + timedelta(minutes=End_time[i_1])).strftime("%Y-%m-%d %H:%M")
                            routing = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['工艺路线']
                            opencard = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['开卡标记']
                            process_times = compute_process_times(json_dict, routing, start_time, end_time, opencard)

                            pt += job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时'][job_index] + \
                                  switching_time[Machine.assigned_task[i_1][0] - 1]
                            count += 1
                            temp_tempDict = copy.deepcopy(tempDict)
                            orderDict[
                                job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][
                                    job_index]] = temp_tempDict
                            orderDict_1[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']] = copy.deepcopy(temp_tempDict)
                            orderDict_1[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']].update(
                                process_times)
                            tempMachineDict[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][job_index]] = \
                                orderDict[
                                    job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][job_index]]
                            # print("tempMachineDict", tempMachineDict)
                    else:
                        for job_index in range(len(job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'])):
                            # print("job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单']", job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'])
                            tempDict["CooperativeNumber"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0][
                                '合作序号']
                            tempDict["MachineCapacity"] = int(
                                job_message_list[Machine.assigned_task[i_1][0] - 1][0]['缸型'])
                            tempDict["ColourNumber"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['色号']
                            tempDict["Color"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['深浅色']
                            tempDict["OrderId"] = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][
                                job_index]
                            tempDict["MachineId"] = machine_id_dict[i]
                            tempDict["ProductionSequence"] = count
                            tempDict["OrderStatus"] = "已排产"
                            tempDict["StartTime"] = (
                                    current_datatime + timedelta(minutes=Start_time[i_1] + pt)).strftime(
                                "%Y-%m-%d %H:%M")
                            tempDict["EndTime"] = (current_datatime + timedelta(minutes=Start_time[i_1] +
                                                                                        job_message_list[
                                                                                            Machine.assigned_task[i_1][
                                                                                                0] - 1][0]['合作染程用时'][
                                                                                            job_index] + pt)).strftime(
                                "%Y-%m-%d %H:%M")
                            start_time = (current_datatime + timedelta(minutes=Start_time[i_1])).strftime(
                                "%Y-%m-%d %H:%M")
                            end_time = (current_datatime + timedelta(minutes=End_time[i_1])).strftime("%Y-%m-%d %H:%M")
                            routing = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['工艺路线']
                            opencard = job_message_list[Machine.assigned_task[i_1][0] - 1][0]['开卡标记']
                            process_times = compute_process_times(json_dict, routing, start_time, end_time, opencard)
                            pt += job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作染程用时'][job_index] + \
                                  switching_time[Machine.assigned_task[i_1][0] - 1]
                            count += 1
                            temp_tempDict = copy.deepcopy(tempDict)
                            orderDict[
                                job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][
                                    job_index]] = temp_tempDict
                            orderDict_1[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']] = copy.deepcopy(temp_tempDict)
                            orderDict_1[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['标识号']].update(
                                process_times)
                            tempMachineDict[job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][job_index]] = \
                                orderDict[
                                    job_message_list[Machine.assigned_task[i_1][0] - 1][0]['合作订单'][job_index]]
                            # print("tempMachineDict", tempMachineDict)
            machineDict[machine_id_dict[i]] = {
                "MachineCapacity": json_dict["Factory"][factoryId]["Machine"][machine_id_dict[i]]["MachineClass"],
                "Order": tempMachineDict}
            MachineDict["ByMachine"] = machineDict
    factoryDict = {"ByOrder": orderDict_1}
    print("++++++++++++++++++++++++++++++++++++++++++++++++", len(orderDict))
    factoryDict.update(MachineDict)
    AllDict = {factoryId: factoryDict}
    # with open("output_result.json", "w", encoding="utf-8") as file:
    #     json.dump(AllDict, file, ensure_ascii=False)
    return AllDict

# "Flag":""
# "Message":""
# "Result":AllDict



# # 改进
# def out_put_json(Machines, job_message_list, machine_id_dict, switching_time, json_dict):
#     current_datetime = datetime.now()
#     factoryId = list(json_dict["Factory"].keys())[0]
#     all_dict = {}
#     by_order = {}
#     by_machine = {}
#
#     for i, Machine in enumerate(Machines):
#         if not Machine.assigned_task:
#             continue
#
#         start_times = Machine.O_start
#         end_times = Machine.O_end
#         temp_machine_orders = {}
#         count = 1
#
#         for idx in range(len(end_times)):
#             job_info = job_message_list[Machine.assigned_task[idx][0] - 1][0]
#             is_cooperative = bool(job_info['合作订单'])
#             if not is_cooperative:
#                 order_id = job_info['标识号']
#                 base_info = {
#                     "CooperativeNumber": job_info['合作序号'],
#                     "MachineCapacity": int(job_info['缸型']),
#                     "ColourNumber": job_info['色号'],
#                     "Color": job_info['深浅色'],
#                     "OrderId": order_id,
#                     "MachineId": machine_id_dict[i],
#                     "ProductionSequence": count,
#                     "OrderStatus": "已排产",
#                     "StartTime": (current_datetime + timedelta(minutes=start_times[idx])).strftime("%Y-%m-%d %H:%M"),
#                     "EndTime": (current_datetime + timedelta(minutes=end_times[idx])).strftime("%Y-%m-%d %H:%M"),
#                 }
#
#                 # 工艺时间
#                 routing = job_info['工艺路线']
#                 process_times = compute_process_times(json_dict, routing,
#                                                       base_info["StartTime"],
#                                                       base_info["EndTime"])
#
#                 # 更新 ByOrder（含工艺时间）
#                 order_full = copy.deepcopy(base_info)
#                 order_full.update(process_times)
#                 by_order[order_id] = order_full
#
#                 # 更新 ByMachine（不含工艺时间）
#                 temp_machine_orders[order_id] = base_info
#                 count += 1
#
#             else:
#                 pt = 0
#                 cooperative_order_ids = job_info['合作订单']
#                 coop_time_list = job_info['合作染程用时']
#                 lock_order_list = job_info.get('合作锁定顺序', [])
#
#                 if len(lock_order_list) > 1:
#                     sorted_idx = sorted(range(len(lock_order_list)), key=lambda k: lock_order_list[k])
#                 else:
#                     sorted_idx = range(len(cooperative_order_ids))
#
#                 for j in sorted_idx:
#                     order_id = cooperative_order_ids[j]
#                     start_minute = start_times[idx] + pt
#                     end_minute = start_minute + coop_time_list[j]
#
#                     base_info = {
#                         "CooperativeNumber": job_info['合作序号'],
#                         "MachineCapacity": int(job_info['缸型']),
#                         "ColourNumber": job_info['色号'],
#                         "Color": job_info['深浅色'],
#                         "OrderId": order_id,
#                         "MachineId": machine_id_dict[i],
#                         "ProductionSequence": count,
#                         "OrderStatus": "已排产",
#                         "StartTime": (current_datetime + timedelta(minutes=start_minute)).strftime("%Y-%m-%d %H:%M"),
#                         "EndTime": (current_datetime + timedelta(minutes=end_minute)).strftime("%Y-%m-%d %H:%M"),
#                     }
#
#                     # 工艺时间
#                     routing = job_info['工艺路线']
#                     process_times = compute_process_times(json_dict, routing,
#                                                           base_info["StartTime"],
#                                                           base_info["EndTime"])
#
#                     # 更新 ByOrder（含工艺时间）
#                     order_full = copy.deepcopy(base_info)
#                     order_full.update(process_times)
#                     by_order[order_id] = order_full
#                     # 更新 ByMachine（不含工艺时间）
#                     temp_machine_orders[order_id] = base_info
#                     pt += coop_time_list[j] + switching_time[Machine.assigned_task[idx][0] - 1]
#                     count += 1
#
#         by_machine[machine_id_dict[i]] = {
#             "MachineCapacity": json_dict["Factory"][factoryId]["Machine"][machine_id_dict[i]]["MachineClass"],
#             "Order": temp_machine_orders
#         }
#
#     all_dict[factoryId] = {
#         "ByOrder": by_order,
#         "ByMachine": by_machine
#     }
#
#     with open("output_result.json", "w", encoding="utf-8") as file:
#         json.dump(all_dict, file, ensure_ascii=False, indent=2)
#     return all_dict


def compute_process_times(json_dict, routing_type, dyeing_start_time, dyeing_end_time, opencardm):
    from datetime import timedelta
    from Machine_Distribution_lastest._Time_Axis_Manager import TimeAxisManager
    time_axis_manager = TimeAxisManager(json_dict)
    process_times = {
        "LooseProcessStartTime": None,
        "LooseProcessEndTime": None,
        "TightProcessStartTime": None,
        "TightProcessEndTime": None,
        "WarpingProcessStartTime": None,
        "WarpingProcessEndTime": None,
        "DyeingProcessStartTime": None,
        "DyeingProcessEndTime": None
    }

    # 获取工艺路线步骤
    # routing_steps = json_dict.get("Routing", {}).get(routing_key, {}).get(routing_type, [])
    for i in json_dict["Routing"]:
        routing_steps = json_dict["Routing"].get(i, {}).get(routing_type, []) # 获取该订单工艺路线
    if not routing_steps:
        return process_times

    # 获取染色工序在工艺中的索引
    dyeing_index = None
    for idx, step in enumerate(routing_steps):
        if step.get("WorkCenter", "") in ["色纱染色", "染色轴染色"]:
            dyeing_index = idx
            break

    if dyeing_index is None:
        return process_times

    dyeing_start_time = datetime.strptime(dyeing_start_time, "%Y-%m-%d %H:%M")
    dyeing_end_time = datetime.strptime(dyeing_end_time, "%Y-%m-%d %H:%M")
    # process_times["DyeingProcessEndTime"] = dyeing_end_time#.strftime("%Y-%m-%d %H:%M")

    # 上游推算
    current_start = dyeing_start_time
    # opencardm 是开卡标记
    if opencardm:
        for step in reversed(routing_steps[:dyeing_index]):
            label = step.get("WorkCenter", "")
            if label == "松式络筒":
                process_times["LooseProcessStartTime"] = None
                process_times["LooseProcessEndTime"] = None
            elif label == "紧式络筒":
                process_times["TightProcessStartTime"] = None
                process_times["TightProcessEndTime"] = None
            elif label == "原纱整经":
                process_times["WarpingProcessStartTime"] = None
                process_times["WarpingProcessEndTime"] = None
    else:
        for step in reversed(routing_steps[:dyeing_index]):
            wait_time = int(step.get("StandardWaitingTime", 0) * 60)
            prod_time = int(step.get("WorkCenterDetail", [{}])[0].get("StandardProductionTime", 0) * 60)
            # 无班制班次考虑
            # current_end = current_start - timedelta(minutes=wait_time)
            # current_start = current_end - timedelta(minutes=prod_time)
            # 有班制班次考虑
            current_end_shifted, _ = time_axis_manager.reverse_adjust_for_shift_gap(current_start, wait_time)
            current_start_shifted, _ = time_axis_manager.reverse_adjust_for_shift_gap(current_end_shifted, prod_time)

            label = step.get("WorkCenter", "")
            if label == "松式络筒":
                process_times["LooseProcessStartTime"] = current_start_shifted.strftime("%Y-%m-%d %H:%M")
                process_times["LooseProcessEndTime"] = current_end_shifted.strftime("%Y-%m-%d %H:%M")
            elif label == "紧式络筒":
                process_times["TightProcessStartTime"] = current_start_shifted.strftime("%Y-%m-%d %H:%M")
                process_times["TightProcessEndTime"] = current_end_shifted.strftime("%Y-%m-%d %H:%M")
            elif label == "原纱整经":
                process_times["WarpingProcessStartTime"] = current_start_shifted.strftime("%Y-%m-%d %H:%M")
                process_times["WarpingProcessEndTime"] = current_end_shifted.strftime("%Y-%m-%d %H:%M")
            current_start = current_start_shifted

    # 下游推算
    current_start = dyeing_end_time
    for step in routing_steps[dyeing_index + 1:]:
        wait_time = int(step.get("StandardWaitingTime", 0) * 60)
        # wait_time = 120
        prod_time = int(step.get("WorkCenterDetail", [{}])[0].get("StandardProductionTime", 0) * 60)
        # current_start += timedelta(minutes=wait_time)
        # current_end = current_start + timedelta(minutes=prod_time)
        current_start_shifted, _ = time_axis_manager.adjust_for_shift_gap(current_start, wait_time)
        current_end_shifted, _ = time_axis_manager.adjust_for_shift_gap(current_start_shifted, prod_time)

        label = step.get("WorkCenter", "")
        if label == "松式络筒":
            process_times["LooseProcessStartTime"] = current_start_shifted.strftime("%Y-%m-%d %H:%M")
            process_times["LooseProcessEndTime"] = current_end_shifted.strftime("%Y-%m-%d %H:%M")
        elif label == "紧式络筒":
            process_times["TightProcessStartTime"] = current_start_shifted.strftime("%Y-%m-%d %H:%M")
            process_times["TightProcessEndTime"] = current_end_shifted.strftime("%Y-%m-%d %H:%M")
        elif label == "色纱整经":
            process_times["DyeingProcessStartTime"] = current_start_shifted.strftime("%Y-%m-%d %H:%M")
            process_times["DyeingProcessEndTime"] = current_end_shifted.strftime("%Y-%m-%d %H:%M")
        # current_start = current_end
        current_start = current_end_shifted
    return process_times


# def dyeing_main(Json):
#     json_dict = json.loads(Json)
#     # json_dict.decode('utf-8')
#     # json_dict = input_fun.open_json("20250806.json")
#     g = GA(json_dict)
#     result = g.main()
#     # print(result)
#     return result


# dyeing_main(0)

# if __name__ == '__main__':
#     # # from Data_Extraction_from_Excel import Processing_time, J, M_num, J_num, O_num, Priority, new_job_dict, secondary_resource
#     # # from pa_main import Processing_time, J, M_num, J_num, O_num, Priority, new_job_dict, secondary_resource, Color_list, \
#     # #     color_machine_dict, Machine_dict, switching_time, json_dict, Locked_job
#     #
#     # # from pa_main_all import Processing_time, J, M_num, J_num, O_num, Priority, new_job_dict, secondary_resource, Color_list, color_machine_dict
#     # # from pa_test_0322 import Processing_time, J, M_num, J_num, O_num, Priority, new_job_dict, Color_list, color_machine_dict
#     # start = time.time()
#     # g = GA()
#     # result = g.main(Processing_time, J, M_num, J_num, O_num, Priority)
#     # print(result)
#     # # result_02 = g.acquire_condition(result, 10, secondary_resource)
#     # # result_with_condition = result_02[0]
#     # # remain_secondary_resource = result_02[1]
#     # # machine_start_time = result_02[2]
#     # # print(result_with_condition)
#     # # print("remain_secondary_resource", remain_secondary_resource)
#     # # for lst in result_with_condition:
#     # #     if lst[-1] == '生产中':
#     # #         print(lst)
#     # # print("machine_start_time", machine_start_time)
#     #
#     # # g.NSGA2_main(Processing_time, J, M_num, J_num, O_num, Priority)
#     # end = time.time()
#     # print("时间 = ", end - start)
#     # json_dict = json.loads(json)
#     json_dict = input_fun.open_json("222.json")
#     g = GA(json_dict)
#     g.main()
