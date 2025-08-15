import json
import os
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from demo.models import HistoricalResults


@csrf_exempt
def overdueOrder(request):
    id = int(request.GET.get('id'))
    page = int(request.GET.get('page'))
    pageSize = int(request.GET.get('pageSize'))
    try:
        result = HistoricalResults.objects.get(id=id)
    except HistoricalResults.DoesNotExist:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "传入的id未匹配到任何结果",
            "data": []
        })
    inputFile = result.orderData
    outputFile = result.outputFileName
    input_dir = './InputFiles'
    output_dir = './results'
    input_file_path = os.path.join(input_dir, inputFile)
    output_file_path = os.path.join(output_dir, outputFile)
    with open(input_file_path, 'r', encoding='GBK') as file:
        input_data = json.load(file)
    with open(output_file_path, 'r', encoding='utf-8') as file:
        output_data = json.load(file)
    processed_data = []
    Factory = input_data['Order']
    num = 1
    cur_page = 1
    total = 0
    for factory in Factory:
        orders = Factory[factory]
        for order in orders:
            if order['OrderStatus'] == "已完工":
                continue

            RequestDate = order['DyeDeliveryDate']
            OrderId = order['OrderId']
            processed_order = output_data[factory]["ByOrder"][OrderId]
            StartTime = processed_order["StartTime"]
            EndTime = processed_order["EndTime"]
            RequestDate = datetime.strptime(RequestDate, "%Y-%m-%d %H:%M:%S")
            EndTime = datetime.strptime(EndTime, "%Y-%m-%d %H:%M")
            if EndTime > RequestDate:
                total = total + 1
                diff = EndTime - RequestDate
                overtime = diff.days
                if cur_page == page:
                    processed_data.append({
                        "OrderId": OrderId,
                        "startTime": StartTime,
                        "endTime": EndTime.strftime("%Y-%m-%d %H:%M"),
                        "overtime": overtime,
                        "num": num
                    })
                num += 1
                if num == pageSize + 1:
                    cur_page += 1
                    num = 1
    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "page": page,
            "pageSize": pageSize,
            "total": total,
            "data": processed_data
        }
    })

@csrf_exempt
def getCapacity(request):
    id = int(request.GET.get('id'))
    try:
        result = HistoricalResults.objects.get(id=id)
    except HistoricalResults.DoesNotExist:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "传入的id未匹配到任何结果",
            "data": []
        })
    outputFile = result.outputFileName
    output_dir = './results'
    output_file_path = os.path.join(output_dir, outputFile)
    with open(output_file_path, 'r', encoding='utf-8') as file:
        output_data = json.load(file)
    list = []
    for factory in output_data:
        orders = output_data[factory]["ByOrder"]
        for order in orders:
            capacity = orders[order]["MachineCapacity"]
            if capacity not in list:
                list.append(capacity)

    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": sorted(list)
    })

@csrf_exempt
def survivalBarChart(request):
    machineCapacity = int(request.GET.get('machineCapacity'))
    id = int(request.GET.get('id'))
    try:
        result = HistoricalResults.objects.get(id=id)
    except HistoricalResults.DoesNotExist:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "传入的id未匹配到任何结果",
            "data": []
        })
    outputFile = result.outputFileName
    output_dir = './results'
    output_file_path = os.path.join(output_dir, outputFile)
    with open(output_file_path, 'r', encoding='utf-8') as file:
        output_data = json.load(file)
    processed_data = []
    macineId = 1
    for factory in output_data:
        machines = output_data[factory]["ByMachine"]
        for machine in machines:
            machine = machines[machine]
            if int(machine["MachineCapacity"]) != machineCapacity:
                continue
            first_flag = True
            StartTime = 0
            EndTime = 0
            for order in machine["Order"]:
                order = machine["Order"][order]
                if first_flag:
                    StartTime = order["StartTime"]
                    first_flag = False
                EndTime = order["EndTime"]
            start_dt = datetime.strptime(StartTime, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(EndTime, "%Y-%m-%d %H:%M")
            diff_seconds = (end_dt - start_dt).total_seconds() / 3600
            processed_data.append({
                "macineId": macineId,
                "machineCapacity": machineCapacity,
                "alive": round(diff_seconds,2)
            })
            macineId += 1
    if len(processed_data) == 0:
        return JsonResponse({
            "success": True,
            "code": 20000,
            "message": "传入的容量值未匹配到任何染缸",
            "data": []
        })
    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": processed_data
    })