COUNTRIES = {
    "nigeria": "NG",
    "kenya": "KE",
    "angola": "AO",
    "benin": "BJ",
}


def parse_query(q):

    q = q.lower()

    filters = {}

    # gender
    if "male" in q:
        filters["gender"] = "male"

    if "female" in q:
        filters["gender"] = "female"

    # age groups
    if "adult" in q:
        filters["age_group"] = "adult"

    if "teenager" in q:
        filters["age_group"] = "teenager"

    # young mapping
    if "young" in q:
        filters["min_age"] = 16
        filters["max_age"] = 24

    # above age
    import re
    match = re.search(r"above (\d+)", q)
    if match:
        filters["min_age"] = int(match.group(1))

    # country
    for name, code in COUNTRIES.items():
        if name in q:
            filters["country_id"] = code

    if not filters:
        return None

    return filters