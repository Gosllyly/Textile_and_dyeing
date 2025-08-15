import json
from datetime import datetime
import copy


# 读取 JSON 文件
with open("20250310.json", 'r', encoding='utf-8-sig') as f:
    json_dict = json.load(f)
    # print(data)
    print(json_dict.keys())  # 检查字典的顶层键


# 读取工作日历以及班制班次
def Get_Work_Valendar_and_Shifts(json_dict):
    # 提取工作日历
    work_calendar = json_dict.get('WorkCalendar', {})

    # 提取班制班次
    shift_system = json_dict.get('ShiftSystem', {})

    return work_calendar, shift_system


def get_work_calendar(json_dict):
    work_calendar = json_dict["WorkCalendar"]["100.2"]
    work_days = [
        {
            "date": datetime.strptime(entry["Date"], "%Y-%m-%d %H:%M:%S"),
            "is_production": entry["Productiondate"]
        }
        for entry in work_calendar
    ]
    return work_days
# print(get_work_calendar(json_dict))
'''
# 读取工作日历（WorkCalendar）
def get_work_calendar(json_dict):
    work_calendar = json_dict["WorkCalendar"]["100.2"]  
    work_days = [
        {
            "date": datetime.strptime(entry["Date"], "%Y-%m-%d %H:%M:%S"),
            "is_production": entry["Productiondate"]
        }
        for entry in work_calendar
    ]

# 读取班制班次（ShiftSystem）
def get_work_shifts(json_dict):
    shift_system = data["ShiftSystem"]["漂染三厂班制"]
    shifts = [
        {
            "shift_name": entry["Shift"],
            "start_time": entry["ClassStartTime"],
            "end_time": entry["ClassEndTime"]
        }
        for entry in shift_system
    ]
'''


# 读取数据并展示
def Display_Schedule(json_dict):
    work_calendar, shift_system = Get_Work_Valendar_and_Shifts(json_dict)

    # 打印工作日历内容
    print("Work Calendar:")
    for key, value in work_calendar.items():
        print(f"  {key}:")
        for day in value:
            print(f"    Date: {day['Date']}, Production Date: {day['Productiondate']}")

    # 打印班制班次内容
    print("\nShift System:")
    for factory, shifts in shift_system.items():
        print(f" {factory}:")
        for shift in shifts:
            print(f" Shift: {shift['Shift']}, Start Time: {shift['ClassStartTime']}, End Time: {shift['ClassEndTime']}")


# Display_Schedule(json_dict)  # 展示工作日历以及班制班次


# 读取传给算法的工作日历的总天数以及工作日历中进行生产的天数
def Get_Days_num(json_dict):
    """
    :param json_dict:
    :return: (所给工作日历的天数,生产日（Productiondate = True）的天数)
    """
    Total_days_num = 0  # 工作日历所涉及到的总天数
    Production_days_num = 0  # 工作日历中进行生产作业的总天数
    workcalendar = json_dict["WorkCalendar"]["100.2"]
    # 统计工作日历所涉及到的总天数
    for i in workcalendar:
        Total_days_num += 1
    # 统计生产日（Productiondate = True）的天数
    Production_days_num = sum(1 for entry in workcalendar if entry.get("Productiondate", True))
    return Total_days_num, Production_days_num


# print(Get_Days_num(json_dict))


def datetime_to_minutes(dt):
    """时间对象转分钟数"""
    base_date = datetime(2025, 3, 10)  # 与实际基准日期一致

    return (dt - base_date).total_seconds() // 60


# dt = datetime(2025, 4, 2, 8, 30)
# print(datetime_to_minutes(dt))

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
    # pop_json_dict: 删除执行后的; json_dict: 原本的

from input_fun import Get_New_Job_dict,organize_dict
# new_job_dict = Get_New_Job_dict(json_dict)
# new_job_dict01 = list(new_job_dict.values())
# new_job_dict02 = new_job_dict01[0][0]['标识号']
# print(new_job_dict02)

json_dict = process_json(json_dict)[0]      # 去掉执行中的
all_json_dict = process_json(json_dict)[1]  # 全部的
Old_Job_dict = Get_New_Job_dict(json_dict)  # 未考虑合作序号的订单列表
print("未考虑合作之前订单数量", len(Old_Job_dict))
print(Old_Job_dict)

new_job_dict = organize_dict(Old_Job_dict)
# 考虑合作序号的订单列表
new_job_list = list(new_job_dict.values())
# print(new_job_list)
print("未考虑合作之后订单数量", len(new_job_dict))
# new_job_dict02 = new_job_dict01[0][0]['标识号']
# print("new_job_dict", new_job_dict)
#print("new_job_list", new_job_list)
'''
Old_Job_dict的数据格式是字典，形式为：{k:[{}],}
new_job_list的数据格式是列表，形式为：[[{}],[{}],[{}]]

'''
# for job_id, job_info in new_job_dict.items():
#     print(job_info[0])
    # print(job_info[0]['标识号'])
    # date_str = job_info[0]['计划漂染完成日期'].strip()
    # print(date_str)
    # # 去除首尾空格/换行符
    # # date = datetime.strptime(date_str, "%Y-%m-%d  %H:%M:%S")
    # # print(date)
    # print(job_info[0]['计划漂染完成日期'])
    # print(type(job_info[0]['计划漂染完成日期']))  # 应输出 <class 'str'> 是字符串没问题
    # job_info[0]['计划漂染完成日期'].strip()
# delivery_dates = {
#     job_info[0]['标识号']: datetime.strptime(job_info[0]['计划漂染完成日期'], "%Y-%m-%d %H:%M:%S")
#     for job_id, job_info in new_job_dict.items()
# }



def Get_Delivery_Dates(new_job_dict):
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
                print(f"标识号 {job_info[0].get('标识号', '未知')} 的计划漂染日期为空，已替换为 {max_date}")
                delivery_dates[job_info[0]['标识号']] = max_date
    return delivery_dates

print(Get_Delivery_Dates(Old_Job_dict))
print(len(Get_Delivery_Dates(Old_Job_dict)))
print(len(Get_Delivery_Dates(new_job_dict)))
# delivery_dates = {
#     job_info[0]['标识号']: datetime.strptime(job_info[0]['计划漂染完成日期'], "%Y-%m-%d %H:%M:%S")
#     for job_id, job_info in new_job_dict.items()
#     if job_info[0]['计划漂染完成日期']  # 过滤掉空字符串或 None
# }
# print(Get_Delivery_Dates(new_job_dict).get('4736588'))  # 输出：2025-05-05 00:00:00
# 数据报错处理
for job_id, job_info in new_job_dict.items():
    if not job_info[0]['计划漂染完成日期']:  # 如果为空
        print(f"标识号 {job_info[0].get('标识号', '未知')} 的计划漂染日期是空值")




    # for job in self.Jobs:
    #     order_id = self.job_message_list[0][0]['标识号'] # job.Job_index
    #     # 获取计划结束时间（分钟转datetime）
    #     end_time = self.minutes_to_datetime(job.J_end[-1]) if job.J_end else None
    #     # 获取交期时间
    #     delivery_date = self.delivery_dates.get(order_id)