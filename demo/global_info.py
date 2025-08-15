import os
from datetime import datetime

collected_data = {}
# path_file 存放输入文件的文件路径 ( 目录 + 文件名字 )
# populationSize iterationNumber crossoverRate mutationRate nElite
# 五个模型参数
modal_start_timestamp = 0
def cal_timestamp():
    global modal_start_timestamp
    path = "./results"
    for result in os.listdir(path):
        time_str = result[7:-5]
        dt = datetime.strptime(time_str, "%Y%m%d_%H%M%S")
        timestamp = dt.timestamp()
        if timestamp > modal_start_timestamp:
            modal_start_timestamp = int(timestamp)

cal_timestamp()