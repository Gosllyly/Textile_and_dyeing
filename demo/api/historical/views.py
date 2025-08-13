from datetime import datetime
from pydoc import pager
from django.utils import timezone

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from demo.models import HistoricalResults


@csrf_exempt
def query(request):
    date = request.GET['date']
    page = int(request.GET['page'])
    pageSize = int(request.GET['pageSize'])

    try:
        query_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "日期格式错误",
            "data": {}
        })

    queryset = HistoricalResults.objects.filter(
        date=query_date
    ).order_by('-create_date')

    processed_data = []
    num = 1
    cur_page = 1
    total = 0
    for item in queryset:
        total = total + 1
        cur_data = {}
        cur_data['id'] = item.pk
        cur_data['date'] = item.date
        cur_data['orderData'] = item.orderData
        cur_data["dyeingVatData"] = item.dyeingVatData
        cur_data["secondaryData"] = item.secondaryData
        cur_data["modelId"] = item.modelId
        cur_data["num"] = num
        if cur_page == page:
            processed_data.append(cur_data)
        num += 1
        if num == pageSize + 1:
            cur_page += 1
            num = 1
    if processed_data == []:
        return JsonResponse({
            "success": True,
            "code": 20000,
            "message": "未查询到结果",
            "data": {}
        })
    else: return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "page" : page,
            "pageSize" : pageSize,
            "total" : total,
            "list": processed_data
        }
    })



@csrf_exempt
def main(request):
    page = int(request.GET['page'])
    pageSize = int(request.GET['pageSize'])
    queryset = HistoricalResults.objects.all().order_by('-create_date')
    processed_data = []
    num = 1
    cur_page = 1
    total = 0
    for item in queryset:
        total = total + 1
        cur_data = {}
        cur_data['id'] = item.pk
        cur_data['date'] = item.date
        cur_data['orderData'] = item.orderData
        cur_data["dyeingVatData"] = item.dyeingVatData
        cur_data["secondaryData"] = item.secondaryData
        cur_data["modelId"] = item.modelId
        cur_data["num"] = num
        if cur_page == page:
            processed_data.append(cur_data)
        num += 1
        if num == pageSize + 1:
            cur_page += 1
            num = 1
    if processed_data == []:
        return JsonResponse({
            "success": True,
            "code": 20000,
            "message": "暂无数据",
            "data": {}
        })
    else: return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "page" : page,
            "pageSize" : pageSize,
            "total" : total,
            "list": processed_data
        }
    })