from django.contrib import admin
from BookStore.models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'target_user', 'listing', 'reason', 'created_at')
    list_filter = ('created_at', 'reason')
    search_fields = ('message', 'reason')