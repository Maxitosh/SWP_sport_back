from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.db.models import F
from django.utils.html import format_html

from sport.admin.utils import custom_order_filter
from sport.models import Reference
from .site import site


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


@admin.register(Reference, site=site)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "semester",
        "image",
        "uploaded",
        "approval",
    )

    list_filter = (
        StudentTextFilter,
        ("semester", custom_order_filter(("-start",))),
        "approval"
    )

    fields = (
        "student",
        "semester",
        "uploaded",
        "hours",
        "reference_image",
    )

    readonly_fields = (
        "uploaded",
        "reference_image",
    )

    autocomplete_fields = (
        "student",
    )

    ordering = (F("approval").asc(nulls_first=True), "uploaded")

    def reference_image(self, obj):
        return format_html('<a href="{}"><img style="width: 50%" src="{}" /></a>', obj.image.url, obj.image.url)

    reference_image.short_description = 'Reference'
    reference_image.allow_tags = True

    class Media:
        pass
