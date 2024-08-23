from rest_framework import serializers

from brandquad.observability.models import NginxLog


class NginxLogSerializer(serializers.ModelSerializer):
    """Nginx log record serializer."""

    class Meta:
        model = NginxLog
        fields = ["id", "ip_address", "timestamp", "http_method", "request_uri", "response_code", "response_size"]
