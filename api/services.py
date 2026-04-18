import requests


def age_group(age):
    if 0 <= age <= 12:
        return "child"
    elif 13 <= age <= 19:
        return "teenager"
    elif 20 <= age <= 59:
        return "adult"
    return "senior"


def fetch_data(name):

    gender = requests.get(
        f"https://api.genderize.io?name={name}"
    ).json()

    if gender.get("gender") is None or gender.get("count") == 0:
        raise Exception("Genderize")

    agify = requests.get(
        f"https://api.agify.io?name={name}"
    ).json()

    if agify.get("age") is None:
        raise Exception("Agify")

    nationalize = requests.get(
        f"https://api.nationalize.io?name={name}"
    ).json()

    countries = nationalize.get("country")

    if not countries:
        raise Exception("Nationalize")

    best = max(countries, key=lambda x: x["probability"])

    return {
        "gender": gender["gender"],
        "gender_probability": gender["probability"],
        "sample_size": gender["count"],
        "age": agify["age"],
        "age_group": age_group(agify["age"]),
        "country_id": best["country_id"],
        "country_probability": best["probability"],
    }