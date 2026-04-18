from django.urls import path
from .views import *

urlpatterns = [
    path("profiles", list_profiles, name="list_profile"),
    path("profiles", create_profile, name="create_profile"),
    path("profiles/<uuid:id>", get_profile),
    path("profiles/<uuid:id>/delete", delete_profile),
]