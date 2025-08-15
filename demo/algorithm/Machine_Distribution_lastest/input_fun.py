import json
import copy
from datetime import datetime, timedelta

# from Machine_Distribution_lastest._Time_Axis_Manager import TimeAxisManager


def open_json(file):
    # with open(file, 'r', encoding='utf-8-sig') as json_file:
    with open(file, 'r', encoding='gbk') as json_file:
        json_dict = json.load(json_file)
    return json_dict

# def open_json(file):
#     try:
#         with open(file, 'r', encoding='utf-8-sig') as json_file:
#             # 尝试解析文件内容
#             json_dict = json.load(json_file)
#         return json_dict
#     except json.JSONDecodeError as e:
#         # 捕获并报告 JSON 解码错误的详细信息
#         print(f"JSON Decode Error: {e.msg} at line {e.lineno} column {e.colno}")
#         raise
#     except Exception as e:
#         # 捕获其他可能的异常
#         print(f"An error occurred: {str(e)}")
#         raise



def Get_Job_num(New_Job_dict):
    """
    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :return Job_num: 订单数量(去掉相同订单编号后的)
    """
    Job_num = len(New_Job_dict)
    return Job_num


def Get_jobIndex_to_orderID(New_Job_dict):
    """
    将订单序号与订单编号对应起来，输出一个字典
    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :return: 字典，键是订单序号，值是订单编号
    """
    jobIndex_to_orderID_dict = {}
    idx = 1
    for key in New_Job_dict.keys():
        jobIndex_to_orderID_dict[idx] = key
        idx += 1
    return jobIndex_to_orderID_dict


def Get_Job_dict(New_Job_dict):
    """
    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :param Job_num: 订单数量
    :return: 订单工序数量的字典
    """
    # 目前所有订单工序默认为1
    Job_dict = {}
    for i in range(1, len(New_Job_dict) + 1):
        Job_dict[i] = 1
    return Job_dict


def Get_Machine_num(json_dict):
    """

    :param json_dict:
    :return: 机器的数量
    """
    Machine_num = 0
    for i in json_dict["Factory"].keys():
        for j in json_dict["Factory"][i]["Machine"].keys():
            Machine_num += 1
    return Machine_num


def Get_Operation_num(New_Job_dict):
    """
    由于各订单工序数量为1，则操作总数等于订单数量
    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :return:操作数量
    """
    Job_num = len(New_Job_dict)
    Operation_num = Job_num
    return Operation_num


def Get_Job_Priority(New_Job_dict):
    """

    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :return: 订单优先级
    """
    Job_Priority = {}
    jobIndex_to_orderID_dict = {}  # 序号和订单编号对应的字典
    idx = 1
    for key in New_Job_dict.keys():
        jobIndex_to_orderID_dict[idx] = key
        idx += 1

    for i in range(1, len(New_Job_dict) + 1):
        Job_Priority[i] = New_Job_dict[jobIndex_to_orderID_dict[i]][0]["优先级"]
    return Job_Priority


def Get_machine_type(json_dict):
    """

    :param json_dict:
    :return:
    """
    stop_machine = get_stop_machine(json_dict)
    stop_machine_index = [i[1] for i in stop_machine]  # 异常暂停机器的机器号
    # print("stop_machine_index", stop_machine_index)
    for i in json_dict['Factory'].keys():  # 遍历工厂
        # machine_message = json_dict["Factory"][i]["Machine"]
        second_resource_message = json_dict["Factory"][i]["SecondaryResource"]
        yarn_message = second_resource_message["YarnFrame"]
        axle_message = second_resource_message["AxleFrame"]
        yarn_machine_id = {"纱架": [], "蚕丝架": []}
        for key, value in yarn_message.items():
            for key2, value2 in value.items():
                # print(value2["Machine"])
                yarn_machine_id[key].extend(value2["Machine"])
        # for machine_id in yarn_machine_capacity:
        #     machine_capa = machine_message[machine_id]["MachineClass"]
        axle_machine_id = {"S": [], "M": [], "L": [], "Y": [], "G": []}
        for key, value in axle_message.items():
            for key2, value2 in value.items():
                axle_machine_id[key].extend(value2["Machine"])

        for key, values in yarn_machine_id.items():
            values = [element for element in values if element not in stop_machine_index]
            yarn_machine_id[key] = values
        for key, values in axle_machine_id.items():
            values = [element for element in values if element not in stop_machine_index]
            axle_machine_id[key] = values
        # print("yarn_machine_id", len(yarn_machine_id), yarn_machine_id)
        # print("axle_machine_id", len(axle_machine_id), axle_machine_id)
        return yarn_machine_id, axle_machine_id  # 机器号


# def Get_Processing_Time(new_Job_dict,machine_num,json_dict):
#     Processing_Time=[]
#     for i in json_dict['Factory'].keys():  # 遍历工厂
#         machine_message = json_dict["Factory"][i]["Machine"]
#         all_machine = []
#         for machine, v in machine_message.items():
#             all_machine.append(machine)
#         # print("AAA", len(all_machine), all_machine)
#         job_time = [9999 for _ in range(machine_num)]
#         for job_idx in range(len(new_Job_dict)):
#             Processing_Time.append([job_time[:]])
#         for key, value in enumerate(new_Job_dict.values()):
#             machine_capacity = value[0]['缸型']
#             machine_list = []  # 可用机器索引
#             for key2, value2 in machine_message.items():
#                 if value2['MachineClass'] == machine_capacity:
#                     machine_list.append(all_machine.index(key2))
#             for machine_idx in machine_list:
#                 Processing_Time[key][0][machine_idx]=value[0]["染程用时"]
#     return Processing_Time

