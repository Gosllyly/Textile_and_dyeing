import datetime
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def UserLoginView(request):
    username = request.POST.get('username')  # 参数名需和前端一致
    password = request.POST.get('password')
    if username == "admin" and password == "admin":
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # 过期时间1小时
            'iat': datetime.datetime.utcnow()  # 签发时间
        }

        # 生成 token，SECRET_KEY 应该放在 settings.py 中
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        data_list = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "token": token
            }
        }
    elif username == "admin" and password != "admin":
        data_list = {
            "success": False,
            "code": 20001,
            "message": "密码错误",
            "data": {}
        }
    elif username != "admin":
        data_list = {
            "success": False,
            "code": 20001,
            "message": "用户名不存在",
            "data": {}
        }
    return JsonResponse(data_list)
