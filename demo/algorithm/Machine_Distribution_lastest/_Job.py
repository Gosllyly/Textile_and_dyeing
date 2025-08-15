class Job:
    def __init__(self, Job_index, Operation_num):
        self.Job_index = Job_index
        self.Operation_num = Operation_num
        self.Processed = []
        self.Last_Processing_end_time = 0
        self.J_start = []
        self.J_end = []
        self.J_machine = []
        self.J_worker = []
        self.Last_Processing_Machine = None

    def Current_Processed(self):
        return len(self.Processed)

    def _Input(self, W_Eailiest, End_time, Machine):  # 输入 1、最早开始时间 2、此工序的完工时间 3、选择的机器
        self.Processed.append(1)  # 填入数判断哪一道工序
        self.Last_Processing_Machine = Machine  # 更新上道工序的相关信息
        self.Last_Processing_end_time = End_time  # 更新上道工序的相关信息
        self.J_start.append(W_Eailiest)  # 储存此工序的信息 开始时间
        self.J_end.append(End_time)  # 结束时间
        self.J_machine.append(Machine)  # 选择机器