# def judge_unavailable_machine(json_dict):
#     """
#     根据荧光性，去除不可用机器，返回每一个订单和其不可用机器
#     :param json_dict:
#     :return:
#     """
#     machine_limit = []  # 存放每一个订单不能选择的机器，二维列表，存索引号，都能用则存放一个空列表
#     yarn_machine_id, axle_machine_id = Get_machine_type(json_dict)
#     for i in json_dict["Order"].keys():  # 遍历工厂
#         machine_message = json_dict["Factory"][i]["Machine"]
#         all_machine = []
#         for machine, v in machine_message.items():
#             all_machine.append(machine)
#         for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
#             temp = []  # 存放该订单不能选择的机器
#             whether_fluoresce = json_dict["Order"][i][j]["JudgeFluorescence"]  # True为不能沾染荧光
#             job_type = json_dict["Order"][i][j]["DyeType"]  # 染纱/染轴？
#             machine_capacity = json_dict["Order"][i][j]["MachineCapacity"]  # 订单缸型选择
#             if whether_fluoresce:  # 为True
#                 if job_type == '染纱':
#                     for machine_id in yarn_machine_id:  # 机器号
#                         if machine_message[machine_id]["MachineClass"] == machine_capacity \
#                                 and machine_message[machine_id]["Color"][0] == "增白":
#                             temp.append(all_machine.index(machine_id))
#                 else:
#                     for machine_id in axle_machine_id:  # 机器号
#                         if machine_message[machine_id]["MachineClass"] == machine_capacity \
#                                 and machine_message[machine_id]["Color"][0] == "增白":
#                             temp.append(all_machine.index(machine_id))
#             machine_limit.append(temp)
#     return machine_limit


def judge_unavailable_machine(new_job_dict, json_dict):
    """
    根据荧光性，去除不可用机器，返回每一个订单和其不可用机器
    :param json_dict:
    :return:
    """
    machine_limit = []  # 存放每一个订单不能选择的机器，二维列表，存索引号，都能用则存放一个空列表
    yarn_machine_id, axle_machine_id = Get_machine_type(json_dict)
    for i in json_dict["Order"].keys():  # 遍历工厂
        machine_message = json_dict["Factory"][i]["Machine"]
        all_machine = []
        for machine, v in machine_message.items():
            all_machine.append(machine)
        new_job_list = list(new_job_dict.values())
        for j in range(len(new_job_list)):  # 遍历各工厂对应的订单列表
            temp = []  # 存放该订单不能选择的机器
            whether_fluoresce = new_job_list[j][0]["荧光"]  # True为不能沾染荧光
            job_type = new_job_list[j][0]["染色类型"]  # 染纱/染轴？
            used_axle = new_job_list[j][0]["轴型"]  # 纱架/蚕丝架/S...
            machine_capacity = new_job_list[j][0]["缸型"]  # 订单缸型选择
            if whether_fluoresce:  # 为True
                if job_type == '染纱':
                    for machine_id in yarn_machine_id[used_axle]:  # 机器号
                        if machine_message[machine_id]["Color"]:
                            if machine_message[machine_id]["MachineClass"] == machine_capacity \
                                    and machine_message[machine_id]["Color"][0] == "增白":
                                temp.append(all_machine.index(machine_id))
                else:
                    for machine_id in axle_machine_id[used_axle]:  # 机器号
                        if machine_message[machine_id]["Color"]:
                            if machine_message[machine_id]["MachineClass"] == machine_capacity \
                                    and machine_message[machine_id]["Color"][0] == "增白":
                                temp.append(all_machine.index(machine_id))
            machine_limit.append(temp)
    return machine_limit


def Get_Processing_Time(new_Job_dict, machine_num, json_dict):
    # print("len(new_job_dict)", len(new_Job_dict))
    yarn_machine_id, axle_machine_id = Get_machine_type(json_dict)
    Processing_Time = []
    for i in json_dict['Factory'].keys():  # 遍历工厂
        machine_message = json_dict["Factory"][i]["Machine"]
        all_machine = []
        for machine, v in machine_message.items():
            all_machine.append(machine)
        # print("AAA", len(all_machine), all_machine)
        job_time = [9999 for _ in range(machine_num)]
        for job_idx in range(len(new_Job_dict)):
            Processing_Time.append([job_time[:]])
        for key, value in enumerate(new_Job_dict.values()):
            machine_capacity = value[0]['缸型']
            job_type = value[0]['染色类型']
            used_axle = value[0]['轴型']
            if job_type == '染纱':
                machine_list = []  # 可用机器索引
                for key2 in yarn_machine_id[used_axle]:
                    if machine_message[key2]['MachineClass'] == machine_capacity:
                    # if 0 <= int(machine_message[key2]['MachineClass']) - int(machine_capacity) <= 2:
                        machine_list.append(all_machine.index(key2))
                for machine_idx in machine_list:
                    Processing_Time[key][0][machine_idx] = value[0]["染程用时"]
            else:
                machine_list = []  # 可用机器索引
                for key2 in axle_machine_id[used_axle]:
                    # print(machine_message[key2]['MachineClass'], machine_capacity,
                    #       type(machine_message[key2]['MachineClass']), type(machine_capacity))
                    if machine_message[key2]['MachineClass'] == machine_capacity:
                    # if 0 <= int(machine_message[key2]['MachineClass']) - int(machine_capacity) <= 2:
                        machine_list.append(all_machine.index(key2))
                    # print("machine_list", machine_list)
                for machine_idx in machine_list:
                    Processing_Time[key][0][machine_idx] = value[0]["染程用时"]
    # 修改Processing_Time去除不可用机器 ####################
    # machine_limit = judge_unavailable_machine(json_dict)
    machine_limit = judge_unavailable_machine(new_Job_dict, json_dict)
    for i in range(len(machine_limit)):
        job = i
        limited_machines = machine_limit[i]  # 受限制的机器（荧光性）
        for limit_machine_index in limited_machines:
            Processing_Time[job][0][limit_machine_index] = 9999
    # 修改异常停机机器可用性
    stop_machine_list = get_stop_machine(json_dict)
    for job in range(len(Processing_Time)):
        for stop_machine in stop_machine_list:
            Processing_Time[job][0][stop_machine[0]] = 9999
    # 续作订单固定机器
    # continue_job = Get_continue_order(new_Job_dict)
    # for job_machine in continue_job:
    #     job = job_machine[0]
    #     machine = all_machine.index(job_machine[1])
    #     if [machine, job_machine[1]] not in stop_machine_list:
    #         for i in range(len(Processing_Time[job][0])):
    #             if i != machine:
    #                 Processing_Time[job][0][i] = 9999
    return Processing_Time


