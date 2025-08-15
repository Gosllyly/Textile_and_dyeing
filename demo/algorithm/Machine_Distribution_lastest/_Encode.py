import numpy as np
import random


class Encode:  # 生成CHS1
    def __init__(self, Matrix, Pop_size, J, J_num, M_num, job_message):
        self.Matrix = Matrix  # 工件各工序对应各机器加工时间矩阵
        self.RS_num = Pop_size  # 随机选择初始化
        self.J = J  # 各工件对应的工序数
        self.J_num = J_num  # 工件数
        self.M_num = M_num  # 机器数
        self.CHS = []
        self.Len_Chromo = 0
        for i in J.values():  # 计算总工序（各工件工序和）
            self.Len_Chromo += i
        self.job_message = job_message

    # 生成工序准备的部分
    def OS_List(self):
        OS_list = []
        for k, v in self.J.items():  # k:key  v:value
            OS_add = [k - 1 for j in range(v)]
            OS_list.extend(OS_add)
        return OS_list

    # 生成初始化矩阵
    def CHS_Matrix(self, C_num):
        return np.zeros([C_num, self.Len_Chromo], dtype=int)  # C_num行，Len_Chromo列

    def Random_initial(self, log):
        # log.write(f"编码阶段 \n\n")
        MS = self.CHS_Matrix(self.RS_num)
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.RS_num)
        for i in range(self.RS_num):
            random.shuffle(OS_list)  # 生成工序排序部分
            OS_chs = OS_list
            OS[i] = np.array(OS_chs)  # 填入OS，代表工序
            job_list = [i_1 for i_1 in range(self.J_num)]
            job_operation = 0
            for job in job_list:
                # print(self.job_message[job][0]['标识号'])
                # log.write(f"编码 当前处理订单: {self.job_message[job][0]['标识号']}\n")
                job_processing_time = np.array(self.Matrix[job])  # 第一个工件及其对应工序的加工时间
                try:
                    for j in range(len(job_processing_time)):  # 从工件的第一个工序开始选择机器
                        operation_processing_time = np.array(job_processing_time[j])
                        can_use_machine_idx = []  # 存放可用机器索引（可用索引）
                        Site = 0  # 标记
                        for k in range(len(operation_processing_time)):  # 每道工序可使用的机器以及机器的加工时间
                            if operation_processing_time[k] == 9999:  # 确定可加工该工序的机器
                                pass
                            else:
                                can_use_machine_idx.append(Site)
                                Site += 1
                        # print("can_use_machine_idx =", can_use_machine_idx, job)
                        Machine_Index_add = random.choice(can_use_machine_idx)  # 随机选择机器（染缸）
                        MS[i][job_operation] = MS[i][job_operation] + Machine_Index_add

                        job_operation += 1
                except Exception as e:
                    # print(e)
                    print("处理订单 ", self.job_message[job][0]['标识号'], " 出错，错误信息：", e, " 编码阶段")
                    log.close()
                    break
            # log.write(f"编码阶段完成\n\n")
        CHS = np.hstack((MS, OS))
        return CHS

