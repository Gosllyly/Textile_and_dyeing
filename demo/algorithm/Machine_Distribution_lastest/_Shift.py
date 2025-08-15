class ShiftSystem:
    def __init__(self, shift_type, shifts):
        """
        :param shift_type: 班制类型
        :param shifts: 班次列表，每个班次格式为 {"start": 8, "end": 16}
        """
        self.shift_type = shift_type
        self.shifts = shifts




    def adjust_time_by_shifts(start_time, processing_time, shift_system):
        """
        根据班制调整作业的开始和结束时间。
        :param start_time: 初始计算的开始时间（绝对时间，单位：小时）
        :param processing_time: 加工时间（单位：小时）
        :param shift_system: 班制对象（ShiftSystem）
        :return: 修正后的 (start_time, end_time)
        """
        current_time = start_time
        remaining_time = processing_time

        while remaining_time > 0:
            # 找到当前时间所在的班次
            current_shift = None
            current_day = current_time // 24  # 当前是第几天
            for shift in shift_system.shifts:
                shift_start = current_day * 24 + shift["start"]
                shift_end = current_day * 24 + shift["end"]
                if shift_start <= current_time < shift_end:
                    current_shift = shift
                    break

            if current_shift is None:
                # 当前时间不在任何班次内，跳到下一个班次的开始时间
                next_shift_start = _find_next_shift_start(current_time, shift_system)
                current_time = next_shift_start
                continue

            # 计算当前班次剩余时间
            shift_end_time = current_day * 24 + current_shift["end"]
            available_time = shift_end_time - current_time

            if available_time >= remaining_time:
                # 当前班次可以完成加工
                end_time = current_time + remaining_time
                remaining_time = 0
            else:
                # 当前班次只能完成部分加工
                current_time += available_time
                remaining_time -= available_time

        return start_time, end_time

    def _find_next_shift_start(current_time, shift_system):
        """找到下一个有效班次的开始时间"""
        current_day = current_time // 24
        next_day = current_day + 1

        # 检查当天剩余的班次
        for shift in shift_system.shifts:
            shift_start = current_day * 24 + shift["start"]
            if shift_start > current_time:
                return shift_start

        # 当天没有后续班次，跳到下一天的第一个班次
        first_shift_start = next_day * 24 + shift_system.shifts[0]["start"]
        return first_shift_start