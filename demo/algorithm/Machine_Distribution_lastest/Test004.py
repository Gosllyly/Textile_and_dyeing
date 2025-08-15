import json
from datetime import datetime
from _Time_Axis_Manager import TimeAxisManager


def compute_process_times(json_dict, routing_type, dyeing_start_time, dyeing_end_time):
    from datetime import timedelta
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
        routing_steps = json_dict["Routing"].get(i, {}).get(routing_type, [])  # 获取该订单工艺路线
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

    dyeing_start_time = datetime.strptime(dyeing_start_time, "%Y-%m-%d %H:%M")  # 转化为datetime格式
    dyeing_end_time = datetime.strptime(dyeing_end_time, "%Y-%m-%d %H:%M")
    # process_times["DyeingProcessEndTime"] = dyeing_end_time#.strftime("%Y-%m-%d %H:%M")

    # 上游推算
    current_end = dyeing_start_time
    for step in reversed(routing_steps[:dyeing_index]):
        wait_time = int(step.get("StandardWaitingTime", 0) * 60)
        prod_time = int(step.get("WorkCenterDetail", [{}])[0].get("StandardProductionTime", 0) * 60)
        # current_end = current_start - timedelta(minutes=wait_time)
        # current_start = current_end - timedelta(minutes=prod_time)
        # current_end = current_start - timedelta(minutes=wait_time)
        current_end_shifted, _ = time_axis_manager.reverse_adjust_for_shift_gap(current_end, wait_time)
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
        current_end = current_start_shifted

    # 下游推算
    current_start = dyeing_end_time
    for step in routing_steps[dyeing_index + 1:]:
        wait_time = int(step.get("StandardWaitingTime", 0) * 60)
        prod_time = int(step.get("WorkCenterDetail", [{}])[0].get("StandardProductionTime", 0) * 60)
        # current_start += timedelta(minutes=wait_time)
        # current_end = current_start + timedelta(minutes=prod_time)
        # current_start += timedelta(minutes=wait_time)
        # current_start_shifted = time_axis_manager.find_valid_time(current_start)
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


with open("testjson.json", "r", encoding="utf-8-sig") as f:
    json_dict = json.load(f)
    # for i in json_dict["Routing"]:
    #     routings = json_dict["Routing"].get(i, {})
    #
    # print(routings)
routing_type = 'TZZJH'
dyeing_start_time = "2025-04-25 08:22"
dyeing_end_time = "2025-04-25 14:22"

p = compute_process_times(json_dict, routing_type, dyeing_start_time, dyeing_end_time)
print(p)

# group_entries = [(66, 221), (65, 338), (67, 377)]
# MS = [2, 4, 2, 2, 0, 4, 2, 3, 1, 2, 1, 1, 2, 0, 9, 5, 0, 0, 3, 2, 6, 2, 11, 0, 4, 0, 3, 1, 6, 4, 1, 3, 3, 0, 1, 0, 0, 0,
#       3, 2, 4, 10, 1, 0, 2, 10, 4, 0, 0, 2, 1, 8, 7, 8, 8, 0, 1, 2, 7, 6, 3, 8, 1, 3, 0, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0,
#       7, 4, 1, 2, 1, 1, 3, 2, 5, 2, 0, 2, 6, 9, 11, 2, 5, 3, 2, 4, 3, 3, 5, 2, 1, 4, 0, 1, 0, 3, 0, 1, 0, 0, 0, 1, 0, 2,
#       1, 0, 1, 0, 0, 0, 3, 0, 0, 3, 0, 1, 2, 0, 1, 0, 1, 1, 1, 0, 1, 2, 2, 2, 0, 6, 3, 0, 0, 0, 0, 1, 1, 1, 1, 2, 0, 1,
#       4, 4, 4, 1, 3, 10, 1, 1, 3, 0, 1, 1, 0, 0, 1, 0, 0, 3, 3, 1, 5, 2, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 5, 0, 7, 3, 3, 2,
#       10, 5, 0, 1, 1, 1, 2, 0, 3, 4, 0, 1, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 1, 1, 2, 1, 7, 0, 2, 0, 2, 3, 4, 5, 5, 3,
#       3, 9, 3, 5, 0, 5, 8, 3, 0, 3, 2, 0, 3, 0, 1, 2, 7, 4, 11, 1, 4, 9, 2, 0, 0, 6, 1, 5, 1, 7, 0, 0, 5, 3, 6, 1, 4, 1,
#       4, 4, 5, 4, 0, 2, 0, 1, 1, 1, 2, 2, 7, 2, 10, 2, 0, 0, 2, 10, 1, 1, 7, 0, 1, 4, 0, 8, 0, 2, 0, 7, 0, 4, 0, 1, 1,
#       6, 5, 9, 1, 4, 4, 0, 0, 2, 0, 4, 1, 2, 1, 7, 7, 2, 0, 0, 1, 0, 1, 2, 2, 2, 6, 3, 4, 1, 8, 2, 0, 3, 9, 0, 3, 1, 1,
#       7, 0, 4, 5, 5, 5, 1, 4, 0, 0, 8, 7, 0, 10, 6, 0, 2, 0, 0, 3, 1, 8, 0, 1, 4, 1, 1, 3, 4, 2, 1, 5, 1, 4, 9, 4, 1, 2,
#       3, 1, 2, 7, 9, 1, 3, 1, 1, 8, 5, 4, 2, 0, 5, 6, 8, 5, 2, 8, 7, 1, 9, 4, 2, 0, 3, 1, 3, 5, 5, 1, 6, 3, 0, 6, 1, 0,
#       0, 0, 2, 0, 5, 1, 2, 0, 2, 1, 1, 2, 1, 4, 1, 0, 4, 2, 3, 3, 5, 5, 1, 0, 3, 0, 8, 0, 0, 1, 4, 4, 1, 0, 6, 0, 2, 3,
#       0, 2, 1, 2, 1, 3, 7, 5, 4, 1, 3, 6, 1, 2, 7, 0, 2, 0, 3, 5, 5, 9, 7, 0, 4, 0, 3]
# print(MS[221], MS[358], MS[377])
# count = 0
# for job, pos in group_entries:
#     count += 1
#     print("循环次数", count)
#     print("job=", job)
#     print("pos=", pos)
#     # MS[job] = 1
#     print("==========================================")
#     valid_machines = []
#     print("set=====", set(MS[pos] for pos in [j for j, idx in group_entries]))
#     print("set=====", [MS[pos] for pos in [j for j, idx in group_entries]])
#
#     count1 = 0
#     for machine in [MS[pos] for pos in [j for j, idx in group_entries]]:
#         count1 += 1
#         print("循环次数1", count1)
#         # if self.Processing_time[job][O_num][machine] != 9999:
#         valid_machines.append(machine)
#     print("valid_machines", valid_machines)
