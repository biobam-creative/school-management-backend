from django.contrib import admin
from .models import Result, TermlyReportCard, ResultPdf, Csv

admin.site.register(Result)
admin.site.register(TermlyReportCard)
admin.site.register(ResultPdf)
admin.site.register(Csv)

