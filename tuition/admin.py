from django.contrib import admin
from .models import TuitionTerm, Tuition, Payment, PayDay

admin.site.register(TuitionTerm)
admin.site.register(Tuition)
admin.site.register(Payment)
admin.site.register(PayDay)
