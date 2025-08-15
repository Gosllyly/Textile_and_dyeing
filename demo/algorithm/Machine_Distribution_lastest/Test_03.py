def iterative_process(num_iterations):
    # 打开文件以写入模式，如果文件不存在则创建一个新的
    with open('output.txt', 'w') as f:
        for i in range(num_iterations):
            # 执行一些计算或处理
            result = some_function(i)

            # 将结果写入文件
            f.write(f"Iteration {i}: Result = {result}\n")

            # 输出到控制台
            print(f"Iteration {i}: Result = {result}")


def some_function(test_list):
    f = open('log_message.txt', 'w')
    obj_list = []
    for i in range(len(test_list)):
        obj = test_list[i][0]
        f.write(f"Iteration {i}: obj = {obj}\n")
        obj_list.append(obj)
    return obj_list


if __name__ == "__main__":
    # 设定迭代次数
    list_01 = [[1, 2], [3, 4], [5, 6], [7, 8]]
    some_function(list_01)
