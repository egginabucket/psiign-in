from django.contrib import admin

from attendance import models

@admin.register(models.Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_active",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]
    list_filter = [
        "is_active"
    ]
    actions = [
        "activate",
        "deactivate",
    ]
    @admin.action()
    def activate(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action()
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(models.LearnerRecord)
class LearnerRecordAdmin(admin.ModelAdmin):
    list_display = [
        "learner",
        "time",
        "action",
        "notes",
    ]
    search_fields = [
        "learner__first_name",
        "learner__last_name",
        "learner__email",
    ]