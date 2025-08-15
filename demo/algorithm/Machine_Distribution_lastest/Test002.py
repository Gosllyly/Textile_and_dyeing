import json
from datetime import datetime, timedelta
import bisect

with open("testjson.json", "r", encoding="utf-8-sig") as f:
    json_dict = json.load(f)


# def Get_Days_num(json_dict):
#     """
#     :param json_dict:
#     :return: (所给工作日历的天数,生产日（Productiondate = True）的天数)
#     """
#     Total_days_num = 0  # 工作日历所涉及到的总天数
#     Production_days_num = 0  # 工作日历中进行生产作业的总天数
#     workcalendar = json_dict["WorkCalendar"]["100.2"]
#     # 统计工作日历所涉及到的总天数
#     for i in workcalendar:
#         Total_days_num += 1
#     # 统计生产日（Productiondate = True）的天数
#     Production_days_num = sum(1 for entry in workcalendar if entry.get("Productiondate", True))
#     return Total_days_num, Production_days_num
# print(Get_Days_num(json_dict))


def _parse_work_calendar(json_dict):
    """
    解析工作日历数据
    work_days: 字典
    """
    work_days = {}
    try:
        calendar_container = json_dict.get("WorkCalendar", {})

        # 兼容两种数据结构：字典直接包含"100.2" 或 列表包含多个字典
        if isinstance(calendar_container, dict):
            calendar_data = calendar_container.get("100.2", [])
        elif isinstance(calendar_container, list):
            calendar_data = []
            for item in calendar_container:
                if isinstance(item, dict):
                    calendar_data.extend(item.get("100.2", []))

        # 解析有效工作日
        for item in calendar_data:
            if not isinstance(item, dict):
                continue
            date_str = item.get("Date", "").split()[0]  # 提取日期部分
            if date_str:
                work_days[date_str] = item.get("Productiondate", False)
    except Exception as e:
        print(f"[ERROR] 解析工作日历时出错: {str(e)}")
    # print(work_days)
    return work_days


# def _parse_work_calendar(json_dict):
#     """解析工作日历"""
#     work_days = {}
#     for item in json_dict["WorkCalendar"]["100.2"]:
#         date_str = item["Date"].split()[0]
#         work_days[date_str] = item["Productiondate"]
#         return work_days
#     # print(work_days)
#     return work_days


# print(_parse_work_calendar(json_dict))

# def _parse_shift_system(json_dict):
#     """解析班次系统数据"""
#     default_shifts = [
#         (datetime.strptime("08:00:00", "%H:%M:%S").time(),
#          datetime.strptime("20:00:00", "%H:%M:%S").time())
#     ]
#
#     try:
#         shift_system = json_dict.get("ShiftSystem", {}).get("漂染三厂班制", [])
#         shifts = []
#
#         for shift in shift_system:
#             start = datetime.strptime(
#                 shift.get("ClassStartTime", "08:00:00"),
#                 "%H:%M:%S"
#             ).time()
#             end = datetime.strptime(
#                 shift.get("ClassEndTime", "20:00:00"),
#                 "%H:%M:%S"
#             ).time()
#             shifts.append((start, end))
#
#         if not shifts:
#             shifts = default_shifts
#
#     except Exception as e:
#         print(f"[WARNING] 使用默认班次: {str(e)}")
#     shifts = default_shifts
#     return shifts

def _parse_shift_system(json_dict):
    """
    解析班次
    shifts: list
    """
    shifts = []
    # shift_system = [{'Shift': '漂染三厂早班', 'ClassStartTime': '08:00:00', 'ClassEndTime': '12:00:00'},
    #                 {'Shift': '漂染三厂中班', 'ClassStartTime': '12:00:00', 'ClassEndTime': '16:00:00'}]
    shift_system = json_dict.get("ShiftSystem", {}).get("漂染三厂班制", [])

    for shift in shift_system:
        try:
            start = datetime.strptime(shift["ClassStartTime"], "%H:%M:%S").time()
            end = datetime.strptime(shift["ClassEndTime"], "%H:%M:%S").time()
            shifts.append((start, end))
            shifts.sort()
        except KeyError as e:
            print(f"班次数据格式错误: {e}")
    return shifts