def Get_New_Job_dict(json_dict):
    '''
    该函数的输出需要传入organize_dict（）函数
    :param json_dict:
    :return New_Job_dict:订单对应的属性,
    '''
    # New_Job_dict = {}  # 需要移动至下方，为多工厂准备数据结构--zl
    # OrderId_list = []  # 二维列表，行数是订单数量，列数是该订单对应的合作订单数量
    # 获取切换时间
    YarnSwitchTime = json_dict["Rule"]["YarnSwitchTime"]  # 染纱切换时间
    AxleSwitchTime = json_dict["Rule"]["AxleSwitchTime"]  # 染轴切换时间
    SwitchTime = 0  # 初始化切换时间
    Type = 0
    axle_number = 0
    # New_Job_dict赋值
    for i in json_dict["Order"].keys():  # 遍历工厂
        New_Job_dict = {}
        OrderId_list = []  # 二维列表，行数是订单数量，列数是该订单对应的合作订单数量
        for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
            is_exsit = 0  # 判断该订单是否已经记录过
            for k in range(len(OrderId_list)):  # 判断是否存在相同订单编号的订单
                if OrderId_list[k][0] == json_dict["Order"][i][j]["OrderId"]:
                    is_exsit = 1
                    # 若存在合作订单，则增加一个订单编号
                    OrderId_list[k].append(json_dict["Order"][i][j]["OrderId"])
            if is_exsit == 0:  # 若不存在相同编号的订单，则没有合作订单
                OrderId_list.append([])  # 增加一个空列表，该列表的长度为合作订单的数量
                # 在空列表中增加OrderId
                OrderId_list[len(OrderId_list) - 1].append(json_dict["Order"][i][j]["OrderId"])
                # 在New_Job_dict={}加入该订单属性
                # 根据漂染类型，更新切换时间
                if json_dict["Order"][i][j]["DyeType"] == "染纱":
                    SwitchTime = YarnSwitchTime
                    Type = "FrameType"
                    axle_number = 0
                elif json_dict["Order"][i][j]["DyeType"] == "染轴":
                    SwitchTime = AxleSwitchTime
                    Type = "Axle"
                    axle_number = json_dict["Order"][i][j]["AxleNumber"]
                # 染程用时有合作序号的要翻倍
                New_Job_dict[json_dict["Order"][i][j]["OrderId"]] = [
                    {"染色类型": json_dict["Order"][i][j]["DyeType"],
                     "标识号": json_dict["Order"][i][j]["OrderId"],
                     "缸型": json_dict["Order"][i][j]["MachineCapacity"],
                     "合作序号": json_dict["Order"][i][j]["CooperativeNumber"],
                     "优先级": json_dict["Order"][i][j]["Priority"],
                     "深浅色": json_dict["Order"][i][j]["Color"],
                     "染程用时": json_dict["Order"][i][j]["ProcessingTime"],
                     "切换时间": SwitchTime,
                     "色号": json_dict["Order"][i][j]["ColourNumber"],
                     "轴型": json_dict["Order"][i][j][Type],
                     "根数": 1,
                     "用轴数量": axle_number,
                     "生产物流号": json_dict["Order"][i][j]["ProductionNumber"],
                     "续作机器": json_dict["Order"][i][j]["OriginalMachineId"],
                     "锁定状态": json_dict["Order"][i][j]["LockedState"],
                     "锁定机器": json_dict["Order"][i][j]["MachineId"],
                     "锁定顺序": int(json_dict["Order"][i][j]["LockJobOrder"]),
                     "荧光": json_dict["Order"][i][j]["JudgeFluorescence"],
                     # 工艺路线
                     "工艺路线": json_dict["Order"][i][j]["Routing"],
                     # 交期
                     "计划漂染完成日期": json_dict["Order"][i][j]["DyeDeliveryDate"],
                     # 锅号
                     "锅号": json_dict["Order"][i][j]["Potno"],
                     # 开卡标记
                     "开卡标记": json_dict["Order"][i][j]["OpenCardMark"],
                     # 发纱标记
                     "发纱标记": json_dict["Order"][i][j]["HairYarnMark"]
                     }]
    return New_Job_dict


