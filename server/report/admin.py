from django.contrib import admin
from .models import Report, ReportDecision, Appeal, AppealDecision
# Register your models here.
admin.site.register(Report)
admin.site.register(ReportDecision)
admin.site.register(Appeal)
admin.site.register(AppealDecision)