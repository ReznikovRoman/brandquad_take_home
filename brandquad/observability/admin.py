from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from .models import NginxLog

if TYPE_CHECKING:
    from django.http import HttpRequest


@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "timestamp", "http_method", "request_uri"]
    search_fields = ["ip_address", "request_uri"]
    list_filter = ["http_method"]
    ordering = ["-timestamp"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: NginxLog | None = None) -> bool:
        return False
