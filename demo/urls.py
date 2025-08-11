
from django.urls import path
from .api.user import views as UserViews
from .api.taskData import views as TaskDataViews

urlpatterns = [
    path('user/login/', UserViews.UserLoginView, name='user_login'),
    path('taskData/dateSelect/', TaskDataViews.dateSelect, name='dateSelect'),
    path('taskData/showOrderTable/', TaskDataViews.showOrderTable, name='showOrderTable'),
    path('taskData/dyeingVatTable/', TaskDataViews.dyeingVatTable, name='dyeingVatTable'),
]