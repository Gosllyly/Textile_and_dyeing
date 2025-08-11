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
    if not request.FILES:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "未检测到上传文件",
            "data": []
        })
    uploaded_file = request.FILES['orderData']
    # 检查文件扩展名
    if not uploaded_file.name.endswith('.json'):
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "上传文件必须为json格式",
            "data": []
        })

    # 读取并解析JSON文件
    file_content = uploaded_file.read().decode('GBK')
    original_data = json.loads(file_content)
    print(original_data)

    # selected_fields = [
    #     'order_id',
    #     'customer_name',
    #     'order_date',
    #     'total_amount',
    #     'status'
    # ]
    #
    # # 构建新的JSON数据
    # processed_data = {}
    # for field in selected_fields:
    #     if field in original_data:
    #         processed_data[field] = original_data[field]
    #     else:
    #         processed_data[field] = None  # 或者可以设置为默认值
    #
    # # 返回处理后的数据
    # return JsonResponse({
    #     "success": True,
    #     "message": "数据处理成功",
    #     "data": processed_data
    # })

@csrf_exempt
def dyeingVatTable(request):
    print(request.FILES)
    if not request.FILES:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "未检测到上传文件",
            "data": []
        })
    uploaded_file = request.FILES['dyeingVatData']
    # 检查文件扩展名
    if not uploaded_file.name.endswith('.json'):
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "上传文件必须为json格式",
            "data": []
        })

    # 读取并解析JSON文件
    file_content = uploaded_file.read().decode('GBK')
    original_data = json.loads(file_content)

    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": []
    })