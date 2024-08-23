from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("schema/", include("brandquad.api.v1.schema.urls")),

    path("observability/", include("brandquad.api.v1.observability.urls")),
]
