from .api.user import views as UserViews
from .api.taskData import views as TaskDataViews
from django.urls import path, include
urlpatterns = [
    path('orderSchedule/', include([
        path('user/login/', UserViews.UserLoginView, name='user_login'),
        path('taskData/dateSelect/', TaskDataViews.dateSelect, name='dateSelect'),
        path('taskData/showOrderTable/', TaskDataViews.showOrderTable, name='showOrderTable'),
        path('taskData/dyeingVatTable/', TaskDataViews.dyeingVatTable, name='dyeingVatTable'),
        path('taskData/secondaryDataTable/', TaskDataViews.secondaryDataTable, name='secondaryDataTable'),
    ])),
]