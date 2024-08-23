from django.db import models


class NginxLog(models.Model):
    """Log record from Nginx."""

    ip_address = models.GenericIPAddressField(verbose_name="IP address")
    http_method = models.CharField(verbose_name="HTTP method", max_length=15)
    request_uri = models.CharField(verbose_name="Request URI", max_length=255)
    response_code = models.PositiveSmallIntegerField(verbose_name="Response HTTP status code")
    response_size = models.PositiveIntegerField(verbose_name="Response size", help_text="Size in bytes")
    timestamp = models.DateTimeField(verbose_name="Request timestamp")

    class Meta:
        verbose_name = "Nginx log"
        verbose_name_plural = "Nginx logs"

    def __str__(self) -> str:
        return self.ip_address
