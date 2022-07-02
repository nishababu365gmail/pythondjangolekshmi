from django.contrib import admin
from lekshmiapp.models import (
    Sweets,
    Employee,
    Vendor,
    PurchaseMaster,
    ItemMaster,
    PurchaseDetail,
    State,
    City,
    course,
    student,
    studentcourse
)

# Register your models here.

admin.site.register(Sweets)
admin.site.register(Employee)
admin.site.register(Vendor)
admin.site.register(PurchaseMaster)
admin.site.register(ItemMaster)
admin.site.register(PurchaseDetail)
admin.site.register(State)
admin.site.register(City)
admin.site.register(course)
admin.site.register(student)
admin.site.register(studentcourse)
