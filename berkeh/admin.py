from django.contrib import admin
from .models import Berkeh, Location, BerkehPhoto, Comment

admin.site.register(Comment)


class BerkehPhotoInline(admin.TabularInline):
    model = BerkehPhoto
    extra = 1
    show_change_link = False


@admin.register(Berkeh)
class BerkehAdmin(admin.ModelAdmin):
    list_display = ("code",)
    search_fields = ("code", "location__city")
    actions = ["generate_berkeh_code"]
    inlines = [BerkehPhotoInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "village", "district")
    search_fields = ("country", "province", "county", "city", "village", "district")
    list_filter = ("country", "province", "county")
