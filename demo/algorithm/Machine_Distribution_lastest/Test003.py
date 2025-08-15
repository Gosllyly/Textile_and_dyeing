import input_fun
import json
from datetime import datetime, timedelta
from collections import defaultdict
import bisect
from _Time_Axis_Manager import TimeAxisManager

with open("20250806.json", "r", encoding="gbk") as f:
    json_dict = json.load(f)

time_axis = TimeAxisManager(json_dict)

# 测试输出当前时间
datetime = datetime.now().replace(microsecond=0)
print(datetime)

# 以当前时间作为基准时间，上推下拉得到染色工序的可进行的时间区间
'''
RSJH:染纱计划
TZZJH:筒子轴计划
RSZJH:染色轴计划
'''


# 计算染色工序可行时间窗
# def calculate_time_intervals(json_dict, buffer_days=3):
#     # 遍历工厂
#     for factory_id in json_dict["Order"]:
#         orders = json_dict["Order"][factory_id]
#         routings = json_dict["Routing"].get(factory_id, {})
#     # for i in json_dict["Order"].keys():  # 遍历工厂
#     #     orders = json_dict['Order'][i]
#     #     routings = json_dict['Routing'][i]
#
#         # 获取当前时间
#         current_time = datetime.now()
#         results = []
#         for order in orders:
#             order_id = order['OrderId']
#             routing_key = order['Routing']
#             dye_delivery_str = order['DyeDeliveryDate']
#
#             # 检查工艺路线是否存在
#             if not routing_key or routing_key not in routings:
#                 results.append({
#                     'order_id': order_id,
#                     'error': f"工艺路线'{routing_key}'不存在或未指定"
#                 })
#                 continue
#
#             processes = routings[routing_key]
#             sorted_processes = sorted(processes, key=lambda x: int(x['OperationNum']))
#
#             # 查找染色工序
#             dye_index = None
#             for idx, process in enumerate(sorted_processes):
#                 if '染色' in process['WorkCenter']:
#                     dye_index = idx
#                     break
#             if dye_index is None:
#                 results.append({
#                     'order_id': order_id,
#                     'error': "未找到染色工序"
#                 })
#                 continue
#
#             # 分割上下游
#             upstream = sorted_processes[:dye_index]
#             downstream = sorted_processes[dye_index + 1:]
#
#             # 计算总时间（小时）
#             upstream_total = sum(
#                 p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']
#                 for p in upstream
#             )
#             downstream_total = sum(
#                 p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']
#                 for p in downstream
#             )
#
#             # 解析交期时间
#             try:
#                 dye_delivery = datetime.strptime(dye_delivery_str, "%Y-%m-%d %H:%M:%S")
#             except:
#                 results.append({
#                     'order_id': order_id,
#                     'error': "交期时间格式错误"
#                 })
#                 continue
#
#             # 计算时间区间
#             # earliest_start = current_time + timedelta(hours=upstream_total)
#             earliest_start, gap = adjust_for_shift_gap(current_time, upstream_total * 60)
#             # buffer_date = dye_delivery - timedelta(days=buffer_days)
#             # buffer_date = buffer_date.replace(hour=0, minute=0, second=0)
#             # latest_end = buffer_date - timedelta(hours=downstream_total)
#             latest_end = dye_delivery - timedelta(days=buffer_days)
#
#             # 检测冲突
#             time_conflict = latest_end < earliest_start
#             warning = "冲突：染色工序无法在时限内完成" if time_conflict else None
#
#             results.append({
#                 'order_id': order_id,
#                 'earliest_start': earliest_start.strftime("%Y-%m-%d %H:%M:%S"),
#                 'latest_end': latest_end.strftime("%Y-%m-%d %H:%M:%S"),
#                 'warning': warning
#             })
#
#     return results
# def calculate_time_intervals(json_dict, buffer_days=3):
#     """计算染色工序时间窗并存储为字典 {订单ID: (最早开始时间, 最晚结束时间)}"""
#     time_windows = {}
#     for factory_id in json_dict["Order"]:
#         orders = json_dict["Order"][factory_id]
#         routings = json_dict["Routing"].get(factory_id, {})
#
#         for order in orders:
#             order_id = order['OrderId']
#             routing_key = order['Routing']
#             dye_delivery_str = order.get('DyeDeliveryDate', '')
#
#             # 检查工艺路线是否存在
#             if not routing_key or routing_key not in routings:
#                 continue  # 跳过无效条目
#
#             processes = routings[routing_key]
#             sorted_processes = sorted(processes, key=lambda x: int(x['OperationNum']))
#
#             # 查找染色工序
#             dye_index = None
#             for idx, process in enumerate(sorted_processes):
#                 if '染色' in process['WorkCenter']:
#                     dye_index = idx
#                     break
#             if dye_index is None:
#                 continue  # 无染色工序则跳过
#
#             # 计算上下游时间
#             upstream = sorted_processes[:dye_index]
#             downstream = sorted_processes[dye_index + 1:]
#
#             # 计算总时间（转换为分钟）
#             upstream_total = sum(
#                 (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
#                 for p in upstream
#             )
#             downstream_total = sum(
#                 (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
#                 for p in downstream
#             )
#
#             # 解析交期时间
#             try:
#                 dye_delivery = datetime.strptime(dye_delivery_str, "%Y-%m-%d %H:%M:%S")
#             except:
#                 dye_delivery = None
#
#             # 计算时间窗
#             if upstream_total > 0:
#                 earliest_start, _ = adjust_for_shift_gap(datetime.now(), upstream_total)
#             else:
#                 earliest_start = datetime.now()
#
#             if dye_delivery and downstream_total > 0:
#                 latest_end = dye_delivery - timedelta(days=buffer_days)
#                 latest_end -= timedelta(minutes=downstream_total)
#             else:
#                 latest_end = None
#
#             time_windows[order_id] = (earliest_start, latest_end)
#     return time_windows
# def calculate_time_intervals(json_dict, buffer_days=3):
#     """
#     返回时间窗字典和错误字典
#     time_windows: {订单ID: (最早开始时间, 最晚结束时间)}
#     order_errors: 结构：{订单ID: {'error': str, 'warning': str}}
#     """
#     time_windows = {}
#     order_errors = defaultdict(dict)
#
#     for factory_id in json_dict["Order"]:
#         orders = json_dict["Order"][factory_id]
#         routings = json_dict["Routing"].get(factory_id, {})
#
#         for order in orders:
#             order_id = order['OrderId']
#             routing_key = order['Routing']
#             dye_delivery_str = order.get('DyeDeliveryDate', '')
#
#             error_info = {'error': None}
#
#             # 检查工艺路线是否存在
#             if not routing_key or routing_key not in routings:
#                 error_info['error'] = f"工艺路线'{routing_key}'不存在"
#                 order_errors[order_id] = error_info
#                 continue
#
#             processes = routings[routing_key]
#             sorted_processes = sorted(processes, key=lambda x: int(x['OperationNum']))
#
#             # 查找染色工序
#             dye_index = None
#             for idx, process in enumerate(sorted_processes):
#                 if '染色' in process['WorkCenter']:
#                     dye_index = idx
#                     break
#             if dye_index is None:
#                 error_info['error'] = f"未找到染色工序"
#                 order_errors[order_id] = error_info
#                 continue
#
#             # 计算上下游时间
#             upstream = sorted_processes[:dye_index]
#             downstream = sorted_processes[dye_index + 1:]
#
#             # 计算总时间（转换为分钟）
#             upstream_total = sum(
#                 (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
#                 for p in upstream
#             )
#             downstream_total = sum(
#                 (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
#                 for p in downstream
#             )
#
#             # 解析交期时间
#             try:
#                 dye_delivery = datetime.strptime(dye_delivery_str, "%Y-%m-%d %H:%M:%S")
#             except:
#                 error_info['error'] = f"交期时间格式错误"
#                 order_errors[order_id] = error_info
#                 # dye_delivery = None
#
#             # 计算时间窗
#             if upstream_total > 0:
#                 earliest_start, _ = adjust_for_shift_gap(datetime.now(), upstream_total)
#             else:
#                 earliest_start = datetime.now()
#
#             # if dye_delivery and downstream_total > 0:
#             #     latest_end = dye_delivery - timedelta(days=buffer_days)
#             #     # latest_end -= timedelta(minutes=downstream_total)
#             # else:
#             #     latest_end = None
#             latest_end = dye_delivery - timedelta(days=buffer_days)
#
#             time_windows[order_id] = (earliest_start.strftime("%Y-%m-%d %H:%M:%S"), latest_end.strftime("%Y-%m-%d %H:%M:%S"))
#             time_conflict = latest_end < earliest_start
#             if time_conflict:
#                 error_info['error'] = "染色工序时间冲突"
#                 order_errors[order_id] = error_info
#     return time_windows, order_errors
# test
# def calculate_time_intervals(json_dict, buffer_days=3):
#     """
#     返回时间窗字典和错误字典
#     time_windows: {订单ID: (最早开始时间, 最晚结束时间)}
#     order_errors: 结构：{订单ID: {'error': str, 'warning': str}}
#     """
#     time_windows = {}
#     order_errors = defaultdict(dict)
#
#     for factory_id in json_dict["Order"]:
#         orders = json_dict["Order"][factory_id]
#         routings = json_dict["Routing"].get(factory_id, {})
#
#         for order in orders:
#             order_id = order['OrderId']
#             routing_key = order['Routing']
#             dye_delivery_str = order.get('DyeDeliveryDate', '')
#
#             error_info = {'error': None, 'warning': None}
#             apply_custom_rule = False
#             dye_delivery = None
#
#             # ================= 第一阶段：基础校验 =================
#             # 校验工艺路线是否存在
#             routing_exists = routing_key and routing_key in routings
#             if not routing_exists:
#                 error_info['error'] = f"工艺路线'{routing_key}'不存在"
#                 apply_custom_rule = True
#             else:
#                 # 校验染色工序是否存在
#                 processes = routings[routing_key]
#                 sorted_processes = sorted(processes, key=lambda x: int(x['OperationNum']))
#                 dye_index = next(
#                     (idx for idx, p in enumerate(sorted_processes) if '染色' in p['WorkCenter']),
#                     None
#                 )
#                 if dye_index is None:
#                     error_info['error'] = "未找到染色工序"
#                     apply_custom_rule = True
#
#             # ================= 第二阶段：时间解析 =================
#             # 解析染色交期时间
#             try:
#                 dye_delivery = datetime.strptime(dye_delivery_str, "%Y-%m-%d %H:%M:%S")
#             except:
#                 error_msg = "交期时间格式错误"
#                 if error_info['error']:
#                     error_info['error'] += f"; {error_msg}"
#                 else:
#                     error_info['error'] = error_msg
#
#             # ================= 第三阶段：时间计算 =================
#             if apply_custom_rule:
#                 # 应用特殊规则计算时间窗
#                 earliest_start = datetime.now()
#                 latest_end = None
#
#                 # 计算最晚时间（如果交期有效）
#                 if dye_delivery:
#                     latest_end = dye_delivery - timedelta(days=buffer_days)
#                 else:
#                     error_msg = "交期时间无效"
#                     if error_info['error']:
#                         error_info['error'] += f"; {error_msg}"
#                     else:
#                         error_info['error'] = error_msg
#
#                 # 处理时间冲突
#                 if dye_delivery and latest_end < earliest_start:
#                     error_msg = "染色工序时间冲突"
#                     if error_info['error']:
#                         error_info['error'] += f"; {error_msg}"
#                     else:
#                         error_info['error'] = error_msg
#
#                 # 生成时间窗字符串
#                 earliest_str = earliest_start.strftime("%Y-%m-%d %H:%M:%S")
#                 latest_str = latest_end.strftime("%Y-%m-%d %H:%M:%S") if latest_end else ""
#                 time_windows[order_id] = (earliest_str, latest_str)
#
#             else:
#                 # ============== 正常流程计算时间窗 ==============
#                 # 前置校验（确保染色交期有效）
#                 if not dye_delivery:
#                     error_info['error'] = "交期时间无效，无法计算时间窗"
#                     order_errors[order_id] = error_info
#                     continue
#
#                 # 计算上下游时间
#                 upstream = sorted_processes[:dye_index]
#                 downstream = sorted_processes[dye_index+1:]
#
#                 upstream_total = sum(
#                     (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
#                     for p in upstream
#                 )
#                 downstream_total = sum(
#                     (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
#                     for p in downstream
#                 )
#
#                 # 计算最早开始时间
#                 if upstream_total > 0:
#                     earliest_start, _ = adjust_for_shift_gap(datetime.now(), upstream_total)
#                 else:
#                     earliest_start = datetime.now()
#
#                 # 计算最晚结束时间
#                 latest_end = dye_delivery - timedelta(days=buffer_days)
#
#                 # 时间冲突检查
#                 if latest_end < earliest_start:
#                     error_info['error'] = "染色工序时间冲突"
#
#                 # 记录时间窗
#                 time_windows[order_id] = (
#                     earliest_start.strftime("%Y-%m-%d %H:%M:%S"),
#                     latest_end.strftime("%Y-%m-%d %H:%M:%S")
#                 )
#
#             # ================= 第四阶段：错误处理 =================
#             # 记录错误信息（过滤空值）
#             if error_info['error']:
#                 order_errors[order_id] = {k: v for k, v in error_info.items() if v}
#
#     return time_windows, order_errors