def Get_Secondary_Resource(json_dict):
    """

    :param json_dict:
    :return:副资源组
    """
    second_resource_num = []
    for i in json_dict['Factory'].keys():  # 遍历工厂
        second = json_dict['Factory'][i]['SecondaryResource']
        YarnFrame_dict = second['YarnFrame']
        for key, yarnframe in YarnFrame_dict.items():
            for type, typevalue in yarnframe.items():
                num = typevalue['Number']
                second_resource_num.append(num)

        AxleFrame_dict = second['AxleFrame']
        for key, axleframe in AxleFrame_dict.items():
            for type, typevalue in axleframe.items():
                num = typevalue['Number']
                second_resource_num.append(num)
    return second_resource_num


# def Get_axle_resource(json_dict):
#     axle_resource = []
#     for i in json_dict["Factory"]["341557"]["SecondaryResource"]["Axle"].values():
#         axle_resource.append(i['漂染APS轴数']["Number"])
#     return axle_resource

def Get_axle_resource(json_dict):
    axle_resource = []
    for i in json_dict["Factory"].keys():
        for j in json_dict["Factory"][i]["SecondaryResource"]["Axle"].values():
            axle_resource.append(j['漂染APS轴数']["Number"])
    return axle_resource


def Get_Switch_time(new_Job_dict):
    """
    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :return: 切换时间
    """
    Switching_time = []
    for value in new_Job_dict.values():
        Switching_time.append(value[0]["切换时间"])
    return Switching_time


def Get_Category(New_Job_dict, json_dict):
    """
    :param New_Job_dict:organize_dict（）函数的输出的修改过的New_Job_dict
    :param json_dict:
    :return: 返回一个各颜色对应的订单，最外层索引为颜色索引，内层索引对应的值为订单，该二维列表与Color_list对应
    """
    Color_list = []
    for key in json_dict["Rule"]["SwitchCost"].keys():  # 遍历SwitchCost中的颜色
        Color_list.append(key)

    # 初始化category
    category = []
    for k in range(len(Color_list)):
        category.append([])

    # 找到订单序号与订单ID的对应关系
    jobIndex_to_orderID_dict = {}
    idx = 1
    for key in New_Job_dict.keys():
        jobIndex_to_orderID_dict[idx] = key
        idx += 1
    # 对category赋值
    for i in range(len(Color_list)):  # 遍历颜色列表
        for key in New_Job_dict.keys():  # 遍历New_Job_dict
            if New_Job_dict[key][0]["深浅色"] == Color_list[i]:  # 找到对应的颜色，得到订单ID
                for j in jobIndex_to_orderID_dict.keys():  # 根据订单ID找到订单序号
                    if key == jobIndex_to_orderID_dict[j]:
                        category[i].append(j - 1)  # 在对应颜色列表中增加订单序号
    return category


def Get_Switching_cost(json_dict):
    Switching_cost = []
    for value in json_dict["Rule"]["SwitchCost"].values():
        Switching_cost.append(value)
    return Switching_cost


def Get_Color_list(json_dict):
    """

    :param json_dict:
    :return Color_list: 返回一个颜色列表
    """
    Color_list = []
    for key in json_dict["Rule"]["SwitchCost"].keys():  # 遍历SwitchCost中的颜色
        Color_list.append(key)
    return Color_list


def Get_Non_Continuous_Production(json_dict):
    non_continuous_production = ['深色', '中色', '浅色']
    return non_continuous_production


# def Get_color_machine_dict(json_dict):
#     """
#
#     :param json_dict:
#     :return:
#     """
#     cap = []  # 存放出现的容量
#     color_machine_dict = {}
#     all_machine = []
#     for i in json_dict["Order"].keys():  # 遍历工厂
#         for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
#             ca = json_dict["Order"][i][j]["MachineCapacity"]
#             if ca not in cap:
#                 cap.append(json_dict["Order"][i][j]["MachineCapacity"])
#     for machine_ in range(len(cap)):
#         temp_dict = {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []}
#         machine_capacity = cap[machine_]
#         for i in json_dict["Factory"].keys():
#             for j in json_dict["Factory"][i]["Machine"].keys():
#                 all_machine.append(j)
#                 # print("sss", json_dict["Factory"][i]["Machine"][j])
#                 if json_dict["Factory"][i]["Machine"][j]["MachineClass"] == machine_capacity:
#                     color = json_dict["Factory"][i]["Machine"][j]["Color"][0]  # 循环？？
#                     # print("ddd", color)
#                     temp_dict[color].append(json_dict["Factory"][i]["Machine"][j]["MachineName"])
#         color_machine_dict[machine_capacity] = temp_dict
#     # print("color_machine_dict", color_machine_dict)
#     # print("all_machine", all_machine)
#     mapped_color_machine_dict = {}
#     for key, value in color_machine_dict.items():  # 遍历 color_machine_dict 中的键值对
#         mapped_color_machine_dict[key] = {}
#         for color, machines in value.items():  # 遍历值中的字典
#             mapped_color_machine_dict[key][color] = [all_machine.index(machine) for machine in machines]
#     # print("映射后的 color_machine_dict:", mapped_color_machine_dict)
#     return mapped_color_machine_dict


