from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser

from brandquad.api.pagination import SmallResultsSetPagination
from brandquad.observability.models import NginxLog

from .serializers import NginxLogSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.response import Response


class NginxLogViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for working with nginx logs."""

    queryset = NginxLog.objects.order_by("-timestamp")
    serializer_class = NginxLogSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["http_method"]
    search_fields = ["ip_address", "request_uri"]
    pagination_class = SmallResultsSetPagination

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List all nginx log records."""
        return super().list(request, *args, **kwargs)
