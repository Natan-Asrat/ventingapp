import django_filters
from .models import Report

class ReportFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="report_type", lookup_expr="iexact")
    dismissed = django_filters.BooleanFilter(field_name="dismissed")
    concluded = django_filters.BooleanFilter(field_name="concluded")

    class Meta:
        model = Report
        fields = ["type", "dismissed", "concluded"]
