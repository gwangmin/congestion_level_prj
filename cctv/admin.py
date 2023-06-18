from django.contrib import admin
from .models import *

# Register your models here.
class FacilityAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 검색할 필드
    readonly_fields = () # 수정 불가능한 필드

admin.site.register(Facility, FacilityAdmin)


class BuildingAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 검색할 필드
    readonly_fields = ('congest_lv',) # 수정 불가능한 필드

admin.site.register(Building, BuildingAdmin)


class CCTVAdmin(admin.ModelAdmin):
    # search_fields = [] # 검색할 필드
    # readonly_fields = ('computed_congest_lv',) # 수정 불가능한 필드
    pass

admin.site.register(CCTV, CCTVAdmin)


class StatisticsAdmin(admin.ModelAdmin):
    # search_fields = [] # 검색할 필드
    # readonly_fields = () # 수정 불가능한 필드
    pass

admin.site.register(Statistics, StatisticsAdmin)