def _generate_timeline(json_dict):
    """
    生成分钟级生产时间轴
    timeline: list
    """
    timeline = []
    shifts = _parse_shift_system(json_dict)
    work_days = _parse_work_calendar(json_dict)
    current_date = datetime(2025, 3, 10)
    end_date = datetime(2025, 6, 10)

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        if work_days.get(date_str, False):
            for shift_start, shift_end in shifts:
                # 处理跨午夜班次
                start_dt = datetime.combine(current_date.date(), shift_start)
                end_dt = datetime.combine(current_date.date(), shift_end)
                if shift_end < shift_start:
                    end_dt += timedelta(days=1)

                # 生成时间点
                current = start_dt
                while current < end_dt:
                    timeline.append(current)
                    current += timedelta(minutes=1)

        current_date += timedelta(days=1)

    timeline.sort()
    return timeline


def _find_current_shift_end(time_point):
    """
    找到当前班次结束时间
    time_point: datetime

    """
    shifts = _parse_shift_system(json_dict)
    for shift_start, shift_end in shifts:
        # 创建当天的时间对象
        start_dt = datetime.combine(time_point.date(), shift_start)
        end_dt = datetime.combine(time_point.date(), shift_end)

        # 处理跨午夜班次
        if shift_end < shift_start:
            end_dt += timedelta(days=1)

        if start_dt <= time_point < end_dt:
            return end_dt
    return None


def _find_next_shift_start(time_point):
    """
    找到下一个班次开始时间
    time_point: datetime
    """
    candidates = []
    work_days = _parse_work_calendar(json_dict)
    shifts = _parse_shift_system(json_dict)
    # 检查未来3天范围
    for day_offset in range(0, 4):
        check_date = time_point.date() + timedelta(days=day_offset)
        date_str = check_date.strftime("%Y-%m-%d")

        if not work_days.get(date_str, False):
            continue

        for shift_start, _ in shifts:
            candidate = datetime.combine(check_date, shift_start)

            # 过滤早于当前时间的候选
            if candidate >= time_point:
                candidates.append(candidate)

    return min(candidates) if candidates else None


def calculate_gap(start_time, end_time):
    """
    计算两个时间点之间的无效时间
    start_time: datetime
    end_time: datetime
    """
    gap = 0
    current = start_time
    timeline = _generate_timeline(json_dict)
    while current < end_time:
        # 使用二分查找快速判断是否在生产时间轴中
        idx = bisect.bisect_left(timeline, current)
        if idx >= len(timeline) or timeline[idx] != current:
            gap += 1
        current += timedelta(minutes=1)

    return gap


# def find_valid_time(start_time, duration):
#     """
#     找到最近的合法开始时间
#     start_time: datetime
#     duration : int 表示分钟数
#     """
#     # 后续可以改进duration
#     timeline = _generate_timeline(json_dict)
#     duration = int(duration)
#     idx = bisect.bisect_left(timeline, start_time)
#     while idx < len(timeline):
#         # 检查是否有足够的连续时间
#         if idx + duration > len(timeline):
#             return None
#         expected_end = timeline[idx] + timedelta(minutes=duration)
#         if timeline[idx + duration - 1] == expected_end - timedelta(minutes=1):
#             return timeline[idx]
#         idx += 1
#     return None
def find_valid_time(start_time):
    """
    找到最近的合法开始时间，允许跨班次和跨天，只要总有效时间满足duration
    start_time: datetime
    """
    timeline = _generate_timeline(json_dict)
    idx = bisect.bisect_left(timeline, start_time)
    if idx < len(timeline):
        return timeline[idx]
    return None  # 时间轴之外


'''Test'''
print(_parse_work_calendar(json_dict))
print(_parse_shift_system(json_dict))

#
#
print("timeline 前500：", _generate_timeline(json_dict)[:500])


# time_point_1 = datetime(2025, 3, 11, 12, 00)
# print(_find_current_shift_end(time_point_1))
# print(_find_next_shift_start(time_point_1))


# time_point_2 = datetime(2025, 3, 12, 8, 30)
# print(calculate_gap(time_point_1, time_point_2))
# start_time = datetime(2025, 3, 15, 15, 44)
# print(find_valid_time(start_time, duration=480))
#
#
# shift_system = json_dict.get("ShiftSystem", {}).get("漂染三厂班制", [])
# print(shift_system)