def Get_color_machine_dict(json_dict):
    """

    :param json_dict:
    :return:
    """
    yarn_machine_id, axle_machine_id = Get_machine_type(json_dict)
    # yarn_machine_id = [value for sublist in yarn_machine_id.values() for value in sublist]
    # axle_machine_id = [value for sublist in axle_machine_id.values() for value in sublist]
    cap = []  # 存放出现的容量
    color_machine_dict = {}
    all_machine = []
    for i in json_dict["Factory"].keys():
        all_machine = list(json_dict["Factory"][i]["Machine"].keys())
    for i in json_dict["Order"].keys():  # 遍历工厂
        for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
            ca = json_dict["Order"][i][j]["MachineCapacity"]
            if ca not in cap:
                cap.append(json_dict["Order"][i][j]["MachineCapacity"])
    for machine_ in range(len(cap)):
        # temp_dict = {'深色': {"染纱":[], "染轴":[]}, '中色': {"染纱":[], "染轴":[]}, '浅色': {"染纱":[], "染轴":[]},
        #              '浅浅': {"染纱":[], "染轴":[]}, '增白': {"染纱":[], "染轴":[]}}
        temp_dict = {"纱架": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []},
                     "蚕丝架": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []},
                     "S": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []},
                     "M": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []},
                     "L": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []},
                     "Y": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []},
                     "G": {'深色': [], '中色': [], '浅色': [], '浅浅': [], '增白': []}}
        machine_capacity = cap[machine_]
        for i in json_dict["Factory"].keys():
            for j in json_dict["Factory"][i]["Machine"].keys():
                # all_machine.append(j)
                if json_dict["Factory"][i]["Machine"][j]["MachineClass"] == machine_capacity:
                # if 2 >= int(json_dict["Factory"][i]["Machine"][j]["MachineClass"]) - int(machine_capacity) >= 0:
                    if json_dict["Factory"][i]["Machine"][j]["Color"]:
                        color = json_dict["Factory"][i]["Machine"][j]["Color"][0]
                        machine_id = all_machine.index(json_dict["Factory"][i]["Machine"][j]["MachineName"])
                        for key in yarn_machine_id.keys():
                            if json_dict["Factory"][i]["Machine"][j]["MachineName"] in yarn_machine_id[key]:
                                temp_dict[key][color].append(machine_id)
                        for key in axle_machine_id.keys():
                            if json_dict["Factory"][i]["Machine"][j]["MachineName"] in axle_machine_id[key]:
                                temp_dict[key][color].append(machine_id)
                    else:
                        machine_id = all_machine.index(json_dict["Factory"][i]["Machine"][j]["MachineName"])
                        for color in list(temp_dict['纱架'].keys()):
                            for key in yarn_machine_id.keys():
                                if json_dict["Factory"][i]["Machine"][j]["MachineName"] in yarn_machine_id[key]:
                                    temp_dict[key][color].append(machine_id)
                            for key in axle_machine_id.keys():
                                if json_dict["Factory"][i]["Machine"][j]["MachineName"] in axle_machine_id[key]:
                                    temp_dict[key][color].append(machine_id)

        color_machine_dict[machine_capacity] = temp_dict
    # print("color_machine_dict", color_machine_dict)
    # print("all_machine", all_machine)
    # mapped_color_machine_dict = {}
    # for key, value in color_machine_dict.items():  # 遍历 color_machine_dict 中的键值对
    #     mapped_color_machine_dict[key] = {}
    #     for color, machines in value.items():  # 遍历值中的字典
    #         mapped_color_machine_dict[key][color] = [all_machine.index(machine) for machine in machines]
    # # print("映射后的 color_machine_dict:", mapped_color_machine_dict)
    return color_machine_dict


def organize_dict(job_dict_old):
    job_dict = copy.deepcopy(job_dict_old)
    cooperative_order = {}  # 合作序号对应的作业标识号
    cooperative_production_number = {}  # 合作序号对应的生产序列号
    cooperative_production_time = {}  # 合作序号对应的生产时间
    cooperative_locked_order = {}  # 合作序号对应的锁定顺序
    for key, value in job_dict.items():  # 提取需要合作的订单
        if value[0]['合作序号'] != 'nan':
            # print(key, value[0]['生产物流号'])
            if value[0]['合作序号'] not in cooperative_order:
                cooperative_order[value[0]['合作序号']] = [key]
                cooperative_production_number[value[0]['合作序号']] = [value[0]['生产物流号']]
                cooperative_production_time[value[0]['合作序号']] = [value[0]['染程用时']]
                # if value[0]['锁定状态'] != '0':
                cooperative_locked_order[value[0]['合作序号']] = [value[0]['锁定顺序']]
            else:
                # print(cooperative_locked_order)
                cooperative_order[value[0]['合作序号']].append(key)
                cooperative_production_number[value[0]['合作序号']].append(value[0]['生产物流号'])
                cooperative_production_time[value[0]['合作序号']].append(value[0]['染程用时'])
                # if value[0]['锁定状态'] != '0':
                cooperative_locked_order[value[0]['合作序号']].append(value[0]['锁定顺序'])
        # if value[0]['合作序号'] != 'nan':
        #     if value[0]['合作序号'] not in cooperative_production_number:
        #         cooperative_production_number[value[0]['合作序号']] = [value[0]['生产物流号']]
        #     else:
        #         cooperative_production_number[value[0]['合作序号']].append(value[0]['生产物流号'])
    # print("合作序号", cooperative_order)
    cooperative_order = {value: keys for value, keys in cooperative_order.items() if len(keys) > 1000}
    cooperative_production_number = {value: keys for value, keys in cooperative_production_number.items() if
                                     len(keys) > 1}
    cooperative_production_time = {value: keys for value, keys in cooperative_production_time.items() if len(keys) > 1}
    cooperative_locked_order = {value: keys for value, keys in cooperative_locked_order.items() if len(keys) > 1}
    print("合作序号", cooperative_order)
    print("生产物流号", cooperative_production_number)
    print("染程用时", cooperative_production_time)
    print("合作锁定顺序", cooperative_locked_order)
    first_cooperative_order = []  # 存放第一个合作订单
    for key, value in cooperative_order.items():  # 将需要合作的订单合并
        first_cooperative_order.append(value[0])
        total_sum = 0
        for id in value:  # 除了第一个外，合作序号
            total_sum += job_dict[id][0]['染程用时']
        for id in value[:-1]:  # 除了最后一个外，合作序号
            total_sum += job_dict[id][0]['切换时间']
        for id in value[1:]:  # 删除重复的
            job_dict.pop(id)
        # print("value[0]", value[0])
        # print("job_dict[value[0]", job_dict[value[0]])
        # print("job_dict[value[0][0]['染程用时']]", job_dict[value[0]][0]['染程用时'])
        job_dict[value[0]][0]['染程用时'] = total_sum  # 更新染程
        # print("新染程total_sum", total_sum)
    print("第一个合作订单", first_cooperative_order)
    for key2, value2 in job_dict.items():
        if key2 in first_cooperative_order:
            cooperative_number = value2[0]["合作序号"]  # 提取合作序号
            other_cooperative_order = cooperative_order[cooperative_number]
            value2[0]["合作订单"] = other_cooperative_order  # 存入其他合作订单
            value2[0]["合作生产物流号"] = cooperative_production_number[cooperative_number]
            value2[0]["合作染程用时"] = cooperative_production_time[cooperative_number]
            if value2[0]['锁定状态'] != '0':
                value2[0]["合作锁定顺序"] = cooperative_locked_order[cooperative_number]
            else:
                value2[0]["合作锁定顺序"] = ""
        else:
            value2[0]["合作订单"] = ""  # 存入空值
            value2[0]["合作生产物流号"] = ""
            value2[0]["合作染程用时"] = ""
            value2[0]["合作锁定顺序"] = ""
    return job_dict


