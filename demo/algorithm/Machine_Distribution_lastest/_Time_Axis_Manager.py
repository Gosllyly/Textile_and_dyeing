import json
from datetime import datetime, timedelta
import bisect


class TimeAxisManager:
    def __init__(self, json_dict):
        self.json_dict = json_dict
        # self.work_days = {'2025-03-10': True, '2025-03-11': True, '2025-03-12': True, '2025-03-13': True,
        #                   '2025-03-14': True, '2025-03-15': True, '2025-03-16': False, '2025-03-17': True,
        #                   '2025-03-18': True, '2025-03-19': True, '2025-03-20': True, '2025-03-21': True,
        #                   '2025-03-22': True, '2025-03-23': False, '2025-03-24': True, '2025-03-25': True,
        #                   '2025-03-26': True, '2025-03-27': True, '2025-03-28': True, '2025-03-29': True,
        #                   '2025-03-30': False, '2025-03-31': True, '2025-04-01': True, '2025-04-02': True,
        #                   '2025-04-03': True, '2025-04-04': True, '2025-04-05': True, '2025-04-06': False,
        #                   '2025-04-07': True, '2025-04-08': True, '2025-04-09': True, '2025-04-10': True,
        #                   '2025-04-11': True, '2025-04-12': True, '2025-04-13': False, '2025-04-14': True,
        #                   '2025-04-15': True, '2025-04-16': True, '2025-04-17': True, '2025-04-18': True,
        #                   '2025-04-19': True, '2025-04-20': False, '2025-04-21': True, '2025-04-22': True,
        #                   '2025-04-23': True, '2025-04-24': True, '2025-04-25': True, '2025-04-26': True,
        #                   '2025-04-27': False, '2025-04-28': True, '2025-04-29': True, '2025-04-30': True,
        #                   '2025-05-01': True, '2025-05-02': True, '2025-05-03': True, '2025-05-04': False,
        #                   '2025-05-05': True, '2025-05-06': True, '2025-05-07': True, '2025-05-08': True,
        #                   '2025-05-09': True, '2025-05-10': True, '2025-05-11': False, '2025-05-12': True,
        #                   '2025-05-13': True, '2025-05-14': True, '2025-05-15': True, '2025-05-16': True,
        #                   '2025-05-17': True, '2025-05-18': False, '2025-05-19': True, '2025-05-20': True,
        #                   '2025-05-21': True, '2025-05-22': True, '2025-05-23': True, '2025-05-24': True,
        #                   '2025-05-25': False, '2025-05-26': True, '2025-05-27': True, '2025-05-28': True,
        #                   '2025-05-29': True, '2025-05-30': True, '2025-05-31': True, '2025-06-01': False,
        #                   '2025-06-02': True, '2025-06-03': True, '2025-06-04': True, '2025-06-05': True,
        #                   '2025-06-06': True, '2025-06-07': True, '2025-06-08': False, '2025-06-09': True,
        #                   '2025-06-10': True}
        self.work_days = self._parse_work_calendar(json_dict)
        self.shifts = self._parse_shift_system(json_dict)
        self.timeline = self._generate_timeline(json_dict)

    def _parse_work_calendar(self, json_dict):
        """
        解析工作日历数据
        work_days: 字典
        """
        work_days = {}
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
                date_str = item.get("Date", "").split()[0]
                if date_str:
                    work_days[date_str] = item.get("Productiondate", False)
        except Exception as e:
            print(f"[ERROR] 解析工作日历时出错: {str(e)}")
        # print(work_days)
        return work_days

    def _parse_shift_system(self, json_dict):
        """
        解析班次
        shifts: list
        """
        shifts = []
        # shift_system = [{'Shift': '漂染三厂早班', 'ClassStartTime': '08:00:00', 'ClassEndTime': '12:00:00'},
        #                 {'Shift': '漂染三厂中班', 'ClassStartTime': '12:00:00', 'ClassEndTime': '16:00:00'}]
        shift_system = self.json_dict.get("ShiftSystem", {}).get("漂染三厂班制", [])
        for shift in shift_system:
            try:
                start = datetime.strptime(shift["ClassStartTime"], "%H:%M:%S").time()
                end = datetime.strptime(shift["ClassEndTime"], "%H:%M:%S").time()
                shifts.append((start, end))
            except KeyError as e:
                print(f"班次数据格式错误: {e}")
        return shifts

    def _generate_timeline(self, json_dict):
        """
        生成分钟级生产时间轴
        timeline: list
        current_date 、end_date暂定这样
        """
        timeline = []
        # current_date = datetime(2025, 3, 10) # 测试用
        current_date = datetime.now().replace(microsecond=0) # 读取当前时间

        end_date = datetime(2030, 6, 15) # 改进成班制班次最后一天

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
                        timeline.append(current)
                        current += timedelta(minutes=1)
            current_date += timedelta(days=1)
        timeline.sort()
        return timeline

    def _find_current_shift_end(self, time_point):
        """
        找到当前班次结束时间
        time_point: datetime

        """
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
        """
        找到下一个班次开始时间
        time_point: datetime
        """
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
                if candidate >= time_point:
                    candidates.append(candidate)
        return min(candidates) if candidates else None

    def calculate_gap(self, start_time, end_time):
        """
        计算两个时间点之间的无效时间
        start_time: datetime
        end_time: datetime
        """
        gap = 0
        current = start_time
        while current < end_time:
            idx = bisect.bisect_left(self.timeline, current)
            if idx >= len(self.timeline) or self.timeline[idx] != current:
                gap += 1
            current += timedelta(minutes=1)
        return gap

    # def find_valid_time(self, start_time, duration):
    #     """
    #     找到最近的合法开始时间
    #     start_time: datetime
    #     duration : int 表示分钟数
    #     """
    #     duration = int(duration)
    #     idx = bisect.bisect_left(self.timeline, start_time)
    #     while idx < len(self.timeline):
    #         # 检查是否有足够的连续时间
    #         if idx + duration > len(self.timeline):
    #             return None
    #         expected_end = self.timeline[idx] + timedelta(minutes=duration)
    #         if self.timeline[idx + duration - 1] == expected_end - timedelta(minutes=1):
    #             return self.timeline[idx]
    #         idx += 1
    #     return None

    def find_valid_time(self, start_time):
        """
        找到最近的合法开始时间，允许跨班次和跨天。
        start_time: datetime
        """
        idx = bisect.bisect_left(self.timeline, start_time)
        if idx < len(self.timeline):
            return self.timeline[idx]
        return None  # 时间轴之外

    def minutes_to_datetime(self, minutes):
        """
        分钟数转时间对象
        minutes：int
        """
        # if minutes is None or not isinstance(minutes, (int, float)):
        #     raise ValueError(f"[ERROR] 非法 minutes 值: {minutes}")
        return datetime.now().replace(microsecond=0) + timedelta(minutes=minutes)

    def datetime_to_minutes(self, dt):
        """
        时间对象转分钟数

        """
        # base_date = datetime(2025, 3, 10)  # 以传入工作日历的第一天的零点为基准时间
        base_date = datetime.now().replace(microsecond=0)  # 以当前时间为基准时间
        return (dt - base_date).total_seconds() // 60

    # def minutes_to_datetime(self, minutes):
    #     """
    #     分钟数转时间对象
    #     minutes：int
    #     """
    #     # if minutes is None or not isinstance(minutes, (int, float)):
    #     #     raise ValueError(f"[ERROR] 非法 minutes 值: {minutes}")
    #     valid_time = self.find_valid_time(datetime.now().replace(microsecond=0))
    #     time = valid_time + timedelta(minutes=minutes)
    #     return time
    #
    # def datetime_to_minutes(self, dt):
    #     """
    #     时间对象转分钟数
    #
    #     """
    #     # base_date = datetime(2025, 3, 10)  # 以传入工作日历的第一天的零点为基准时间
    #     base_date = self.find_valid_time(datetime.now().replace(microsecond=0))  # 以当前时间为基准时间
    #     return (dt - base_date).total_seconds() // 60

    def adjust_for_shift_gap(self, start_time, duration):
        """
        核心时间调整函数：处理班次间隔和节假日
        start_time:datetime
        duration: int 分钟
        """
        current_time = self.find_valid_time(start_time)
        # current_time = start_time
        remaining = duration
        total_gap = 0

        while remaining > 0:
            # 找到当前班次结束时间
            shift_end = self._find_current_shift_end(current_time)
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
                next_shift_start = self._find_next_shift_start(shift_end)
                if next_shift_start:
                    gap = (next_shift_start - shift_end).seconds // 60  # 分钟
                    total_gap += gap
                    current_time = next_shift_start  # + timedelta(minutes=remaining)
                else:
                    break

        return current_time, total_gap
        # 返回的值 1.切换时间或染程的结束时间，格式为datetime 2.班次之间的间隔时间,格式为 int 分钟

    def reverse_adjust_for_shift_gap(self, end_time, duration):
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
            shift_start = self._find_current_shift_start(current_time)
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
                current_time = shift_start + timedelta(minutes=1)

                # 找到前一个班次结束时间
                prev_shift_end = self._find_previous_shift_end(current_time)
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
    def _find_current_shift_start(self, time_point):
        """找到当前班次的开始时间"""
        for shift_start, shift_end in self.shifts:
            start_dt = datetime.combine(time_point.date(), shift_start)
            end_dt = datetime.combine(time_point.date(), shift_end)
            if shift_end < shift_start:
                end_dt += timedelta(days=1)
            if start_dt < time_point <= end_dt:
                return start_dt
        return None

    def _find_previous_shift_end(self, time_point):
        """找到前一个班次的结束时间"""
        candidates = []
        for day_offset in range(0, 4):
            check_date = time_point.date() - timedelta(days=day_offset)
            date_str = check_date.strftime("%Y-%m-%d")
            if not self.work_days.get(date_str, False):
                continue
            for shift_start, shift_end in reversed(self.shifts):
                end_dt = datetime.combine(check_date, shift_end)
                if shift_end < shift_start:
                    end_dt += timedelta(days=1)
                if end_dt < time_point:
                    candidates.append(end_dt)
        return max(candidates) if candidates else None



# if __name__ == "__main__":
#     import json
#
#     # 加载你已有的 JSON 数据（或模拟一个）
#     with open("testjson.json", "r", encoding="utf-8-sig") as f:
#         json_data = json.load(f)
#
#     tam = TimeAxisManager(json_data)
#
#     end_time = datetime(2025, 4, 25, 8, 22)
#     duration = 120
#
#     start_time, gap = tam.reverse_adjust_for_shift_gap(end_time, duration)
#
#     print("反推开始时间:", start_time)
#     print("班次间隔:", gap)