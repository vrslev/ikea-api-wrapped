from __future__ import annotations

from typing import Any, TypedDict

from box import Box

from ikea_api_wrapped.parsers import get_box

STORE_NAMES = {"IKEA": "Интернет-магазин", "Санкт-Петербург: Парнас": "Парнас"}


def parse_purchase_history(history: dict[str, Any]):
    list_: list[Box] = get_box(history).data.history
    return [PurchaseHistoryItem(i)() for i in list_]


class PurchaseHistoryItemDict(TypedDict):
    datetime: str | None
    datetime_formatted: str
    price: float
    purchase_id: int
    status: str
    store: str | None


class PurchaseHistoryItem:
    def __init__(self, history_item: Box):
        self.d = history_item

    def _get_datetime(self):
        if self.d.dateAndTime.date and self.d.dateAndTime.time:
            return f"{self.d.dateAndTime.date}T{self.d.dateAndTime.time}"

    def _get_datetime_formatted(self) -> str:
        return self.d.dateAndTime.formattedLongDateTime

    def _get_price(self):
        raw_price: float | None = self.d.totalCost.value
        return raw_price or 0.0

    def _get_purchase_id(self) -> int:
        return self.d.id

    def _get_status(self) -> str:
        return self.d.status

    def _get_store(self) -> str | None:
        return STORE_NAMES.get(self.d.storeName)

    def __call__(self) -> PurchaseHistoryItemDict:
        return PurchaseHistoryItemDict(
            datetime=self._get_datetime(),
            datetime_formatted=self._get_datetime_formatted(),
            price=self._get_price(),
            purchase_id=self._get_purchase_id(),
            status=self._get_status(),
            store=self._get_store(),
        )


class CostsOrderDict(TypedDict):
    delivery_cost: float
    total_cost: float


class CostsOrder:
    def __init__(self, costs_order: dict[str, Any]):
        self.d = get_box(costs_order).data.order.costs

    def _get_delivery_cost(self) -> float:
        return self.d.delivery.value or 0.0

    def _get_total_cost(self) -> float:
        return self.d.total.value or 0.0

    def __call__(self):
        return CostsOrderDict(
            delivery_cost=self._get_delivery_cost(),
            total_cost=self._get_total_cost(),
        )


class StatusBannerOrderDict(TypedDict):
    purchase_date: str | None
    delivery_date: str | None


class StatusBannerOrder:
    def __init__(self, status_banner_order: dict[str, Any]):
        self.d = get_box(status_banner_order).data.order

    def _get_purchase_date(self) -> str | None:
        return self.d.dateAndTime.date or None

    def _get_delivery_date(self) -> str | None:
        delivery_methods: list[Box] = self.d.deliveryMethods
        if delivery_methods:
            return delivery_methods[0].deliveryDate.estimatedFrom.date

    def __call__(self):
        return StatusBannerOrderDict(
            purchase_date=self._get_purchase_date(),
            delivery_date=self._get_delivery_date(),
        )
