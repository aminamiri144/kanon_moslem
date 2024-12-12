from django.db import models

# Create your models here.
from django.db import models


# Create your models here.


class Logger(models.Model):
    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = "گزارش ها"

    LOG_TYPES = (
        ('SMS', 'sms'),
        ('SYSTEM', 'system'),
        ('CELETY_MAIN', 'celery main'),
        ('CELERY_BEAT', 'celery beat'),
    )

    type = models.CharField(max_length=30, choices=LOG_TYPES, default='SYSTEM')
    text = models.TextField(blank=True, null=True)
    decs = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} - {self.created_time}'
