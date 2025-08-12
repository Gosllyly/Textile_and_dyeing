import json
import os
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def dateSelect(request):
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
    endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

    if startDate > endDate:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "起始时间不能大于结束时间",
            "data": []
        })
    input_dir = './InputFiles'
    all_files = os.listdir(input_dir)
    matched_files = []
    for filename in all_files:
        if not filename.endswith('.json'):
            continue
        # 提取日期部分(前8个字符)
        date_str = filename[:8]
        file_date = datetime.strptime(date_str, '%Y%m%d').date()
        if startDate <= file_date <= endDate:
            matched_files.append({"orderData":filename})
    if len(matched_files) == 0:
        return JsonResponse({
            "success": True,
            "code": 20000,
            "message": "查询结果为空",
            "data": [matched_files]
        })
    else: return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": [matched_files]
    })



@csrf_exempt
def showOrderTable(request):
    page = int(request.POST.get('page'))
    pageSize = int(request.POST.get('pageSize'))
    file_name = request.POST.get('orderData')
    file_path = './InputFiles/' + file_name
    if not os.path.exists(file_path):
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "文件不存在",
            "data": {}
        })
    with open(file_path, 'r', encoding='GBK') as file:
        data = json.load(file)
    order = data['Order']
    processed_data = []
    num = 1
    cur_page = 1
    total = 0
    for items in order:
        for item in order[items]:
            total = total + 1
            cur_data = {}
            cur_data["priority"] = item["Priority"]
            cur_data["color"] = item["Color"]
            cur_data["colourNumber"] = item["ColourNumber"]
            cur_data["productionNumber"] = item["ProductionNumber"]
            cur_data["machineCapacity"] = item["MachineCapacity"]
            cur_data["axle"] = item["Axle"]
            cur_data["axleNumber"] = item["AxleNumber"]
            cur_data["num"] = num
            if cur_page == page:
                processed_data.append(cur_data)
            num += 1
            if num == pageSize + 1:
                cur_page += 1
                num = 1

    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "page" : page,
            "pageSize" : pageSize,
            "total" : total,
            "data": processed_data
        }
    })

@csrf_exempt
def dyeingVatTable(request):
    page = int(request.POST.get('page'))
    pageSize = int(request.POST.get('pageSize'))
    file_name = request.POST.get('dyeingVatData')
    file_path = './InputFiles/' + file_name
    if not os.path.exists(file_path):
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "文件不存在",
            "data": {}
        })
    with open(file_path, 'r', encoding='GBK') as file:
        data = json.load(file)
    Factory = data['Factory']
    processed_data = []
    num = 1
    cur_page = 1
    total = 0
    for factory in Factory:
        machine = Factory[factory]["Machine"]
        for items in machine:
            total = total + 1
            cur_data = {}
            item = machine[items]
            cur_data["machineId"] = item["MachineName"]
            cur_data["machineName"] = item["MachineName"]
            cur_data["machineClass"] = item["MachineClass"]
            cur_data["machineType"] = item["MachineType"]
            cur_data["color"] = item["Color"]
            cur_data["currentStatus"] = item["CurrentStatus"]
            cur_data["prevColor"] = item["PrevColor"]
            cur_data["num"] = num
            if cur_page == page:
                processed_data.append(cur_data)
            num += 1
            if num == pageSize + 1:
                cur_page += 1
                num = 1


    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "page" : page,
            "pageSize" : pageSize,
            "total" : total,
            "data": processed_data
        }
    })

@csrf_exempt
def secondaryDataTable(request):
    page = int(request.POST.get('page'))
    pageSize = int(request.POST.get('pageSize'))
    file_name = request.POST.get('secondaryData')
    file_path = './InputFiles/' + file_name
    if not os.path.exists(file_path):
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "文件不存在",
            "data": {}
        })
    with open(file_path, 'r', encoding='GBK') as file:
        data = json.load(file)
    Factory = data["Factory"]
    processed_data = []
    num = 1
    cur_page = 1
    total = 0
    for factory in Factory:
        SecRes = Factory[factory]["SecondaryResource"]
        YarnFrame = SecRes["YarnFrame"]
        for type in YarnFrame: # 纱架 蚕丝架
            for item_name in YarnFrame[type]:
                total += 1
                cur_data = {}
                item = YarnFrame[type][item_name]
                cur_data["identifier"] = item_name
                cur_data["type"] = type
                cur_data["machine"] = item["Machine"]
                cur_data["number"] = item["Number"]
                cur_data["num"] = num
                if cur_page == page:
                    processed_data.append(cur_data)
                num += 1
                if num == pageSize + 1:
                    cur_page += 1
                    num = 1

        AxleFrame = SecRes["AxleFrame"]
        for type in AxleFrame: # "S" "M" "L" "Y"
            for item_name in AxleFrame[type]:
                total += 1
                cur_data = {}
                item = AxleFrame[type][item_name]
                cur_data["identifier"] = item_name
                cur_data["type"] = "轴架" + type
                cur_data["machine"] = item["Machine"]
                cur_data["number"] = item["Number"]
                cur_data["num"] = num
                if cur_page == page:
                    processed_data.append(cur_data)
                num += 1
                if num == pageSize + 1:
                    cur_page += 1
                    num = 1

        Axle = SecRes["Axle"]
        for type in Axle:
            for item in Axle[type]:
                total += 1
                cur_data = {}
                cur_data["identifier"] = "轴"
                cur_data["number"] = Axle[type][item]["Number"]
                cur_data["type"] = type
                cur_data["machine"] = "漂染APS轴数"
                cur_data["num"] = num
                if cur_page == page:
                    processed_data.append(cur_data)
                num += 1
                if num == pageSize + 1:
                    cur_page += 1
                    num = 1

    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "page" : page,
            "pageSize" : pageSize,
            "total" : total,
            "data": processed_data
        }
    })