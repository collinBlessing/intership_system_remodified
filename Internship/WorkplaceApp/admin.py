from django.contrib import admin
from .models import (
    studentDataTable,
    companyDataTable,
    flyerdata,
    studentfavorite,
    studentapply,
    message,
    StuNotification,
    ComNotification,
    StdntLog,
    lecturerDataTable,

)

admin.site.register(studentDataTable)
admin.site.register(companyDataTable)
admin.site.register(flyerdata)
admin.site.register(studentfavorite)
admin.site.register(studentapply)
admin.site.register(message)
admin.site.register(StuNotification)
admin.site.register(ComNotification)
admin.site.register(lecturerDataTable)


# make areas readonly
class StdntLogAdmin(admin.ModelAdmin):
    readonly_fields = (
        "stuid",
        "title",
        "date",
        "summary",
        "description",
        "lect_comment",
    )


admin.site.register(StdntLog, StdntLogAdmin)