# 获取工作日历的第一天与最后一天的日期（datetime）


def adjust_for_shift_gap(start_time, duration):
    """
    核心时间调整函数：处理班次间隔和节假日
    start_time:datetime
    duration: int 分钟
    """
    # current_time = find_valid_time(start_time,duration)
    current_time = start_time
    remaining = duration
    total_gap = 0

    while remaining > 0:
        # 找到当前班次结束时间
        shift_end = _find_current_shift_end(current_time)
        if not shift_end:
            # print("找不到班次的结束时间")
            break

        # 计算当前班次剩余时间
        available_time = (shift_end - current_time).seconds // 60
        # print("available_time = ", available_time)
        if available_time >= remaining:
            return current_time + timedelta(minutes=remaining), total_gap
        else:
            remaining -= available_time
            current_time = shift_end

            # 找到下一个班次开始时间
            next_shift_start = _find_next_shift_start(shift_end)
            if next_shift_start:
                gap = (next_shift_start - shift_end).seconds // 60  # 分钟
                total_gap += gap
                current_time = next_shift_start  # + timedelta(minutes=remaining)
            else:
                break

    return current_time, total_gap
    # 返回的值 1.切换时间或染程的结束时间，格式为datetime 2.班次之间的间隔时间,格式为 int 分钟


start_time = datetime(2025, 4, 10, 9, 00, 00)
duration = 680
print("_find_current_shift_end()函数输出:", _find_current_shift_end(start_time))
# print(adjust_for_shift_gap(start_time, duration))  # 输出格式有问题，结果也有问题
# # (datetime.datetime(2025, 3, 11, 10, 40), 960)
# # print(datetime(2025, 3, 11, 10, 40))
end_time, gap = adjust_for_shift_gap(start_time, duration)
print("结束时间:", end_time)
print("间隔 gap:", gap)
#
# # 读取传入班制班次的最后一天
# def get_shift_last_day(json_dict)
test_time = find_valid_time(start_time)
print(test_time)


def reverse_adjust_for_shift_gap(end_time, duration):
    """
    反向计算：根据结束时间和持续时间，找到受班次影响的开始时间
    :param end_time: datetime 计划结束时间
    :param duration: int 持续时间（分钟）
    :return: (start_time, total_gap)
        - start_time: datetime 实际开始时间
        - total_gap: int 班次间隔总时间（分钟）
    """
    current_time = end_time
    if current_time is None:
        return None, 0

    remaining = duration
    total_gap = 0

    while remaining > 0:
        # 找到当前时间所在的班次开始时间
        shift_start = _find_current_shift_start(current_time)
        if not shift_start:
            break

        # 计算当前班次可用时间
        available_time = (current_time - shift_start).total_seconds() // 60
        if available_time >= remaining:
            start_time = current_time - timedelta(minutes=remaining)
            return start_time.replace(second=0), total_gap
        else:
            remaining -= available_time
            # current_time = shift_start
            current_time = shift_start - timedelta(minutes=1)

            # 找到前一个班次结束时间
            prev_shift_end = _find_previous_shift_end(current_time)
            if prev_shift_end:
                gap = (shift_start - prev_shift_end).total_seconds() // 60
                total_gap += gap
                current_time = prev_shift_end
            else:
                break
    print(f"[DEBUG-reverse] 输入 end_time={end_time}, duration={duration}")
    print(f"[DEBUG-reverse] 输出 start_time={current_time}, total_gap={total_gap}")

    return current_time, total_gap


# 新增辅助函数（需在 TimeAxisManager 中实现）
def _find_current_shift_start(time_point):
    """找到当前班次的开始时间"""
    # work_days = _parse_work_calendar(json_dict)
    shifts = _parse_shift_system(json_dict)
    for shift_start, shift_end in shifts:
        start_dt = datetime.combine(time_point.date(), shift_start)
        end_dt = datetime.combine(time_point.date(), shift_end)
        if shift_end < shift_start:
            end_dt += timedelta(days=1)
        if start_dt < time_point <= end_dt:
            return start_dt
    return None