def Get_machine_id_dict(json_dict):
    machine_list = []  # 二维列表，各副资源组对应的机器
    second_resource_type_num = {}  # 各副资源组数量
    for fac in json_dict['Factory'].keys():
        second_resource = json_dict['Factory'][fac]['SecondaryResource']
        type_value = second_resource['YarnFrame']
        # for type, type_value in second_resource.items():
        for key, value_temp in type_value.items():
            second_resource_type_num[key] = len(value_temp)
            for key2, value2 in value_temp.items():
                # print(key2)
                use_machine = value2['Machine']
                machine_list.append(use_machine)
        type_value = second_resource['AxleFrame']
        for key, value_temp in type_value.items():
            second_resource_type_num[key] = len(value_temp)
            for key2, value2 in value_temp.items():
                # print(value2)
                use_machine = value2['Machine']
                machine_list.append(use_machine)
    return machine_list, second_resource_type_num


def Get_Machine_dict(json_dict):
    machine_dict = {}
    machine_num = 0
    for i in json_dict["Factory"].keys():
        for j in json_dict["Factory"][i]["Machine"].keys():
            machine_dict[machine_num] = j
            machine_num += 1
    return machine_dict


# def Get_locked_state(json_dict):
#     """
#     获取锁定状态
#     :param json_dict:
#     :return:
#     """
#     locked_job = []  # 存放锁定的订单和相应的机器 [0, '201']
#     for i in json_dict["Order"].keys():  # 遍历工厂
#         for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
#             lock_state = json_dict["Order"][i][j]["LockedState"]
#             if lock_state == '1':
#                 # print("有锁定")
#                 lock_machine = json_dict["Order"][i][j]["MachineId"]
#                 locked_job.append([j, lock_machine])
#     return locked_job

def Get_locked_state(new_job_dict):
    """
    获取锁定状态
    :param json_dict:
    :return:
    """
    locked_job = []  # 存放锁定的订单和相应的机器 [0, '201']
    new_job_list = list(new_job_dict.values())
    # print("new_job_list",new_job_list)
    for j in range(len(new_job_list)):  # 遍历各工厂对应的订单列表
        # print("new_job_list[j]",new_job_list[j])
        lock_state = new_job_list[j][0]["锁定状态"]
        if lock_state == '1':
            # print("有锁定")
            lock_machine = new_job_list[j][0]["锁定机器"]
            locked_job.append([j, lock_machine])
    return locked_job


# def Get_continue_order(json_dict):
#     """
#     提取续作订单
#     :param json_dict:
#     :return:
#     """
#     continue_job = []  # 存放续作的订单和相应的机器 [0, '201']
#     for i in json_dict["Order"].keys():  # 遍历工厂
#         for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
#             continue_state = json_dict["Order"][i][j]["OriginalMachineId"]
#             if len(continue_state) != 0:
#                 # print("该订单是续作订单")
#                 lock_machine = json_dict["Order"][i][j]["OriginalMachineId"][0]  # 取续作的第一台
#                 continue_job.append([j, lock_machine])
#     return continue_job

def Get_continue_order(new_job_dict):
    """
    提取续作订单
    :param new_job_dict:
    :return:
    """
    continue_job = []  # 存放续作的订单和相应的机器 [0, '201']
    new_job_list = list(new_job_dict.values())
    for j in range(len(new_job_list)):  # 遍历各工厂对应的订单列表
        continue_state = new_job_list[j][0]["续作机器"]
        if len(continue_state) != 0:
            # print("该订单是续作订单")
            lock_machine = continue_state[0]  # 取续作的第一台
            continue_job.append([j, lock_machine])
    return continue_job


