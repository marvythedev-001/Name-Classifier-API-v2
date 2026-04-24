from django.urls import path
from .views import list_profiles, profiles, get_profile, delete_profile, search_profiles

urlpatterns = [
    # path("profiles", profiles, name="list_profile"),
    path("profiles/", profiles, name="create_profile"),
    path("profiles/<uuid:id>", get_profile),
    path("profiles/<uuid:id>/delete", delete_profile),
    path("profiles", list_profiles),
    path("profiles/search", search_profiles),
]