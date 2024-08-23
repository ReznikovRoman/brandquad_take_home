from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import NginxLogViewSet

app_name = "observability"

router = SimpleRouter(trailing_slash=False)
router.register("nginx/logs", NginxLogViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
