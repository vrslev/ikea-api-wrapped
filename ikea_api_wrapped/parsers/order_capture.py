from __future__ import annotations

from datetime import date, datetime
from typing import Any, TypedDict

from box import Box

from ikea_api_wrapped.parsers import get_box_list

DELIVERY_TYPES = {
    "HOME_DELIVERY": "Доставка",
    "PUP": "Пункт самовывоза",
    "PUOP": "Магазин",
    "CLICK_COLLECT_STORE": "Магазин",
    "MOCKED_CLICK_COLLECT_STORE": "Магазин",
    "IBES_CLICK_COLLECT_STORE": "Магазин",
}

SERVICE_TYPES = {"CURBSIDE": " без подъёма", "STANDARD": ""}

SERVICE_PROVIDERS = {
    "DPD": "DPD",
    "BUSINESSLINES": "Деловые линии",
    "russianpost": "Почта России",
}


def parse_delivery_options(options_list: list[dict[str, Any]]):
    return [DeliveryOption(d)() for d in get_box_list(options_list)]


class DeliveryOptionDict(TypedDict):
    delivery_date: date | None
    delivery_type: str
    price: int
    service_provider: str | None
    unavailable_items: list[dict[str, str | int]]


class DeliveryOption:
    def __init__(self, dictionary: Box):
        self.d = dictionary

    def _get_delivery_date(self) -> date | None:
        deliveries: list[Box] | None = self.d.deliveries
        if deliveries:
            raw_delivery_time: str | None = deliveries[
                0
            ].selectedTimeWindow.fromDateTime
            if raw_delivery_time:
                return datetime.strptime(
                    raw_delivery_time, "%Y-%m-%dT%H:%M:%S.%f"
                ).date()

    def _get_delivery_type(self):
        raw_delivery_type: str = self.d.fulfillmentMethodType
        raw_service_type: str = self.d.servicetype
        service_type: str = SERVICE_TYPES.get(raw_service_type, "")
        return DELIVERY_TYPES.get(raw_delivery_type, raw_delivery_type) + service_type

    def _get_price(self):
        return int(self.d.servicePrice.amount)

    def _get_service_provider(self):
        deliveries: list[Box] = self.d.deliveries
        if deliveries:
            pickup_points: list[Box] = deliveries[0].pickUpPoints
            if pickup_points:
                identifier: str | None = pickup_points[0].identifier
                if identifier:
                    for provider, pretty_name in SERVICE_PROVIDERS.items():
                        if provider in identifier:
                            return pretty_name

    def _get_unavailable_items(self) -> list[dict[str, str | int]]:
        raw_unavailable_items: list[Box] = self.d.unavailableItems or []
        return [
            {"item_code": item.itemNo, "available_qty": item.availableQuantity}
            for item in raw_unavailable_items
            if item.itemNo is not None and item.availableQuantity is not None
        ]

    def __call__(self) -> DeliveryOptionDict:
        return {
            "delivery_date": self._get_delivery_date(),
            "delivery_type": self._get_delivery_type(),
            "price": self._get_price(),
            "service_provider": self._get_service_provider(),
            "unavailable_items": self._get_unavailable_items(),
        }
