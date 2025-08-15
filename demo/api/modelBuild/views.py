import threading

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from demo.algorithm.run_model import run_model
from demo.global_info import collected_data
from demo.models import HistoricalResults


@csrf_exempt
def setParam(request):
    try:
        collected_data["populationSize"] = int(request.GET.get("populationSize"))
        collected_data["iterationNumber"] = int(request.GET.get("iterationNumber"))
        collected_data["crossoverRate"] = float(request.GET.get("crossoverRate"))
        collected_data["mutationRate"] = float(request.GET.get("mutationRate"))
        collected_data["nElite"] = float(request.GET.get("nElite"))

    except Exception as e:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "模型参数获取失败",
            "data": []
        })

    if "path_file" not in collected_data:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "模型参数设置成功，但检测到输入文件为空",
            "data": []
        })

    def background_task():
        data = collected_data
        output_file = run_model(
            data["populationSize"], data["crossoverRate"],
            data["mutationRate"], data["nElite"],
            data["iterationNumber"], data["path_file"]
        )
        latest_record = HistoricalResults.objects.order_by('-id').first()
        input_file = latest_record.orderData
        temp_record = (
            HistoricalResults.objects
            .filter(orderData=input_file)  # 找 orderData 一样的
            .exclude(modelId__isnull=True)
            .order_by('-modelId')  # 按 modelId 降序
            .first()  # 取 modelId 最大的那条
        )
        modelId = 1
        if temp_record is not None:
            modelId = temp_record.modelId + 1
        latest_record.modelId = modelId
        latest_record.outputFileName = output_file
        latest_record.save()

    threading.Thread(target=background_task, daemon=True).start()
    latest_record = HistoricalResults.objects.order_by('-id').first()
    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "模型参数设置成功，正在求解",
        "data": {
            "id" : latest_record.id
        }
    })


@csrf_exempt
def getProgress(request):
    id = int(request.GET.get("id"))
    populationSize = int(request.GET.get("populationSize"))
    timeDifference = int(request.GET.get("timeDifference"))
    try:
        result = HistoricalResults.objects.get(id=id)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "code": 20001,
            "message": "传入的id未匹配到数据",
            "data": {}
        })
    if result.outputFileName is not None:
        return JsonResponse({
            "success": True,
            "code": 20000,
            "message": "模型结果计算完成！",
            "data": {
                "progress": 100,
                "status": True
            }
        })
    total_time = 65 + (populationSize / 100 - 1) * 50
    # 根据前端传的种群数，公式：种群数100的时候，是1分05秒，每多100，就+50秒
    progress = round(timeDifference / total_time * 100,1)
    progress = max(progress, 99.0)
    return JsonResponse({
        "success": True,
        "code": 20000,
        "message": "模型仍在计算中，请稍候！",
        "data": {
            "progress": progress,
            "status": False
        }
    })