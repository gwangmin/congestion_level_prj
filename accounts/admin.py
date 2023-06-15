from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FacilityMgr

# Register your models here.
class FacilityMgrAdmin(admin.ModelAdmin):
    # search_fields = ['subject', ...] # 검색할 필드
    # readonly_fields = ('create_date', ...) # 수정 불가능한 필드
    pass

admin.site.register(FacilityMgr, FacilityMgrAdmin)