def Get_machine_start_time(json_dict, M_num, Machine_dict):
    """
    改变机器开始时间
    :param json_dict:
    :return:
    """
    # print(json_dict["Order"]["341557"][0])
    machine_start_time = [0 for _ in range(M_num)]
    for i in json_dict["Order"].keys():  # 遍历工厂
        for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
            order_state = json_dict["Order"][i][j]["OrderStatus"]
            if order_state == '执行中':
                # print("you  qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
                machine_id = json_dict["Order"][i][j]["ActualMachineId"]
                # print("machine_id", machine_id)
                pt = json_dict["Order"][i][j]["ProcessingTime"]
                # print("pt", pt)
                machine_real_idx = None
                for key, val in Machine_dict.items():
                    if val == machine_id:
                        machine_real_idx = key
                        break
                # print("machine_real_idx", machine_real_idx)
                current_datetime = datetime.now() # 使用当前时间
                actualStartTime = json_dict["Order"][i][j]["ActualStartTime"]
                actualStartTime = datetime.strptime(actualStartTime, "%Y-%m-%d %H:%M:%S")
                pt = json_dict["Order"][i][j]["ProcessingTime"]
                st_type = json_dict["Order"][i][j]["DyeType"]  # 染纱还是染轴
                if st_type == '染纱':
                    st = json_dict["Rule"]["YarnSwitchTime"]
                else:
                    st = json_dict["Rule"]["AxleSwitchTime"]
                end_time = actualStartTime + timedelta(minutes=(pt + st)) - current_datetime
                total_minutes = end_time.total_seconds() / 60 # 转化为分钟
                # print("machine_real_idx", machine_real_idx)
                machine_start_time[machine_real_idx] = total_minutes
    # print(machine_start_time)
    return machine_start_time


# def extract_lock_job_and_order(json_dict):
#     """
#     提取具有顺序的锁定计划
#     :param json_dict:
#     :return: lockedjob: {'201':[[12,1], [13,2], [14,3]]} 121314锁定生产，顺序分别为123
#     """
#     lockedjob = {}
#     for i in json_dict["Order"].keys():  # 遍历工厂
#         machine_message = json_dict["Factory"][i]["Machine"]
#         all_machine = []
#         for machine, v in machine_message.items():
#             all_machine.append(machine)
#             lockedjob[machine] = []
#         for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
#             locked_state = json_dict["Order"][i][j]["LockedState"]  # 锁定状态
#             locked_machine = json_dict["Order"][i][j]["MachineId"]
#             locked_order = json_dict["Order"][i][j]["LockJobOrder"]  # 顺序
#             if locked_order is not None:
#                 lockedjob[locked_machine].append([j, locked_order])
#     return lockedjob


def extract_lock_job_and_order(new_job_dict, json_dict):
    """
    提取具有顺序的锁定计划
    :param json_dict:
    :return: lockedjob: {'201':[[12,1], [13,2], [14,3]]} 121314锁定生产，顺序分别为123
    """
    lockedjob = {}
    new_job_list = list(new_job_dict.values())
    for i in json_dict["Order"].keys():  # 遍历工厂
        machine_message = json_dict["Factory"][i]["Machine"]
        all_machine = []
        for machine, v in machine_message.items():
            all_machine.append(machine)
            lockedjob[machine] = []
        for j in range(len(new_job_list)):  # 遍历各工厂对应的订单列表
            locked_state = new_job_list[j][0]["锁定状态"]  # 锁定状态
            locked_machine = new_job_list[j][0]["锁定机器"]
            locked_order = new_job_list[j][0]["锁定顺序"]  # 顺序
            # print(locked_state, locked_machine, locked_order)
            if locked_order != 0:
                # print(locked_state)
                # print("j", j, "locked_order", locked_order, "locked_machine", locked_machine)
                lockedjob[locked_machine].append([j, locked_order])
    return lockedjob


def get_machine_message(json_dict):
    machine_message = 0
    for i in json_dict["Order"].keys():  # 遍历工厂
        machine_message = json_dict["Factory"][i]["Machine"]
    machine_message = list(machine_message.values())
    return machine_message


def update_second_resource_num(json_dict, second_resource_type_num, srn_machine_list, secondary_resource_num):
    """
    更新副资源数量，执行中的更新，同时更新releases_resource_time
    :param secondary_resource_num:
    :param json_dict:
    :param second_resource_type_num:
    :param srn_machine_list:
    :return:
    """
    # 提取执行中
    processing_job = []  # 内存订单字典
    for i in json_dict["Order"].keys():  # 遍历工厂
        for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
            order_state = json_dict["Order"][i][j]["OrderStatus"]
            if order_state == '执行中':
                processing_job.append(json_dict["Order"][i][j])
    for job in processing_job:
        machine_id = job["ActualMachineId"]  # 确定机器的真实编号如401
        dye_type = job["DyeType"]  # 染纱还是染轴
        if dye_type == "染纱":
            srn_type = job["FrameType"]  # 获取副资源（架）类型
        else:
            srn_type = job["Axle"]  # 获取副资源（架）类型
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
        srn_index = [index + sum(class_lengths[:srn_type_index]) for index, sublist in
                     enumerate(sliced_classes[srn_type_index]) if machine_id in sublist]  # 获取使用副资源的索引
        if not srn_index:
            print("副资源（架）类型与机器不匹配", "机器为", machine_id)
        second_resource_index = srn_index[0]
        secondary_resource_num[second_resource_index] -= 1
    return secondary_resource_num


