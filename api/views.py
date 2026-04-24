from django.shortcuts import render
from rest_framework.response import Response

from api.models import Profile
from api.serializers import ProfileSerializer
from api.services import fetch_data
from rest_framework.decorators import api_view

from django.core.paginator import Paginator
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
    

@api_view(["GET", "POST"])
def profiles(request):
    # Handle POST -> create profile
    if request.method == "POST":
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

    # Handle GET -> list profiles with optional filters
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


@api_view(["GET"])
def list_profiles(request):

    qs = Profile.objects.all()

    # ---------- FILTERS ----------
    gender = request.GET.get("gender")
    age_group = request.GET.get("age_group")
    country_id = request.GET.get("country_id")

    min_age = request.GET.get("min_age")
    max_age = request.GET.get("max_age")

    min_gp = request.GET.get("min_gender_probability")
    min_cp = request.GET.get("min_country_probability")

    if gender:
        qs = qs.filter(gender__iexact=gender)

    if age_group:
        qs = qs.filter(age_group__iexact=age_group)

    if country_id:
        qs = qs.filter(country_id__iexact=country_id)

    if min_age:
        qs = qs.filter(age__gte=int(min_age))

    if max_age:
        qs = qs.filter(age__lte=int(max_age))

    if min_gp:
        qs = qs.filter(gender_probability__gte=float(min_gp))

    if min_cp:
        qs = qs.filter(country_probability__gte=float(min_cp))

    # ---------- SORTING ----------
    sort_by = request.GET.get("sort_by", "created_at")
    order = request.GET.get("order", "asc")

    allowed = ["age", "created_at", "gender_probability"]

    if sort_by not in allowed:
        return error("Invalid query parameters", 400)
    
    order = request.GET.get("order", "asc")

    if order not in ["asc", "desc"]:
        return error("Invalid query parameters", 400)

    if order == "desc":
        sort_by = f"-{sort_by}"

    qs = qs.order_by(sort_by)

    # ---------- PAGINATION ----------
    page = int(request.GET.get("page", 1))
    limit = min(int(request.GET.get("limit", 10)), 50)

    paginator = Paginator(qs, limit)
    page_obj = paginator.get_page(page)    

    data = list(page_obj.object_list.values())

    return Response({
        "status": "success",
        "page": page,
        "limit": limit,
        "total": paginator.count,
        "data": data
    })
    
    
from .parser import parse_query


@api_view(["GET"])
def search_proles(request):

    q = request.GET.get("q")

    if not q:
        return error("Missing or empty parameter", 400)

    filters = parse_query(q)

    if filters is None:
        return error("Unable to interpret query", 400)

    request.GET._mutable = True
    for k, v in filters.items():
        request.GET[k] = v

    return list_profiles(request)


@api_view(["GET"])
def search_profiles(request):

    q = request.GET.get("q")

    if not q:
        return error("Missing or empty parameter", 400)

    filters = parse_query(q)

    if filters is None:
        return error("Unable to interpret query", 400)

    # Apply filters directly
    qs = Profile.objects.all()

    if "gender" in filters:
        qs = qs.filter(gender__iexact=filters["gender"])

    if "age_group" in filters:
        qs = qs.filter(age_group__iexact=filters["age_group"])

    if "country_id" in filters:
        qs = qs.filter(country_id__iexact=filters["country_id"])

    if "min_age" in filters:
        qs = qs.filter(age__gt=filters["min_age"])

    if "max_age" in filters:
        qs = qs.filter(age__lte=filters["max_age"])

    # Pagination (reuse logic safely)
    page = int(request.GET.get("page", 1))
    limit = min(int(request.GET.get("limit", 10)), 50)

    paginator = Paginator(qs, limit)
    page_obj = paginator.get_page(page)

    data = list(page_obj.object_list.values())

    return Response({
        "status": "success",
        "page": page,
        "limit": limit,
        "total": paginator.count,
        "data": data
    })