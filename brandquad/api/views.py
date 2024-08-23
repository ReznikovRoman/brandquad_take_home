from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rest_framework.serializers import BaseSerializer
    from rest_framework.viewsets import GenericViewSet
    _BaseViewSet = GenericViewSet
else:
    _BaseViewSet = object


class MultiSerializerViewSetMixin(_BaseViewSet):
    """Mixin for selecting an appropriate serializer from `serializer_classes`."""

    serializer_classes: dict[str, type[BaseSerializer]] | None = None

    def get_serializer_class(self) -> type[BaseSerializer]:
        try:
            return self.serializer_classes[self.action]  # type: ignore[index]
        except (KeyError, TypeError):
            return super().get_serializer_class()
