from django.urls import path
from ..views.htmx import berkeh_list, berkeh_detail

urlpatterns = [
    path("berkehs", berkeh_list, name="berkeh_list"),
    path("berkehs/<int:berkeh_id>", berkeh_detail, name="berkeh_detail"),
]
