from django.urls import path
from .views import profiles, get_profile, delete_profile

urlpatterns = [
    path("profiles", profiles, name="list_profile"),
    path("profiles/", profiles, name="create_profile"),
    path("profiles/<uuid:id>", get_profile),
    path("profiles/<uuid:id>/delete", delete_profile),
]