def _find_previous_shift_end(time_point):
    """找到前一个班次的结束时间"""
    candidates = []
    work_days = _parse_work_calendar(json_dict)
    shifts = _parse_shift_system(json_dict)
    for day_offset in range(0, 4):
        check_date = time_point.date() - timedelta(days=day_offset)
        date_str = check_date.strftime("%Y-%m-%d")
        if not work_days.get(date_str, False):
            continue
        for shift_start, shift_end in reversed(shifts):
            end_dt = datetime.combine(check_date, shift_end)
            if shift_end < shift_start:
                end_dt += timedelta(days=1)
            if end_dt < time_point:
                candidates.append(end_dt)
    return max(candidates) if candidates else None


duration2 = 120
end_time2 = datetime(2025, 4, 20, 8, 17, 00)
shift_start = _find_current_shift_start(end_time2)
print("当前班次开始时间：", shift_start)
# shift_start = datetime(2025, 4, 10, 16, 00, 00)
#
prev_shift_end = _find_previous_shift_end(shift_start)
print("上一个班次的结束时间：", prev_shift_end)
(start_time2, gap2) = reverse_adjust_for_shift_gap(end_time2, duration2)
print("start_time2:", start_time2)
print("gap2:", gap2)


# shifts = _parse_shift_system(json_dict)
# work_days = _parse_work_calendar(json_dict)
# print("[DEBUG] 班次:", shifts)
# print("[DEBUG] 2025-04-10 是否工作日:", work_days.get("2025-04-10", False))
# print("[DEBUG] 当前班次开始时间:", _find_current_shift_start(datetime(2025, 4, 10, 12, 20)))

def compute_process_times(json_dict, routing_type, dyeing_start_time, dyeing_end_time):
    from datetime import timedelta
    from _Time_Axis_Manager import TimeAxisManager
    time_axis_manager = TimeAxisManager(json_dict)
    count = 0
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
    print("dyeing_start_time:", dyeing_start_time)
    dyeing_end_time = datetime.strptime(dyeing_end_time, "%Y-%m-%d %H:%M")
    print("dyeing_end_time:", dyeing_end_time)
    # process_times["DyeingProcessEndTime"] = dyeing_end_time#.strftime("%Y-%m-%d %H:%M")

    # 上游推算
    current_end = dyeing_start_time
    for step in reversed(routing_steps[:dyeing_index]):
        wait_time = int(step.get("StandardWaitingTime", 0) * 60)
        print("wait_time:", wait_time)
        prod_time = int(step.get("WorkCenterDetail", [{}])[0].get("StandardProductionTime", 0) * 60)
        print("prod_time:", prod_time)
        # current_end = current_start - timedelta(minutes=wait_time)
        # current_start = current_end - timedelta(minutes=prod_time)
        # current_end = current_start - timedelta(minutes=wait_time)
        current_end_shifted, _ =  time_axis_manager.reverse_adjust_for_shift_gap(current_end, wait_time)
        print("current_end_shifted:", current_end_shifted)
        current_start_shifted, _ = time_axis_manager.reverse_adjust_for_shift_gap(current_end_shifted, prod_time)
        print("current_start_shifted:", current_start_shifted)
        count += 1
        print(count)

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
        print("wait_time:", wait_time)
        prod_time = int(step.get("WorkCenterDetail", [{}])[0].get("StandardProductionTime", 0) * 60)
        print("prod_time:", prod_time)
        # current_start += timedelta(minutes=wait_time)
        # current_end = current_start + timedelta(minutes=prod_time)
        # current_start += timedelta(minutes=wait_time)
        # current_start_shifted = time_axis_manager.find_valid_time(current_start)
        count += 1
        current_start_shifted, _ = time_axis_manager.adjust_for_shift_gap(current_start, wait_time)
        print("current_start_shifted:", current_start_shifted)
        current_end_shifted, _ = time_axis_manager.adjust_for_shift_gap(current_start_shifted, prod_time)
        print("current_end_shifted:", current_end_shifted)
        print(count)
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


routing_type = 'TZZJH'
dyeing_start_time = "2024-04-18 08:17"
dyeing_end_time = "2024-04-18 14:22"

p = compute_process_times(json_dict, routing_type, dyeing_start_time, dyeing_end_time)
print(p)
