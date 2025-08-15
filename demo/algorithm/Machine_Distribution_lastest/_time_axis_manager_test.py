from datetime import datetime, timedelta
import bisect
import json


# 时间轴管理

class TimeAxisManager:
    def __init__(self, json_dict):  # 明确参数名称为json_dict
        self.json_dict = json_dict  # 存储原始JSON数据
        self.work_days = {'2025-03-10': True, '2025-03-11': True, '2025-03-12': True, '2025-03-13': True,
                          '2025-03-14': True, '2025-03-15': True, '2025-03-16': False, '2025-03-17': True,
                          '2025-03-18': True, '2025-03-19': True, '2025-03-20': True, '2025-03-21': True,
                          '2025-03-22': True, '2025-03-23': False, '2025-03-24': True, '2025-03-25': True,
                          '2025-03-26': True, '2025-03-27': True, '2025-03-28': True, '2025-03-29': True,
                          '2025-03-30': False, '2025-03-31': True, '2025-04-01': True, '2025-04-02': True,
                          '2025-04-03': True, '2025-04-04': True, '2025-04-05': True, '2025-04-06': False,
                          '2025-04-07': True, '2025-04-08': True, '2025-04-09': True, '2025-04-10': True,
                          '2025-04-11': True, '2025-04-12': True, '2025-04-13': False, '2025-04-14': True,
                          '2025-04-15': True, '2025-04-16': True, '2025-04-17': True, '2025-04-18': True,
                          '2025-04-19': True, '2025-04-20': False, '2025-04-21': True, '2025-04-22': True,
                          '2025-04-23': True, '2025-04-24': True, '2025-04-25': True, '2025-04-26': True,
                          '2025-04-27': False, '2025-04-28': True, '2025-04-29': True, '2025-04-30': True,
                          '2025-05-01': True, '2025-05-02': True, '2025-05-03': True, '2025-05-04': False,
                          '2025-05-05': True, '2025-05-06': True, '2025-05-07': True, '2025-05-08': True,
                          '2025-05-09': True, '2025-05-10': True, '2025-05-11': False, '2025-05-12': True,
                          '2025-05-13': True, '2025-05-14': True, '2025-05-15': True, '2025-05-16': True,
                          '2025-05-17': True, '2025-05-18': False, '2025-05-19': True, '2025-05-20': True,
                          '2025-05-21': True, '2025-05-22': True, '2025-05-23': True, '2025-05-24': True,
                          '2025-05-25': False, '2025-05-26': True, '2025-05-27': True, '2025-05-28': True,
                          '2025-05-29': True, '2025-05-30': True, '2025-05-31': True, '2025-06-01': False,
                          '2025-06-02': True, '2025-06-03': True, '2025-06-04': True, '2025-06-05': True,
                          '2025-06-06': True, '2025-06-07': True, '2025-06-08': False, '2025-06-09': True,
                          '2025-06-10': True}

        # self.work_days = self._parse_work_calendar()  # 格式: {"2025-03-10": True, ...}
        self.shifts = self._parse_shift_system()  # 格式: [(start_time, end_time), ...]
        self.timeline = self._generate_timeline()
        # self._parse_work_calendar()
        # self._parse_shift_system()
        # self._generate_timeline()

    # def _parse_work_calendar(self):
    #     """正确解析工作日历"""
    #     self.work_days = {}
    #     calendar_data = self.json_data["WorkCalendar"]["100.2"]
    #
    #     for item in calendar_data:
    #         if "Date" in item and "Productiondate" in item:
    #             date_str = item["Date"].split()[0]  # 提取日期部分
    #             self.work_days[date_str] = item["Productiondate"]
    def _parse_work_calendar(self):
        """解析工作日历数据"""
        self.work_days = {}
        try:
            calendar_container = self.json_dict.get("WorkCalendar", {})

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
                    self.work_days[date_str] = item.get("Productiondate", False)

        except Exception as e:
            print(f"[ERROR] 解析工作日历时出错: {str(e)}")
        return self.work_days

    def _parse_shift_system(self):
        """增强班次解析鲁棒性"""
        self.shifts = []
        # shift_system = self.json_dict.get("ShiftSystem", {}).get("漂染三厂班制", [])
        shift_system = [{'Shift': '漂染三厂中班', 'ClassStartTime': '12:00:00', 'ClassEndTime': '16:00:00'},
                        {'Shift': '漂染三厂早班', 'ClassStartTime': '08:00:00', 'ClassEndTime': '12:00:00'}]

        for shift in shift_system:
            try:
                start = datetime.strptime(shift["ClassStartTime"], "%H:%M:%S").time()
                end = datetime.strptime(shift["ClassEndTime"], "%H:%M:%S").time()
                self.shifts.append((start, end))
            except KeyError as e:
                print(f"班次数据格式错误: {e}")
        return self.shifts

    # def _parse_shift_system(self):
    #     """解析班次系统数据"""
    #     default_shifts = [
    #         (datetime.strptime("08:00:00", "%H:%M:%S").time(),
    #          datetime.strptime("20:00:00", "%H:%M:%S").time())
    #     ]
    #
    #     try:
    #         shift_system = self.json_data.get("ShiftSystem", {}).get("漂染三厂班制", [])
    #         self.shifts = []
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
    #             self.shifts.append((start, end))
    #
    #         if not self.shifts:
    #             self.shifts = default_shifts
    #
    #     except Exception as e:
    #         print(f"[WARNING] 使用默认班次: {str(e)}")
    #         self.shifts = default_shifts

    def _generate_timeline(self):
        """生成分钟级生产时间轴"""
        self.timeline = []
        current_date = datetime(2025, 3, 10)
        end_date = datetime(2025, 6, 10)

        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            if self.work_days.get(date_str, False):
                for shift_start, shift_end in self.shifts:
                    # 处理跨午夜班次
                    start_dt = datetime.combine(current_date.date(), shift_start)
                    end_dt = datetime.combine(current_date.date(), shift_end)
                    if shift_end < shift_start:
                        end_dt += timedelta(days=1)

                    # 生成时间点
                    current = start_dt
                    while current < end_dt:
                        self.timeline.append(current)
                        current += timedelta(minutes=1)

            current_date += timedelta(days=1)

        self.timeline.sort()
        return self.timeline

    # endregion

    def find_valid_time(self, start_time, duration):
        """找到最近的合法开始时间"""
        idx = bisect.bisect_left(self.timeline, start_time)
        while idx < len(self.timeline):
            # 检查是否有足够的连续时间
            if idx + duration > len(self.timeline):
                return None
            expected_end = self.timeline[idx] + timedelta(minutes=duration)
            if self.timeline[idx + duration - 1] == expected_end - timedelta(minutes=1):
                return self.timeline[idx]
            idx += 1
        return None

    # def find_valid_time(self, current_time, offset_minutes=0):
    #     """找到下一个有效生产时间点"""
    #     from bisect import bisect_left
    #     idx = bisect_left(self.timeline, current_time)
    #     if idx < len(self.timeline):
    #         return self.timeline[idx + offset_minutes]
    #     return None

    # 计算两个时间点之间的无效时间（空闲时间）
    def calculate_gap(self, start_time, end_time):
        """计算两个时间点之间的无效时间"""
        gap = 0
        current = start_time
        while current < end_time:
            # 使用二分查找快速判断是否在生产时间轴中
            idx = bisect.bisect_left(self.timeline, current)
            if idx >= len(self.timeline) or self.timeline[idx] != current:
                gap += 1
            current += timedelta(minutes=1)

        return gap

    def _find_current_shift_end(self, time_point):
        """找到当前班次结束时间"""
        for shift_start, shift_end in self.shifts:
            # 创建当天的时间对象
            start_dt = datetime.combine(time_point.date(), shift_start)
            end_dt = datetime.combine(time_point.date(), shift_end)

            # 处理跨午夜班次
            if shift_end < shift_start:
                end_dt += timedelta(days=1)

            if start_dt <= time_point < end_dt:
                return end_dt
        return None

    def _find_next_shift_start(self, time_point):
        """找到下一个班次开始时间"""
        candidates = []

        # 检查未来3天范围
        for day_offset in range(0, 4):
            check_date = time_point.date() + timedelta(days=day_offset)
            date_str = check_date.strftime("%Y-%m-%d")

            if not self.work_days.get(date_str, False):
                continue

            for shift_start, _ in self.shifts:
                candidate = datetime.combine(check_date, shift_start)

                # 过滤早于当前时间的候选
                if candidate > time_point:
                    candidates.append(candidate)

        return min(candidates) if candidates else None

# with open("20250310.json", "r", encoding="utf-8-sig") as f:
#     json_dict = json.load(f)
#     manager = TimeAxisManager(json_dict)  # 正确实例化
# print(manager.timeline)  # 访问生成的时间轴
