import random
from datetime import datetime, timedelta
import Machine_Distribution_lastest.input_fun as input_fun
import copy
import os


# json_dict = input_fun.open_json("20250310.json")


def process_json(json_dict):  # 删除执行中
    pop_json_dict = copy.deepcopy(json_dict)
    for i in json_dict["Order"].keys():  # 遍历工厂
        temp = []
        for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
            order_state = json_dict["Order"][i][j]["OrderStatus"]
            if order_state != '执行中' and order_state != '已完工':
                temp.append(json_dict["Order"][i][j])
        pop_json_dict["Order"][i] = temp
        # if pop_json_dict == json_dict:
        #     print("完全一样")
    return pop_json_dict, json_dict


def manage_data(json_dict1):
    current_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
    log_message = open('Data_Prepare_' + current_time + '.txt', 'w')
    log_message.write(f"数据准备开始 \n\n")
    json_dict = process_json(json_dict1)[0]  # 剔除执行中
    all_json_dict = process_json(json_dict1)[1]  # 全部的
    Old_Job_dict = input_fun.Get_New_Job_dict(json_dict)  # 未考虑合作序号的订单列表
    print("未考虑合作之前订单数量", len(Old_Job_dict))
    new_job_dict = input_fun.organize_dict(Old_Job_dict)  # 考虑合作序号的订单列表
    new_job_list = list(new_job_dict.values())
    # print("+++++++++++++++++++++++++",new_job_list[440])
    print("未考虑合作之后订单数量", len(new_job_dict))
    J_num = input_fun.Get_Job_num(new_job_dict)  # 订单数量
    jobIndex_to_orderID_dict = input_fun.Get_jobIndex_to_orderID(new_job_dict)  # 订单标识对应字典
    J = input_fun.Get_Job_dict(new_job_dict)  # 订单字典
    O_num = input_fun.Get_Operation_num(new_job_dict)  # 工序数量
    M_num = input_fun.Get_Machine_num(json_dict)  # 机器数量
    Priority = input_fun.Get_Job_Priority(new_job_dict)  # 优先级字典
    Processing_time = input_fun.Get_Processing_Time(new_job_dict, M_num, json_dict)  # 时间矩阵
    # print("Processing_time", Processing_time)
    secondary_resource = input_fun.Get_Secondary_Resource(json_dict)  # 副资源组对应数量
    switching_time = input_fun.Get_Switch_time(new_job_dict)  # 切换时间
    switching_cost = input_fun.Get_Switching_cost(json_dict)  # 切换成本
    Color_list = input_fun.Get_Color_list(json_dict)  # 颜色列表
    category = input_fun.Get_Category(new_job_dict, json_dict)  # 订单颜色分类
    axle_resource_num = input_fun.Get_axle_resource(json_dict)  # 获取轴数
    tempresult = input_fun.Get_machine_id_dict(json_dict)
    machine_list = tempresult[0]  # 副资源组对应机器
    srn_type_dict = tempresult[1]  # 副资源数量字典
    Machine_dict = input_fun.Get_Machine_dict(json_dict)  # 索引机器号对应字典
    color_machine_dict = input_fun.Get_color_machine_dict(json_dict)  # 获取机器颜色信息
    Locked_job = input_fun.Get_locked_state(new_job_dict)  # 获取锁定的订单和相应的机器 [0, '201']
    continue_job_temp = input_fun.Get_continue_order(new_job_dict)  # 获取续作的订单和相应的机器 [0, '201']
    machine_message = input_fun.get_machine_message(json_dict)  # 获取机器信息
    # print(new_job_dict)
    # print("dddd", list(new_job_dict.values())[443])
    continue_job = change_continue_job(continue_job_temp, Machine_dict, Processing_time, log_message, new_job_list)
    locked_job = change_locked_state_job(Locked_job, Machine_dict, Processing_time, log_message, new_job_list)
    print("continue_job_temp, continue_job", continue_job_temp, continue_job)
    print("Locked_job", Locked_job)
    print("locked_job", locked_job)
    start_time = input_fun.Get_machine_start_time(all_json_dict, M_num, Machine_dict)  # 获取机器开始时间
    locked_job_order_on_machine = input_fun.extract_lock_job_and_order(new_job_dict, json_dict)  # 获取信息 {'201':[[12,1], [13,2], [14,3]]} 121314锁定生产，顺序分别为123
    stop_machine = input_fun.get_stop_machine(json_dict)  # 获取异常机器信息
    machine_pre_color = input_fun.get_machine_pre_color(json_dict)  # 获取各个机器的上个状态的颜色
    # machine_class_dict = input_fun.machine_type_num2(machine_message)
    machine_class_dict = input_fun.machine_type_num3(machine_message)  # 机器分类信息？
    machine_type = machine_class_dict[0]
    machine_type_white = machine_class_dict[1]
    average_quantity = input_fun.get_average_quantity(json_dict)  # 获取均值信息
    print("start_time", start_time)
    # print("M_num", M_num)
    # print(Processing_time[0][0])
    print("订单数量：", J_num)
    # print("订单序号和OerderID的对应关系：", jobIndex_to_orderID_dict)
    print("Job_dic:", J)
    print("O_num", O_num)
    print("Machine_num:", M_num)
    # print("priority:", Priority)
    # print("Processing_Time", Processing_time)
    # print("33333333333333333333", Processing_time[513][0])
    print("second_resource_num:", secondary_resource)
    # print("Old_Job_dict", len(Old_Job_dict), Old_Job_dict)
    print("New_Job_dict", len(new_job_dict), new_job_dict)
    print("==================", list(new_job_dict.values()))
    print("Switching_time", switching_time)
    print("Switching_cost", switching_cost)
    print("Color_list", Color_list)
    print("category:", category)
    print("axle_resource", axle_resource_num)
    print("color_machine_dict", color_machine_dict)
    print("machine_list", machine_list)
    print("srn_type_dict", srn_type_dict)
    print("Machine_dict", Machine_dict)
    print("machine_message", machine_message)
    print("locked_job_order", locked_job_order_on_machine)
    print("stop_machine", stop_machine)
    print("machine_pre_color", machine_pre_color)
    # print("machine_class_dict", machine_class_dict)
    print("machine_type", machine_type)
    print("machine_type_white", machine_type_white)
    print("average_quantity", average_quantity)
    # log_message.write(f"数据准备完成 \n\n")
    log_message.close()
    log_file_path = 'Data_Prepare_' + current_time + '.txt'
    os.remove(log_file_path)
    return J_num, jobIndex_to_orderID_dict, J, O_num, M_num, Priority, Processing_time, secondary_resource, \
           Old_Job_dict, new_job_dict, switching_time, switching_cost, Color_list, category, axle_resource_num, \
           color_machine_dict, machine_list, srn_type_dict, Machine_dict, Locked_job, continue_job, start_time, \
           locked_job_order_on_machine, machine_message, locked_job, stop_machine, machine_pre_color, machine_type, \
           machine_type_white, average_quantity