def calculate_time_intervals(json_dict, buffer_days=3):
    """
    返回时间窗字典和错误字典
    time_windows: {订单ID: (最早开始时间 datetime, 最晚结束时间 datetime)}
    order_errors: 结构：{订单ID: {'error': str, 'warning': str}}
    """
    time_windows = {}
    order_errors = defaultdict(dict)

    for factory_id in json_dict["Order"]:
        orders = json_dict["Order"][factory_id]
        routings = json_dict["Routing"].get(factory_id, {})

        for order in orders:
            order_id = order['OrderId']
            routing_key = order['Routing']
            dye_delivery_str = order.get('DyeDeliveryDate', '')
            now_time = datetime.now()
            error_info = {'error': None}

            # 默认 earliest_start 和 latest_end
            earliest_start = now_time
            dye_delivery = None
            try:
                dye_delivery = datetime.strptime(dye_delivery_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                error_info['error'] = "交期时间格式错误"

            latest_end = dye_delivery - timedelta(days=buffer_days) if dye_delivery else now_time + timedelta(
                days=7)  # fallback

            # 路线判断
            if not routing_key or routing_key not in routings:
                error_info['error'] = error_info['error'] or f"工艺路线'{routing_key}'不存在"
                time_windows[order_id] = (earliest_start, latest_end)
                order_errors[order_id] = error_info
                continue

            processes = routings[routing_key]
            sorted_processes = sorted(processes, key=lambda x: int(x['OperationNum']))
            dye_index = None
            for idx, process in enumerate(sorted_processes):
                if '染色' in process['WorkCenter']:
                    dye_index = idx
                    break

            if dye_index is None:
                error_info['error'] = error_info['error'] or "未找到染色工序"
                time_windows[order_id] = (earliest_start, latest_end)
                order_errors[order_id] = error_info
                continue

            # 正常计算
            upstream = sorted_processes[:dye_index]
            downstream = sorted_processes[dye_index + 1:]

            try:
                upstream_total = sum(
                    (p['WorkCenterDetail'][0]['StandardProductionTime'] + p['StandardWaitingTime']) * 60
                    for p in upstream
                )
                if upstream_total > 0:
                    earliest_start, _ = adjust_for_shift_gap(now_time, upstream_total)

                # downstream_total = ... 可选，不一定要
            except Exception as e:
                error_info['error'] = "工序时间数据缺失或格式错误"

            # 最终写入
            time_windows[order_id] = (earliest_start, latest_end)
            if latest_end < earliest_start:
                error_info['error'] = "染色工序时间冲突"
            if error_info['error']:
                order_errors[order_id] = error_info

    return time_windows, order_errors


def adjust_for_shift_gap(start_time, duration):
    """
    核心时间调整函数：处理班次间隔和节假日
    start_time:datetime
    duration: int 分钟
    """
    current_time = start_time
    remaining = duration
    total_gap = 0

    while remaining > 0:
        # 找到当前班次结束时间
        shift_end = time_axis._find_current_shift_end(current_time)
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
            next_shift_start = time_axis._find_next_shift_start(shift_end)
            if next_shift_start:
                gap = (next_shift_start - shift_end).seconds // 60  # 分钟
                total_gap += gap
                current_time = next_shift_start  # + timedelta(minutes=remaining)
            else:
                break

    return current_time, total_gap
    # 返回的值 1.切换时间或染程的结束时间，格式为datetime 2.班次之间的间隔时间,格式为 int 分钟


json = json_dict['Order']['341557']
# time_win = calculate_time_intervals(json_dict)
# print(time_win)
'''Test
后期改为遍历工厂'''

# 执行计算
# results = calculate_time_intervals(json_dict)
# print(results)

# 输出结果
# for res in results:
#     print(f"订单 {res['order_id']}:")
#     if 'error' in res:
#         print(f"  错误 - {res['error']}")
#     else:
#         print(f"  最早开始时间: {res['earliest_start']}")
#         print(f"  最晚结束时间: {res['latest_end']}")
#         if res['warning']:
#             print(f"  ⚠️警告: {res['warning']}")
#     print("---")

time_windows, order_errors = calculate_time_intervals(json_dict)
print(time_windows)
print(order_errors)

'''
读取参数：
经向同批完成X天
纱轴同批完成X天'''
import re


def get_completion_days(json_dict):
    # 读取字符串字段
    warp_str = json_dict["Rule"].get("WarpCompletionDays", "")
    yarn_axle_str = json_dict["Rule"].get("YarnAxleCompletionDays", "")

    # 使用正则提取数字
    warp_days = int(re.search(r'\d+', warp_str).group()) if re.search(r'\d+', warp_str) else None
    yarn_axle_days = int(re.search(r'\d+', yarn_axle_str).group()) if re.search(r'\d+', yarn_axle_str) else None

    return warp_days, yarn_axle_days


# 示例调用
warp_days, yarn_axle_days = get_completion_days(json_dict)
print("经向同批完成天数:", warp_days)
print("纱轴同批完成时间:", yarn_axle_days)


# # 得到同一合作序号下的订单，同一合作序号下的订单需要安排在同一机台连续生产。
# def get_coop_dict(data):
#     """
#     生成合作号字典，保留包含多个订单的条目
#     dict: 结构为 {合作号: [订单ID1, 订单ID2,...]} 的字典
#     """
#     # 初始化默认字典自动创建列表
#     coop_dict = defaultdict(list)
#
#     # 遍历所有工厂
#     for order_group in data["Order"].values():
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

def get_coop_dict(json_dict):
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
    return {k: v for k, v in coop_dict.items() if len(v) > 1}


result_dict = get_coop_dict(json_dict)
print("coop_dict : ", result_dict)


# 得到同一生产物流号下的订单
def get_prod_dict(json_dict):
    """
    生成生产物流号字典，保留包含多个订单的条目
    dict: 结构为 {合作号: [订单ID1, 订单ID2,...]} 的字典
    """
    # 初始化默认字典自动创建列表
    prod_dict = defaultdict(list)

    # 遍历所有工厂
    for order_group in json_dict["Order"].values():
        # 遍历工厂内的每个订单
        for order in order_group:
            # 提取合作号和订单ID
            prod_number = order.get("ProductionNumber")
            order_id = order.get("OrderId")

            # 当两个字段都存在时记录
            if prod_number and order_id:
                prod_dict[prod_number].append(order_id)
    # 过滤只保留有多个订单的条目
    return {k: v for k, v in prod_dict.items() if len(v) > 1}


prod_dict = get_prod_dict(json_dict)
print(prod_dict)


def get_coop_routing_groups(data):
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

    for order_group in data.get("Order", {}).values():
        for order in order_group:
            prod_num = order.get("ProductionNumber")
            order_id = order.get("OrderId")
            routing = order.get("Routing")

            if prod_num and order_id and routing:
                if routing in ["TZZJH", "RSZJH"]:
                    coop_dict[prod_num]['WarpCompletion'].append(order_id)
                if routing in ["TZZJH", "RSZJH", "RSJH"]:
                    coop_dict[prod_num]['YarnAxleCompletion'].append(order_id)

    # 可选：仅保留 WarpCompletion 或 YarnAxleCompletion 含有多个订单的项
    filtered = {
        k: v for k, v in coop_dict.items()
        if len(v['WarpCompletion']) > 1 or len(v['YarnAxleCompletion']) > 1
    }

    return filtered


filtered = get_coop_routing_groups(json_dict)
print(filtered)


orderidlist = []
orderstatelist = []
yy = 0
for i in json_dict["Order"].keys():  # 遍历工厂
    for j in range(len(json_dict["Order"][i])):  # 遍历各工厂对应的订单列表
        orderidlist.append(json_dict["Order"][i][j]["OrderId"])
        orderstatelist.append(json_dict["Order"][i][j]["OrderStatus"])
print(orderstatelist)

print(len(orderidlist),orderidlist)
orderidlist1 = set(orderidlist)
print(orderidlist)
print(len(orderidlist1),orderidlist1)

from collections import Counter
counter = Counter(orderidlist)
duplicates = [item for item, count in counter.items() if count > 1]
print(f"发现 {len(duplicates)} 个重复订单ID：{duplicates}")

orderidlist2 = []
# with open("output_result.json", "r", encoding="utf-8-sig") as f2:
#     json_dict2 = json.load(f2)
# for i in json_dict2["Order"].keys():  # 遍历工厂
#     for j in range(len(json_dict2["Order"][i])):  # 遍历各工厂对应的订单列表
#         orderidlist.append(json_dict2["Order"][i][j]["OrderId"])
# print(len(orderidlist2),orderidlist2)