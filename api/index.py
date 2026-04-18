import os
from mangum import Mangum

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "name_classifier_api_v2.settings"
)

from django.core.asgi import get_asgi_application

application = get_asgi_application()

handler = Mangum(application)