# print("订单数量：", J_num)
# print("订单序号和OerderID的对应关系：", jobIndex_to_orderID_dict)
# print("Job_dic:", J)
# print("O_num", O_num)
# print("Machine_num:", M_num)
# print("priority:", Priority)
# print("Processing_Time", Processing_time)
# print("second_resource_num:", secondary_resource)
# print("Old_Job_dict", Old_Job_dict)
# print("New_Job_dict", new_job_dict)
# print("Switching_time", switching_time)
# print("Switching_cost", switching_cost)
# print("Color_list", Color_list)
# print("category:", category)
# print("axle_resource", axle_resource_num)
# print("color_machine_dict", color_machine_dict)
# print("machine_list", machine_list)
# print("srn_type_dict", srn_type_dict)
# print("Machine_dict", Machine_dict)
#
# # input_fun.priii(json_dict)
#
# Locked_job = input_fun.Get_locked_state(json_dict)
# print("locked_job", Locked_job)


def change_locked_state_job(locked_job, machine_dict, pt, log, job_list):
    """
    输出锁定订单的订单id，锁定的机器id，用于调整染色体
    :param locked_job: 存放锁定的订单和相应的机器 [[0, '201']]
    :param machine_dict: {0: '514', 1: '515', 2: '905', 3: '916', 4: '907', 5: '908', 6: '815', 7: '509', 8
    :param pt: 时间矩阵
    :return: new_lock_job = []  # 二维列表，存放作业索引，固定机器的可用机器索引
    """
    new_lock_job = []  # 二维列表，存放作业索引，固定机器的可用机器索引
    log.write(f"锁定订单调整机器阶段 \n\n")
    for i in range(len(locked_job)):
        job = locked_job[i][0]  # 作业索引0123
        machine_id = locked_job[i][1]  # 机器id 如'201'
        machine_real_idx = None
        log.write(f"锁定订单调整机器阶段 当前处理订单为: {job_list[job][0]['标识号']}\n")
        try:
            for key, val in machine_dict.items():
                if val == machine_id:
                    machine_real_idx = key  # 真实索引 0-94
                    break
            job_pt = pt[job][0]  # 该订单在所有机器上的生产时间
            # print(job, machine_id)
            can_use_machine_list = [index for index, value in enumerate(job_pt) if value != 9999]  # 所有可用机器的实际索引
            # print(can_use_machine_list)
            new_machine_index = can_use_machine_list.index(machine_real_idx)  # 固定机器在其可用机器列表中的索引
            new_lock_job.append([job, new_machine_index])
        except Exception as e:
            print("处理订单 ", job_list[job][0]['标识号'], " 出错，错误信息：", e, " 锁定订单调整机器阶段")
            log.close()
            break
    # log.write(f"锁定订单调整机器阶段完成 \n\n")
    return new_lock_job


