import Machine_Distribution_lastest._Time_Axis_Manager
class Machine_Time_window:
    def __init__(self, Machine_index, machine_message, decode):
        self.Machine_index = Machine_index
        self.assigned_task = []
        self.worker_for_task = []
        self.O_start = []
        self.O_end = []
        self.End_time = 0
        self.CurrentStatus = machine_message[Machine_index]['CurrentStatus']
        self.d = decode
        # self.time_manager = _Time_Axis_Manager.TimeAxisManager(json_dict)

    # 机器的哪些时间窗是空的,此处只考虑内部封闭的时间窗
    def Empty_time_window(self):
        time_window_start = []
        time_window_end = []
        len_time_window = []
        if self.O_end is None:
            pass
        elif len(self.O_end) == 1:  # O_end数组内有一个数
            if self.O_start[0] != 0:  # 已存在的开始时间若不为0
                time_window_start = [0]  # 空闲时间窗开始
                time_window_end = [self.O_start[0]]  # 空闲时间窗结束
        elif len(self.O_end) > 1:  # O_end数组内有不只一个数
            if self.O_start[0] != 0:  # 已存在的开始时间若不为0
                time_window_start.append(0)
                time_window_end.append(self.O_start[0])
            time_window_start.extend(self.O_end[:-1])  # 因为使用时间窗的结束点就是空时间窗的开始点，填入除最后一个时间外的时间
            time_window_end.extend(self.O_start[1:])  # 填入除第一个时间外的时间
        if time_window_end is not None:
            len_time_window = [time_window_end[i] - time_window_start[i] for i in range(len(time_window_end))]  # 可供使用的时间窗
        return time_window_start, time_window_end, len_time_window

    # def Machine_Burden(self):
    #     if len(self.O_start) == 0:
    #         burden = 0
    #     else:
    #         processing_time = [self.O_end[i] - self.O_start[i] for i in range(len(self.O_start))]
    #         burden = sum(processing_time)
    #     return burden

    def _Input(self, Job, M_Ealiest, P_t, O_num):  # 输入 工件编号 1、最早开始时间 2、加工所需时间 3、工序号
        if self.O_end != []:  # 有时间窗可供使用
            if self.O_start[-1] > M_Ealiest:  # 最后一个时间窗的开始时间是否大于（某工件）最早开始时间，即有换顺序
                for i in range(len(self.O_end)):
                    if self.O_start[i] >= M_Ealiest:
                        self.assigned_task.insert(i, [Job + 1, O_num + 1])
                        break
            else:  # 没有换顺序的
                self.assigned_task.append([Job + 1, O_num + 1])
        else:  # 没有时间窗可用，不换顺序
            self.assigned_task.append([Job + 1, O_num + 1])  # 在最后加入
        self.O_start.append(M_Ealiest)
        self.O_start.sort()
        start_datetime = self.d.minutes_to_datetime(M_Ealiest)
        end_datetime, _ = self.d.adjust_for_shift_gap(start_datetime, P_t)
        End_work_time = self.d.datetime_to_minutes(end_datetime)
        self.O_end.append(End_work_time) # 调整结束时间
        # self.O_end.append(M_Ealiest + P_t)
        self.O_end.sort()
        self.End_time = self.O_end[-1]