def get_stop_machine(json_dict):
    """
    获取异常停机机器号
    :param json_dict:
    :return:
    """
    stop_machine_list = []
    for i in json_dict["Order"].keys():  # 遍历工厂
        machine_message = json_dict["Factory"][i]["Machine"]
        for stop_machine, value in enumerate(list(machine_message.values())):
            if value["CurrentStatus"] == 'E':
                stop_machine_list.append([stop_machine, value['MachineName']])
    return stop_machine_list


def get_machine_pre_color(json_dict):
    """
    获取各个机器的上个状态的颜色
    :param json_dict:
    :return:
    """
    machine_pre_color = {}
    for i in json_dict["Order"].keys():  # 遍历工厂
        machine_message = json_dict["Factory"][i]["Machine"]
        machine_id = 0
        for key, value in machine_message.items():
            machine_pre_color[machine_id] = value["PrevColor"]
            machine_id += 1
    return machine_pre_color


def machine_type_num(machine_message):
    machine_type = {}
    for machine_idx, machine in enumerate(machine_message):
        machine_class = machine["MachineClass"]
        machine_name = machine["MachineName"]
        if machine_class not in machine_type:  # 机器容量
            # machine_type[machine_class] = [machine_idx]
            machine_type[machine_class] = {"SS": [], "QQ": []}
            extra_machine_type = machine["ColorCategory"]  # 机器为深机器还是浅机器
            if extra_machine_type != "ZB":
                print("extra_machine_type", extra_machine_type, machine_name)
                machine_type[machine_class][extra_machine_type].append(machine_idx)
        else:
            # machine_type[machine_class].append(machine_idx)
            extra_machine_type = machine["ColorCategory"]
            if extra_machine_type != "ZB":
                print("extra_machine_type", extra_machine_type, machine_name)
                machine_type[machine_class][extra_machine_type].append(machine_idx)
    return machine_type


def machine_type_num2(machine_message):
    machine_type = {}
    for machine_idx, machine in enumerate(machine_message):
        machine_class = machine["MachineClass"]
        machine_name = machine["MachineName"]
        if machine_class not in machine_type:  # 机器容量
            # machine_type[machine_class] = [machine_idx]
            machine_type[machine_class] = {}
            extra_machine_type = machine["ColorCategory"]  # 机器为深机器还是浅机器
            if extra_machine_type != "ZB":
                if extra_machine_type not in machine_type[machine_class]:
                    # print("extra_machine_type", extra_machine_type, machine_name)
                    machine_type[machine_class][extra_machine_type] = [machine_idx]
                else:
                    machine_type[machine_class][extra_machine_type].append(machine_idx)
        else:
            # machine_type[machine_class].append(machine_idx)
            extra_machine_type = machine["ColorCategory"]
            if extra_machine_type != "ZB":
                if extra_machine_type not in machine_type[machine_class]:
                    # print("extra_machine_type", extra_machine_type, machine_name)
                    machine_type[machine_class][extra_machine_type] = [machine_idx]
                else:
                    machine_type[machine_class][extra_machine_type].append(machine_idx)
    machine_type = {k: v for k, v in machine_type.items() if v}
    return machine_type


def machine_type_num3(machine_message):
    machine_type = {}
    machine_type_white = {}
    for machine_idx, machine in enumerate(machine_message):
        machine_class = machine["MachineClass"]
        machine_name = machine["MachineName"]
        if machine_class not in machine_type:  # 机器容量
            # machine_type[machine_class] = [machine_idx]
            machine_type[machine_class] = {}
            machine_type_white[machine_class] = {}
            extra_machine_type = machine["ColorCategory"]  # 机器为深机器还是浅机器
            if extra_machine_type != "ZB":
                if extra_machine_type not in machine_type[machine_class]:
                    # print("extra_machine_type", extra_machine_type, machine_name)
                    machine_type[machine_class][extra_machine_type] = [machine_idx]
                else:
                    machine_type[machine_class][extra_machine_type].append(machine_idx)
            else:
                if extra_machine_type not in machine_type_white[machine_class]:
                    # print("extra_machine_type", extra_machine_type, machine_name)
                    machine_type_white[machine_class][extra_machine_type] = [machine_idx]
                else:
                    machine_type_white[machine_class][extra_machine_type].append(machine_idx)
        else:
            # machine_type[machine_class].append(machine_idx)
            extra_machine_type = machine["ColorCategory"]
            if extra_machine_type != "ZB":
                if extra_machine_type not in machine_type[machine_class]:
                    # print("extra_machine_type", extra_machine_type, machine_name)
                    machine_type[machine_class][extra_machine_type] = [machine_idx]
                else:
                    machine_type[machine_class][extra_machine_type].append(machine_idx)
            else:
                if extra_machine_type not in machine_type_white[machine_class]:
                    # print("extra_machine_type", extra_machine_type, machine_name)
                    machine_type_white[machine_class][extra_machine_type] = [machine_idx]
                else:
                    machine_type_white[machine_class][extra_machine_type].append(machine_idx)
    machine_type = {k: v for k, v in machine_type.items() if v}
    machine_type_white = {k: v for k, v in machine_type_white.items() if v}
    machine_type_white = {k: v for k, v in machine_type_white.items() if len(v['ZB']) > 1}
    return machine_type, machine_type_white


def get_average_quantity(json_dict):
    average_quantity = json_dict["Rule"]["AverageQuantity"]
    return average_quantity



# def load_time_axis(json_dict):
#     return TimeAxisManager(json_dict)