def change_continue_job(continue_job, machine_dict, pt, log, job_list):
    """
    输出锁定订单的订单id，锁定的机器id，用于调整染色体
    :param continue_job: 存放锁定的订单和相应的机器 [[0, '201']]
    :param machine_dict: {0: '514', 1: '515', 2: '905', 3: '916', 4: '907', 5: '908', 6: '815', 7: '509', 8
    :param pt: 时间矩阵
    :return:
    """
    log.write(f"续作订单调整机器阶段 \n\n")
    new_continue_job = []  # 二维列表，存放作业索引，固定机器的可用机器索引
    for i in range(len(continue_job)):
        job = continue_job[i][0]  # 作业索引0123
        machine_id = continue_job[i][1]  # 机器id 如'201'
        log.write(f"续作订单调整机器阶段 当前处理订单为: {job_list[job][0]['标识号']}\n")
        # print(job, machine_id)
        try:
            machine_real_idx = None
            for key, val in machine_dict.items():
                if val == machine_id:
                    machine_real_idx = key
                    break
            job_pt = pt[job][0]  # 该订单在所有机器上的生产时间
            can_use_machine_list = [index for index, value in enumerate(job_pt) if value != 9999]
            # print(can_use_machine_list)  # 所有可用机器的实际索引
            # new_machine_index = can_use_machine_list.index(machine_real_idx)  # 固定机器在其可用机器列表中的索引
            # new_continue_job.append([job, new_machine_index])
            if job_pt[machine_real_idx] != 9999:
                new_machine_index = can_use_machine_list.index(machine_real_idx)  # 固定机器在其可用机器列表中的索引
                new_continue_job.append([job, new_machine_index])
            # else:  # 续作机器异常，不能使用，随机选择另外一个机器
            #     new_machine_index = random.randint(0, len(can_use_machine_list)-1)
            #     new_continue_job.append([job, new_machine_index])
        except Exception as e:
            print("处理订单 ", job_list[job][0]['标识号'], " 出错，错误信息：", e, " 续作订单调整机器阶段")
            log.close()
            break
    # log.write(f"续作订单调整机器阶段完成 \n\n")
    return new_continue_job


# json_dict = input_fun.open_json("2025051914.json")
# manage_data(json_dict)
