from django.shortcuts import render
from rest_framework.response import Response

from api.models import Profile
from api.serializers import ProfileSerializer
from api.services import fetch_data
from rest_framework.decorators import api_view
# Create your views here.


def error(msg, code):
    return Response(
        {"status": "error", "message": msg},
        status=code
    )
    

@api_view(["POST"])
def create_profile(request):

    name = request.data.get("name")

    if name is None or name == "":
        return error("Missing or empty name", 400)

    if not isinstance(name, str):
        return error("Invalid type", 422)

    name = name.lower()

    existing = Profile.objects.filter(name=name).first()

    if existing:
        return Response({
            "status": "success",
            "message": "Profile already exists",
            "data": ProfileSerializer(existing).data
        })

    try:
        data = fetch_data(name)
    except Exception as e:
        return error(f"{str(e)} returned an invalid response", 502)

    profile = Profile.objects.create(name=name, **data)

    return Response(
        {
            "status": "success",
            "data": ProfileSerializer(profile).data,
        },
        status=201,
    )
    


   
@api_view(["GET"])
def get_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return error("Profile not found", 404)

    return Response({
        "status": "success",
        "data": ProfileSerializer(profile).data
    })
    

@api_view(["GET"])
def list_profiles(request):

    qs = Profile.objects.all()

    gender = request.GET.get("gender")
    country = request.GET.get("country_id")
    age_group = request.GET.get("age_group")

    if gender:
        qs = qs.filter(gender__iexact=gender)

    if country:
        qs = qs.filter(country_id__iexact=country)

    if age_group:
        qs = qs.filter(age_group__iexact=age_group)

    data = [
        {
            "id": str(p.id),
            "name": p.name,
            "gender": p.gender,
            "age": p.age,
            "age_group": p.age_group,
            "country_id": p.country_id,
        }
        for p in qs
    ]

    return Response({
        "status": "success",
        "count": len(data),
        "data": data,
    })
    
    
@api_view(["DELETE"])
def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return error("Profile not found", 404)

    profile.delete()
    return Response(status=204)