import json
from django.core.management.base import BaseCommand
from profiles.models import Profile


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with open("profiles_2026.json") as f:
            data = json.load(f)

        created = 0

        for item in data:

            obj, was_created = Profile.objects.get_or_create(
                name=item["name"],
                defaults={
                    "gender": item["gender"],
                    "gender_probability": item["gender_probability"],
                    "age": item["age"],
                    "age_group": item["age_group"],
                    "country_id": item["country_id"],
                    "country_name": item["country_name"],
                    "country_probability": item["country_probability"],
                }
            )

            if was_created:
                created += 1

        self.stdout.write(f"Seeded {created} profiles")