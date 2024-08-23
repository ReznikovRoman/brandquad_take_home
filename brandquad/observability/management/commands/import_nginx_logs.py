from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any

import orjson
import requests

from django.core.management.base import BaseCommand

from brandquad.observability.models import NginxLog

if TYPE_CHECKING:
    from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = "Import Nginx log records from a URL"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("log_url", type=str, help="URL to the log file")

    def handle(self, *args: Any, **kwargs: Any) -> None:
        log_url = kwargs["log_url"]
        self.import_logs(log_url)

    def import_logs(self, log_url: str) -> None:
        try:
            with requests.Session() as session, session.get(log_url, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        log_entry = orjson.loads(line.decode("utf-8"))
                        self.save_log_entry(log_entry)
            self.stdout.write(self.style.SUCCESS("Log file imported successfully"))
        except requests.RequestException as exc:
            self.stdout.write(self.style.ERROR(f"Error fetching the log file: {exc}"))
        except orjson.JSONDecodeError as exc:
            self.stdout.write(
                self.style.ERROR(
                    f"Error parsing JSON: <{exc}>. "
                    f"Tried to parse the following line (make sure that the URL leads to a txt file): {line}",
                ),
            )

    def save_log_entry(self, log_entry: dict[str, Any]) -> NginxLog:
        return NginxLog.objects.create(
            ip_address=log_entry["remote_ip"],
            timestamp=self._parse_timestamp(log_entry["time"]),
            http_method=log_entry["request"].split(" ")[0],
            request_uri=log_entry["request"].split(" ")[1],
            response_code=log_entry["response"],
            response_size=log_entry["bytes"],
        )

    def _parse_timestamp(self, timestamp: str) -> datetime.datetime:
        return datetime.datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
