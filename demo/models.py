from django.db import models


class HistoricalResults(models.Model):
    date = models.DateField(verbose_name='日期')
    orderData = models.CharField(max_length=255, verbose_name='订单数据')
    dyeingVatData = models.CharField(max_length=255, verbose_name='染缸数据')
    secondaryData = models.CharField(max_length=255, verbose_name='副资源数据')
    modelId = models.CharField(max_length=255, verbose_name='模型编号', null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        db_table = 'historical_results'  # 指定数据库表名
        verbose_name = '历史结果'
        verbose_name_plural = '历史结果'

    def __str__(self):
        return f"{self.date} - {self.modelId}"
