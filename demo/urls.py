from .api.user import views as UserViews
from .api.taskData import views as TaskDataViews
from .api.historical import views as HistoricalViews
from .api.modelBuild import views as ModelBuildViews
from .api.analysis import views as AnalysisViews
from django.urls import path, include
urlpatterns = [
    path('orderSchedule/', include([
        path('user/login/', UserViews.UserLoginView, name='user_login'),
        path('taskData/dateSelect/', TaskDataViews.dateSelect, name='dateSelect'),
        path('taskData/showOrderTable/', TaskDataViews.showOrderTable, name='showOrderTable'),
        path('taskData/dyeingVatTable/', TaskDataViews.dyeingVatTable, name='dyeingVatTable'),
        path('taskData/secondaryDataTable/', TaskDataViews.secondaryDataTable, name='secondaryDataTable'),
        path('taskData/submitJson/', TaskDataViews.submitJson, name='submitJson'),
        path('historical/query/', HistoricalViews.query, name='query'),
        path('historical/main/', HistoricalViews.main, name='main'),
        path('modelBuild/setParam/', ModelBuildViews.setParam, name='setParam'),
        path('modelBuild/getProgress/', ModelBuildViews.getProgress, name='getProgress'),
        path('analysis/overdueOrder/', AnalysisViews.overdueOrder, name='overdueOrder'),
        path('analysis/getCapacity/', AnalysisViews.getCapacity, name='getCapacity'),
        path('analysis/survivalBarChart/', AnalysisViews.survivalBarChart, name='survivalBarChart'),
    ])),
]