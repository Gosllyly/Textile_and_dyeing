import json
import os
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from demo.models import HistoricalResults


@csrf_exempt
def overdueOrder(request):
    id = request.GET.get('id')
    try:
        result = HistoricalResults.objects.get(id=id)
        inputFile = result.orderData
        outputFile = result.outputFileName
    except HistoricalResults.DoesNotExist:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "传入的id未匹配到任何结果",
            "data": []
        })

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
    tot = 0
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
                diff = EndTime - RequestDate
                overtime = diff.days
                processed_data.append({
                    "OrderId": OrderId,
                    "startTime": StartTime,
                    "endTime": EndTime.strftime("%Y-%m-%d %H:%M"),
                    "overtime": overtime
                })
    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": processed_data
    })


